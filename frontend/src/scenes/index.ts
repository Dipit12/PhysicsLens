import type { SceneSpec } from "../types";

export type SceneRenderer = (
  ctx: CanvasRenderingContext2D,
  spec: SceneSpec,
  tSeconds: number,
) => void;

/**
 * TODO(Module 1): one renderer per sceneType in /shared/scene-registry.json.
 *
 * Each renderer draws BOTH paths from one physics state:
 *   - the "ghost": spec.prediction.expectedOutcome, translucent
 *   - the real simulation, driven by spec.params
 * and marks the frame where they diverge (PLAN.md "Ghost overlay" — this is
 * the visual payoff of the whole POE loop, prioritize it over adding scenes).
 *
 * First deliverable per PLAN.md: free-fall + pendulum against the mock JSON in
 * ./src/mocks, before the backend exists.
 */
export const sceneRenderers: Partial<Record<SceneSpec["sceneType"], SceneRenderer>> = {};
