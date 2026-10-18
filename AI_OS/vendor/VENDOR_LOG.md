# Vendor log

Checked 2026-10-15 by Claude. SHA-256 was recomputed from the files on F: and compared with each SOURCE.txt. Status: Approved / Reference only / Not usable as is / Missing.

| Item | Folder | Version | License | Hash matches SOURCE.txt | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Script Reloader (Oops19) | script_reloader | v1.0.0 | GPL-3.0 | Yes | Approved | Install into Mods only when we test reloading. |
| S4CL | s4cl | v3.22 | MIT | Yes | Approved | Dialogs, events, persistence. |
| BluuberryLibrary | bluuberry | main, commit 7dfae66 | none stated | Yes | Reference only | No licence stated: read for ideas, do not copy code. |
| s4pe | s4pe | v0.6.0 | GPL-3.0 | Yes | Approved | Package editor, 2021 build. |
| Lot51 Core Library | lot51 | 1.10.1 | GPL-3.0 | Yes | Approved | GPL: anything that links it must also be GPL. |
| decompyle3 | decompiler | 3.9.3 | GPL-3.0 | Yes | Approved | For game .pyc files. Not installed yet. |
| pycdc | decompiler | master | GPL-3.0 | Yes | Approved | Needs compiling; backup to decompyle3. |
| decompile.py (LuquanLi) | decompiled_game\luquanli_script_builder | master | MIT | Yes | Not usable as is | Needs its missing utils package, uses uncompyle6 and Mac paths. We write our own small script instead. |
| TS4 Premade Household Tool | premade_household | n/a | n/a | n/a | Missing | Login-gated on ModTheSims. User downloads it, or we spawn Sims by script instead. |
| Sims 4 Studio | s4s | n/a | n/a | n/a | Missing | Login-gated. User installs. |
| sims4ai, fivesim, TS4-MCP | sims4ai, fivesim, ts4_mcp | n/a | n/a | n/a | Missing | Gemini could not find them. Not needed for the next phase. |

Gemini's own table in GEMINI_REPORT.md has typos in some hashes and folder names. The SOURCE.txt files and the files themselves are correct.

## actrun (Actionforge) - added 2026-10-16
- File: actrun-v0.16.11.cli-x64-windows (actrun.exe 107,890,733 bytes, hello-world.act 788, readme.md 342)
- Source: https://www.actionforge.dev/download/actrun-v0.16.11.cli-x64-windows.zip (downloaded by the owner into F:\Downloads\actrun-v0.16.11.cli-x64-windows)
- SHA-256 actrun.exe: 8e873c36746a47e221eb0ec2d7f56679c6e87e2020a036a92ba0e4f1068c5ab5
- Checked: PE32+ x86-64 Windows console executable. The download page publishes no checksum or attestation for this release, so the hash is recorded here but NOT verified against a vendor value. Not run yet.
- Licence: Actionforge EULA, free below $500k/yr revenue (https://actionforge.dev/eula). Telemetry on by default; opt-out in docs.
- Location: left in F:\Downloads (107 MB is over the 30 MB copy limit of the file bridge); AI_OS\talk\af_agent.py looks there.
- Agent usage string inside the binary: actrun agent --token <token>

## decompyle3 dependencies (PyPI download) - added 2026-10-16
- Downloaded via pip download decompyle3==3.9.3 -d F:\MrMak\Workspace\AI_OS\vendor\decompiler\
- Files stored in: F:\MrMak\Workspace\AI_OS\vendor\decompiler\

| File | Size (bytes) | SHA-256 |
| --- | --- | --- |
| spark_parser-1.9.0-py313-none-any.whl | 63,427 | fc2e188601a6c8f7a68e2d7bd97ca377f6dc271a67607ff11e6beef39d0e9d1d |
| xdis-6.1.7-py313-none-any.whl | 197,739 | 9706b8ab4616e89315ec7d070961975fdfbec623cc26a27fd3b57d7d26b75264 |
| click-8.5.0-py3-none-any.whl | 125,251 | 255bc9599cf7748b4b1a446ccc735421bd08a2ae529a8b88597d3de5664ee360 |
| six-1.17.0-py2.py3-none-any.whl | 11,050 | 4721f391ed90541fddacab5acf947aa0d3dc7d27b2e1e8eda2be8970586c3274 |
