# SQLAlchemy ORM models live here, one file per table, added module by
# module:
#   - users.py, roles.py        -> Module 1 (Phase B Step 2: Auth)
#   - resumes.py                 -> Module 2 (Phase B Step 3: Resume Upload)
#   - extracted_resume_data.py   -> Module 3 (Resume Parsing)
#   - ats_reports.py             -> Module 4 (ATS Score Engine)
#   - job_descriptions.py, job_matches.py -> Module 5
#   - skill_gap_reports.py       -> Module 6
#   - interview_questions.py, interview_history.py -> Module 8
#   - career_recommendations.py  -> Module 9
#   - placement_analytics.py     -> Module 10
#
# Intentionally empty for this step — there are no tables yet, only the
# engine/session plumbing and the /health endpoint that proves the DB
# file can be created and connected to.
