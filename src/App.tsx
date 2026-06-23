import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from "@/pages/LandingPage";

/**
 * Route map mirrors the original static mockups:
 *   index.html              -> "/"            (LandingPage)
 *   dashboard mockup         -> "/dashboard"    (StudentDashboard)   [next PR]
 *   ATS score breakdown      -> "/ats-score"    (AtsScoreBreakdown)  [next PR]
 *   job match engine         -> "/job-match"    (JobMatchEngine)     [next PR]
 *
 * Dashboard/AtsScore/JobMatch are intentionally not wired yet — they're
 * the next three scaffold steps so each page can be verified before the
 * next one is added.
 */
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
