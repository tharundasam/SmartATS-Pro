interface JobMatchScoreGaugeProps {
  matchPercent: number; // 0-100
  verdictLabel: string;
  summary: string;
}

const RADIUS = 88;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS; // 552.92, matches original's hardcoded stroke-dasharray

/**
 * Ported from the "Score Card" SVG gauge in #analysis-results. The
 * original hardcoded stroke-dasharray="552.92" and
 * stroke-dashoffset="143.76" for a fixed 74% match. Both are now derived
 * from `matchPercent` using the same circle-circumference formula
 * (2 * pi * r), verified to reproduce the exact original values at 74%,
 * so the gauge stays correct for any score instead of only ever showing 74%.
 */
export function JobMatchScoreGauge({ matchPercent, verdictLabel, summary }: JobMatchScoreGaugeProps) {
  const offset = CIRCUMFERENCE * (1 - matchPercent / 100);

  return (
    <div className="glass-card rounded-3xl p-xl shadow-xl ai-glow">
      <div className="flex flex-col items-center text-center">
        <div className="relative w-48 h-48 mb-lg flex items-center justify-center">
          <svg className="w-full h-full -rotate-90" viewBox="0 0 192 192">
            <circle
              className="text-surface-container-high"
              cx="96"
              cy="96"
              fill="transparent"
              r={RADIUS}
              stroke="currentColor"
              strokeWidth="12"
            />
            <circle
              className="transition-all duration-[2000ms] ease-out"
              cx="96"
              cy="96"
              fill="transparent"
              r={RADIUS}
              stroke="url(#scoreGradient)"
              strokeDasharray={CIRCUMFERENCE}
              strokeDashoffset={offset}
              strokeLinecap="round"
              strokeWidth="12"
            />
            <defs>
              <linearGradient id="scoreGradient" x1="0%" x2="100%" y1="0%" y2="0%">
                <stop offset="0%" stopColor="#4648d4" />
                <stop offset="100%" stopColor="#6b38d4" />
              </linearGradient>
            </defs>
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="font-display-xl text-[56px] text-primary">{matchPercent}%</span>
            <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-widest">
              Match Score
            </span>
          </div>
        </div>
        <div className="inline-flex items-center gap-sm px-4 py-2 rounded-full bg-tertiary/10 text-tertiary mb-md">
          <span className="material-symbols-outlined text-[18px]">verified</span>
          <span className="font-label-md text-label-md">{verdictLabel}</span>
        </div>
        <p className="text-body-sm text-on-surface-variant">{summary}</p>
      </div>
    </div>
  );
}
