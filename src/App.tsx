import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from "@/pages/LandingPage";
import StudentDashboard from "@/pages/StudentDashboard";
import AtsScoreBreakdown from "@/pages/AtsScoreBreakdown";

/**
 * Route map mirrors the original static mockups:
 *   index.html              -> "/"            (LandingPage)
 *   dashboard mockup         -> "/dashboard"    (StudentDashboard)
 *   ATS score breakdown      -> "/ats-score"    (AtsScoreBreakdown)
 *   job match engine         -> "/job-match"    (JobMatchEngine)     [next PR]
 *
 * JobMatchEngine is intentionally not wired yet — that's the next
 * scaffold step so it can be verified before the next one is added.
 */
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<StudentDashboard />} />
        <Route path="/ats-score" element={<AtsScoreBreakdown />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
