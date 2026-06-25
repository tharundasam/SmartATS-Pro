# SmartATS Pro — Backend (FastAPI)

**Phase B, Step 1: scaffold, SQLite, health check, OpenAPI docs.**
No business logic yet — auth, resume upload, parsing, ATS scoring, etc.
come in subsequent steps. This step exists to prove the foundation works
before anything is built on top of it.

## What's included (Phase B Step 1 + Step 2)

```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, router mounting, startup hook
│   ├── core/
│   │   └── config.py        # Settings loaded from .env (pydantic-settings)
│   ├── database/
│   │   └── session.py       # SQLAlchemy engine/session, get_db() dependency
│   ├── models/
│   │   └── user.py          # User model + RoleEnum (student/recruiter/placement_officer)
│   ├── schemas/
│   │   ├── health.py        # Pydantic response models for health/root
│   │   └── auth.py          # Register/login/token/user-out schemas
│   ├── auth/
│   │   ├── security.py      # bcrypt hashing, JWT create/decode
│   │   └── dependencies.py  # get_current_user, require_role(...)
│   ├── services/
│   │   └── auth_service.py  # Registration/login business logic
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py  # api_router — every module's routes plug in here
│   │       ├── health.py    # GET /api/v1/health
│   │       └── auth.py      # /auth/register, /auth/login, /auth/login/json, /auth/me
│   ├── ai_engine/             # (empty — parsing/scoring, Phase B Step 4+)
│   └── utils/                 # (empty — shared helpers, added as needed)
├── tests/
│   ├── test_health.py
│   └── test_auth.py          # 9 tests covering register/login/me/RBAC
├── storage/resumes/
├── requirements.txt
├── .env / .env.example
└── README.md
```

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


## Next steps

- ~~**Phase B Step 2:** Authentication~~ ✅ done (this step) — JWT, roles,
  bcrypt hashing, `get_current_user`/`require_role` dependencies
- **Phase B Step 3:** Resume upload API (PDF/DOCX, validation, storage) —
  will use `Depends(get_current_user)` to associate uploads with the
  logged-in student
- **Phase B Step 4:** Resume parsing engine — text extraction via
  pdfplumber/pypdf/python-docx, entity extraction via rule-based
  regex/keyword matching (no spaCy for now)
- **Phase C:** ATS scoring and JD matching via rule-based keyword
  overlap, not embeddings — see "A note on the AI/NLP stack" below

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
