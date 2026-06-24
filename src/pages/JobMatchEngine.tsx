import { useRef, useState } from "react";
import { JobMatchHeader } from "@/components/layout/JobMatchHeader";
import { JobMatchSidebar } from "@/components/layout/JobMatchSidebar";
import { BottomNavBar } from "@/components/layout/BottomNavBar";
import { ResumeSelectCard } from "@/components/job-match/ResumeSelectCard";
import { JobDescriptionCard } from "@/components/job-match/JobDescriptionCard";
import { AnalysisPlaceholderCard } from "@/components/job-match/AnalysisPlaceholderCard";
import { JobMatchScoreGauge } from "@/components/job-match/JobMatchScoreGauge";
import { MissingKeywordsCard } from "@/components/job-match/MissingKeywordsCard";
import { AiInsightsCard } from "@/components/job-match/AiInsightsCard";
import {
  MOCK_RESUME_OPTIONS,
  MOCK_JOB_MATCH_RESULT,
  MOCK_CURRENT_ATS_SCORE,
} from "@/lib/mockJobMatchData";
import type { JobMatchResult } from "@/types/jobMatch";

/**
 * Ported from the fourth document in index.html ("Job Match Engine").
 * The original's simulateAnalysis() directly mutated a button's
 * innerHTML, toggled `hidden` classes on two divs via getElementById,
 * and used a hardcoded 1800ms setTimeout. All of that is replaced with
 * React state:
 *   - `isAnalyzing`   -> drives the button's spinner (was innerHTML swap)
 *   - `result`        -> null shows AnalysisPlaceholderCard, populated
 *                        shows the score gauge + keywords + insights
 *                        (was the hidden-class toggle on two fixed divs)
 *   - `resultsRef` + scrollIntoView on mobile, same as the original's
 *     window.innerWidth < 1024 check
 *
 * `handleAnalyze` currently resolves with MOCK_JOB_MATCH_RESULT after a
 * simulated delay — this is the one function to replace with a real
 * POST /api/job-match/analyze call once Module 5 (Sentence Transformers
 * + cosine similarity) exists in the backend.
 */
export default function JobMatchEngine() {
  const [selectedResumeId, setSelectedResumeId] = useState(MOCK_RESUME_OPTIONS[0].id);
  const [jobDescription, setJobDescription] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<JobMatchResult | null>(null);
  const resultsRef = useRef<HTMLDivElement>(null);

  async function handleAnalyze() {
    setIsAnalyzing(true);

    // Mock async delay standing in for the real backend call. Swap this
    // block for:
    //   const res = await axios.post("/api/job-match/analyze", {
    //     resumeId: selectedResumeId,
    //     jobDescription,
    //   });
    //   setResult(res.data);
    await new Promise((resolve) => setTimeout(resolve, 1800));
    setResult(MOCK_JOB_MATCH_RESULT);

    setIsAnalyzing(false);

    if (window.innerWidth < 1024) {
      resultsRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }

  return (
    <div className="font-body-md text-on-surface bg-background min-h-screen">
      <JobMatchHeader />
      <JobMatchSidebar atsScore={MOCK_CURRENT_ATS_SCORE} />

      <main className="pt-24 pb-32 md:pl-[300px] px-margin-mobile md:px-margin-desktop max-w-[1440px] mx-auto min-h-screen">
        <section className="mb-xl">
          <div className="max-w-3xl">
            <span className="inline-block px-3 py-1 rounded-full bg-secondary/10 text-secondary font-label-md text-label-md mb-md">
              MATCH ENGINE 2.0
            </span>
            <h2 className="font-headline-lg text-headline-lg-mobile md:text-headline-lg text-on-surface mb-sm">
              Job Match Analysis
            </h2>
            <p className="text-on-surface-variant font-body-md">
              Instantly check how well your resume aligns with a specific job role.
              Our AI analyzes semantical relevance, technical keywords, and
              experience depth.
            </p>
          </div>
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
          {/* Input Area */}
          <div className="lg:col-span-7 space-y-gutter">
            <ResumeSelectCard
              options={MOCK_RESUME_OPTIONS}
              value={selectedResumeId}
              onChange={setSelectedResumeId}
              onUploadNew={() => {
                // Wired to POST /api/resumes/upload in Phase B, Module 2.
                console.log("Upload new resume clicked");
              }}
            />
            <JobDescriptionCard
              value={jobDescription}
              onChange={setJobDescription}
              onAnalyze={handleAnalyze}
              isAnalyzing={isAnalyzing}
            />
          </div>

          {/* Analysis Sidebar (Pre-state or Results) */}
          <div className="lg:col-span-5" ref={resultsRef}>
            {!result ? (
              <AnalysisPlaceholderCard />
            ) : (
              <div className="space-y-gutter">
                <JobMatchScoreGauge
                  matchPercent={result.matchPercent}
                  verdictLabel={result.verdictLabel}
                  summary={result.summary}
                />
                <MissingKeywordsCard keywords={result.missingKeywords} />
                <AiInsightsCard
                  insights={result.aiInsights}
                  onApplyChanges={() => {
                    // Wired to the AI Resume Enhancement engine in Phase C, Module 7.
                    console.log("Apply changes with AI clicked");
                  }}
                />
              </div>
            )}
          </div>
        </div>
      </main>

      <BottomNavBar />
    </div>
  );
}
