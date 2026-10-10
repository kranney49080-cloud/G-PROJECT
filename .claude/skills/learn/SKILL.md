---
name: learn
description: Capture a mistake, failed approach, successful correction or repeatable discovery in append-only local lessons, and propose a safely reviewed skill improvement.
---
Invoke after a meaningful failure, user correction, regression, or durable improvement.

1. Separate observed evidence from hypotheses. Capture task, symptom, root cause (or "unknown"), corrective action, proof (or "unverified"), and the narrowly relevant skill.
2. Use python scripts/ai_os.py learn with the required named arguments; do not invent success or proof. Private data stays in ignored .ai-os-data/lessons.jsonl.
3. If this is a recurring problem, invoke python scripts/ai_os.py propose --id <lesson-id>, inspect other similar lessons, and present the suggested single-skill change to the owner. Do not auto-patch canonical skills.
4. After approval, use /skill-factory: add a regression example or deterministic check, test the revised skill on old and new failures, and commit the skill through review.

Lessons are not claims of durable model training. The improvement is in user-owned files and prompts, accessible on future runs.

