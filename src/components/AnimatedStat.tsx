import { useCountUp } from "@/hooks/useCountUp";

interface AnimatedStatProps {
  target: number;
  suffix: string; // e.g. "%", "k+", "x", "k"
  label: string;
}

/** One stat block from the Statistics Section, e.g. "95%  Success Rate". */
export function AnimatedStat({ target, suffix, label }: AnimatedStatProps) {
  const { ref, value } = useCountUp(target);

  return (
    <div className="space-y-base">
      <p
        ref={ref as React.RefObject<HTMLParagraphElement>}
        className="font-display-xl-mobile text-display-xl-mobile text-primary font-bold"
      >
        {value}
        {suffix}
      </p>
      <p className="text-body-sm font-label-md text-on-surface-variant uppercase tracking-widest">
        {label}
      </p>
    </div>
  );
}
