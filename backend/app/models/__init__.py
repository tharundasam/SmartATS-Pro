# SQLAlchemy ORM models live here, one file per table, added module by
# module:
#   - users.py                   -> Module 1 (Phase B Step 2: Auth)  ✅ done
#   - resumes.py                 -> Module 2 (Phase B Step 3: Resume Upload)  ✅ done
#   - extracted_resume_data.py   -> Module 3 (Resume Parsing)  ✅ done
#   - ats_report.py              -> Module 4 (ATS Score Engine)  ✅ done
#   - job_descriptions.py, job_matches.py -> Module 5
#   - skill_gap_reports.py       -> Module 6
#   - interview_questions.py, interview_history.py -> Module 8
#   - career_recommendations.py  -> Module 9
#   - placement_analytics.py     -> Module 10
#
# Every model module must be imported here (even if unused directly) so
# that Base.metadata.create_all() in main.py's startup hook actually
# knows about the table and creates it. Forgetting this import is a
# common and confusing bug — the table silently doesn't get created.
from app.models.user import RoleEnum, User  # noqa: F401
from app.models.resume import Resume  # noqa: F401
from app.models.extracted_resume_data import ExtractedResumeData  # noqa: F401
from app.models.ats_report import ATSReport  # noqa: F401

