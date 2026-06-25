# AI/NLP layer: resume text extraction (pdfplumber, pypdf, python-docx),
# ATS scoring, and JD matching.
#
# Per project decision: rule-based / keyword-overlap logic for now (no
# spaCy, Sentence Transformers, scikit-learn, or nltk — these pull in
# C-extension dependencies without reliable Python 3.14 wheels on Windows
# as of this writing). Built out starting Phase B Step 4 (parsing) and
# Phase C (scoring/matching). The embedding-based approach from the
# original spec can be swapped in later — service function signatures
# are designed so callers (API routes) don't need to change when that
# happens, only the implementation inside services/.
