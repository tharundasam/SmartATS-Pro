"""
AI-generated improvement suggestions — currently a STUBBED PLACEHOLDER.

*** No live LLM call is made by this module yet. ***

This was deliberately left unwired (per project decision) rather than
calling a real provider, so an API key (Anthropic/OpenAI/etc.) doesn't
need to be configured to exercise the rest of the ATS scoring engine,
and so cost/latency isn't introduced into every scoring request before
a provider choice is finalized.

`generate_ai_suggestions` returns realistic, structurally-correct
suggestions derived from the rule-based score and missing keywords —
not from an actual model call. The function signature and return type
(list[str]) are the real contract: swapping in a genuine LLM call later
should only require rewriting this function's body, exactly like the
spaCy-swap note in rule_based_extractor.py's module docstring. Nothing
in ats_service.py or the API layer should need to change.

To wire in a real provider later:
  1. Add the chosen provider's SDK to requirements.txt and an API key
     setting to app/core/config.py (e.g. ANTHROPIC_API_KEY).
  2. Replace this function's body with a real API call — prompt with
     the resume's raw_text, the job_description (if any), and the
     rule-based sub-scores/missing_keywords so the model's suggestions
     are grounded in the same data the rest of the report is built
     from.
  3. Keep the return type as list[str] (or extend ATSReport/the schema
     deliberately, in step with each other) so nothing downstream
     breaks silently.
"""


def _suggest_for_low_score(label: str, score: float) -> str | None:
    """Returns a generic-but-relevant suggestion for a sub-score under
    70, or None if the score doesn't warrant flagging. Threshold and
    wording are placeholder heuristics — see module docstring."""
    if score >= 70:
        return None
    templates = {
        "skills_score": (
            "Your listed skills don't fully cover what this role is "
            "looking for. Consider adding any missing tools or "
            "technologies you have real experience with."
        ),
        "keywords_score": (
            "Several important terms from the job description don't "
            "appear in your resume. Weaving in matching language "
            "(without keyword-stuffing) can improve ATS parsing."
        ),
        "formatting_score": (
            "Your resume may be too short or missing standard sections "
            "(Education, Experience, Projects, Certifications) that ATS "
            "parsers look for. Make sure each section is clearly labeled."
        ),
        "education_score": (
            "Your education section is missing or very brief. Add your "
            "degree, institution, and graduation year if you have them."
        ),
        "projects_score": (
            "Adding a few relevant projects — with a one-line outcome "
            "or metric for each — can strengthen this section "
            "significantly."
        ),
    }
    return templates.get(label)


def generate_ai_suggestions(
    *,
    raw_text: str,
    job_description: str | None,
    sub_scores: dict[str, float],
    missing_keywords: list[str],
) -> list[str]:
    """
    STUBBED PLACEHOLDER — see module docstring. Does not call any
    external LLM API. Builds a small set of suggestions from the
    rule-based sub-scores and missing keywords, so the response shape
    (and the kind of guidance shown) matches what a real LLM call would
    eventually produce.

    `raw_text` is accepted (and currently unused) so the function
    signature already matches what a real LLM-backed implementation
    would need — the resume's full text would be part of that prompt.
    """
    suggestions: list[str] = []

    for label in ["keywords_score", "skills_score", "formatting_score", "education_score", "projects_score"]:
        suggestion = _suggest_for_low_score(label, sub_scores.get(label, 0.0))
        if suggestion:
            suggestions.append(suggestion)

    if missing_keywords:
        top_missing = ", ".join(missing_keywords[:5])
        if job_description and job_description.strip():
            suggestions.append(
                f"Consider addressing these terms from the job description "
                f"if they genuinely apply to your background: {top_missing}."
            )
        else:
            suggestions.append(
                f"These commonly-searched terms weren't found in your resume: "
                f"{top_missing}."
            )

    if not suggestions:
        suggestions.append(
            "Your resume looks solid across the board. Consider quantifying "
            "your achievements with specific metrics where possible to push "
            "your score even higher."
        )

    return suggestions
