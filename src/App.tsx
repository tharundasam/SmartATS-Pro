import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from "@/pages/LandingPage";
import StudentDashboard from "@/pages/StudentDashboard";

/**
 * Route map mirrors the original static mockups:
 *   index.html              -> "/"            (LandingPage)
 *   dashboard mockup         -> "/dashboard"    (StudentDashboard)
 *   ATS score breakdown      -> "/ats-score"    (AtsScoreBreakdown)  [next PR]
 *   job match engine         -> "/job-match"    (JobMatchEngine)     [next PR]
 *
 * AtsScoreBreakdown/JobMatchEngine are intentionally not wired yet —
 * they're the next two scaffold steps so each page can be verified
 * before the next one is added.
 */
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<StudentDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
