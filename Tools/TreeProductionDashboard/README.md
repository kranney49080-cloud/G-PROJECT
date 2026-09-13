# Tree Production Dashboard

A lightweight local dashboard for tracking the first harvestable 2.5D tree asset.

## Run it
Open `index.html` in a browser. No build step, package manager, or server is required.

## Features
- core tree asset checklist
- progress bar
- status cycling
- one-click approval
- production notes
- local persistence using browser `localStorage`
- responsive desktop/mobile layout

## Current scope
This is intentionally a standalone prototype. It does not yet write back to GitHub, Unreal, or project files automatically.

Recommended future integration:
1. load approved tree reference thumbnails from the project repository;
2. read/write a JSON manifest for each tree;
3. expose approval state to Astra/OpenCode;
4. eventually surface harvesting-interface requirements and Unreal import readiness.
