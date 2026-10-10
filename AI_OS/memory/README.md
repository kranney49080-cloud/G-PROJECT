# Memory is owned evidence, not a chat transcript

Two layers:
- CANONICAL knowledge: repo source files and skill versions, reached by AI_OS/MAP.md pointers. Each fact has one home.
- EVENT history: append-only local .ai-os-data/lessons.jsonl. It preserves failures, corrections, success cases, dates, proof and skill affinity. It is gitignored because the repo is public.

Workflow: before action use /recall; after mistake or significant success use /learn; generate a proposed skill revision with python scripts/ai_os.py propose --id LESSON_ID. Proposal goes in private .ai-os-data/proposals/ and never changes a live skill automatically. Only after deterministic/visual evaluation and owner approval should an implementation branch update the skill, tests, examples and version notes.

Capture both failure and successful recovery. A claimed solution without proof remains UNVERIFIED. Never turn a single anecdote into a blanket rule without evaluation. Store causal mechanism and observable symptoms, not blame. For repeated issues, aggregate them by skill and run tests against prior error examples.

Never store credentials, personal messages, copyrighted game assets or private file contents in GitHub. Private local files may be backed up separately only with explicit approval.

