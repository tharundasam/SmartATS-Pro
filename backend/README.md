# SmartATS Pro — Backend (FastAPI)

**Phase B, Steps 1–4: scaffold, auth, resume upload, resume parsing.**
**Phase C: ATS scoring engine (rule-based + stubbed AI suggestions).**
Remaining modules (JD/job-match persistence, skill-gap reports,
interview coach, etc.) come in subsequent steps.

## What's included (Phase B Step 1–4 + Phase C)

```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, router mounting, startup hook
│   ├── core/
│   │   └── config.py        # Settings loaded from .env (pydantic-settings)
│   ├── database/
│   │   └── session.py       # SQLAlchemy engine/session, get_db() dependency
│   ├── models/
│   │   ├── user.py                    # User model + RoleEnum
│   │   ├── resume.py                  # Resume model — versioned, tied to a user
│   │   ├── extracted_resume_data.py   # Parsed fields, 1:1 with Resume
│   │   └── ats_report.py              # NEW — one row per scoring run
│   ├── schemas/
│   │   ├── health.py        # Pydantic response models for health/root
│   │   ├── auth.py          # Register/login/token/user-out schemas
│   │   ├── resume.py        # ResumeOut, ResumeListResponse, ResumeUploadResponse
│   │   ├── parsing.py       # ExtractedResumeDataOut
│   │   └── ats.py            # NEW — ATSScoreRequest, ATSReportOut, ATSReportListResponse
│   ├── auth/
│   │   ├── security.py      # bcrypt hashing, JWT create/decode
│   │   └── dependencies.py  # get_current_user, require_role(...)
│   ├── ai_engine/
│   │   ├── text_extraction.py         # PDF (pdfplumber->pypdf) / DOCX -> raw text
│   │   ├── rule_based_extractor.py    # raw text -> name/email/phone/skills/sections
│   │   ├── rule_based_scorer.py       # NEW — generic + JD-aware ATS scoring
│   │   └── llm_suggestions.py         # NEW — AI suggestions (STUBBED, no live LLM call)
│   ├── services/
│   │   ├── auth_service.py    # Registration/login business logic
│   │   ├── resume_service.py  # File storage, versioning, list/get/delete
│   │   ├── parsing_service.py  # Orchestrates extraction, persists result
│   │   └── ats_service.py      # NEW — orchestrates scoring, persists ATSReport
│   ├── utils/
│   │   └── file_validation.py # Extension/size/magic-byte checks
│   └── api/
│       └── v1/
│           ├── __init__.py  # api_router — every module's routes plug in here
│           ├── health.py    # GET /api/v1/health
│           ├── auth.py      # /auth/register, /auth/login, /auth/login/json, /auth/me
│           ├── resumes.py   # upload (auto-parses), list, get, download, delete,
│           │                  # parsed-data, reparse
│           └── ats.py        # NEW — score, reports (list + single detail)
├── tests/
│   ├── test_health.py
│   ├── test_auth.py
│   ├── test_resumes.py
│   ├── test_parsing.py        # 7 tests covering the extraction pipeline
│   └── test_ats.py            # NEW — 10 tests covering the scoring engine
├── storage/resumes/           # Uploaded files land here (gitignored contents)
├── requirements.txt
├── .env / .env.example
└── README.md
```

## ⚠️ Breaking change in this step: upload response shape

`POST /resumes/upload` no longer returns a flat `ResumeOut` object. It
now returns:

```json
{
  "resume": { "id": "...", "original_filename": "...", "version": 1, "is_current": true, ... },
  "extracted_data": { "full_name": "...", "email": "...", "skills": [...], ... },
  "parsing_error": null
}
```

instead of the old flat shape (`{"id": ..., "original_filename": ..., ...}`).
This was necessary to return parsing results from the same call that
uploads the file, without a second round-trip. If you'd written any
frontend code against the old shape already, it needs `response.resume.id`
instead of `response.id` (and so on for every resume field). Nothing in
the frontend currently calls this endpoint for real yet (see
`StudentDashboard.tsx`/`JobMatchEngine.tsx` — both have it as a
`console.log` placeholder), so this is unlikely to have broken anything
on your side, but flagged here in case.

`test_resumes.py` (from Step 3) was updated to match — every assertion
that used to read fields directly off the upload response now reads them
from `response["resume"]` instead.

## Why this structure

- **`api/v1/`** is versioned from day one. When Module 1 (Auth) lands, its
  router is added as `app/api/v1/auth.py` and registered in
  `app/api/v1/__init__.py` — `main.py` never changes.
- **`get_db()`** in `database/session.py` is a FastAPI dependency every
  future route will use (`db: Session = Depends(get_db)`), so each request
  gets its own session that's guaranteed to close.
- **SQLite now, Postgres later, zero code changes.** `DATABASE_URL` in
  `.env` is the only thing that changes. The SQLite-specific
  `check_same_thread` connect arg is applied conditionally — it's simply
  not added when the URL isn't SQLite.
- **`Base.metadata.create_all()` on startup**, not Alembic, for now. This
  is fine while there are no real tables and no production database. Once
  the first real models exist (Module 1), this project should switch to
  Alembic migrations so schema changes are tracked and reversible —
  flagged here so it isn't forgotten.

## Setup

You'll need Python 3.11+ (3.12 used in development).

```bash
cd backend
python -m venv venv

# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

`.env` is already created with working defaults (SQLite, permissive
local CORS). Adjust `JWT_SECRET_KEY` before any real deployment — the
default value is a placeholder, not a secret.

Run the server:

```bash
uvicorn app.main:app --reload
```

## Testing instructions

1. **Start the server** (`uvicorn app.main:app --reload`) and confirm the
   terminal shows no errors and ends with something like
   `Application startup complete.`

2. **Visit Swagger UI:** http://localhost:8000/docs
   - You should see two tags: "Root" and "Health", each with one GET
     endpoint, and a working "Try it out" button for each.

3. **Visit ReDoc:** http://localhost:8000/redoc — alternate API doc view.

4. **Hit the root endpoint:**
   ```bash
   curl http://localhost:8000/
   ```
   Expected: `{"message":"SmartATS Pro API is running.","docs_url":"/docs","api_version":"/api/v1"}`

5. **Hit the health endpoint:**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```
   Expected: `{"status":"ok","app_name":"SmartATS Pro API","environment":"development","database":"connected"}`

6. **Confirm the SQLite file was created:**
   ```bash
   ls backend/smartats.db
   ```
   This file is created automatically on first run by the `on_startup`
   hook in `main.py`. It will currently be near-empty (no tables yet) —
   that's expected for this step.

7. **Run the automated test suite:**
   ```bash
   pytest -v
   ```
   All 4 tests in `tests/test_health.py` should pass.

8. **Confirm CORS works with the frontend:** with the FastAPI server
   running on port 8000 and the Vite dev server running on port 5173
   (`npm run dev` in `frontend/`), open the browser console on
   `http://localhost:5173` and run:
   ```js
   fetch("http://localhost:8000/api/v1/health").then(r => r.json()).then(console.log)
   ```
   This should succeed without a CORS error in the console.

## Honest note on verification

This backend was written and reviewed carefully, but it has **not** been
executed in an automated way before being handed to you — the sandbox
this was built in has no network access, so `pip install` cannot run
there. Please run the steps above and report back anything that fails
(a traceback, a wrong status code, an import error) and it'll be fixed
immediately before moving to Step 2.

## Testing instructions — Phase B Step 2 (Authentication)

1. **Restart the server** if it's already running, so the new `users`
   table gets created:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Confirm the table was created:**
   ```bash
   python -c "import sqlite3; print(sqlite3.connect('smartats.db').execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall())"
   ```
   Should include `('users',)`.

3. **Register a user via Swagger UI** (http://localhost:8000/docs):
   - Expand `POST /api/v1/auth/register`, "Try it out"
   - Body:
     ```json
     {"full_name": "Alex Rivers", "email": "alex@example.com", "password": "supersecret123", "role": "student"}
     ```
   - Expect `201`, with `access_token` and a `user` object in the response.

4. **Use Swagger's "Authorize" button** (top right, padlock icon):
   - username: `alex@example.com`, password: `supersecret123`
   - This hits `/auth/login` under the hood (OAuth2 form flow) and stores
     the token for all subsequent "Try it out" calls automatically.

5. **Call `GET /api/v1/auth/me`** via "Try it out" — should return Alex's
   profile without you manually pasting a token anywhere.

6. **Test role protection:**
   - With Alex (a student) still authorized, call
     `GET /api/v1/auth/placement-officer-check` — expect `403`.
   - Register a second user with `"role": "placement_officer"`,
     re-authorize as that user, call the same endpoint — expect `200`.

7. **Test from curl directly (JSON login variant):**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/login/json \
     -H "Content-Type: application/json" \
     -d '{"email": "alex@example.com", "password": "supersecret123"}'
   ```

8. **Run the automated test suite:**
   ```bash
   pytest -v
   ```
   13 tests total should pass (4 from Step 1, 9 new in `test_auth.py`),
   covering registration, duplicate-email rejection, both login styles,
   `/me` with and without a token, and both sides of the role check.

## A note on the JWT secret

`.env` ships with a real randomly-generated value for `JWT_SECRET_KEY`
(not the placeholder string), so auth works immediately without any
manual setup step. That said, **this exact value should never be reused
in a real deployment** — `.env` is gitignored specifically so secrets
like this don't end up in version control. Generate a fresh one for
production with:
```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```


## Testing instructions — Phase B Step 3 (Resume Upload)

1. **Restart the server** so the new `resumes` table gets created.

2. **Get a token** (register or login via Swagger, or reuse one from
   Step 2's testing).

3. **Upload a resume via Swagger UI:**
   - Expand `POST /api/v1/resumes/upload`, "Try it out"
   - Click "Choose File", pick any real `.pdf` or `.docx` on your machine
   - Execute — expect `201` with `version: 1`, `is_current: true`

4. **Upload a second file** (different file, or the same one again) —
   expect `version: 2`, `is_current: true`.

5. **List your resumes:** `GET /api/v1/resumes` — expect `total: 2`,
   with the second upload's `is_current` true and the first's false.

6. **Download a resume:** `GET /api/v1/resumes/{resume_id}/download` —
   should return the actual file bytes (Swagger will offer to download
   it).

7. **Cross-user isolation:** register a second account, authorize as
   that user, try `GET /api/v1/resumes/{first_users_resume_id}` — expect
   `404` (not 403 — this avoids confirming the resume exists at all to
   someone who doesn't own it).

8. **Validation checks** (all via "Try it out" with a deliberately wrong
   file):
   - Upload a `.txt` or `.exe` file → expect `400` ("Unsupported file type")
   - Rename a `.txt` file to `.pdf` and upload it → expect `400`
     ("File content does not match a valid PDF") — this is the
     magic-byte check catching a mismatched extension
   - Upload a file larger than 10MB → expect `413`

9. **Delete and version promotion:** delete your current (most recent)
   resume via `DELETE /api/v1/resumes/{resume_id}` — expect `204`, then
   `GET /api/v1/resumes` again and confirm the next-most-recent version
   automatically became `is_current: true`.

10. **Run the automated test suite:**
    ```bash
    pytest -v
    ```
    24 tests total should pass (4 health + 9 auth + 11 resume), including
    the renamed-file-extension attack case and the cross-user isolation
    check.

## Testing instructions — Phase B Step 4 (Resume Parsing)

1. **Restart the server** so the new `extracted_resume_data` table gets
   created.

2. **Upload a real PDF or DOCX resume via Swagger UI** (a real one this
   time — a file with actual text content, not the magic-bytes-only test
   fixtures used in automated tests):
   - `POST /api/v1/resumes/upload`, "Try it out", choose your file, Execute
   - Expect `201`, with the response now shaped as
     `{"resume": {...}, "extracted_data": {...}, "parsing_error": null}`
   - Check `extracted_data.skills` contains skills that are actually in
     your resume and in the keyword list (`app/ai_engine/rule_based_extractor.py`'s
     `SKILL_KEYWORDS`) — anything not in that list won't be detected,
     by design (see "A note on the AI/NLP stack" below)
   - Check `extracted_data.email` and `.full_name` look right

3. **Fetch parsed data separately:**
   `GET /api/v1/resumes/{resume_id}/parsed-data` — should return the same
   data as the upload response's `extracted_data`.

4. **Test the graceful-failure path:** upload a PDF that's actually a
   scanned image (no selectable text) or a corrupted file. Expect `201`
   still (the resume itself saves fine), with `extracted_data: null` and
   `parsing_error` describing why parsing failed.

5. **Test reparse:** `POST /api/v1/resumes/{resume_id}/reparse` — should
   return fresh extraction results read from the stored file on disk
   (no re-upload needed).

6. **Run the automated test suite:**
   ```bash
   pytest -v
   ```
   31 tests total should pass (4 health + 9 auth + 11 resume + 7 parsing).

## A note on test fixtures for this step

`test_parsing.py` needed *real* parseable PDF/DOCX content to test
extraction meaningfully — the existing `FAKE_PDF_BYTES` in
`test_resumes.py` is just enough to pass the magic-byte check, with no
actual text. So `test_parsing.py` hand-builds a minimal valid PDF (raw
PDF syntax, no external library needed) and a real DOCX (via
`python-docx`, which is already a dependency). These fixture builders
were verified directly against `pdfplumber`/`pypdf`/`python-docx` before
being included here, not just written and assumed correct.

## Next steps

- ~~**Phase B Step 2:** Authentication~~ ✅ done — JWT, roles, bcrypt
  hashing, `get_current_user`/`require_role` dependencies
- ~~**Phase B Step 3:** Resume upload API~~ ✅ done — PDF/DOCX upload with
  extension + size + magic-byte validation, versioning, ownership-scoped
  list/get/download/delete
- ~~**Phase B Step 4:** Resume parsing engine~~ ✅ done — text extraction
  via pdfplumber/pypdf/python-docx, field extraction via regex/keyword
  matching, auto-runs on upload with graceful failure handling
- ~~**Phase C:** ATS scoring and JD matching~~ ✅ done — rule-based
  scoring (generic + JD-aware), with AI suggestions currently stubbed —
  see "Testing instructions — Phase C" and "A note on AI suggestions
  (stubbed)" below

## Testing instructions — Phase C (ATS Scoring Engine)

**What's new:** `app/models/ats_report.py` (new `ats_reports` table),
`app/ai_engine/rule_based_scorer.py`, `app/ai_engine/llm_suggestions.py`
(stubbed — see note below), `app/services/ats_service.py`,
`app/schemas/ats.py`, `app/api/v1/ats.py` (mounted at `/api/v1/ats`).
`tests/test_ats.py` — 10 new tests.

1. **Restart the server** so the new `ats_reports` table gets created.

2. **Upload and parse a resume** (per Phase B Step 4 above) if you
   don't already have one — scoring requires `extracted_data` to exist.

3. **Generic score (no job description):**
   - `POST /api/v1/ats/score/{resume_id}`, "Try it out", body `{}`
   - Expect `201` with `overall_score` plus five sub-scores
     (`skills_score`, `keywords_score`, `formatting_score`,
     `education_score`, `projects_score`), an empty `missing_keywords`
     list, and a non-empty `ai_suggestions` list.

4. **JD-matched score:**
   - Same endpoint, body `{"job_description": "<paste a real job posting>"}`
   - Expect `skills_score`/`keywords_score` to differ from the generic
     run, and `missing_keywords` to list terms from the JD not found in
     the resume (capped at 10).

5. **Score history:** `GET /api/v1/ats/reports/{resume_id}` — expect
   `total` to reflect every scoring call made so far for that resume,
   most recent first. This is what would back a score-over-time trend
   chart on the frontend.

6. **Single report detail:** `GET /api/v1/ats/reports/{resume_id}/{report_id}`
   using an `id` from the previous step's response — expect the full
   report, including the `job_description` it was scored against (or
   `null` for a generic run).

7. **Score an unparsed resume:** if you have a resume whose parsing
   failed (`extracted_data: null` on upload), try scoring it — expect
   `404`, since there's nothing for the scorer to read yet.

8. **Cross-user isolation:** same pattern as Phase B Step 3/4 — a
   second user's token should get `404` on another user's resume_id,
   report_id, or report list.

9. **Run the automated test suite:**
   ```bash
   pytest -v
   ```
   41 tests total should pass (4 health + 9 auth + 11 resume + 7
   parsing + 10 ATS).

## A note on AI suggestions (stubbed)

`app/ai_engine/llm_suggestions.py` does **not** call any real LLM yet —
this was an explicit decision for this step, so the scoring engine's
shape (endpoints, schemas, persisted report structure) could be built
and tested completely without requiring an API key or introducing
per-request cost/latency before a provider is chosen.

`generate_ai_suggestions()` currently returns templated suggestions
derived from the rule-based sub-scores and missing keywords — real
guidance, just not model-generated. The function's signature already
accepts everything a real prompt would need (`raw_text`,
`job_description`, `sub_scores`, `missing_keywords`), so wiring in a
real provider later (Anthropic, OpenAI, etc.) means:
1. Add the SDK to `requirements.txt` and an API key setting to
   `app/core/config.py`.
2. Rewrite this one function's body to call the provider instead.
3. Nothing in `app/services/ats_service.py` or `app/api/v1/ats.py`
   needs to change — same pattern as the spaCy-swap note below for
   `rule_based_extractor.py`.

## A note on the AI/NLP stack (Python 3.14 on Windows)

The original project spec calls for spaCy, Sentence Transformers,
scikit-learn, and NLTK. All four were dropped from this scaffold by
explicit decision, because:

- spaCy's dependencies (`thinc`, `blis`) are C-extension packages with
  no prebuilt Windows wheels for Python 3.14 (released Oct 2025) as of
  this writing. Without a wheel, pip tries to compile from source, which
  needs Visual Studio Build Tools — the exact error this step hit.
- Sentence Transformers (via PyTorch), scikit-learn, and NLTK all carry
  similar compiled-dependency risk on a Python version this new.

**The plan instead:** ATS scoring and JD/skill matching will use
rule-based logic — keyword extraction via regex/string matching, and
resume-vs-JD overlap via simple set intersection / TF-style scoring
rather than embeddings and cosine similarity. This is weaker than the
semantic matching in the original spec, but it has zero compiled
dependencies and will run identically on any Python version.

**Revisiting this later:** once either (a) these packages publish
Python 3.14 wheels, or (b) the project moves to Python 3.11/3.12 — where
all four already have wheels today — the embedding-based approach can be
swapped in. The `app/ai_engine/` and `app/services/` layers are
structured so that swap only touches their internals, not the API route
signatures or response shapes other modules depend on.
