import type { SceneSpec } from "../types";
import { sceneRenderers } from "../scenes";

export function startRenderLoop(canvas: HTMLCanvasElement, spec: SceneSpec): void {
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("2D canvas context unavailable");

  const renderer = sceneRenderers[spec.sceneType];
  if (!renderer) {
    ctx.font = "16px sans-serif";
    ctx.fillText(`No renderer registered yet for "${spec.sceneType}"`, 20, 40);
    return;
  }

  const start = performance.now();
  function frame(now: number) {
    const tSeconds = (now - start) / 1000;
    ctx!.clearRect(0, 0, canvas.width, canvas.height);
    renderer!(ctx!, spec, tSeconds);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
