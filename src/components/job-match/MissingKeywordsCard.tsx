interface MissingKeywordsCardProps {
  keywords: string[];
}

/** Ported from the "Missing Keywords" glass-card. */
export function MissingKeywordsCard({ keywords }: MissingKeywordsCardProps) {
  return (
    <div className="glass-card rounded-2xl p-lg shadow-sm">
      <h4 className="font-headline-sm text-headline-sm mb-md flex items-center gap-sm">
        <span className="material-symbols-outlined text-error">warning</span>
        Missing Keywords
      </h4>
      <div className="flex flex-wrap gap-sm">
        {keywords.map((keyword) => (
          <span
            key={keyword}
            className="px-md py-base rounded-full bg-error-container text-on-error-container font-label-md text-label-md flex items-center gap-xs"
          >
            {keyword}
            <span className="material-symbols-outlined text-[14px]">add</span>
          </span>
        ))}
      </div>
    </div>
  );
}
