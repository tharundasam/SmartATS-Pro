# SmartATS Pro — Frontend (React + TypeScript + Tailwind)

React migration of the static `index.html` mockups, built incrementally.

**Done so far:**
- Step 1 — Project scaffold + Landing Page
- Step 2 — Student Dashboard
- Step 3 — ATS Score Breakdown
- Step 4 — Job Match Engine

**All four original mockups are now migrated.** Not yet done: backend
wiring (Phase B onward).

## What's in this scaffold

- Vite + React 18 + TypeScript (strict mode)
- Tailwind CSS, config ported **exactly** from the original `tailwind.config`
  blocks in `index.html` (every color, spacing, fontFamily, fontSize token),
  plus fixes for tokens the original HTML referenced but never defined —
  see "Deviations" below
- ShadCN CLI config (`components.json`) ready to use — no components
  installed yet, added as each page needs them
- React Router with routes for `/` (Landing), `/dashboard` (Student
  Dashboard), `/ats-score` (ATS Score Breakdown), and `/job-match`
  (Job Match Engine) — all four original pages are now routed

### Pages

- **`LandingPage.tsx`** — hero, animated stats, bento feature grid,
  "how it works", final CTA.
- **`StudentDashboard.tsx`** — welcome banner, 4 KPI cards, ATS evolution
  bar chart, skill profile spider chart, recent uploads feed, recommended
  actions.
- **`AtsScoreBreakdown.tsx`** — circular score gauge, critical insight
  panel, job fit / ATS rank stats, 5 metric breakdown cards (Skills,
  Formatting, Keywords, Education, Projects) plus an "Add Comparison"
  placeholder card.
- **`JobMatchEngine.tsx`** — resume selector, job description textarea,
  "Analyze Match" flow (mock 1.8s delay) that reveals a circular match-score
  gauge, missing keywords list, and AI insights card. Desktop-only sidebar
  navigation with route-based active state.

All four are driven by typed mock data (`src/lib/mock*.ts`) rather than
hardcoded JSX values, so each is a one-file swap once its backend endpoint
exists.

### Shared layout

- `TopAppBar` — landing page header
- `DashboardHeader` — dashboard's header variant (hamburger + wordmark,
  Dashboard/Jobs/Learning links)
- `AtsScoreHeader` — ATS Score page's header variant (back button + page
  title, smaller avatar)
- `JobMatchHeader` — Job Match page's header variant (hamburger + wordmark,
  "UPGRADE" pill button)
- `JobMatchSidebar` — Job Match page's desktop-only side navigation, with
  real route-based active state via `NavLink` (the original used a click
  listener that activated whichever link you clicked, regardless of where
  it pointed — see "Deviations")
- `BottomNavBar` — mobile nav, shared across all pages, active state
  driven by real route matching (`NavLink`)

The original design used four distinct header layouts and one sidebar
across its four pages, so each is its own component rather than one
over-configured shared header.

### Hooks

- `useCountUp` — Landing page stat counters
- `useStaggeredReveal` — Dashboard's staggered glass-card fade-in
- `useAnimatedWidth` — ATS Score page's progress bars animating from 0%
  to their real width 100ms after mount

### Types

- `src/types/dashboard.ts` — `DashboardSummary`, `ResumeUpload`
- `src/types/atsScore.ts` — `AtsScoreSummary`, `AtsMetric`
- `src/types/jobMatch.ts` — `ResumeOption`, `JobMatchResult`

All three mirror the shape their future backend endpoints will return
(Modules 4, 5, and 10), so swapping mock data for a real fetch is a
one-file change.

## Deviations from the original HTML (and why)

- **Decorative images removed.** Original `<img>` placeholders pointed at
  temporary Google-hosted demo URLs, not real assets. Avatars are now
  optional props on each header component.
- **Three undefined Tailwind tokens fixed.** The original HTML referenced
  `headline-lg-mobile`, `headline-sm-mobile`, and used `display-xl-mobile`
  inconsistently across its four embedded `tailwind.config` blocks — some
  pages defined tokens others didn't. `headline-lg-mobile` and
  `headline-sm-mobile` were never defined in *any* of the four configs,
  so on the original static pages those classes silently fell back to
  default browser sizing. Per explicit decision, these are fixed rather
  than reproduced as bugs:
  - `headline-lg-mobile`: 28px / 36px line-height (between `headline-sm`
    24px and `headline-lg` 32px)
  - `headline-sm-mobile`: 20px / 28px line-height (between `body-lg` 18px
    and `headline-sm` 24px)
- **Dynamic Tailwind class generation avoided.** Both the dashboard's ATS
  Evolution chart and the ATS Score page's metric cards originally
  hardcoded per-item color/opacity classes inline. Interpolating a class
  name at runtime (e.g. `` `bg-${color}/10` ``) doesn't work with Tailwind,
  since it scans source for literal strings at build time — not actual
  runtime values. Both components instead use a static lookup object
  mapping each known variant to its literal class strings.
- **ATS Score back button is now functional.** The original was a static
  decorative arrow icon with no behavior. `AtsScoreHeader` wires it to
  `useNavigate(-1)` (browser back), since a non-functional back button in
  a real app would be a regression, not a faithful port.
- **Job Match sidebar active-state is now route-driven, not click-driven.**
  The original sidebar's <script> attached a click listener that swapped
  CSS classes onto whichever link you clicked — so it would show "Skill
  Gap" as active if you clicked it, even though every link pointed to
  `href="#"` and went nowhere. `JobMatchSidebar` now uses real `NavLink`s:
  "Dashboard" links to `/dashboard`, "Resume Analysis" to `/ats-score`,
  "Job Match" to `/job-match`. **"Skill Gap" and "AI Enhancer" link to
  `/skill-gap` and `/ai-enhancer`, which don't have pages yet** (Modules 6
  and 7) — clicking them will 404 until those pages are built. This is the
  one known gap in this step; flagging it rather than leaving silent.
- **Job Match score gauge generalized from a hardcoded example.** The
  original SVG only ever rendered a 74% match (`stroke-dasharray="552.92"`,
  `stroke-dashoffset="143.76"` were hand-calculated for that one value).
  `JobMatchScoreGauge` derives both from `matchPercent` using the circle
  circumference formula (2πr), verified to reproduce the original's exact
  74% values, so the gauge renders correctly for any score. Also added an
  explicit `viewBox="0 0 192 192"` to the `<svg>`, which the original
  omitted — it worked only because the parent happened to be sized to
  exactly 192px; without a viewBox this breaks if that sizing ever
  changes. Purely a robustness fix, not a visual change.
- Tailwind is compiled via PostCSS, not the CDN script (CDN Tailwind isn't
  meant for production builds).

## Setup

You'll need [Node.js](https://nodejs.org) 18+ installed.

```bash
cd frontend
npm install
npm run dev
```

Routes:
- `/` — Landing Page
- `/dashboard` — Student Dashboard
- `/ats-score` — ATS Score Breakdown
- `/job-match` — Job Match Engine

The Vite config proxies `/api/*` to `http://localhost:8000`, so once the
FastAPI backend exists, frontend calls to `/api/...` reach it without CORS
config in dev.

To type-check and build for production:

```bash
npm run build
npm run preview
```

## Testing instructions for Step 4 (Job Match Engine)

1. `npm install && npm run dev`
2. Open `http://localhost:5173/job-match`
3. Check against the original Job Match Engine mockup:
   - Desktop (≥768px): left sidebar visible with "Job Match" highlighted
     as active (purple background); "Dashboard" and "Resume Analysis" are
     real links — clicking them navigates to `/dashboard` and `/ats-score`
     respectively and the sidebar correctly updates which item is active
   - Sidebar shows **84 / 100** in the ATS Score widget at the bottom
   - "MATCH ENGINE 2.0" pill, "Job Match Analysis" heading
   - "Select Resume" dropdown defaults to "Senior Software Engineer_v4.pdf"
     with 2 other options
   - Job Description textarea accepts typed text
   - Click **Analyze Match**:
     - Button shows a spinning icon + "Analyzing..." and is disabled
       for ~1.8 seconds
     - "Ready for Analysis" placeholder is replaced by:
       - A circular gauge showing **74%** with "Match Score" label and a
         partial purple ring matching ~74% of the circle
       - "STRONG POTENTIAL" pill + summary text
       - 4 missing-keyword pills (Kubernetes, Python, Microservices,
         CI/CD Pipelines)
       - "AI Insights" card with 2 tips and an "APPLY CHANGES WITH AI"
         button (currently logs to console)
4. Resize below 1024px width, click **Analyze Match** again, and confirm
   the page auto-scrolls down to the results once they appear (matches the
   original's mobile scroll-into-view behavior)
5. Resize below 768px and confirm the sidebar disappears and the bottom
   nav bar appears with "Match" highlighted as active
6. Try clicking "Skill Gap" or "AI Enhancer" in the sidebar (desktop width)
   — these will 404, which is expected; see "Deviations" above
7. Run `npm run build` and confirm it completes with no TypeScript errors

## Next steps

- All four original UI pages are migrated. Next is Phase B: FastAPI
  backend foundation (PostgreSQL schema, auth, resume upload/parsing),
  followed by wiring each page's mock data source to a real API call.
- Build `/skill-gap` and `/ai-enhancer` pages when those modules are
  designed (Modules 6 and 7), so the sidebar's existing links resolve.
