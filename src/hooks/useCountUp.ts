import { useEffect, useRef, useState } from "react";

/**
 * Re-implements the vanilla-JS counter animation from the original
 * index.html <script> block: counts from 0 to `target` once the element
 * scrolls into view (50% visible), over `durationMs`.
 */
export function useCountUp(target: number, durationMs = 2000) {
  const [value, setValue] = useState(0);
  const ref = useRef<HTMLElement | null>(null);
  const hasAnimated = useRef(false);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasAnimated.current) {
            hasAnimated.current = true;
            const startTime = performance.now();

            const step = (now: number) => {
              const elapsed = now - startTime;
              const progress = Math.min(elapsed / durationMs, 1);
              setValue(Math.floor(progress * target));
              if (progress < 1) {
                requestAnimationFrame(step);
              } else {
                setValue(target);
              }
            };

            requestAnimationFrame(step);
            observer.unobserve(node);
          }
        });
      },
      { threshold: 0.5 }
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, [target, durationMs]);

  return { ref, value };
}
