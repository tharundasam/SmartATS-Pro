import { useEffect, useState } from "react";

/**
 * Re-implements the ATS Score page's original script: every progress bar
 * started at width:0% and animated to its real width 100ms after mount
 * (relying on the `transition-all duration-1000` class already on the
 * element for the animation itself). Returns 0 until 100ms after mount,
 * then the real value — paired with a CSS transition class, this
 * produces the same fill-in effect.
 */
export function useAnimatedWidth(targetPercent: number, delayMs = 100) {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    const timeout = setTimeout(() => setWidth(targetPercent), delayMs);
    return () => clearTimeout(timeout);
  }, [targetPercent, delayMs]);

  return width;
}
