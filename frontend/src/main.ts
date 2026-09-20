import { startRenderLoop } from "./render/loop";
import type { SceneSpec } from "./types";
import freeFallMock from "./mocks/free-fall.json";

const app = document.querySelector<HTMLDivElement>("#app")!;
app.innerHTML = `
  <main style="font-family: system-ui, sans-serif; max-width: 840px; margin: 2rem auto;">
    <h1>PhysicsLens</h1>
    <p>Rendering from a hand-written mock scene spec (PLAN.md: build against mock
       JSON from day one). Swap <code>freeFallMock</code> below for the real
       <code>/predict</code> response once Module 2 is up.</p>
    <canvas id="scene" width="800" height="480" style="border: 1px solid #ccc; width: 100%; height: auto;"></canvas>
  </main>
`;

const canvas = document.querySelector<HTMLCanvasElement>("#scene")!;
startRenderLoop(canvas, freeFallMock as SceneSpec);
