# Deploy rules (written after repeated stale-file incidents, 2026-10-14)

Root cause: writing a file to the PC with the same staging path a second time re-sent the FIRST copy.
So run.bat, survey.py and run2.bat all ended up older than what was meant.

Rules for every file written to this machine:
1. Stage each write under a NEW path (e.g. /mnt/user-data/outputs/vN/<name>); never re-use one.
2. After writing, list the target folder and compare size + modified time with the local file.
   A mismatch means the write did not take: stop and redo with a new path.
3. Builds go through run3.bat, which logs the source size/hash and the installed size,
   so run_log.txt proves what was actually built.
4. Never trust "written": trust the size on disk.
