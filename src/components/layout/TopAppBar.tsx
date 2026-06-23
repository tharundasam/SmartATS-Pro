import { Link } from "react-router-dom";

interface TopAppBarProps {
  /** Avatar image URL for the logged-in user. Falls back to a placeholder block if omitted. */
  avatarUrl?: string;
  avatarAlt?: string;
}

/**
 * Ported from the <header> in the original index.html hero mockup.
 * Markup/classes are unchanged; only the nav links became <Link> for
 * client-side routing and the avatar became a prop instead of a hardcoded
 * Google-hosted image URL.
 */
export function TopAppBar({ avatarUrl, avatarAlt }: TopAppBarProps) {
  return (
    <header className="fixed top-0 w-full z-50 bg-surface/90 dark:bg-surface-dim/90 backdrop-blur-xl border-b border-outline-variant/50 shadow-sm flex items-center justify-between px-margin-mobile md:px-margin-desktop h-16">
      <div className="flex items-center gap-base">
        <span className="material-symbols-outlined text-primary text-3xl">
          auto_awesome
        </span>
        <span className="font-display-xl-mobile text-headline-sm text-gradient font-bold">
          Aura Intelligence
        </span>
      </div>
      <nav className="hidden md:flex items-center space-x-lg">
        <Link className="text-primary font-bold font-body-md" to="/">
          Home
        </Link>
        <Link
          className="text-on-surface-variant hover:bg-primary/5 px-sm py-base rounded-lg transition-colors font-body-md"
          to="/ats-score"
        >
          Analysis
        </Link>
        <Link
          className="text-on-surface-variant hover:bg-primary/5 px-sm py-base rounded-lg transition-colors font-body-md"
          to="/pricing"
        >
          Pricing
        </Link>
        <Link
          className="text-on-surface-variant hover:bg-primary/5 px-sm py-base rounded-lg transition-colors font-body-md"
          to="/ai-coach"
        >
          AI Coach
        </Link>
      </nav>
      <div className="flex items-center gap-md">
        <button className="hidden md:block px-md py-sm font-semibold text-primary hover:bg-primary/5 rounded-xl transition-all">
          Sign In
        </button>
        <div className="w-10 h-10 rounded-full bg-primary-container flex items-center justify-center text-on-primary-container overflow-hidden">
          {avatarUrl ? (
            <img
              className="w-full h-full object-cover"
              src={avatarUrl}
              alt={avatarAlt ?? "User avatar"}
            />
          ) : (
            <span className="material-symbols-outlined text-lg">person</span>
          )}
        </div>
      </div>
    </header>
  );
}
