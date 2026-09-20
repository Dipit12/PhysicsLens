# PartyRock prompt — draft (prototyping only)

Per CLAUDE.md, PartyRock is used **once, pre-build**, to prototype the query →
scene-spec prompt. It is not part of the running app — once the prompt below is
stable, hand it to Module 2 to embed in the Strands agent's tool descriptions /
system prompt.

## Prompt under test

```
You are extracting structured data from a high-school student's physics belief.

Given the student's message, identify:
1. Which ONE canonical scene it describes: free-fall, projectile, pendulum,
   circular-motion, elastic-collision, or spring-shm.
2. The scenario parameters implied or stated (use reasonable defaults for
   anything not mentioned — e.g. "a bowling ball and a tennis ball" implies
   massA >> massB, not exact numbers).
3. The student's CLAIM — their stated or implied belief, in their own words.
4. The EXPECTED OUTCOME that claim implies, phrased so it can be checked against
   the real simulation (e.g. "massA reaches the ground before massB").

Do not generate simulation code. Do not invent a misconception category — that
comes from a fixed catalogue you'll be given separately. Only extract scenario +
prediction.

Student message: "{{text}}"

Respond as JSON: { sceneType, params, prediction: { claim, expectedOutcome } }
```

## Test phrasings to run through PartyRock before handing off (PLAN.md risk: "test
against many phrasings early")

- "a heavier ball falls faster than a light one"
- "if I drop a bowling ball and a feather at the same time, the bowling ball
  wins"
- "when you swing a pendulum with a heavier weight, it swings faster"
- "a spinning ball on a string feels like it's being flung outward"
- "the heavier car in a crash just plows through the lighter one"
- "a spring loses energy every time it bounces, that's why it stops"

## Status

- [ ] Prompt drafted (this file)
- [ ] Run against all 6 test phrasings in PartyRock
- [ ] Stable version copied into `/backend/src/agent.py` tool docstrings /
      system prompt
- [ ] Handed off to Module 2 owner
