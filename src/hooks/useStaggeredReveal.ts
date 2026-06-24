import { useEffect, useState } from "react";

/**
 * Re-implements the dashboard's original DOMContentLoaded script that
 * faded in every `.glass-card` with a 100ms stagger per card index.
 * Returns the style object to spread onto each card's `style` prop.
 */
export function useStaggeredReveal(index: number, staggerMs = 100) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const timeout = setTimeout(() => setVisible(true), index * staggerMs);
    return () => clearTimeout(timeout);
  }, [index, staggerMs]);

  return {
    opacity: visible ? 1 : 0,
    transform: visible ? "translateY(0)" : "translateY(20px)",
    transition: "all 0.6s cubic-bezier(0.22, 1, 0.36, 1)",
  } as const;
}
