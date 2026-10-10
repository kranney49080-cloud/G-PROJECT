#!/usr/bin/env python3
"""Validate a two-hop, repository-relative MAPS memory index.

This tool is deterministic and read-only. It never modifies source documents.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER = Path("Tools/AIDevTeam/memory/MAP.md")
EXPECTED_HEADERS = ("Projects", "State", "Skills", "Memory", "Routines", "Not here")
LINKS = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def referenced_paths(file: Path) -> list[str]:
    return LINKS.findall(file.read_text(encoding="utf-8"))


def verify_map(root: Path) -> dict:
    root = root.resolve()
    index = root / MASTER
    result = {"ok": False, "areas": 0, "documents": 0, "issues": [], "index": str(index)}
    if not index.is_file():
        result["issues"].append("Missing master memory map: " + str(index))
        return result

    area_links = referenced_paths(index)
    if not area_links:
        result["issues"].append("Master map has no area links.")
    observed_docs: set[Path] = set()
    for raw_area in area_links:
        area = (index.parent / raw_area).resolve()
        if not area.is_relative_to(root) or not area.is_file():
            result["issues"].append("Missing or out-of-root area signpost: " + raw_area)
            continue
        if not area.is_relative_to(index.parent):
            result["issues"].append("Area signpost must live inside memory/: " + raw_area)
            continue
        result["areas"] += 1
        area_text = area.read_text(encoding="utf-8")
        headers = re.findall(r"^## (.*)$", area_text, flags=re.MULTILINE)
        if tuple(headers) != EXPECTED_HEADERS:
            result["issues"].append(str(area.relative_to(root)) + ": invalid six section headers.")
        for raw_doc in referenced_paths(area):
            if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#)", raw_doc, flags=re.IGNORECASE):
                result["issues"].append("Use local repository-relative file paths only: " + raw_doc)
                continue
            doc = (area.parent / raw_doc).resolve()
            if not doc.is_relative_to(root) or not doc.is_file():
                result["issues"].append(str(area.relative_to(root)) + ": broken link " + raw_doc)
            elif doc in observed_docs:
                result["issues"].append("Document linked from multiple areas: " + str(doc.relative_to(root)))
            else:
                observed_docs.add(doc)
    result["documents"] = len(observed_docs)
    result["ok"] = not result["issues"] and result["areas"] > 0 and result["documents"] > 0
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true", help="machine-readable JSON")
    args = parser.parse_args()
    result = verify_map(args.root)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("Memory index:", "PASS" if result["ok"] else "FAIL")
        print("Area signposts:", result["areas"], "source documents:", result["documents"])
        for issue in result["issues"]:
            print(" -", issue, file=sys.stderr)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
