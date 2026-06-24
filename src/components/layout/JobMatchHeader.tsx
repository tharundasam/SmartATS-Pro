interface JobMatchHeaderProps {
  avatarUrl?: string;
  avatarAlt?: string;
}

/**
 * Ported from the Job Match Engine page's own <header>. Distinct from
 * both TopAppBar (landing) and DashboardHeader (student dashboard) — this
 * one has an "UPGRADE" pill button instead of Sign In/nav links, since
 * the page assumes you're already inside the authenticated app shell
 * (the desktop sidebar carries primary navigation here instead).
 */
export function JobMatchHeader({ avatarUrl, avatarAlt }: JobMatchHeaderProps) {
  return (
    <header className="fixed top-0 w-full z-50 bg-surface/90 backdrop-blur-xl border-b border-outline-variant/50 shadow-sm h-16 flex items-center justify-between px-margin-mobile md:px-margin-desktop">
      <div className="flex items-center gap-md">
        <span className="material-symbols-outlined text-primary">menu</span>
        <h1 className="font-display-xl-mobile text-display-xl-mobile md:text-headline-lg bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
          Aura Intelligence
        </h1>
      </div>
      <div className="flex items-center gap-md">
        <button className="hidden md:flex items-center gap-sm px-md py-sm rounded-full bg-primary/5 text-primary hover:bg-primary/10 transition-colors">
          <span className="material-symbols-outlined text-[20px]">bolt</span>
          <span className="font-label-md text-label-md">UPGRADE</span>
        </button>
        <div className="w-10 h-10 rounded-full bg-surface-container-high border border-outline-variant/30 flex items-center justify-center overflow-hidden">
          {avatarUrl ? (
            <img
              className="w-full h-full object-cover"
              src={avatarUrl}
              alt={avatarAlt ?? "User avatar"}
            />
          ) : (
            <span className="material-symbols-outlined text-on-surface-variant text-lg">
              person
            </span>
          )}
        </div>
      </div>
    </header>
  );
}
