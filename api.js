/**
 * SmartATS Pro — shared API client.
 *
 * Wraps the backend at API_BASE_URL (default: http://localhost:8000).
 * Stores the JWT in localStorage under TOKEN_KEY and attaches it to every
 * authenticated call automatically.
 *
 * Every exported function either resolves with the parsed JSON body the
 * backend returned, or throws an ApiError with a human-readable `.message`
 * and the original `.status` / `.detail` attached, so callers can show
 * something useful instead of a raw fetch failure.
 */

const API_BASE_URL = window.SMARTATS_API_BASE_URL || "http://localhost:8000";
const TOKEN_KEY = "smartats_token";
const USER_KEY = "smartats_user";

class ApiError extends Error {
  constructor(message, status, detail) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

// ---------------------------------------------------------------------------
// Token / session helpers
// ---------------------------------------------------------------------------

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setSession(accessToken, user) {
  localStorage.setItem(TOKEN_KEY, accessToken);
  if (user) localStorage.setItem(USER_KEY, JSON.stringify(user));
}

function clearSession() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

function getCachedUser() {
  const raw = localStorage.getItem(USER_KEY);
  return raw ? JSON.parse(raw) : null;
}

function isLoggedIn() {
  return Boolean(getToken());
}

// ---------------------------------------------------------------------------
// Core request helper
// ---------------------------------------------------------------------------

/**
 * @param {string} path - e.g. "/api/v1/auth/me"
 * @param {object} options
 * @param {string} options.method
 * @param {object|FormData} [options.body] - plain object is JSON-encoded; FormData is sent as-is
 * @param {boolean} [options.auth=true] - attach Authorization header if a token exists
 * @param {boolean} [options.form=false] - send body as application/x-www-form-urlencoded
 */
async function request(path, { method = "GET", body, auth = true, form = false } = {}) {
  const headers = {};
  const init = { method, headers };

  if (body instanceof FormData) {
    init.body = body; // browser sets the multipart boundary itself
  } else if (form && body) {
    headers["Content-Type"] = "application/x-www-form-urlencoded";
    init.body = new URLSearchParams(body).toString();
  } else if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(body);
  }

  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, init);
  } catch (networkErr) {
    throw new ApiError(
      "Can't reach the SmartATS Pro server. Check that the backend is running and the API base URL is correct.",
      0,
      networkErr
    );
  }

  // 204 No Content — nothing to parse
  if (response.status === 204) return null;

  const isJson = response.headers.get("content-type")?.includes("application/json");
  const payload = isJson ? await response.json().catch(() => null) : await response.text();

  if (!response.ok) {
    if (response.status === 401) {
      clearSession();
    }
    const message = extractErrorMessage(payload, response.status);
    throw new ApiError(message, response.status, payload);
  }

  return payload;
}

/** Turns FastAPI's error shapes (HTTPValidationError / {detail: str}) into one readable line. */
function extractErrorMessage(payload, status) {
  if (!payload) return `Request failed (${status}).`;
  if (typeof payload.detail === "string") return payload.detail;
  if (Array.isArray(payload.detail)) {
    return payload.detail
      .map((e) => `${(e.loc || []).slice(-1)[0] ?? "field"}: ${e.msg}`)
      .join("; ");
  }
  return `Request failed (${status}).`;
}

// ---------------------------------------------------------------------------
// Auth
// ---------------------------------------------------------------------------

/** POST /api/v1/auth/register — creates an account and logs the user in immediately. */
async function register({ fullName, email, password, role = "student" }) {
  const data = await request("/api/v1/auth/register", {
    method: "POST",
    auth: false,
    body: { full_name: fullName, email, password, role },
  });
  setSession(data.access_token, data.user);
  return data;
}

/** POST /api/v1/auth/login/json — JSON login (email + password). */
async function login({ email, password }) {
  const data = await request("/api/v1/auth/login/json", {
    method: "POST",
    auth: false,
    body: { email, password },
  });
  setSession(data.access_token, data.user);
  return data;
}

function logout() {
  clearSession();
}

/** GET /api/v1/auth/me */
async function getMe() {
  const user = await request("/api/v1/auth/me", { method: "GET" });
  localStorage.setItem(USER_KEY, JSON.stringify(user));
  return user;
}

// ---------------------------------------------------------------------------
// Resumes
// ---------------------------------------------------------------------------

/** POST /api/v1/resumes/upload — multipart upload, field name must be "file". */
async function uploadResume(file) {
  const formData = new FormData();
  formData.append("file", file);
  return request("/api/v1/resumes/upload", { method: "POST", body: formData });
}

/** GET /api/v1/resumes — most recent first. */
async function listResumes() {
  return request("/api/v1/resumes", { method: "GET" });
}

/** GET /api/v1/resumes/{resumeId} */
async function getResume(resumeId) {
  return request(`/api/v1/resumes/${resumeId}`, { method: "GET" });
}

/** DELETE /api/v1/resumes/{resumeId} */
async function deleteResume(resumeId) {
  return request(`/api/v1/resumes/${resumeId}`, { method: "DELETE" });
}

/** GET /api/v1/resumes/{resumeId}/parsed-data */
async function getParsedData(resumeId) {
  return request(`/api/v1/resumes/${resumeId}/parsed-data`, { method: "GET" });
}

/** POST /api/v1/resumes/{resumeId}/reparse */
async function reparseResume(resumeId) {
  return request(`/api/v1/resumes/${resumeId}/reparse`, { method: "POST" });
}

// ---------------------------------------------------------------------------
// ATS scoring
// ---------------------------------------------------------------------------

/**
 * POST /api/v1/ats/score/{resumeId}
 * Omit jobDescription (or pass null/empty) for generic ATS checks.
 * Pass jobDescription for JD-matched scoring (Job Match Engine page).
 */
async function scoreResume(resumeId, jobDescription = null) {
  const jd = jobDescription && jobDescription.trim() ? jobDescription.trim() : null;
  return request(`/api/v1/ats/score/${resumeId}`, {
    method: "POST",
    body: { job_description: jd },
  });
}

/** GET /api/v1/ats/reports/{resumeId} — full history of reports for one resume. */
async function listReports(resumeId) {
  return request(`/api/v1/ats/reports/${resumeId}`, { method: "GET" });
}

/** GET /api/v1/ats/reports/{resumeId}/{reportId} */
async function getReport(resumeId, reportId) {
  return request(`/api/v1/ats/reports/${resumeId}/${reportId}`, { method: "GET" });
}

/** Convenience: most recent report for a resume, or null if none exist yet. */
async function getLatestReport(resumeId) {
  const reports = await listReports(resumeId);
  const list = Array.isArray(reports) ? reports : reports?.reports ?? [];
  if (!list.length) return null;
  return [...list].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))[0];
}

// ---------------------------------------------------------------------------
// Derived / approximate UI metrics
//
// The mockups show a few numbers the backend schema does not provide
// (job-match %, percentile rank, skill radar). These helpers derive a
// labelled approximation from real ATSReportOut fields rather than
// inventing data outright. Every value returned here is presentational
// only — never treat it as a score the backend actually computed.
// ---------------------------------------------------------------------------

/**
 * Approximate "Job Match %" shown on the dashboard / hero mockups.
 * When a JD-matched report exists, overall_score from that report IS
 * effectively a job-match score already (see ATSScoreRequest docstring),
 * so we surface it as-is but labelled "approximate".
 */
function approxJobMatchPercent(report) {
  if (!report || report.job_description == null) return null;
  return Math.round(report.overall_score);
}

/** Approximate percentile framing for the "ATS Rank" / "Top X%" UI chip. Coarse banding, not a real percentile computed against other users. */
function approxRankLabel(overallScore) {
  if (overallScore == null) return "—";
  if (overallScore >= 90) return "Top 5%";
  if (overallScore >= 80) return "Top 15%";
  if (overallScore >= 65) return "Top 35%";
  if (overallScore >= 50) return "Top 60%";
  return "Needs work";
}

window.SmartATSApi = {
  ApiError,
  // session
  isLoggedIn,
  getCachedUser,
  logout,
  // auth
  register,
  login,
  getMe,
  // resumes
  uploadResume,
  listResumes,
  getResume,
  deleteResume,
  getParsedData,
  reparseResume,
  // ats
  scoreResume,
  listReports,
  getReport,
  getLatestReport,
  // derived
  approxJobMatchPercent,
  approxRankLabel,
};
