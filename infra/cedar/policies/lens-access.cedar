// Three depth lenses gated by role (PLAN.md):
//   student -> intuition only
//   major   -> + formal
//   teacher -> + authoring, all scenes unlocked
//
// Confirm this against the current Cedar policy syntax/CLI before wiring into
// the Lambda authorizer (infra/README.md) -- this is a first-pass scaffold.

// Every session may view the intuition lens.
permit (
  principal,
  action == PhysicsLens::Action::"viewLens",
  resource
) when {
  resource.lens == "intuition"
};

// Physics-major and teacher sessions may additionally view the formal lens.
permit (
  principal in [PhysicsLens::Role::"major", PhysicsLens::Role::"teacher"],
  action == PhysicsLens::Action::"viewLens",
  resource
) when {
  resource.lens == "formal"
};

// Only teacher sessions may author POE prompts or unlock every scene.
permit (
  principal in [PhysicsLens::Role::"teacher"],
  action in [PhysicsLens::Action::"authorPrompt", PhysicsLens::Action::"unlockAllScenes"],
  resource
);
