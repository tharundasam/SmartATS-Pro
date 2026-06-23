# SmartATS Pro — Frontend (React + TypeScript + Tailwind)

This is the React migration of the static `index.html` mockups. **Step 1 of
the build plan**: only the Landing Page is migrated so far. Dashboard, ATS
Score Breakdown, and Job Match Engine pages come next, one at a time.

## What's in this scaffold

- Vite + React 18 + TypeScript (strict mode)
- Tailwind CSS, config ported **exactly** from the original `tailwind.config`
  block in `index.html` (every color, spacing, fontFamily, fontSize token —
  unchanged)
- ShadCN CLI config (`components.json`) ready to use — no components
  installed yet, added as each page needs them
- React Router (routes for `/`, with `/dashboard`, `/ats-score`, `/job-match`
  reserved for upcoming pages)
- `LandingPage.tsx` — full migration of the hero, stats, bento grid,
  "how it works", and final CTA sections, pixel-for-pixel matching the
  original markup/classes
- `TopAppBar` and `BottomNavBar` extracted as shared layout components
  (they were duplicated across all 4 original HTML files — now one
  source of truth)
- `useCountUp` hook replacing the original vanilla-JS `IntersectionObserver`
  counter script

## What's intentionally different from the original HTML

- The original decorative `<img>` placeholders pointed at temporary
  Google-hosted demo URLs (`lh3.googleusercontent.com/aida-public/...`).
  These aren't real assets, so the user avatar is now a prop
  (`<TopAppBar avatarUrl="..." />`) and the one decorative analysis-image
  block is a gradient placeholder until you have a real screenshot/asset.
- Tailwind is now compiled via PostCSS (the original used the Tailwind CDN
  script, which isn't meant for production).

## Setup

You'll need [Node.js](https://nodejs.org) 18+ installed.

```bash
cd frontend
npm install
npm run dev
```

This starts the dev server at `http://localhost:5173`. The Vite config
also proxies `/api/*` to `http://localhost:8000` so once the FastAPI
backend exists, frontend calls to `/api/...` will reach it without CORS
config in dev.

To type-check and build for production:

```bash
npm run build
npm run preview
```

## Next steps (not yet done)

- Migrate Student Dashboard, ATS Score Breakdown, Job Match Engine pages
- Add ShadCN components as each page's forms need them (Select, Textarea,
  Progress, etc. — installed via `npx shadcn@latest add <component>`)
- Wire pages to backend once Phase B (FastAPI) starts
