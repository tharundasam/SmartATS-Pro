"""
Rule-based extraction of structured fields from raw resume text.

No spaCy/NLP model is used here — per project decision, this is regex
and keyword-list matching only (see requirements.txt for why). This is
inherently less robust than NER-based extraction: it will miss
unconventional formatting and occasionally mis-grab adjacent text. It's
deliberately built as small, independently-testable functions per field
so weaknesses can be found and patched without risking the others, and
so a future swap to spaCy-based extraction only needs to replace
individual functions, not the calling code in services/parsing_service.py.
"""

import re

# --- Section header patterns ---------------------------------------------
# Resumes are split into sections using these as anchors. Matching is
# case-insensitive and tolerant of common variants (e.g. "Work Experience"
# vs "Experience" vs "Professional Experience").
_SECTION_HEADERS = {
    "education": r"education|academic background|qualifications",
    "experience": r"experience|employment history|work history|professional experience",
    "projects": r"projects|personal projects|academic projects",
    "certifications": r"certifications?|licenses?( and certifications?)?",
    "skills": r"skills|technical skills|core competencies",
}

_EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Matches common phone formats: +1 (555) 123-4567, 555-123-4567,
# 555.123.4567, +91 98765 43210, etc. Deliberately permissive — phone
# formats vary too much globally to nail down precisely with regex.
_PHONE_PATTERN = re.compile(
    r"(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}"
)

# A reasonably broad skills vocabulary for keyword matching. This is the
# single biggest limitation of a non-NLP approach: anything not in this
# list won't be detected as a skill. Grouped by category purely for
# readability — extraction treats them as one flat list.
SKILL_KEYWORDS: list[str] = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "ruby", "php", "swift", "kotlin", "scala", "r", "sql",
    # Web / frontend
    "react", "angular", "vue", "next.js", "html", "css", "tailwind",
    "redux", "webpack",
    # Backend / frameworks
    "node.js", "express", "django", "flask", "fastapi", "spring",
    "spring boot", ".net", "rails",
    # Data / ML
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
    "spark", "hadoop", "tableau", "power bi", "matplotlib",
    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins",
    "ci/cd", "github actions", "linux",
    # Databases
    "postgresql", "mysql", "mongodb", "redis", "sqlite", "oracle",
    "elasticsearch",
    # Tools / other
    "git", "jira", "figma", "rest api", "graphql", "microservices",
    "agile", "scrum",
]


def extract_email(text: str) -> str | None:
    match = _EMAIL_PATTERN.search(text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    match = _PHONE_PATTERN.search(text)
    if not match:
        return None
    candidate = match.group(0).strip()
    # Reject matches that are mostly punctuation/too short to plausibly be
    # a phone number (the permissive regex above can occasionally match
    # short numeric fragments like a date or a list bullet "1.2024").
    digit_count = sum(ch.isdigit() for ch in candidate)
    if digit_count < 7:
        return None
    return candidate


def extract_name(text: str) -> str | None:
    """
    Heuristic: the candidate's name is usually the first non-empty line
    of the document, as long as that line doesn't look like a section
    header, an email, or a phone number. This is a weak heuristic — it
    will be wrong for resumes with a logo/header line before the name —
    but it's a reasonable first pass without an NER model.
    """
    for line in text.splitlines():
        candidate = line.strip()
        if not candidate:
            continue
        if _EMAIL_PATTERN.search(candidate) or _PHONE_PATTERN.search(candidate):
            continue
        if len(candidate) > 60:  # a name is short; a long first line is probably not one
            continue
        if any(re.search(pattern, candidate, re.IGNORECASE) for pattern in _SECTION_HEADERS.values()):
            continue
        return candidate
    return None


def extract_skills(text: str) -> list[str]:
    """
    Keyword match against SKILL_KEYWORDS, case-insensitive, matched as
    whole words/phrases (not substrings) so e.g. "java" doesn't also
    match inside "javascript". Returns matches in the order they appear
    in SKILL_KEYWORDS (a stable, predictable order) rather than order of
    appearance in the resume.
    """
    text_lower = text.lower()
    found: list[str] = []
    for skill in SKILL_KEYWORDS:
        # \b word boundaries don't work cleanly for skills containing
        # punctuation (c++, .net, ci/cd), so those are matched as plain
        # substrings; alphanumeric-only skills use \b to avoid partial
        # matches like "java" inside "javascript".
        if re.search(r"[^a-z0-9]", skill):
            if skill in text_lower:
                found.append(skill)
        else:
            if re.search(rf"\b{re.escape(skill)}\b", text_lower):
                found.append(skill)
    return found


def _extract_section(text: str, section_key: str) -> str | None:
    """
    Extracts the raw text between this section's header and the next
    recognized section header (or end of document). Returns None if the
    section header isn't found at all.
    """
    lines = text.splitlines()
    pattern = _SECTION_HEADERS[section_key]

    start_idx = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Treat as a header only if the line is short (a real header is a
        # label, not a full sentence that happens to contain the word).
        if len(stripped) <= 50 and re.search(rf"^\s*{pattern}\s*:?\s*$", stripped, re.IGNORECASE):
            start_idx = i
            break

    if start_idx is None:
        return None

    end_idx = len(lines)
    all_header_patterns = "|".join(_SECTION_HEADERS.values())
    for i in range(start_idx + 1, len(lines)):
        stripped = lines[i].strip()
        if len(stripped) <= 50 and re.search(rf"^\s*({all_header_patterns})\s*:?\s*$", stripped, re.IGNORECASE):
            end_idx = i
            break

    section_lines = [l.strip() for l in lines[start_idx + 1 : end_idx] if l.strip()]
    return "\n".join(section_lines) if section_lines else None


def extract_education(text: str) -> str | None:
    return _extract_section(text, "education")


def extract_experience(text: str) -> str | None:
    return _extract_section(text, "experience")


def extract_projects(text: str) -> str | None:
    return _extract_section(text, "projects")


def extract_certifications(text: str) -> str | None:
    return _extract_section(text, "certifications")


def extract_all_fields(text: str) -> dict:
    """Runs every extractor and returns a single dict matching
    ExtractedResumeData's fields. The orchestration point for this module."""
    return {
        "full_name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education_raw": extract_education(text),
        "experience_raw": extract_experience(text),
        "projects_raw": extract_projects(text),
        "certifications_raw": extract_certifications(text),
    }
