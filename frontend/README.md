# /frontend — Module 1

Rendering engine, ghost-prediction overlay, depth lenses. Vite + TypeScript,
Canvas 2D (no framework — the whole surface is one `requestAnimationFrame`
loop per PLAN.md, a framework would fight that more than help it).

## Run

```bash
npm install
npm run dev
```

## What's here vs. what's TODO

- `src/types.ts` — mirrors `/shared/scene-spec.schema.json` by hand.
- `src/render/loop.ts` — the animation loop shell; looks up a renderer by
  `sceneType` and calls it every frame.
- `src/scenes/index.ts` — **empty registry, this is the actual Module 1 work.**
  Add one renderer per scene in `/shared/scene-registry.json`, each drawing the
  ghost (from `spec.prediction`) and the real physics from one shared physics
  state, with a divergence marker where they part ways.
- `src/mocks/*.json` — hand-written fixtures so you never have to wait on the
  backend. Swap for the real `/predict` response in `src/main.ts` once Module 2
  is up (PLAN.md Day 1 afternoon checkpoint).

## First deliverable (PLAN.md)

Free-fall + pendulum rendering from mock JSON, including a hardcoded ghost
overlay, before the backend exists.

## Later: depth lenses

Two renderers sharing one physics state (PLAN.md):
- **Intuition** — energy bars, force vectors, plain-language callout
- **Formal** — phase-space canvas, equation via KaTeX, approximation toggle

Which lens is available is a Cedar decision, not a frontend one — the frontend
only ever renders what the backend/Cedar already authorized.
