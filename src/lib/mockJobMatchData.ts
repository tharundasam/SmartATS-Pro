import type { ResumeOption, JobMatchResult } from "@/types/jobMatch";

/** Ported directly from the original <select> options. */
export const MOCK_RESUME_OPTIONS: ResumeOption[] = [
  { id: "1", fileName: "Senior Software Engineer_v4.pdf", updatedLabel: "Updated 2 days ago" },
  { id: "2", fileName: "Product Manager_v1.pdf", updatedLabel: "Updated 1 week ago" },
  { id: "3", fileName: "Tech Lead_Executive_v2.pdf", updatedLabel: "Updated 1 month ago" },
];

/**
 * Ported from the original's hardcoded #analysis-results block. This is
 * what the original showed every time, regardless of what was actually
 * typed into the textarea — the "simulation" was purely cosmetic. Once
 * Module 5 (Sentence Transformers + cosine similarity) exists, this is
 * replaced by a real POST /api/job-match/analyze call.
 */
export const MOCK_JOB_MATCH_RESULT: JobMatchResult = {
  matchPercent: 74,
  verdictLabel: "STRONG POTENTIAL",
  summary:
    "Your resume has a high semantic match for technical leadership, but some specific stack keywords are missing.",
  missingKeywords: ["Kubernetes", "Python", "Microservices", "CI/CD Pipelines"],
  aiInsights: [
    {
      title: "Quantify Your Impact",
      description:
        'The job description emphasizes "scalability". Add metrics regarding user growth or server performance.',
    },
    {
      title: "Skill Reframing",
      description:
        'Swap "Cloud Infrastructure" with "AWS & Kubernetes" to align with their specific tech stack.',
    },
  ],
};

/** Current ATS score shown in the sidebar widget — ported from the hardcoded "84 / 100". */
export const MOCK_CURRENT_ATS_SCORE = 84;
