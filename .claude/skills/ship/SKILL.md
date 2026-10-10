---
name: ship
description: Orchestrate a four-agent software implementation with independent specification, coding, testing, review and owner acceptance. Use on scoped development requests.
disable-model-invocation: false
---
Run the four subagents in order, never in parallel on one worktree.

1. Create an isolated feature branch if none exists; never touch main directly. Create a fresh .pipeline/run-id folder or clear ONLY handoff files from a prior run (leave historical runs untouched). Announce where handoffs will live. If .pipeline/spec.md from another run exists, archive it to .pipeline/archive/<unique-run-id>/, never reuse it.
2. Read AI_OS/MAP.md, relevant signpost, and execute python scripts/ai_os.py recall "<task>" and route "<task>" to determine prior lessons/specialty. If any command is unavailable state why.
3. Delegate request to planner. Read its spec and stop if OPEN QUESTIONS or missing inputs block an accurate implementation.
4. Delegate to coder using planner spec. Confirm .pipeline/changes.md exists and is current.
5. Delegate to tester with full spec and code. Check .pipeline/test-results.md, exit codes, coverage of failure case, and Unreal visual/audio checks. Stop if FAIL or BLOCKED. Never infer that tests passed from a handoff's existence.
6. Delegate to independent read-only reviewer. Because reviewer cannot write, copy the final review verbatim to .pipeline/review.md. If review blocks, leave branch unmerged.
7. Summarize exact changed paths, hashes if committed, test evidence, remaining blockers and reviewer verdict. Do not merge without owner approval. On failure or durable improvement trigger /learn.

No automatic looping on failure, no hidden new permissions, no bypassing owner approval.

