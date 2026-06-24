import type { AtsMetric, MetricColor } from "@/types/atsScore";
import { cn } from "@/lib/utils";
import { useAnimatedWidth } from "@/hooks/useAnimatedWidth";

interface MetricCardProps {
  metric: AtsMetric;
}

// Tailwind needs literal class strings at build time, so dynamic
// `bg-${color}/10` interpolation would not be picked up by the scanner.
// Each color variant used by a metric is mapped to its literal classes here.
const COLOR_CLASSES: Record<
  MetricColor,
  { iconBg: string; iconText: string; badgeBg: string; badgeText: string; barBg: string }
> = {
  primary: {
    iconBg: "bg-primary/10",
    iconText: "text-primary",
    badgeBg: "bg-primary-fixed",
    badgeText: "text-primary",
    barBg: "bg-primary",
  },
  tertiary: {
    iconBg: "bg-tertiary/10",
    iconText: "text-tertiary",
    badgeBg: "bg-tertiary-fixed",
    badgeText: "text-tertiary",
    barBg: "bg-tertiary",
  },
  error: {
    iconBg: "bg-error/10",
    iconText: "text-error",
    badgeBg: "bg-error-container",
    badgeText: "text-error",
    barBg: "bg-error",
  },
  secondary: {
    iconBg: "bg-secondary/10",
    iconText: "text-secondary",
    badgeBg: "bg-secondary-fixed",
    badgeText: "text-secondary",
    barBg: "bg-secondary",
  },
  "tertiary-container": {
    iconBg: "bg-tertiary-container/10",
    iconText: "text-tertiary-container",
    badgeBg: "bg-surface-container-highest",
    badgeText: "text-tertiary-container",
    barBg: "bg-tertiary-container",
  },
};

/**
 * Ported from the "Detailed Breakdown Bento Grid" cards (Skills Score,
 * Formatting, Keywords, Education, Projects). The Keywords card had an
 * extra warning treatment (red border + tinted background) in the
 * original — preserved here via `metric.isWarning`.
 */
export function MetricCard({ metric }: MetricCardProps) {
  const colors = COLOR_CLASSES[metric.color];
  const animatedWidth = useAnimatedWidth(metric.percent);

  return (
    <div
      className={cn(
        "glass-card p-lg rounded-2xl flex flex-col justify-between hover:translate-y-[-4px] transition-transform duration-300",
        metric.isWarning && "border-2 border-error/10 bg-error-container/5"
      )}
    >
      <div className="flex justify-between items-start mb-lg">
        <div className={cn("w-12 h-12 rounded-xl flex items-center justify-center", colors.iconBg)}>
          <span className={cn("material-symbols-outlined", colors.iconText)}>{metric.icon}</span>
        </div>
        <span
          className={cn(
            "font-label-md text-label-md px-2 py-0.5 rounded-full",
            colors.badgeBg,
            colors.badgeText
          )}
        >
          {metric.percent}%
        </span>
      </div>
      <div>
        <h4 className="font-headline-sm text-[20px] mb-base">{metric.title}</h4>
        <p className="text-on-surface-variant text-body-sm mb-lg">{metric.description}</p>
        <div className="w-full bg-surface-container-high h-2 rounded-full overflow-hidden">
          <div
            className={cn("h-full rounded-full transition-all duration-1000", colors.barBg)}
            style={{ width: `${animatedWidth}%` }}
          />
        </div>
      </div>
    </div>
  );
}
