import type { DashboardSummary } from "@/types/dashboard";
import { KpiCard } from "@/components/dashboard/KpiCard";
import { useStaggeredReveal } from "@/hooks/useStaggeredReveal";

interface KpiGridProps {
  kpis: DashboardSummary["kpis"];
}

/** Ported from the "KPI Cards Grid" section: ATS Score, Resume Strength, Job Matches, Missing Skills. */
export function KpiGrid({ kpis }: KpiGridProps) {
  const atsScoreReveal = useStaggeredReveal(0);
  const resumeStrengthReveal = useStaggeredReveal(1);
  const jobMatchesReveal = useStaggeredReveal(2);
  const missingSkillsReveal = useStaggeredReveal(3);

  return (
    <section className="grid grid-cols-2 md:grid-cols-4 gap-md mb-xl">
      <KpiCard style={atsScoreReveal}>
        <div>
          <span className="text-label-md font-label-md text-on-surface-variant uppercase tracking-wider block mb-sm">
            ATS Score
          </span>
          <div className="flex items-baseline gap-1">
            <span className="text-headline-lg font-headline-lg text-primary">
              {kpis.atsScore}
            </span>
            <span className="text-body-sm text-on-surface-variant">/100</span>
          </div>
        </div>
        <div className="mt-md h-1 w-full bg-surface-variant rounded-full overflow-hidden">
          <div className="h-full bg-primary" style={{ width: `${kpis.atsScore}%` }} />
        </div>
      </KpiCard>

      <KpiCard style={resumeStrengthReveal}>
        <div>
          <span className="text-label-md font-label-md text-on-surface-variant uppercase tracking-wider block mb-sm">
            Resume Strength
          </span>
          <div className="text-headline-sm font-headline-sm text-secondary">
            {kpis.resumeStrength}
          </div>
        </div>
        <div className="mt-md flex items-center gap-1">
          <span
            className="material-symbols-outlined text-secondary text-sm"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            auto_awesome
          </span>
          <span className="ai-badge px-2 py-0.5 rounded-full text-[10px]">AI VERIFIED</span>
        </div>
      </KpiCard>

      <KpiCard style={jobMatchesReveal}>
        <div>
          <span className="text-label-md font-label-md text-on-surface-variant uppercase tracking-wider block mb-sm">
            Job Matches
          </span>
          <div className="text-headline-lg font-headline-lg text-tertiary">
            {kpis.jobMatches}
          </div>
        </div>
        <div className="mt-md text-body-sm text-on-surface-variant">
          {kpis.jobMatchesDelta}
        </div>
      </KpiCard>

      <KpiCard style={missingSkillsReveal}>
        <div>
          <span className="text-label-md font-label-md text-on-surface-variant uppercase tracking-wider block mb-sm">
            Missing Skills
          </span>
          <div className="text-headline-lg font-headline-lg text-error">
            {kpis.missingSkillsCount}
          </div>
        </div>
        <div className="mt-md text-body-sm text-error font-medium">Critical Gaps</div>
      </KpiCard>
    </section>
  );
}
