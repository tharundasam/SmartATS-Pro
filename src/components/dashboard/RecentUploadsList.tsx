import type { ResumeUpload } from "@/types/dashboard";
import { cn } from "@/lib/utils";

interface RecentUploadsListProps {
  uploads: ResumeUpload[];
}

const STATUS_BADGE: Record<ResumeUpload["status"], { label: string; className: string }> = {
  PROCESSED: {
    label: "PROCESSED",
    className: "bg-surface-container-high text-on-surface-variant",
  },
  LOW_MATCH: {
    label: "LOW MATCH",
    className: "bg-error-container text-on-error-container",
  },
  PROCESSING: {
    label: "PROCESSING",
    className: "bg-tertiary/10 text-tertiary",
  },
  FAILED: {
    label: "FAILED",
    className: "bg-error-container text-error",
  },
};

const ICON_COLOR_BY_INDEX = ["bg-primary/10 text-primary", "bg-secondary/10 text-secondary", "bg-tertiary/10 text-tertiary"];
const SCORE_COLOR_BY_STATUS: Record<ResumeUpload["status"], string> = {
  PROCESSED: "text-primary",
  LOW_MATCH: "text-error",
  PROCESSING: "text-tertiary",
  FAILED: "text-error",
};

/** Ported from the "Recent Uploads" activity feed. */
export function RecentUploadsList({ uploads }: RecentUploadsListProps) {
  return (
    <section className="glass-card rounded-2xl overflow-hidden">
      <div className="p-lg border-b border-outline-variant/30 flex items-center justify-between">
        <h3 className="font-headline-sm text-headline-sm">Recent Uploads</h3>
        <button className="text-primary text-body-sm font-semibold hover:underline">
          View All
        </button>
      </div>
      <div className="divide-y divide-outline-variant/20">
        {uploads.map((upload, i) => {
          const badge = STATUS_BADGE[upload.status];
          const iconColor = ICON_COLOR_BY_INDEX[i % ICON_COLOR_BY_INDEX.length];
          const scoreColor = SCORE_COLOR_BY_STATUS[upload.status];

          return (
            <div
              key={upload.id}
              className="p-md hover:bg-surface-container-low transition-colors flex items-center justify-between group"
            >
              <div className="flex items-center gap-4">
                <div className={cn("w-12 h-12 rounded-xl flex items-center justify-center", iconColor)}>
                  <span className="material-symbols-outlined">description</span>
                </div>
                <div>
                  <p className="font-body-md font-semibold text-on-surface">
                    {upload.fileName}
                  </p>
                  <p className="text-body-sm text-on-surface-variant">
                    Uploaded {upload.uploadedAt} • {upload.fileSizeLabel}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <span
                  className={cn(
                    "hidden md:inline-block px-3 py-1 rounded-full text-[11px] font-bold",
                    badge.className
                  )}
                >
                  {badge.label}
                </span>
                <div className="flex flex-col items-end">
                  <span className={cn("font-bold", scoreColor)}>{upload.atsScore}</span>
                  <span className="text-[10px] text-on-surface-variant uppercase">
                    ATS Score
                  </span>
                </div>
                <span className="material-symbols-outlined text-on-surface-variant group-hover:text-primary transition-colors cursor-pointer">
                  chevron_right
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
