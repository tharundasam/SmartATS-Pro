# SmartATS Pro — Frontend (React + TypeScript + Tailwind)

React migration of the static `index.html` mockups, built incrementally.

**Done so far:**
- Step 1 — Project scaffold + Landing Page
- Step 2 — Student Dashboard

**Not yet done:** ATS Score Breakdown, Job Match Engine, backend wiring.

## What's in this scaffold

- Vite + React 18 + TypeScript (strict mode)
- Tailwind CSS, config ported **exactly** from the original `tailwind.config`
  blocks in `index.html` (every color, spacing, fontFamily, fontSize token —
  unchanged), plus one intentional fix — see "Deviations" below
- ShadCN CLI config (`components.json`) ready to use — no components
  installed yet, added as each page needs them
- React Router with routes for `/` (Landing) and `/dashboard` (Student
  Dashboard); `/ats-score` and `/job-match` reserved for upcoming pages

### Pages

- **`LandingPage.tsx`** — hero, animated stats, bento feature grid,
  "how it works", final CTA. Pixel-for-pixel match of the original markup.
- **`StudentDashboard.tsx`** — welcome banner, 4 KPI cards, ATS evolution
  bar chart, skill profile spider chart, recent uploads feed, recommended
  actions. Same markup/classes as the original, now driven by typed mock
  data (`src/lib/mockDashboardData.ts`) instead of hardcoded JSX values.

### Shared layout

- `TopAppBar` — landing page header (reused if other marketing-style pages
  are added later)
- `DashboardHeader` — the dashboard's distinct header variant (hamburger +
  wordmark, Dashboard/Jobs/Learning links) — kept separate from `TopAppBar`
  since the original used two different header designs across pages
- `BottomNavBar` — mobile nav, shared across all pages, active state now
  driven by real route matching (`NavLink`) instead of a click listener
  that just toggled CSS classes

### Hooks

- `useCountUp` — replaces the original vanilla-JS `IntersectionObserver`
  counter animation (Landing page stats)
- `useStaggeredReveal` — replaces the original dashboard script that faded
  in every `.glass-card` with a 100ms stagger per card, in DOM order

### Types

- `src/types/dashboard.ts` defines `DashboardSummary` and `ResumeUpload` —
  these mirror the shape the future `GET /api/dashboard/summary` endpoint
  (Module 10) will return, so swapping mock data for a real fetch later is
  a one-file change, not a rewrite.

## Deviations from the original HTML (and why)

- **Decorative images removed.** The original `<img>` placeholders pointed
  at temporary Google-hosted demo URLs (`lh3.googleusercontent.com/aida-public/...`),
  not real assets. User avatars are now optional props
  (`<DashboardHeader avatarUrl="..." />`); the one decorative analysis image
  on the landing page is a gradient placeholder pending a real asset.
- **`headline-lg-mobile` token added (bug fix, by request).** The original
  HTML referenced `font-headline-lg-mobile` / `text-headline-lg-mobile` on
  the dashboard's "Welcome back" heading and the Job Match page's heading,
  but this class was never defined in any of the four `tailwind.config`
  blocks in the source file — a latent bug that silently fell back to
  default browser sizing on mobile. Fixed in `tailwind.config.ts`: defined
  as 28px/36px line-height, between `headline-sm` (24px) and `headline-lg`
  (32px).
- **Dynamic Tailwind class generation avoided.** The dashboard's ATS
  Evolution chart originally hardcoded 6 bars with manually-chosen opacity
  classes (`bg-primary/10` through `/80`). Rather than interpolate
  `bg-primary/${value}` at runtime — which Tailwind cannot detect at build
  time since it scans for literal strings — `AtsEvolutionChart.tsx` uses a
  static lookup array of literal class names, preserving the exact same
  visual progression.
- Tailwind is compiled via PostCSS, not the CDN script (CDN Tailwind isn't
  meant for production builds).

## Setup

You'll need [Node.js](https://nodejs.org) 18+ installed.

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173/` for the Landing Page and
`http://localhost:5173/dashboard` for the Student Dashboard.

The Vite config proxies `/api/*` to `http://localhost:8000`, so once the
FastAPI backend exists, frontend calls to `/api/...` reach it without CORS
config in dev.

To type-check and build for production:

```bash
npm run build
npm run preview
```

## Testing instructions for this step

1. `npm install && npm run dev`
2. Open `http://localhost:5173/dashboard`
3. Check against the original dashboard mockup:
   - Welcome banner shows "Welcome back, Alex" / "Top 15%"
   - 4 KPI cards (ATS Score 82, Resume Strength High, Job Matches 12,
     Missing Skills 3) fade in with a staggered animation on page load
   - ATS Evolution bar chart shows 6 bars (Oct 1 → Dec 15) with hover
     tooltips showing the score value
   - Skill Profile spider-chart visual + 3 skill badges (92% Python, 78%
     AWS, 45% React)
   - Recent Uploads list shows 3 resumes with correct status badges
     (PROCESSED / PROCESSED / LOW MATCH) and score colors
   - "Run Analysis" and "Upload New Resume" buttons log to the browser
     console (not wired to real actions yet — that's Phase B/C)
   - Bottom nav (mobile width) correctly highlights "Home" when on
     `/dashboard`, since there's no literal `/dashboard` nav item — this
     matches the original, which always showed "Home" as active on this
     page
4. Resize to mobile width and confirm responsive behavior matches the
   original (KPI grid 2-column, bottom nav visible, top nav collapses)
5. Run `npm run build` and confirm it completes with no TypeScript errors

## Next steps

- Migrate ATS Score Breakdown page
- Migrate Job Match Engine page
- Wire pages to backend once Phase B (FastAPI) starts
