import type { DashboardSummary } from "@/types/dashboard";

interface SkillProfileProps {
  data: DashboardSummary["skillProfile"];
}

/**
 * Ported from the "Skill Profile" card. The original spider-chart blob
 * used a hardcoded clip-path polygon and hardcoded axis label positions —
 * those are visual-only in the original (not actually computed from
 * data), so they're kept as-is rather than reverse-engineered into a
 * dynamic polygon generator, which the original design never had either.
 * `data.axes` is accepted as a prop so a real radar-chart can swap in
 * later without changing the parent's interface.
 */
export function SkillProfile({ data }: SkillProfileProps) {
  return (
    <div className="glass-card p-lg rounded-2xl flex flex-col">
      <h3 className="font-headline-sm text-headline-sm mb-lg">Skill Profile</h3>
      <div className="flex-grow flex items-center justify-center relative">
        <div className="w-48 h-48 rounded-full border-2 border-outline-variant/30 flex items-center justify-center relative">
          <div className="absolute inset-4 rounded-full border border-outline-variant/20" />
          <div className="absolute inset-10 rounded-full border border-outline-variant/10" />
          <div
            className="absolute inset-0 bg-primary/20"
            style={{
              clipPath: "polygon(50% 10%, 90% 40%, 70% 90%, 20% 80%, 10% 30%)",
            }}
          />
          {data.axes[0] && (
            <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-6 text-[10px] font-medium uppercase text-on-surface-variant">
              {data.axes[0].label}
            </div>
          )}
          {data.axes[1] && (
            <div className="absolute right-0 top-1/2 translate-x-10 -translate-y-1/2 text-[10px] font-medium uppercase text-on-surface-variant">
              {data.axes[1].label}
            </div>
          )}
          {data.axes[2] && (
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-6 text-[10px] font-medium uppercase text-on-surface-variant">
              {data.axes[2].label}
            </div>
          )}
          {data.axes[3] && (
            <div className="absolute left-0 top-1/2 -translate-x-14 -translate-y-1/2 text-[10px] font-medium uppercase text-on-surface-variant">
              {data.axes[3].label}
            </div>
          )}
        </div>
      </div>
      <div className="mt-6 flex flex-wrap gap-2 justify-center">
        {data.topSkills.map((skill) => (
          <span key={skill.name} className="ai-badge px-3 py-1 rounded-full text-[10px]">
            {skill.percent}% {skill.name}
          </span>
        ))}
      </div>
    </div>
  );
}
