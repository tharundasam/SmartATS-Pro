import { NavLink } from "react-router-dom";
import { cn } from "@/lib/utils";

const SIDEBAR_LINKS = [
  { to: "/dashboard", icon: "dashboard", label: "Dashboard" },
  { to: "/ats-score", icon: "analytics", label: "Resume Analysis" },
  { to: "/job-match", icon: "target", label: "Job Match" },
  { to: "/skill-gap", icon: "trending_up", label: "Skill Gap" },
  { to: "/ai-enhancer", icon: "auto_awesome", label: "AI Enhancer" },
] as const;

interface JobMatchSidebarProps {
  atsScore: number;
}

/**
 * Ported from the Job Match Engine page's <aside> desktop sidebar.
 * The original's active-state was a click listener that manually swapped
 * className strings on every <a> in the sidebar (so it activated whatever
 * you clicked, regardless of where it linked — a purely cosmetic demo).
 * Replaced here with NavLink's real isActive, so the highlighted item
 * actually reflects the current route.
 */
export function JobMatchSidebar({ atsScore }: JobMatchSidebarProps) {
  return (
    <aside className="hidden md:flex fixed left-0 top-0 h-full w-[280px] z-[60] bg-surface/95 backdrop-blur-2xl border-r border-outline-variant/30 flex-col p-md space-y-base shadow-2xl">
      <div className="mb-xl pt-4">
        <h2 className="font-headline-lg text-headline-lg bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent px-4">
          Aura
        </h2>
      </div>
      <nav className="flex-1 space-y-2">
        {SIDEBAR_LINKS.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-md p-md rounded-xl transition-transform hover:translate-x-1",
                isActive
                  ? "bg-primary-container text-on-primary-container font-bold"
                  : "text-on-surface-variant hover:bg-surface-variant/50"
              )
            }
          >
            <span className="material-symbols-outlined">{link.icon}</span>
            <span className="font-body-md">{link.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="p-md bg-surface-container-low rounded-2xl">
        <div className="flex items-center gap-sm mb-2">
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
          <span className="font-label-md text-label-md text-primary uppercase">
            ATS Score
          </span>
        </div>
        <p className="font-headline-sm text-headline-sm">
          {atsScore}{" "}
          <span className="text-on-surface-variant font-normal text-body-sm">/ 100</span>
        </p>
      </div>
    </aside>
  );
}
