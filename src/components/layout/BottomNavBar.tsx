import { NavLink } from "react-router-dom";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { to: "/", icon: "home", label: "Home" },
  { to: "/ats-score", icon: "query_stats", label: "Analysis" },
  { to: "/job-match", icon: "travel_explore", label: "Match" },
  { to: "/ai-coach", icon: "psychology", label: "AI Coach" },
] as const;

/**
 * Ported from the <nav> bottom bar markup repeated across all four mockups.
 * Active-state styling (text-primary + scale-110) is now driven by
 * NavLink's isActive instead of the original per-page hardcoded class.
 */
export function BottomNavBar() {
  return (
    <nav className="md:hidden fixed bottom-0 w-full z-50 rounded-t-xl bg-surface/80 dark:bg-surface-container/80 backdrop-blur-lg border-t border-outline-variant/20 shadow-[0_-4px_20px_rgba(0,0,0,0.03)] flex justify-around items-center h-20 pb-safe px-sm">
      {NAV_ITEMS.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) =>
            cn(
              "flex flex-col items-center justify-center transition-all active:scale-90 duration-150",
              isActive
                ? "text-primary scale-110"
                : "text-on-surface-variant/70 hover:text-primary"
            )
          }
        >
          {({ isActive }) => (
            <>
              <span
                className="material-symbols-outlined"
                style={isActive ? { fontVariationSettings: "'FILL' 1" } : undefined}
              >
                {item.icon}
              </span>
              <span className="font-label-md text-label-md">{item.label}</span>
            </>
          )}
        </NavLink>
      ))}
    </nav>
  );
}
