/** Ported from the #result-placeholder dashed-border card. */
export function AnalysisPlaceholderCard() {
  return (
    <div className="glass-card rounded-3xl p-xl h-full flex flex-col items-center justify-center text-center border-dashed border-2 border-outline-variant/50">
      <div className="w-20 h-20 rounded-full bg-primary/5 flex items-center justify-center mb-md">
        <span className="material-symbols-outlined text-primary text-[40px] animate-pulse">
          analytics
        </span>
      </div>
      <h4 className="font-headline-sm text-headline-sm text-on-surface-variant mb-sm">
        Ready for Analysis
      </h4>
      <p className="text-on-surface-variant/70 text-body-sm max-w-[240px]">
        Select your resume and paste a job description to see your Aura Match score.
      </p>
    </div>
  );
}
