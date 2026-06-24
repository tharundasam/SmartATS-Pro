import type { DashboardSummary } from "@/types/dashboard";

/**
 * Hardcoded values lifted directly from the original static mockup.
 * This is the single place to swap in a real `useQuery(['dashboard'], ...)`
 * call once the backend's GET /api/dashboard/summary exists — every
 * component below reads from this shape already.
 */
export const MOCK_DASHBOARD_SUMMARY: DashboardSummary = {
  studentName: "Alex",
  percentileLabel: "Top 15%",
  kpis: {
    atsScore: 82,
    resumeStrength: "High",
    jobMatches: 12,
    jobMatchesDelta: "+3 this week",
    missingSkillsCount: 3,
  },
  atsEvolution: [
    { label: "Oct 1", score: 62 },
    { label: "Oct 15", score: 68 },
    { label: "Oct 30", score: 64 },
    { label: "Nov 15", score: 75 },
    { label: "Nov 30", score: 79 },
    { label: "Dec 15", score: 82 },
  ],
  skillProfile: {
    axes: [
      { label: "Coding", value: 90 },
      { label: "Cloud", value: 70 },
      { label: "UX/UI", value: 60 },
      { label: "Management", value: 40 },
    ],
    topSkills: [
      { name: "Python", percent: 92 },
      { name: "AWS", percent: 78 },
      { name: "React", percent: 45 },
    ],
  },
  recentUploads: [
    {
      id: "1",
      fileName: "Alex_Rivers_SWE_Resume_V4.pdf",
      uploadedAt: "2 hours ago",
      fileSizeLabel: "1.2 MB",
      atsScore: 82,
      status: "PROCESSED",
    },
    {
      id: "2",
      fileName: "Alex_Rivers_Product_Designer_V1.pdf",
      uploadedAt: "Dec 12, 2023",
      fileSizeLabel: "2.4 MB",
      atsScore: 76,
      status: "PROCESSED",
    },
    {
      id: "3",
      fileName: "Master_Resume_Draft_Backup.pdf",
      uploadedAt: "Dec 10, 2023",
      fileSizeLabel: "1.1 MB",
      atsScore: 48,
      status: "LOW_MATCH",
    },
  ],
};
