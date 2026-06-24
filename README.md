# SmartATS Pro — Frontend (React + TypeScript + Tailwind)

React migration of the static `index.html` mockups, built incrementally.

**Done so far:**
- Step 1 — Project scaffold + Landing Page
- Step 2 — Student Dashboard
- Step 3 — ATS Score Breakdown

**Not yet done:** Job Match Engine, backend wiring.

## What's in this scaffold

- Vite + React 18 + TypeScript (strict mode)
- Tailwind CSS, config ported **exactly** from the original `tailwind.config`
  blocks in `index.html` (every color, spacing, fontFamily, fontSize token),
  plus fixes for tokens the original HTML referenced but never defined —
  see "Deviations" below
- ShadCN CLI config (`components.json`) ready to use — no components
  installed yet, added as each page needs them
- React Router with routes for `/` (Landing), `/dashboard` (Student
  Dashboard), and `/ats-score` (ATS Score Breakdown); `/job-match` reserved
  for the next page

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

All three are driven by typed mock data (`src/lib/mock*.ts`) rather than
hardcoded JSX values, so each is a one-file swap once its backend endpoint
exists.

### Shared layout

- `TopAppBar` — landing page header
- `DashboardHeader` — dashboard's header variant (hamburger + wordmark,
  Dashboard/Jobs/Learning links)
- `AtsScoreHeader` — ATS Score page's header variant (back button + page
  title, smaller avatar)
- `BottomNavBar` — mobile nav, shared across all pages, active state
  driven by real route matching (`NavLink`)

The original design used three distinct header layouts across its four
pages, so each is its own component rather than one over-configured
shared header.

### Hooks

- `useCountUp` — Landing page stat counters
- `useStaggeredReveal` — Dashboard's staggered glass-card fade-in
- `useAnimatedWidth` — ATS Score page's progress bars animating from 0%
  to their real width 100ms after mount

### Types

- `src/types/dashboard.ts` — `DashboardSummary`, `ResumeUpload`
- `src/types/atsScore.ts` — `AtsScoreSummary`, `AtsMetric`

Both mirror the shape their future backend endpoints will return (Modules
4 and 10), so swapping mock data for a real fetch is a one-file change.

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

The Vite config proxies `/api/*` to `http://localhost:8000`, so once the
FastAPI backend exists, frontend calls to `/api/...` reach it without CORS
config in dev.

To type-check and build for production:

```bash
npm run build
npm run preview
```

## Testing instructions for Step 3 (ATS Score Breakdown)

1. `npm install && npm run dev`
2. Open `http://localhost:5173/ats-score`
3. Check against the original ATS Score Breakdown mockup:
   - Header shows a back arrow + "ATS Score Breakdown" title; clicking
     the back arrow navigates to the previous page in browser history
   - Circular gauge shows **82** in the center with "Score / 100" below,
     and the ring fill visually matches an 82% arc (not a full circle,
     not near-empty)
   - "AI ANALYZED" pill + "performing better than 74% of applicants" text
   - Critical Insight card (left border accent) shows the keyword-density
     message and an "Improve Keywords" button (currently logs to console)
   - Job Fit: **High**, ATS Rank: **Top 5%** in the two small stat cards
   - "Metric Breakdown" section shows 5 cards: Skills Score (75%),
     Formatting (95%), Keywords (60%, with red/error border treatment),
     Education (100%), Projects (80%) — each with a progress bar that
     animates from 0% to its target width shortly after the page loads
   - A 6th dashed "Add Comparison" placeholder card appears after the 5
     metric cards
4. Resize to mobile width and confirm the layout matches the original
   (single column metric cards, gauge stacks above the insight panel)
5. Run `npm run build` and confirm it completes with no TypeScript errors

## Next steps

- Migrate Job Match Engine page
- Wire pages to backend once Phase B (FastAPI) starts
