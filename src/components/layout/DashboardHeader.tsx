import { Link } from "react-router-dom";

interface DashboardHeaderProps {
  avatarUrl?: string;
  avatarAlt?: string;
}

/**
 * Ported from the dashboard mockup's <header>. This is a distinct
 * component from TopAppBar (landing page) — different layout (hamburger
 * + wordmark on the left, Dashboard/Jobs/Learning links, smaller avatar)
 * even though both share the same fixed/blur/border treatment.
 */
export function DashboardHeader({ avatarUrl, avatarAlt }: DashboardHeaderProps) {
  return (
    <header className="fixed top-0 w-full z-50 bg-surface/90 dark:bg-surface-dim/90 backdrop-blur-xl border-b border-outline-variant/50 shadow-sm flex items-center justify-between px-margin-mobile h-16">
      <div className="flex items-center gap-3">
        <span className="material-symbols-outlined text-primary">menu</span>
        <h1 className="font-display-xl-mobile text-display-xl-mobile bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent font-extrabold tracking-tight">
          Aura
        </h1>
      </div>
      <div className="flex items-center gap-4">
        <div className="hidden md:flex items-center gap-6 mr-6">
          <Link className="text-primary font-bold font-body-md" to="/dashboard">
            Dashboard
          </Link>
          <Link
            className="text-on-surface-variant hover:text-primary transition-colors font-body-md"
            to="/jobs"
          >
            Jobs
          </Link>
          <Link
            className="text-on-surface-variant hover:text-primary transition-colors font-body-md"
            to="/learning"
          >
            Learning
          </Link>
        </div>
        <div className="w-10 h-10 rounded-full overflow-hidden border-2 border-primary/20">
          {avatarUrl ? (
            <img
              className="w-full h-full object-cover"
              src={avatarUrl}
              alt={avatarAlt ?? "User avatar"}
            />
          ) : (
            <div className="w-full h-full bg-surface-container-high flex items-center justify-center">
              <span className="material-symbols-outlined text-on-surface-variant text-lg">
                person
              </span>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
