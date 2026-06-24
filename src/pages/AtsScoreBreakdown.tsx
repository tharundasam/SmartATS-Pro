import { AtsScoreHeader } from "@/components/layout/AtsScoreHeader";
import { BottomNavBar } from "@/components/layout/BottomNavBar";
import { ScoreGauge } from "@/components/ats-score/ScoreGauge";
import { CriticalInsightPanel } from "@/components/ats-score/CriticalInsightPanel";
import { MetricCard } from "@/components/ats-score/MetricCard";
import { AddComparisonCard } from "@/components/ats-score/AddComparisonCard";
import { MOCK_ATS_SCORE } from "@/lib/mockAtsScoreData";

/**
 * Ported from the third document in index.html ("ATS Score Breakdown").
 * Markup/classes for each section are unchanged from the original; the
 * page is data-driven from MOCK_ATS_SCORE instead of hardcoded JSX
 * values, so swapping in a real `GET /api/ats/score/:resumeId` call
 * later (Phase C, Module 4) only touches this one data source.
 *
 * Two behaviors from the original page are reproduced via hooks:
 *   - the score gauge's SVG ring math (was hardcoded for score=82,
 *     now derived from any score)        -> ScoreGauge
 *   - progress bars animating from 0% to their real width on mount
 *                                          -> useAnimatedWidth (in MetricCard)
 */
export default function AtsScoreBreakdown() {
  const data = MOCK_ATS_SCORE;

  return (
    <div className="bg-background text-on-surface font-body-md min-h-screen pb-32">
      <AtsScoreHeader title="ATS Score Breakdown" />

      <main className="pt-24 px-margin-mobile md:px-margin-desktop max-w-7xl mx-auto">
        {/* Hero Score Section */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-gutter mb-xl items-center">
          <ScoreGauge score={data.overallScore} percentileLabel={data.percentileLabel} />
          <CriticalInsightPanel
            message={data.criticalInsight.message}
            jobFitLabel={data.jobFitLabel}
            atsRankLabel={data.atsRankLabel}
            onImproveKeywords={() => {
              // Wired to the AI Resume Enhancement flow in Phase C, Module 7.
              console.log("Improve Keywords clicked");
            }}
          />
        </section>

        {/* Detailed Breakdown Bento Grid */}
        <h2 className="font-headline-sm text-headline-sm text-on-surface mb-lg">
          Metric Breakdown
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-gutter">
          {data.metrics.map((metric) => (
            <MetricCard key={metric.id} metric={metric} />
          ))}
          <AddComparisonCard />
        </div>
      </main>

      <BottomNavBar />
    </div>
  );
}
