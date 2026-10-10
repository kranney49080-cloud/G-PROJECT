---
name: skill-factory
description: Create or improve one narrowly scoped, testable Claude skill from a golden example and observed successes/failures; require evidence before promotion.
---
Skill design protocol (one job, one trigger):
1. Define a golden output/example that owner approves; work backwards to required inputs, decisions, and outputs.
2. Create exactly one job and activation description; avoid overlapping with existing skills. Pick fixed rules for mechanical steps, flexible instructions for creative steps.
3. Include inputs, tools, project canonical references, expected output, edge cases, stop conditions, safety constraints and verifiable completion tests in SKILL.md YAML+body. Use supporting files only when needed, keeping initial instructions brief.
4. Build two positive and two negative/edge-case fixtures. Run objective checks and real Unreal PIE/screenshot/audio inspection when relevant. Do not declare subjective quality mechanically verified.
5. Benchmark the same fixed evaluation cases with lower-cost models only where available and authorized; choose based on repeated quality, latency and usage, not marketing.
6. After runs record failures with /learn, compare against golden fixtures, propose surgical changes and retest against old regressions. Only owner-approved changes become versioned skill updates.

The skill is a reusable procedure and knowledge file, not a self-training model. Do not silently overwrite an accepted version.

