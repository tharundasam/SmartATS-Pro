import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from "@/pages/LandingPage";
import StudentDashboard from "@/pages/StudentDashboard";
import AtsScoreBreakdown from "@/pages/AtsScoreBreakdown";
import JobMatchEngine from "@/pages/JobMatchEngine";

/**
 * Route map mirrors the original static mockups:
 *   index.html              -> "/"            (LandingPage)
 *   dashboard mockup         -> "/dashboard"    (StudentDashboard)
 *   ATS score breakdown      -> "/ats-score"    (AtsScoreBreakdown)
 *   job match engine         -> "/job-match"    (JobMatchEngine)
 *
 * All four original mockups are now migrated. Routes referenced by the
 * JobMatchSidebar ("/skill-gap", "/ai-enhancer") are placeholders for
 * future modules (6 and 7) and are not yet implemented — see README.
 */
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<StudentDashboard />} />
        <Route path="/ats-score" element={<AtsScoreBreakdown />} />
        <Route path="/job-match" element={<JobMatchEngine />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
