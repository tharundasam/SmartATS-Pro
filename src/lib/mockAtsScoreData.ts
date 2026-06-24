import type { AtsScoreSummary } from "@/types/atsScore";

/**
 * Hardcoded values lifted directly from the original static mockup.
 * Single place to swap for a real `GET /api/ats/score/:resumeId` call
 * once Module 4 (ATS Score Engine) exists in the backend.
 */
export const MOCK_ATS_SCORE: AtsScoreSummary = {
  overallScore: 82,
  percentileLabel: 74,
  criticalInsight: {
    message:
      "Your skills and formatting are excellent, but keyword density is lagging behind industry benchmarks for Senior roles. Improving this could boost your score to 94/100.",
    projectedScore: 94, // kept for future use (e.g. as the "Improve Keywords" CTA's target score), not parsed out of the message above
  },
  jobFitLabel: "High",
  atsRankLabel: "Top 5%",
  metrics: [
    {
      id: "skills",
      title: "Skills Score",
      description: "Core competency alignment with job description.",
      percent: 75,
      icon: "psychology",
      color: "primary",
    },
    {
      id: "formatting",
      title: "Formatting",
      description: "Machine readability and layout parsing stability.",
      percent: 95,
      icon: "grid_view",
      color: "tertiary",
    },
    {
      id: "keywords",
      title: "Keywords",
      description: "Missing 4 out of 10 essential industry terms.",
      percent: 60,
      icon: "search_check",
      color: "error",
      isWarning: true,
    },
    {
      id: "education",
      title: "Education",
      description: "Academic credentials perfectly match requirements.",
      percent: 100,
      icon: "school",
      color: "secondary",
    },
    {
      id: "projects",
      title: "Projects",
      description: "Relevance of listed case studies and portfolio.",
      percent: 80,
      icon: "deployed_code",
      color: "tertiary-container",
    },
  ],
};
