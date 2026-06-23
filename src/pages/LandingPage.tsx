import { useState } from "react";
import { TopAppBar } from "@/components/layout/TopAppBar";
import { BottomNavBar } from "@/components/layout/BottomNavBar";
import { AnimatedStat } from "@/components/AnimatedStat";

/**
 * Ported from the first document in index.html ("Design System" /
 * SmartATS Pro landing page). All Tailwind classes are unchanged from the
 * original markup. The only real additions are:
 *   - button press states (was a global mousedown/mouseup/mouseleave
 *     listener attached to every <button> in vanilla JS; now local state
 *     per button via onMouseDown/onMouseUp/onMouseLeave)
 *   - AnimatedStat extracted as its own component (see useCountUp hook)
 */
export default function LandingPage() {
  return (
    <div className="font-body-md text-body-md">
      <TopAppBar />

      {/* Hero Section */}
      <section className="relative min-h-screen pt-32 pb-xl px-margin-mobile md:px-margin-desktop overflow-hidden">
        <div className="relative z-10 max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-xl items-center">
          <div className="space-y-lg text-left">
            <div className="inline-flex items-center gap-xs px-sm py-1 bg-primary/10 border border-primary/20 rounded-full">
              <span
                className="material-symbols-outlined text-primary text-sm"
                style={{ fontVariationSettings: "'FILL' 1" }}
              >
                stars
              </span>
              <span className="text-label-md font-label-md text-primary uppercase tracking-wider">
                New: AI Resume Enhancer 2.0
              </span>
            </div>
            <h1 className="font-display-xl-mobile md:font-display-xl text-display-xl-mobile md:text-display-xl text-on-surface leading-tight">
              Land More Interviews with{" "}
              <span className="text-gradient">AI-Powered</span> Resume
              Intelligence
            </h1>
            <p className="font-body-lg text-body-lg text-on-surface-variant max-w-lg">
              Stop getting ghosted by ATS bots. Our Aura AI analyzes your
              resume against 50,000+ job descriptions to give you a winning
              edge.
            </p>
            <div className="flex flex-col sm:flex-row gap-md pt-base">
              <PressableButton className="px-2xl py-md rounded-xl primary-gradient text-on-primary font-bold text-body-lg shadow-lg hover:shadow-primary/30 transition-all">
                Analyze Resume
              </PressableButton>
              <PressableButton className="px-2xl py-md rounded-xl border-2 border-outline-variant bg-white/50 backdrop-blur text-on-surface font-bold text-body-lg flex items-center justify-center gap-base hover:bg-white transition-all">
                <span className="material-symbols-outlined">play_circle</span>
                Watch Demo
              </PressableButton>
            </div>
            <div className="flex items-center gap-md pt-md">
              <div className="flex -space-x-sm">
                <div className="w-8 h-8 rounded-full border-2 border-surface bg-slate-200" />
                <div className="w-8 h-8 rounded-full border-2 border-surface bg-slate-300" />
                <div className="w-8 h-8 rounded-full border-2 border-surface bg-slate-400" />
              </div>
              <p className="text-body-sm font-body-sm text-on-surface-variant">
                Trusted by 12,000+ professionals
              </p>
            </div>
          </div>

          {/* Dashboard Mockup Card */}
          <div className="relative animate-float">
            <div className="glass-card rounded-2xl p-lg shadow-2xl relative overflow-hidden">
              <div className="flex justify-between items-center mb-xl">
                <div>
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">
                    Analysis Report
                  </h3>
                  <p className="text-body-sm text-on-surface-variant">
                    Product Designer - Senior Level
                  </p>
                </div>
                <div className="w-16 h-16 rounded-full border-4 border-primary/20 flex items-center justify-center">
                  <span className="text-headline-sm font-bold text-primary">
                    84
                  </span>
                </div>
              </div>
              <div className="space-y-lg">
                <div className="space-y-sm">
                  <div className="flex justify-between text-body-sm">
                    <span>ATS Compatibility</span>
                    <span className="font-bold text-primary">High</span>
                  </div>
                  <div className="w-full h-2 bg-surface-variant rounded-full overflow-hidden">
                    <div className="h-full primary-gradient w-[84%]" />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-md">
                  <div className="p-md rounded-xl bg-primary/5 border border-primary/10">
                    <span className="material-symbols-outlined text-primary mb-base">
                      trending_up
                    </span>
                    <p className="text-label-md font-label-md text-primary uppercase">
                      Job Match
                    </p>
                    <p className="text-headline-sm font-bold">92%</p>
                  </div>
                  <div className="p-md rounded-xl bg-secondary/5 border border-secondary/10">
                    <span className="material-symbols-outlined text-secondary mb-base">
                      error_outline
                    </span>
                    <p className="text-label-md font-label-md text-secondary uppercase">
                      Skill Gaps
                    </p>
                    <p className="text-headline-sm font-bold">3 Detected</p>
                  </div>
                </div>
                <div className="p-md rounded-xl bg-white border border-outline-variant/30">
                  <div className="flex items-center gap-sm mb-base">
                    <span
                      className="bg-primary/10 text-primary p-1 rounded-md material-symbols-outlined text-sm"
                      style={{ fontVariationSettings: "'FILL' 1" }}
                    >
                      bolt
                    </span>
                    <p className="text-body-sm font-bold">AI Suggestion</p>
                  </div>
                  <p className="text-body-sm text-on-surface-variant italic">
                    "Quantify your impact in the 'Design System' section by
                    mentioning a 15% increase in dev efficiency."
                  </p>
                </div>
              </div>
            </div>
            <div className="absolute -top-10 -right-10 w-40 h-40 bg-secondary/20 rounded-full blur-3xl z-[-1]" />
            <div className="absolute -bottom-10 -left-10 w-48 h-48 bg-primary/20 rounded-full blur-3xl z-[-1]" />
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-2xl bg-surface relative">
        <div className="max-w-7xl mx-auto px-margin-mobile md:px-margin-desktop">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-xl text-center">
            <AnimatedStat target={95} suffix="%" label="Success Rate" />
            <AnimatedStat target={50} suffix="k+" label="Resumes Scanned" />
            <AnimatedStat target={3} suffix="x" label="Faster Response" />
            <AnimatedStat target={12} suffix="k" label="Pro Users" />
          </div>
        </div>
      </section>

      {/* Feature Bento Grid */}
      <section className="py-2xl px-margin-mobile md:px-margin-desktop bg-surface-container-low">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-2xl space-y-md">
            <h2 className="font-headline-lg text-headline-lg text-on-surface">
              Intelligence Beyond Simple Keywords
            </h2>
            <p className="text-body-lg text-on-surface-variant max-w-2xl mx-auto">
              Our deep-learning engine understands context, seniority, and
              industry nuance better than any standard scanner.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-lg">
            {/* Large Card */}
            <div className="md:col-span-2 glass-card rounded-2xl p-lg flex flex-col justify-between overflow-hidden relative group">
              <div className="relative z-10">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-md">
                  <span className="material-symbols-outlined text-primary">
                    analytics
                  </span>
                </div>
                <h3 className="font-headline-sm text-headline-sm mb-sm">
                  Deep ATS Analysis
                </h3>
                <p className="text-body-md text-on-surface-variant max-w-md">
                  Understand how Applicant Tracking Systems perceive your
                  experience. We simulate top-tier ATS algorithms to ensure
                  you rank #1.
                </p>
              </div>
              <div className="mt-xl relative h-32 md:h-48 overflow-hidden rounded-xl border border-outline-variant/30 bg-gradient-to-br from-primary/10 to-secondary/10" />
            </div>

            {/* Vertical Card */}
            <div className="glass-card rounded-2xl p-lg space-y-md flex flex-col group">
              <div className="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center">
                <span className="material-symbols-outlined text-secondary">
                  target
                </span>
              </div>
              <h3 className="font-headline-sm text-headline-sm">
                Semantic Job Match
              </h3>
              <p className="text-body-md text-on-surface-variant">
                Don't just match words; match intent. We analyze your
                accomplishments against job requirements for a semantic fit
                score.
              </p>
              <div className="flex-grow flex items-end">
                <div className="w-full p-md bg-surface-variant/50 rounded-xl border border-outline-variant/20">
                  <div className="flex justify-between items-center mb-base">
                    <span className="text-label-md font-label-md">
                      Match Quality
                    </span>
                    <span className="text-label-md font-bold text-secondary">
                      EXCELLENT
                    </span>
                  </div>
                  <div className="h-2 w-full bg-white rounded-full overflow-hidden">
                    <div className="h-full bg-secondary w-full" />
                  </div>
                </div>
              </div>
            </div>

            {/* Bottom Row */}
            <div className="glass-card rounded-2xl p-lg space-y-md group">
              <div className="w-12 h-12 rounded-xl bg-tertiary/10 flex items-center justify-center">
                <span className="material-symbols-outlined text-tertiary">
                  trending_up
                </span>
              </div>
              <h3 className="font-headline-sm text-headline-sm">
                Skill Gap Analysis
              </h3>
              <p className="text-body-sm text-on-surface-variant">
                Identify specific certifications or software tools missing
                from your profile that are holding you back from high-paying
                roles.
              </p>
            </div>
            <div className="glass-card rounded-2xl p-lg space-y-md group">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                <span className="material-symbols-outlined text-primary">
                  auto_awesome
                </span>
              </div>
              <h3 className="font-headline-sm text-headline-sm">
                AI Bullet Rewriter
              </h3>
              <p className="text-body-sm text-on-surface-variant">
                Transform "Handled customer calls" into "Optimized client
                communication pipelines, reducing resolution time by 22%."
              </p>
            </div>
            <div className="glass-card rounded-2xl p-lg space-y-md group">
              <div className="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center">
                <span className="material-symbols-outlined text-secondary">
                  forum
                </span>
              </div>
              <h3 className="font-headline-sm text-headline-sm">
                Interview Coach
              </h3>
              <p className="text-body-sm text-on-surface-variant">
                Generate customized interview questions based on your
                specific resume and the job description you're applying for.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-2xl px-margin-mobile md:px-margin-desktop bg-surface">
        <div className="max-w-7xl mx-auto">
          <h2 className="font-headline-lg text-headline-lg text-center mb-2xl">
            The Path to Your Next Career Move
          </h2>
          <div className="relative">
            <div className="hidden md:block absolute top-1/2 left-0 w-full h-px border-t border-dashed border-outline-variant/50 -translate-y-1/2 z-0" />
            <div className="grid grid-cols-1 md:grid-cols-3 gap-xl relative z-10">
              <HowItWorksStep
                step={1}
                title="Upload Resume"
                description="Drag and drop your PDF or DOCX file. Our engine parses it in seconds with 99.9% accuracy."
              />
              <HowItWorksStep
                step={2}
                title="Get Aura Score"
                description="View your score, identified skill gaps, and ATS readability report instantly on your dashboard."
              />
              <HowItWorksStep
                step={3}
                title="Optimize & Apply"
                description="Apply suggested changes using our AI rewriter and hit 'Apply' with absolute confidence."
              />
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-2xl px-margin-mobile md:px-margin-desktop mb-2xl">
        <div className="max-w-5xl mx-auto primary-gradient rounded-[2rem] p-xl text-center text-on-primary relative overflow-hidden">
          <div className="relative z-10 space-y-lg">
            <h2 className="font-display-xl-mobile md:font-headline-lg text-display-xl-mobile md:text-headline-lg font-bold">
              Ready to outsmart the bots?
            </h2>
            <p className="text-body-lg opacity-90 max-w-xl mx-auto">
              Join thousands of job seekers who landed interviews at Google,
              Meta, and Stripe using Aura Intelligence.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-md pt-md">
              <PressableButton className="px-2xl py-md rounded-xl bg-white text-primary font-bold text-body-lg shadow-xl hover:scale-105 transition-transform">
                Get Started for Free
              </PressableButton>
              <PressableButton className="px-2xl py-md rounded-xl border border-white/30 bg-white/10 backdrop-blur font-bold text-body-lg hover:bg-white/20 transition-all">
                View Pricing Plans
              </PressableButton>
            </div>
          </div>
          <div className="absolute -top-24 -right-24 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
          <div className="absolute -bottom-24 -left-24 w-64 h-64 bg-secondary-container/20 rounded-full blur-3xl" />
        </div>
      </section>

      <div className="h-32" />
      <BottomNavBar />
    </div>
  );
}

/** One numbered card in the "How It Works" section. */
function HowItWorksStep({
  step,
  title,
  description,
}: {
  step: number;
  title: string;
  description: string;
}) {
  return (
    <div className="bg-white p-lg rounded-2xl shadow-sm border border-outline-variant/30 text-center space-y-md">
      <div className="w-16 h-16 rounded-full primary-gradient text-on-primary flex items-center justify-center mx-auto text-headline-sm font-bold shadow-lg">
        {step}
      </div>
      <h4 className="font-headline-sm text-headline-sm">{title}</h4>
      <p className="text-body-md text-on-surface-variant">{description}</p>
    </div>
  );
}

/**
 * Replicates the original global mousedown/mouseup/mouseleave listeners
 * that added/removed `scale-95` on every button, but scoped to a single
 * button via local state instead of a document-wide querySelectorAll pass.
 */
function PressableButton({
  className,
  children,
}: {
  className: string;
  children: React.ReactNode;
}) {
  const [pressed, setPressed] = useState(false);

  return (
    <button
      className={`${className} active:scale-95 ${pressed ? "scale-95" : ""}`}
      onMouseDown={() => setPressed(true)}
      onMouseUp={() => setPressed(false)}
      onMouseLeave={() => setPressed(false)}
    >
      {children}
    </button>
  );
}
