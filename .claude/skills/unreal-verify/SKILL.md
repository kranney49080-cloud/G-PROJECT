---
name: unreal-verify
description: Verify an Unreal Engine change with actual compile, Play-In-Editor, scene screenshots, animation preview, audio and performance evidence. Use on UE assets or gameplay changes.
---
Require exact .uproject location and editor access. Before running verify tool versions, project dirty state and known baseline. Never assume an editor is reachable from this chat.

For code: capture compile result and log. For animation: verify skeleton, retarget, root motion, feet/ground, start/end transitions, side/gameplay camera and montage compatibility. For materials/trees/UI: compare against reference from canonical project files, verify in gameplay camera and second view. For any harvested move capture accompanying SFX and trigger synchronization. Record performance against the project's test target only from actual measurement.

Evidence report: what changed, engine/version, executable commands, timestamps, result, at least two relevant visual views or explanation of unavailable evidence, audio result, reproducibility, remaining regressions. If no PIE/video/sound test, mark visually BLOCKED, not PASS. User accepts final result, not agents.

