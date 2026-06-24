import type { DashboardSummary } from "@/types/dashboard";

interface AtsEvolutionChartProps {
  data: DashboardSummary["atsEvolution"];
}

/**
 * Ported from the "ATS Evolution" card. The original hardcoded 6 bars
 * with hand-picked height percentages (40%, 55%, 45%, 70%, 75%, 82%) that
 * happened to roughly track the score values (62, 68, 64, 75, 79, 82).
 * Heights are now derived from `score` directly so the chart stays
 * correct if the data changes, instead of needing manual height tuning
 * per bar.
 */
// Tailwind scans source for literal class strings at build time, so
// `bg-primary/${opacity}` would not be detected/generated. Mapping to a
// fixed set of literal classes keeps the same visual progression the
// original markup used (10/15/20/30/50/80% opacity per bar).
const BAR_OPACITY_CLASSES = [
  "bg-primary/10",
  "bg-primary/15",
  "bg-primary/20",
  "bg-primary/30",
  "bg-primary/50",
  "bg-primary/80",
] as const;

export function AtsEvolutionChart({ data }: AtsEvolutionChartProps) {
  const maxScore = Math.max(...data.map((d) => d.score), 100);

  return (
    <div className="glass-card p-lg rounded-2xl">
      <div className="flex items-center justify-between mb-lg">
        <h3 className="font-headline-sm text-headline-sm">ATS Evolution</h3>
        <select className="bg-surface border-none text-body-sm font-medium focus:ring-0 rounded-lg">
          <option>Last 30 Days</option>
          <option>Last 6 Months</option>
        </select>
      </div>
      <div className="h-[240px] w-full flex items-end justify-between gap-2 px-2">
        {data.map((point, i) => {
          const barClass =
            BAR_OPACITY_CLASSES[Math.min(i, BAR_OPACITY_CLASSES.length - 1)];
          return (
            <div
              key={point.label}
              className={`flex-1 ${barClass} rounded-t-lg transition-all hover:bg-primary/30 relative group`}
              style={{ height: `${(point.score / maxScore) * 100}%` }}
            >
              <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-on-surface text-surface text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                {point.score}
              </div>
            </div>
          );
        })}
      </div>
      <div className="flex justify-between mt-md text-label-md text-on-surface-variant px-2">
        {data.map((point) => (
          <span key={point.label}>{point.label}</span>
        ))}
      </div>
    </div>
  );
}
