import { useNavigate } from "react-router-dom";

interface AtsScoreHeaderProps {
  title: string;
  avatarUrl?: string;
  avatarAlt?: string;
}

/**
 * Ported from the ATS Score Breakdown page's <header>. A third distinct
 * header variant (back button + page title, smaller avatar) — kept
 * separate from TopAppBar and DashboardHeader since the original design
 * used three different header layouts across the four pages.
 */
export function AtsScoreHeader({ title, avatarUrl, avatarAlt }: AtsScoreHeaderProps) {
  const navigate = useNavigate();

  return (
    <header className="fixed top-0 w-full z-50 bg-surface/90 dark:bg-surface-dim/90 backdrop-blur-xl border-b border-outline-variant/50 shadow-sm flex items-center justify-between px-margin-mobile h-16 w-full">
      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate(-1)}
          className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-primary/5 active:scale-95 transition-all"
          aria-label="Go back"
        >
          <span className="material-symbols-outlined text-primary">arrow_back</span>
        </button>
        <h1 className="font-headline-sm text-headline-sm-mobile text-primary">{title}</h1>
      </div>
      <div className="flex items-center">
        <div className="w-8 h-8 rounded-full bg-primary-container flex items-center justify-center overflow-hidden border border-outline-variant/30">
          {avatarUrl ? (
            <img
              className="w-full h-full object-cover"
              src={avatarUrl}
              alt={avatarAlt ?? "User avatar"}
            />
          ) : (
            <span className="material-symbols-outlined text-on-primary-container text-sm">
              person
            </span>
          )}
        </div>
      </div>
    </header>
  );
}
