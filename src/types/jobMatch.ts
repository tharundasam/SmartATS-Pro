/**
 * Shapes for the Job Match Engine. Mirrors the future
 * POST /api/job-match/analyze response (Module 5, Phase C), so the mock
 * version below is a drop-in swap later.
 */

export interface ResumeOption {
  id: string;
  fileName: string;
  updatedLabel: string; // e.g. "Updated 2 days ago"
}

export interface JobMatchResult {
  matchPercent: number; // 0-100
  verdictLabel: string; // e.g. "STRONG POTENTIAL"
  summary: string;
  missingKeywords: string[];
  aiInsights: { title: string; description: string }[];
}
