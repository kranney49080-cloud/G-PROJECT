"""Map integrity, Pulse caps, and non-mutating dry-run regression tests."""
import json
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL_DIR = ROOT / "Tools" / "AIDevTeam"
sys.path.insert(0, str(TOOL_DIR))
import memory_check  # noqa: E402
import pulse  # noqa: E402


class MemoryAndPulseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.master = self.root / memory_check.MASTER
        self.master.parent.mkdir(parents=True)
        area = self.master.parent / "areas" / "one.md"
        area.parent.mkdir(parents=True)
        original = self.root / "Design" / "state.md"
        original.parent.mkdir(parents=True)
        original.write_text("Canonical details go here.\n", encoding="utf-8")
        area.write_text("# Area\n\n## Projects\n- [Canonical](../../../../Design/state.md)\n\n"
                        "## State\nState lives in the linked file.\n\n## Skills\nNone.\n\n"
                        "## Memory\nNone.\n\n## Routines\nNone.\n\n## Not here\nNone.\n",
                        encoding="utf-8")
        self.master.write_text("# Memory map\n- [One area](areas/one.md)\n", encoding="utf-8")
        self.area = area
        self.original = original

    def test_two_hop_map_success(self):
        report = memory_check.verify_map(self.root)
        self.assertTrue(report["ok"], report["issues"])
        self.assertEqual((report["areas"], report["documents"]), (1, 1))

    def test_broken_link_fails(self):
        self.original.unlink()
        report = memory_check.verify_map(self.root)
        self.assertFalse(report["ok"])
        self.assertTrue(any("broken link" in issue for issue in report["issues"]))

    def test_malformed_signpost_fails(self):
        self.area.write_text("## Projects\n- [Canonical](../../../../Design/state.md)\n",
                             encoding="utf-8")
        self.assertFalse(memory_check.verify_map(self.root)["ok"])

    def test_rolling_hour_limit(self):
        now = datetime.now(timezone.utc)
        record = {"routine": pulse.ROUTINE, "started_utc": now.isoformat()}
        file = pulse.history_file(self.root, now.date().isoformat())
        file.parent.mkdir(parents=True)
        file.write_text((json.dumps(record) + "\n") * pulse.ROLLING_HOUR_LIMIT,
                        encoding="utf-8")
        ok, _ = pulse.allowed(self.root, now)
        self.assertFalse(ok)

    def test_daily_limit(self):
        now = datetime.now(timezone.utc)
        past = now - timedelta(hours=4)
        record = {"routine": pulse.ROUTINE, "started_utc": past.isoformat()}
        file = pulse.history_file(self.root, now.date().isoformat())
        file.parent.mkdir(parents=True)
        file.write_text((json.dumps(record) + "\n") * pulse.DAY_LIMIT,
                        encoding="utf-8")
        self.assertFalse(pulse.allowed(self.root, now)[0])

    def test_invalid_log_fails_closed(self):
        now = datetime.now(timezone.utc)
        file = pulse.history_file(self.root, now.date().isoformat())
        file.parent.mkdir(parents=True)
        file.write_text("not JSON!\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            pulse.allowed(self.root, now)

    def test_real_audit_appends_record_without_editing_original(self):
        before = self.original.read_bytes()
        self.assertEqual(pulse.run_audit(self.root), 0)
        self.assertEqual(self.original.read_bytes(), before)
        date = datetime.now(timezone.utc).date().isoformat()
        records = pulse.prior_records(pulse.history_file(self.root, date))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["cost_usd"], 0)

    def test_missing_master_report_fails(self):
        self.master.unlink()
        self.assertFalse(memory_check.verify_map(self.root)["ok"])


if __name__ == "__main__":
    unittest.main()
