/** Ported from the dashed "Add Comparison" placeholder card. Purely static — no data/props needed. */
export function AddComparisonCard() {
  return (
    <div className="glass-card p-lg rounded-2xl border-dashed border-2 border-outline-variant/50 flex flex-col items-center justify-center text-center opacity-70">
      <div className="w-12 h-12 bg-surface-container rounded-full flex items-center justify-center mb-md">
        <span className="material-symbols-outlined text-on-surface-variant">add_chart</span>
      </div>
      <h4 className="font-headline-sm text-[16px] text-on-surface-variant">Add Comparison</h4>
      <p className="text-on-surface-variant text-body-sm mt-xs">
        Benchmark against other job IDs
      </p>
    </div>
  );
}
