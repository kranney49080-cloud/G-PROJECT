"""Build GProjectBridge.ts4script. MUST run under Python 3.7 (the game's version).

Usage: python build_mod.py <project_dir>
Output: <project_dir>/dist/GProjectBridge.ts4script + bridge_config.json
Only .pyc files go in the archive (the game loads compiled modules).
"""
import importlib.util
import os
import py_compile
import shutil
import sys
import zipfile

NAME = "GProjectBridge.ts4script"
EXPECTED_MAGIC = b"B\r\r\n"  # Python 3.7 bytecode magic (3394)


def main():
    if sys.version_info[:2] != (3, 7):
        sys.exit("ERROR: build must run under Python 3.7, got %s" % sys.version.split()[0])
    if importlib.util.MAGIC_NUMBER != EXPECTED_MAGIC:
        sys.exit("ERROR: unexpected bytecode magic %r" % importlib.util.MAGIC_NUMBER)
    if len(sys.argv) != 2:
        sys.exit("usage: build_mod.py <project_dir>")

    proj = os.path.abspath(sys.argv[1])
    src = os.path.join(proj, "src")
    stage = os.path.join(proj, "build", "stage")
    dist = os.path.join(proj, "dist")
    if not os.path.isdir(src):
        sys.exit("ERROR: no src folder at %s" % src)

    shutil.rmtree(os.path.join(proj, "build"), ignore_errors=True)
    os.makedirs(stage)
    os.makedirs(dist, exist_ok=True)

    compiled = []
    for root, _dirs, files in os.walk(src):
        for f in sorted(files):
            if not f.endswith(".py"):
                continue
            rel = os.path.relpath(os.path.join(root, f), src)
            out = os.path.join(stage, rel + "c")  # foo.py -> foo.pyc, no __pycache__
            os.makedirs(os.path.dirname(out), exist_ok=True)
            py_compile.compile(os.path.join(root, f), cfile=out, dfile=rel, doraise=True)
            compiled.append(rel + "c")

    target = os.path.join(dist, NAME)
    if os.path.exists(target):
        os.remove(target)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in sorted(compiled):
            zf.write(os.path.join(stage, rel), rel.replace(os.sep, "/"))

    # Self-check: every entry must carry the 3.7 magic.
    with zipfile.ZipFile(target) as zf:
        for info in zf.infolist():
            if zf.read(info.filename)[:4] != EXPECTED_MAGIC:
                sys.exit("ERROR: bad bytecode magic in %s" % info.filename)

    cfg = os.path.join(proj, "config", "bridge_config.json")
    if os.path.exists(cfg):
        shutil.copy2(cfg, os.path.join(dist, "bridge_config.json"))
    print("OK: %s (%d modules)" % (target, len(compiled)))


if __name__ == "__main__":
    main()
