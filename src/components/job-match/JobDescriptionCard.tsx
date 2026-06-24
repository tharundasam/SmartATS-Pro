interface JobDescriptionCardProps {
  value: string;
  onChange: (value: string) => void;
  onAnalyze: () => void;
  isAnalyzing: boolean;
}

/**
 * Ported from the "Job Description" glass-card. The original's
 * "Analyze Match" button called a global `simulateAnalysis()` that
 * mutated the button's innerHTML directly and used a hardcoded
 * setTimeout. Replaced with controlled props: `isAnalyzing` drives the
 * spinner/disabled state, `onAnalyze` is the parent's responsibility
 * (currently a mock delay, later a real API call).
 */
export function JobDescriptionCard({
  value,
  onChange,
  onAnalyze,
  isAnalyzing,
}: JobDescriptionCardProps) {
  return (
    <div className="glass-card rounded-2xl p-lg shadow-sm">
      <div className="flex items-center justify-between mb-md">
        <h3 className="font-headline-sm text-headline-sm flex items-center gap-sm">
          <span className="material-symbols-outlined text-primary">work_outline</span>
          Job Description
        </h3>
        <div className="flex gap-sm">
          <button className="p-2 rounded-lg bg-surface-container-high text-on-surface-variant hover:text-primary transition-colors">
            <span className="material-symbols-outlined text-[20px]">link</span>
          </button>
          <button className="p-2 rounded-lg bg-surface-container-high text-on-surface-variant hover:text-primary transition-colors">
            <span className="material-symbols-outlined text-[20px]">upload_file</span>
          </button>
        </div>
      </div>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full h-80 bg-surface-container-lowest border border-outline-variant/30 rounded-xl p-md font-body-md focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all outline-none resize-none custom-scrollbar"
        placeholder="Paste the job description here to analyze match accuracy..."
      />
      <div className="mt-lg flex items-center justify-end">
        <button
          onClick={onAnalyze}
          disabled={isAnalyzing}
          className="primary-gradient text-white px-xl py-md rounded-xl font-headline-sm flex items-center gap-md hover:shadow-lg hover:shadow-primary/20 active:scale-95 transition-all duration-200 disabled:opacity-80"
        >
          {isAnalyzing ? (
            <>
              <span className="material-symbols-outlined animate-spin">sync</span>
              Analyzing...
            </>
          ) : (
            <>
              Analyze Match
              <span className="material-symbols-outlined">auto_awesome</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
