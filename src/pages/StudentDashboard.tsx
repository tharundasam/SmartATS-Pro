import { DashboardHeader } from "@/components/layout/DashboardHeader";
import { BottomNavBar } from "@/components/layout/BottomNavBar";
import { KpiGrid } from "@/components/dashboard/KpiGrid";
import { AtsEvolutionChart } from "@/components/dashboard/AtsEvolutionChart";
import { SkillProfile } from "@/components/dashboard/SkillProfile";
import { RecentUploadsList } from "@/components/dashboard/RecentUploadsList";
import { RecommendedActions } from "@/components/dashboard/RecommendedActions";
import { MOCK_DASHBOARD_SUMMARY } from "@/lib/mockDashboardData";
import { useStaggeredReveal } from "@/hooks/useStaggeredReveal";

/**
 * Ported from the second document in index.html ("Aura Intelligence -
 * Student Dashboard"). Markup/classes for each section are unchanged
 * from the original; the page is now data-driven from
 * MOCK_DASHBOARD_SUMMARY instead of hardcoded JSX values, so swapping in
 * a real API call later (Phase B, Module 10) only touches this one data
 * source.
 *
 * Two behaviors from the original <script> are reproduced via hooks:
 *   - staggered glass-card fade-in on mount      -> useStaggeredReveal,
 *     applied here in the same top-to-bottom DOM order the original
 *     querySelectorAll('.glass-card') would have walked: the 4 KPI
 *     cards, then the ATS Evolution + Skill Profile cards, then the
 *     Recent Uploads card.
 *   - bottom-nav active-state on click           -> BottomNavBar (NavLink)
 */
export default function StudentDashboard() {
  const data = MOCK_DASHBOARD_SUMMARY;

  // Index 0-3 reserved for the 4 KPI cards (applied inside KpiGrid via prop),
  // 4-5 for the two analytics cards, 6 for Recent Uploads.
  const atsChartReveal = useStaggeredReveal(4);
  const skillProfileReveal = useStaggeredReveal(5);
  const uploadsReveal = useStaggeredReveal(6);

  return (
    <div className="font-body-md text-on-surface selection:bg-primary/20">
      <DashboardHeader />

      <main className="pt-20 pb-28 px-margin-mobile md:px-margin-desktop max-w-[1280px] mx-auto min-h-screen">
        {/* Welcome Summary */}
        <section className="mb-xl">
          <h2 className="font-headline-lg-mobile text-headline-lg-mobile md:font-headline-lg md:text-headline-lg text-on-surface mb-xs">
            Welcome back, {data.studentName}
          </h2>
          <p className="text-on-surface-variant font-body-md">
            Your career profile is currently in the{" "}
            <span className="text-primary font-semibold">{data.percentileLabel}</span>{" "}
            of applicants in your field.
          </p>
        </section>

        <KpiGrid kpis={data.kpis} />

        {/* Visualizers & Analytics Grid */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-lg mb-xl">
          <div className="md:col-span-2" style={atsChartReveal}>
            <AtsEvolutionChart data={data.atsEvolution} />
          </div>
          <div style={skillProfileReveal}>
            <SkillProfile data={data.skillProfile} />
          </div>
        </section>

        <div style={uploadsReveal}>
          <RecentUploadsList uploads={data.recentUploads} />
        </div>

        <RecommendedActions
          onRunAnalysis={() => {
            // Wired to POST /api/ats/analyze in Phase C, Module 4.
            console.log("Run Analysis clicked");
          }}
          onUploadNew={() => {
            // Wired to POST /api/resumes/upload in Phase B, Module 2.
            console.log("Upload New Resume clicked");
          }}
        />
      </main>

      <BottomNavBar />
    </div>
  );
}
