/**
 * Shapes for the ATS Score Breakdown page. Mirrors the eventual
 * GET /api/ats/score/:resumeId response shape (Module 4), per the
 * sample response in the project spec:
 *   { ats_score, skills_score, education_score, projects_score,
 *     experience_score, keyword_score }
 */

export interface AtsScoreSummary {
  overallScore: number; // 0-100
  percentileLabel: number; // e.g. 74 -> "better than 74% of applicants"
  criticalInsight: {
    message: string;
    projectedScore: number;
  };
  jobFitLabel: "Low" | "Medium" | "High";
  atsRankLabel: string; // e.g. "Top 5%"
  metrics: AtsMetric[];
}

export type MetricIcon =
  | "psychology"
  | "grid_view"
  | "search_check"
  | "school"
  | "deployed_code";

export type MetricColor = "primary" | "tertiary" | "error" | "secondary" | "tertiary-container";

export interface AtsMetric {
  id: string;
  title: string;
  description: string;
  percent: number; // 0-100
  icon: MetricIcon;
  color: MetricColor;
  /** True for metrics that should render with the error/warning border treatment (e.g. Keywords below threshold). */
  isWarning?: boolean;
}
