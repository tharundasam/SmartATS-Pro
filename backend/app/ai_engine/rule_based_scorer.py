"""
Rule-based ATS scoring engine.

No embeddings/cosine-similarity here — per the same project decision
documented in requirements.txt and rule_based_extractor.py, matching
uses keyword overlap and simple heuristics rather than spaCy/Sentence
Transformers. This module is pure logic: it takes already-extracted
fields (an ExtractedResumeData row) plus an optional job description
string, and returns plain numbers/lists. It has no knowledge of the
database or HTTP layer — see services/ats_service.py for orchestration
and persistence, matching the same split used for
rule_based_extractor.py / parsing_service.py.

Scoring is always computed in two parts:
  - Generic ATS checks (formatting, education, projects, base skills
    presence) that run regardless of whether a JD was supplied — this
    is what powers the standalone "ATS Score Breakdown" screen.
  - JD-specific keyword matching (skills/keywords overlap against the
    JD's text) — only meaningfully differentiated when a JD is
    supplied. Without a JD, keyword/skills scoring falls back to
    "how many of our known SKILL_KEYWORDS did we find at all", which is
    a weaker but still useful generic signal.
"""

import re

from app.ai_engine.rule_based_extractor import SKILL_KEYWORDS

# Weights used to combine sub-scores into the overall score. Kept as a
# module-level constant (not hardcoded inline) so the weighting scheme
# is visible and easy to tune in one place. Mirrors the rough
# proportions implied by the dashboard mockups (skills/keywords weighted
# most heavily, education/projects supporting).
_WEIGHTS = {
    "skills": 0.30,
    "keywords": 0.25,
    "formatting": 0.20,
    "education": 0.10,
    "projects": 0.15,
}

# A resume below this length is penalized on formatting — too sparse to
# be a complete resume, which both hurts a human reading it and gives
# an ATS parser little to extract.
_MIN_SUBSTANTIAL_LENGTH = 200

# Roughly how many distinct skills a strong technical resume tends to
# list. Used only as a normalization denominator for the generic
# (no-JD) skills score — not a hard requirement.
_STRONG_SKILL_COUNT = 8


def _tokenize_keywords(text: str) -> set[str]:
    """
    Extracts a JD's "important" words as a lowercase set, for overlap
    scoring. Deliberately simple: strips punctuation, lowercases, drops
    very short/common words. This is weaker than TF-IDF or embeddings
    but has zero compiled dependencies (see requirements.txt).
    """
    raw_words = re.findall(r"[a-zA-Z][a-zA-Z0-9+./#-]*", text.lower())
    # The character class above intentionally allows '.', '/', '#', '-'
    # mid-token (so "node.js", "c#", "ci/cd" survive intact), but that
    # also lets a sentence-final period or trailing punctuation tag
    # along (e.g. "required." at the end of a sentence). Stripping
    # trailing non-alphanumeric characters removes that without
    # affecting genuinely punctuated skill names, since real ones never
    # end in punctuation themselves.
    words = [w.rstrip(".,/#-") for w in raw_words]
    stopwords = {
        "the", "and", "for", "with", "you", "are", "our", "will", "this",
        "that", "from", "have", "has", "will", "your", "all", "able",
        "who", "can", "their", "they", "job", "role", "team", "work",
        "experience", "years", "year", "skills", "skill", "ability",
        "strong", "good", "excellent", "looking", "candidate", "etc",
    }
    return {w for w in words if len(w) > 2 and w not in stopwords}


def score_formatting(raw_text: str, sections_present: dict[str, bool]) -> float:
    """
    Generic ATS formatting/readability score (0-100). Approximates what
    an ATS parser cares about: is there enough text, and are standard
    sections present and detectable (the same section headers
    rule_based_extractor.py already looks for).

    This is necessarily a rough proxy for "machine readability" —
    a true ATS-simulation would also check fonts, columns, tables, and
    embedded images, none of which are knowable from extracted text
    alone.
    """
    score = 0.0

    length = len(raw_text.strip())
    if length >= _MIN_SUBSTANTIAL_LENGTH:
        score += 40.0
    else:
        # Partial credit, scaled linearly, for short-but-not-empty text.
        score += 40.0 * (length / _MIN_SUBSTANTIAL_LENGTH)

    # Up to 60 points spread across the four structural sections we can
    # detect (education, experience, projects, certifications) — 15
    # each. Skills are scored separately, so not double-counted here.
    structural_keys = ["education", "experience", "projects", "certifications"]
    detected = sum(1 for key in structural_keys if sections_present.get(key))
    score += 15.0 * detected

    return round(min(score, 100.0), 1)


def score_education(education_raw: str | None) -> float:
    """Generic education score (0-100). Presence-based: a non-empty,
    reasonably substantial education section scores well. This can't
    judge degree relevance without a JD to compare against — see
    score_keywords_against_jd for JD-aware matching instead."""
    if not education_raw or not education_raw.strip():
        return 0.0
    if len(education_raw.strip()) < 10:
        return 40.0  # something was detected, but too thin to be confident
    return 100.0


def score_projects(projects_raw: str | None) -> float:
    """Generic projects score (0-100), same presence-based logic as
    score_education. A missing projects section isn't necessarily
    disqualifying (many strong resumes rely on work experience
    instead), so this is weighted lower than skills/keywords overall —
    see _WEIGHTS."""
    if not projects_raw or not projects_raw.strip():
        return 0.0
    if len(projects_raw.strip()) < 10:
        return 40.0
    return 100.0


def score_skills_generic(skills: list[str]) -> float:
    """
    Generic (no-JD) skills score (0-100): how many recognized
    SKILL_KEYWORDS were found, normalized against _STRONG_SKILL_COUNT.
    This rewards breadth of detected skills in the absence of any
    specific job to compare against.
    """
    if not skills:
        return 0.0
    return round(min(len(skills) / _STRONG_SKILL_COUNT, 1.0) * 100.0, 1)


def score_skills_against_jd(skills: list[str], jd_text: str) -> tuple[float, list[str]]:
    """
    JD-aware skills score (0-100) plus the list of missing skills.
    Looks only within SKILL_KEYWORDS that actually appear in the JD —
    skills the JD never mentions aren't penalized, matching how a real
    ATS keyword match would behave (it cares about overlap with this
    specific posting, not the candidate's total skill count).

    Returns (score, missing_skills). If the JD doesn't mention any
    known SKILL_KEYWORDS at all, returns (100.0, []) rather than
    dividing by zero — an unscoreable JD shouldn't be penalized as a 0.
    """
    jd_lower = jd_text.lower()
    jd_required_skills = [
        skill
        for skill in SKILL_KEYWORDS
        if (skill in jd_lower if re.search(r"[^a-z0-9]", skill)
            else re.search(rf"\b{re.escape(skill)}\b", jd_lower))
    ]

    if not jd_required_skills:
        return 100.0, []

    resume_skills_set = set(skills)
    matched = [s for s in jd_required_skills if s in resume_skills_set]
    missing = [s for s in jd_required_skills if s not in resume_skills_set]

    score = round((len(matched) / len(jd_required_skills)) * 100.0, 1)
    return score, missing


def score_keywords_against_jd(raw_text: str, jd_text: str) -> tuple[float, list[str]]:
    """
    Broader (non-skill-list) keyword overlap score (0-100) plus the
    top missing keywords, using simple set intersection over
    tokenized words rather than embeddings/cosine similarity (see
    module docstring). This catches JD-important words that aren't in
    SKILL_KEYWORDS at all (e.g. domain terms, soft skills, methodologies).

    Missing keywords are capped at 10 entries, ordered by their first
    appearance in the JD, so the response stays focused on the most
    prominent gaps rather than dumping every unmatched word.
    """
    jd_keywords_ordered = []
    seen = set()
    for raw_word in re.findall(r"[a-zA-Z][a-zA-Z0-9+./#-]*", jd_text.lower()):
        word = raw_word.rstrip(".,/#-")
        if word in seen:
            continue
        seen.add(word)
        jd_keywords_ordered.append(word)

    jd_keyword_set = _tokenize_keywords(jd_text)
    resume_keyword_set = _tokenize_keywords(raw_text)

    if not jd_keyword_set:
        return 100.0, []

    matched = jd_keyword_set & resume_keyword_set
    missing_set = jd_keyword_set - resume_keyword_set

    score = round((len(matched) / len(jd_keyword_set)) * 100.0, 1)

    # Preserve JD order, filtered down to the missing set, capped at 10.
    missing_ordered = [w for w in jd_keywords_ordered if w in missing_set][:10]
    return score, missing_ordered


def compute_overall_score(sub_scores: dict[str, float]) -> float:
    """Weighted average of sub-scores using _WEIGHTS. Assumes every key
    in _WEIGHTS is present in sub_scores — callers (ats_service.py)
    always pass the full set."""
    total = sum(sub_scores[key] * weight for key, weight in _WEIGHTS.items())
    return round(total, 1)


def run_rule_based_scoring(
    raw_text: str,
    skills: list[str],
    education_raw: str | None,
    experience_raw: str | None,
    projects_raw: str | None,
    certifications_raw: str | None,
    job_description: str | None,
) -> dict:
    """
    Orchestration point for this module — runs every sub-score and
    combines them. Mirrors the structure of
    rule_based_extractor.extract_all_fields: one function services
    layer code calls, returning a plain dict ready to build an
    ATSReport from.

    When job_description is None or blank, JD-specific scores
    (skills/keywords) fall back to their generic equivalents and
    missing_keywords is empty — there's nothing to be "missing"
    relative to, without a JD to compare against.
    """
    sections_present = {
        "education": bool(education_raw and education_raw.strip()),
        "experience": bool(experience_raw and experience_raw.strip()),
        "projects": bool(projects_raw and projects_raw.strip()),
        "certifications": bool(certifications_raw and certifications_raw.strip()),
    }

    formatting_score = score_formatting(raw_text, sections_present)
    education_score = score_education(education_raw)
    projects_score = score_projects(projects_raw)

    missing_keywords: list[str] = []

    if job_description and job_description.strip():
        skills_score, missing_skills = score_skills_against_jd(skills, job_description)
        keywords_score, missing_general_keywords = score_keywords_against_jd(
            raw_text, job_description
        )
        # Missing skills surfaced first (more actionable/specific), then
        # broader missing keywords, deduplicated, capped at 10 total so
        # the response stays focused — matches the mockup's small chip
        # list rather than an exhaustive dump.
        seen = set()
        for kw in missing_skills + missing_general_keywords:
            if kw not in seen:
                seen.add(kw)
                missing_keywords.append(kw)
        missing_keywords = missing_keywords[:10]
    else:
        skills_score = score_skills_generic(skills)
        keywords_score = skills_score

    sub_scores = {
        "skills": skills_score,
        "keywords": keywords_score,
        "formatting": formatting_score,
        "education": education_score,
        "projects": projects_score,
    }
    overall_score = compute_overall_score(sub_scores)

    return {
        "overall_score": overall_score,
        "skills_score": skills_score,
        "keywords_score": keywords_score,
        "formatting_score": formatting_score,
        "education_score": education_score,
        "projects_score": projects_score,
        "missing_keywords": missing_keywords,
    }
