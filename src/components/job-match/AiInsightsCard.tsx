interface AiInsightsCardProps {
  insights: { title: string; description: string }[];
  onApplyChanges?: () => void;
}

/** Ported from the "Recommended Improvements" / "AI Insights" glass-card. */
export function AiInsightsCard({ insights, onApplyChanges }: AiInsightsCardProps) {
  return (
    <div className="glass-card rounded-2xl p-lg shadow-sm">
      <h4 className="font-headline-sm text-headline-sm mb-md flex items-center gap-sm">
        <span className="material-symbols-outlined text-primary">tips_and_updates</span>
        AI Insights
      </h4>
      <div className="space-y-md">
        {insights.map((insight) => (
          <div key={insight.title} className="flex gap-md p-md rounded-xl bg-surface-container-low">
            <span className="material-symbols-outlined text-primary mt-1">lightbulb</span>
            <div>
              <p className="font-body-md font-semibold text-on-surface">{insight.title}</p>
              <p className="text-body-sm text-on-surface-variant">{insight.description}</p>
            </div>
          </div>
        ))}
      </div>
      <button
        onClick={onApplyChanges}
        className="w-full mt-lg border border-primary/30 text-primary py-md rounded-xl font-label-md hover:bg-primary/5 transition-colors"
      >
        APPLY CHANGES WITH AI
      </button>
    </div>
  );
}
