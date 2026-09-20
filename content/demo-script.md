# Demo script (draft — M4 refines and rehearses)

Straight from PLAN.md's draft, expanded with the actual UI beats to hit.

1. **Predict.** As a student, type a belief — "a heavier ball falls faster."
2. **Observe.** The ghost (student's prediction) and real physics run together;
   they land at the same time; a divergence marker highlights where the student
   was wrong.
3. **Explain.** The named misconception + correct model + syllabus unit appear
   (pulled from `/content/misconceptions.json`).
4. **Depth via auth.** Switch to physics-major role → Cedar unlocks the formal
   lens; the same pendulum now shows its phase portrait and a small-angle toggle
   that visibly breaks period-independence at large amplitude.
5. **Live curveball.** Let a judge phrase a belief in their own words →
   OpenSearch narrows candidates, the agent picks the right scene.
6. **Close** on the architecture slide: Firecracker as the production sandbox for
   teacher-authored custom force laws (stretch, architecture-only).

## Pre-demo checklist

- [ ] Offline model fallback confirmed (Ollama, no network dependency)
- [ ] All 3 scenes used in the script are complete quads (see
      `/shared/scene-registry.json`)
- [ ] `docker-compose up` from `/infra` brings up a clean stack from cold
- [ ] Cut anything flaky — a tight POE loop on 3 scenes beats a shaky 6
      (PLAN.md risk list)

## Fallback plan if live demo breaks

Record a screen capture of steps 1–5 once the loop is proven end-to-end (PLAN.md
Day 1 evening milestone), as insurance against live LocalStack/Docker flakiness
during judging.
