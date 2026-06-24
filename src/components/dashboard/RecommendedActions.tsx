interface RecommendedActionsProps {
  onRunAnalysis?: () => void;
  onUploadNew?: () => void;
}

/**
 * Ported from the "Recommended Actions" bento section: the primary
 * "AI Resume Optimizer" CTA card and the dashed "Upload New Resume" card.
 * Click handlers are optional props so this stays a dumb presentational
 * component — the dashboard page decides what happens (navigate, open
 * upload modal, etc.) once that's wired to real behavior.
 */
export function RecommendedActions({ onRunAnalysis, onUploadNew }: RecommendedActionsProps) {
  return (
    <section className="mt-xl grid grid-cols-1 md:grid-cols-2 gap-md">
      <div className="glass-card p-lg rounded-2xl bg-primary text-white overflow-hidden relative group cursor-pointer">
        <div className="relative z-10">
          <h4 className="font-headline-sm mb-base">AI Resume Optimizer</h4>
          <p className="text-primary-fixed text-sm opacity-90 mb-md max-w-[240px]">
            Improve your current score by 15 points using tailored AI suggestions.
          </p>
          <button
            onClick={onRunAnalysis}
            className="bg-white text-primary px-lg py-sm rounded-full text-body-sm font-bold shadow-lg active:scale-95 transition-transform"
          >
            Run Analysis
          </button>
        </div>
        <span className="material-symbols-outlined absolute -right-4 -bottom-4 text-9xl opacity-10 group-hover:scale-110 transition-transform duration-500">
          auto_awesome
        </span>
      </div>
      <button
        onClick={onUploadNew}
        className="glass-card p-lg rounded-2xl border-2 border-dashed border-primary/30 flex flex-col items-center justify-center text-center cursor-pointer hover:border-primary transition-colors"
      >
        <div className="w-14 h-14 rounded-full bg-primary/5 flex items-center justify-center mb-md">
          <span className="material-symbols-outlined text-primary text-3xl">add</span>
        </div>
        <p className="font-body-md font-semibold text-on-surface">Upload New Resume</p>
        <p className="text-body-sm text-on-surface-variant">PDF, DOCX up to 10MB</p>
      </button>
    </section>
  );
}
