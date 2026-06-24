interface KpiCardProps {
  className?: string;
  style?: React.CSSProperties;
  children: React.ReactNode;
}

/** Thin wrapper applying the shared glass-card classes for KPI cards. */
export function KpiCard({ className = "", style, children }: KpiCardProps) {
  return (
    <div
      className={`glass-card p-md rounded-xl flex flex-col justify-between ${className}`}
      style={style}
    >
      {children}
    </div>
  );
}
