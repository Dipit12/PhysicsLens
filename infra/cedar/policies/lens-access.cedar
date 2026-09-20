// Three depth lenses gated by role (PLAN.md):
//   student -> intuition only
//   major   -> + formal
//   teacher -> + authoring, all scenes unlocked
//
// Default-deny: a request is allowed only if a permit matches and no forbid
// matches. Sessions are members of PhysicsLens::Role::{"student","major","teacher"}.
// Scope `in` takes a single entity UID (Cedar 4); role unions live in `when`.

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
  principal,
  action == PhysicsLens::Action::"viewLens",
  resource
) when {
  resource.lens == "formal" &&
  (principal in PhysicsLens::Role::"major" ||
   principal in PhysicsLens::Role::"teacher")
};

// Students are explicitly forbidden from the formal lens (demo-critical).
forbid (
  principal,
  action == PhysicsLens::Action::"viewLens",
  resource
) when {
  resource.lens == "formal" &&
  principal in PhysicsLens::Role::"student"
};

// Only teacher sessions may author POE prompts.
permit (
  principal,
  action == PhysicsLens::Action::"authorPrompt",
  resource
) when {
  principal in PhysicsLens::Role::"teacher"
};

// Only teacher sessions may unlock every scene.
permit (
  principal,
  action == PhysicsLens::Action::"unlockAllScenes",
  resource
) when {
  principal in PhysicsLens::Role::"teacher"
};
