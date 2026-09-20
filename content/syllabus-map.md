# Syllabus map

**Chosen syllabus (Day 1 decision, PLAN.md):** AP Physics 1.

Rationale: broad US high-school adoption, unit structure maps cleanly onto the six
canonical scenes without stretching, and the College Board's own unit names are
citable in the demo ("this is Unit 6: Simple Harmonic Motion").

If the team prefers CBSE 11-12 or A-level instead, swap the `syllabusUnit` strings
below and in `/content/misconceptions.json` — nothing else in the schema depends
on which syllabus is chosen, so this is a low-risk swap even mid-hackathon.

| Scene | AP Physics 1 unit |
|---|---|
| Free fall (two masses) | Unit 1: Kinematics |
| Projectile arc | Unit 3: Two-Dimensional Motion |
| Pendulum | Unit 6: Simple Harmonic Motion |
| Circular motion | Unit 5: Circular Motion and Gravitation |
| Elastic collision | Unit 4: Momentum |
| Spring / SHM | Unit 6: Simple Harmonic Motion |

## Depth toggle mapping (Cedar lenses, PLAN.md)

| Lens | Audience | Adds |
|---|---|---|
| Intuition | Student | ghost-vs-real, energy bars, force vectors, plain-language misconception callout |
| Formal | Physics major | + phase-space portrait, approximation toggles, governing equation, limiting cases |
| Author | Teacher | + create a POE prompt, pick which misconception to target, all scenes unlocked |
