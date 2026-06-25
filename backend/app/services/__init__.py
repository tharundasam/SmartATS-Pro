# Business logic layer. Each module gets a service file here that
# orchestrates models + ai_engine + external calls, kept separate from
# the API route handlers (which should stay thin — parse request,
# call service, return response).
#
#   resume_service.py     -> Module 2/3
#   ats_service.py         -> Module 4
#   job_match_service.py   -> Module 5
#   skill_gap_service.py    -> Module 6
#   enhancement_service.py -> Module 7
#   interview_service.py    -> Module 8
#   career_service.py       -> Module 9
#   analytics_service.py    -> Module 10
