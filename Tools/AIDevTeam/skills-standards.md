# One job · one trigger · one verifiable result

This is our local interpretation of the skills-engineering ideas in the Oct 2026 video **How to Build AI Agent Skills Better Than 99% of People**, https://youtube.com/shorts/mpobP7xQ-oQ . Only the video's title and partial public description were retrievable; this document is a project design decision, **not** a claimed verbatim six-step transcript.

## Skill authoring contract

1. **Golden target first.** For each skill, document one real desired example and at least one failure case; never fabricate a successful Unreal screenshot or automation output.
2. **One job, one trigger.** State a clear input and output; avoid vague all-purpose prompts. The owner-invoked `/ship` skill has one job: coordinate a four-stage gated software change.
3. **Freedom by risk.** The planner and code agent may reason about implementation *within the approved spec*. Shell commands, destructive actions, code publication, source asset edits and production deployment are restricted.
4. **Automated gates.** Run syntax/unit tests for Python scripts; use existing automation for Unreal; capture real before/after screenshots for visual tasks; return BLOCKED when required evidence is missing.
5. **Model choice.** Opus is proposed for planner/reviewer and Sonnet for coder/tester. Measure actual local quality and cost before changing routing; never assume cheapest means adequate. No secret key in repository.
6. **Feedback after each run.** Store findings in each isolated RUN_DIR/review.md. Proposed updates to agents/skills require a reviewed PR or explicit manual patch. Do not silently self-modify instructions based on a single run.

## Example A — documentation-only test change

- **Trigger:** `/ship Add one focused regression test to existing dashboard JSON parsing`.
- **Expected:** Planner names existing files, Coder touches an approved file, Tester runs a real targeted test, Reviewer checks diff and test output, coordinator reports READY_FOR_OWNER_REVIEW.
- **Failure check:** If tests were not run or no test log exists, gate blocks.

## Example B — UE material tweak

- **Trigger:** `/ship Fix hard cel-shade banding on daemon skin in the UE test map`.
- **Expected:** Planner locates actual Unreal project and materials, Coder uses authorized assets only, Tester runs Unreal test + authentic before/after screenshots, Reviewer checks camera match and performance considerations.
- **Failure check:** Missing .uproject or screenshot blocks, even if the material graph description seems correct.

## Example C — unattended routine

- **Trigger:** Manual `py -3 Tools/AIDevTeam/pulse.py` to audit the two-hop memory map.
- **Expected:** A deterministic read-only check, one append-only JSONL record, 0 model calls and 0 cost.
- **Failure check:** Two runs in one rolling hour prevent a third; malformed logs block rather than resetting counters.

### Calibration

Run the same **nonproduction** task several times with the same inputs before measuring Sonnet vs other models. Log correctness, human corrections, tokens and billing as reported by the provider. Do not present speculative savings as real measurements.
