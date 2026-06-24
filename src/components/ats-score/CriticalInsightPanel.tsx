interface CriticalInsightPanelProps {
  /** Full insight message, rendered as one block of text (AI-generated copy in the real system — not a template with fixed slots to parse). */
  message: string;
  jobFitLabel: string;
  atsRankLabel: string;
  onImproveKeywords?: () => void;
}

/**
 * Ported from the "Insights / Quick Stats" column next to the score
 * gauge. The original mockup hand-bolded specific words/numbers inside
 * the paragraph via inline <span> tags. Real insight copy will come from
 * an LLM and can't be reliably string-matched for "which words to bold",
 * so this component renders the whole message plainly — same content,
 * without brittle parsing logic standing in for what should eventually
 * be either rich-text from the API or a dedicated highlight field.
 */
export function CriticalInsightPanel({
  message,
  jobFitLabel,
  atsRankLabel,
  onImproveKeywords,
}: CriticalInsightPanelProps) {
  return (
    <div className="lg:col-span-7 space-y-md">
      <div className="glass-card p-lg rounded-2xl border-l-4 border-l-secondary">
        <h3 className="font-headline-sm text-headline-sm text-on-surface mb-xs">
          Critical Insight
        </h3>
        <p className="text-on-surface-variant font-body-md">{message}</p>
        <button
          onClick={onImproveKeywords}
          className="mt-lg bg-gradient-to-r from-primary to-secondary text-on-primary px-lg py-md rounded-xl font-bold hover:shadow-lg hover:shadow-primary/20 active:scale-95 transition-all flex items-center gap-2"
        >
          <span className="material-symbols-outlined">edit_note</span>
          Improve Keywords
        </button>
      </div>
      <div className="grid grid-cols-2 gap-md">
        <div className="glass-card p-md rounded-xl">
          <div className="text-on-surface-variant font-label-md uppercase mb-xs">
            Job Fit
          </div>
          <div className="font-headline-sm text-primary">{jobFitLabel}</div>
        </div>
        <div className="glass-card p-md rounded-xl">
          <div className="text-on-surface-variant font-label-md uppercase mb-xs">
            ATS Rank
          </div>
          <div className="font-headline-sm text-secondary">{atsRankLabel}</div>
        </div>
      </div>
    </div>
  );
}
