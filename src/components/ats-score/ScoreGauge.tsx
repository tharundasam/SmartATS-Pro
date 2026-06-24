interface ScoreGaugeProps {
  score: number; // 0-100
  percentileLabel: number;
}

const RADIUS = 44;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

/**
 * Ported from the Hero Score Section's circular gauge. The original
 * hardcoded `stroke-dasharray="276.46" stroke-dashoffset="49.76"` for a
 * fixed 82% score; here both values are derived from the `score` prop
 * (circumference = 2πr, offset = circumference * (1 - score/100)), so
 * the ring renders correctly for any score, not just 82.
 */
export function ScoreGauge({ score, percentileLabel }: ScoreGaugeProps) {
  const dashOffset = CIRCUMFERENCE * (1 - score / 100);

  return (
    <div className="lg:col-span-5 flex flex-col items-center justify-center p-lg glass-card rounded-2xl animate-score">
      <div className="relative w-64 h-64 flex items-center justify-center">
        <div className="absolute inset-0 rounded-full border-[12px] border-surface-container" />
        <div className="absolute inset-0 rounded-full border-[12px] border-transparent score-gradient opacity-20" />
        <svg className="absolute inset-0 w-full h-full -rotate-90" viewBox="0 0 100 100">
          <circle
            className="text-primary"
            cx="50"
            cy="50"
            fill="transparent"
            r={RADIUS}
            stroke="currentColor"
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={dashOffset}
            strokeWidth="8"
          />
        </svg>
        <div className="text-center z-10">
          <div className="font-display-xl text-display-xl bg-gradient-to-br from-primary to-secondary bg-clip-text text-transparent">
            {score}
          </div>
          <div className="font-label-md text-label-md text-on-surface-variant uppercase tracking-widest">
            Score / 100
          </div>
        </div>
      </div>
      <div className="mt-lg text-center">
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-tertiary/10 text-tertiary font-label-md text-label-md">
          <span
            className="material-symbols-outlined text-[16px]"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            auto_awesome
          </span>
          AI ANALYZED
        </span>
        <p className="mt-md text-on-surface-variant font-body-sm max-w-xs mx-auto">
          Your resume is performing better than{" "}
          <span className="font-bold text-primary">{percentileLabel}%</span> of
          applicants in this category.
        </p>
      </div>
    </div>
  );
}
