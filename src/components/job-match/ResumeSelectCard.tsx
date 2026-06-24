import type { ResumeOption } from "@/types/jobMatch";

interface ResumeSelectCardProps {
  options: ResumeOption[];
  value: string;
  onChange: (resumeId: string) => void;
  onUploadNew?: () => void;
}

/** Ported from the "Select Resume" glass-card. */
export function ResumeSelectCard({ options, value, onChange, onUploadNew }: ResumeSelectCardProps) {
  return (
    <div className="glass-card rounded-2xl p-lg shadow-sm">
      <div className="flex items-center justify-between mb-md">
        <h3 className="font-headline-sm text-headline-sm flex items-center gap-sm">
          <span className="material-symbols-outlined text-primary">description</span>
          Select Resume
        </h3>
        <button
          onClick={onUploadNew}
          className="text-primary font-label-md text-label-md hover:underline"
        >
          UPLOAD NEW
        </button>
      </div>
      <div className="relative group">
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-full appearance-none bg-surface-container-lowest border border-outline-variant/30 rounded-xl px-md py-4 font-body-md focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all outline-none cursor-pointer"
        >
          {options.map((option) => (
            <option key={option.id} value={option.id}>
              {option.fileName} ({option.updatedLabel})
            </option>
          ))}
        </select>
        <span className="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-on-surface-variant">
          expand_more
        </span>
      </div>
    </div>
  );
}
