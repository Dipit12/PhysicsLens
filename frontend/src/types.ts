/**
 * Hand-mirrors /shared/scene-spec.schema.json. Keep in sync — this file has no
 * codegen step yet (fine for a hackathon; flag if drift becomes a problem).
 */

export type SceneType =
  | "free-fall"
  | "projectile"
  | "pendulum"
  | "circular-motion"
  | "elastic-collision"
  | "spring-shm";

export interface Prediction {
  claim: string;
  expectedOutcome: string;
}

export interface Explanation {
  summary?: string;
  misconception: string;
  correctModel: string;
  syllabusUnit: string;
  /** LaTeX, rendered via KaTeX in the formal lens. */
  equation: string;
}

export interface SceneSpec {
  sceneType: SceneType;
  params: Record<string, number | boolean | string>;
  prediction: Prediction;
  explanation: Explanation;
}

export type Role = "student" | "major" | "teacher";
export type Lens = "intuition" | "formal" | "author";
