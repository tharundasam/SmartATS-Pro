/**
 * Shapes for the Student Dashboard. These mirror what the eventual
 * GET /api/dashboard/summary endpoint (Module 10 / Phase B) will return,
 * so swapping the hardcoded data below for a real fetch later is a
 * drop-in change rather than a rewrite.
 */

export interface DashboardSummary {
  studentName: string;
  percentileLabel: string; // e.g. "Top 15%"
  kpis: {
    atsScore: number; // 0-100
    resumeStrength: "Low" | "Medium" | "High";
    jobMatches: number;
    jobMatchesDelta: string; // e.g. "+3 this week"
    missingSkillsCount: number;
  };
  atsEvolution: { label: string; score: number }[];
  skillProfile: {
    axes: { label: string; value: number }[]; // for the spider chart
    topSkills: { name: string; percent: number }[];
  };
  recentUploads: ResumeUpload[];
}

export interface ResumeUpload {
  id: string;
  fileName: string;
  uploadedAt: string; // ISO date string
  fileSizeLabel: string; // e.g. "1.2 MB"
  atsScore: number;
  status: "PROCESSED" | "LOW_MATCH" | "PROCESSING" | "FAILED";
}
