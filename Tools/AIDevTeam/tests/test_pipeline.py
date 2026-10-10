"""Offline regression tests for the Claude orchestration gates; no Unreal required."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOL_DIR))
import pipeline  # noqa: E402
import run_unreal_tests  # noqa: E402


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.run_id = pipeline.create_run(self.root, "Add a safe test feature")
        self.run_dir = pipeline.get_run_dir(self.root, self.run_id)
        self.write("spec.md", "OPEN_QUESTIONS: NONE\nUNREAL_REQUIRED: NO\nVISUAL_REQUIRED: NO\n")

    def write(self, name, contents):
        target = self.run_dir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding="utf-8")
        return target

    def code_ready(self):
        self.write("changes.md", "STATUS: IMPLEMENTED\nFILES_CHANGED:\n- example.py\n")

    def tests_ready(self):
        self.code_ready()
        self.write("actual-tests.log", "one real test ran\n")
        self.write("test-results.md", "RESULT: PASS\nTESTS_RUN: 1\nCOMMANDS: python -m unittest\nOUTPUT_LOG: actual-tests.log\nUNREAL_RESULTS: NOT_REQUIRED\n")

    def test_unique_isolated_run(self):
        other = pipeline.create_run(self.root, "Add a safe test feature")
        self.assertNotEqual(self.run_id, other)
        self.assertTrue((self.run_dir / "request.md").exists())

    def test_plan_passes_with_explicit_flags(self):
        self.assertEqual(pipeline.check_run(self.root, self.run_id, "plan"), "PLAN PASS")

    def test_plan_blocks_questions(self):
        self.write("spec.md", "OPEN_QUESTIONS: BLOCKED\nUNREAL_REQUIRED: NO\nVISUAL_REQUIRED: NO\n")
        with self.assertRaises(pipeline.GateError):
            pipeline.check_run(self.root, self.run_id, "plan")

    def test_code_needs_changes_summary(self):
        self.write("changes.md", "STATUS: IMPLEMENTED\nFILES_CHANGED:\n")
        with self.assertRaises(pipeline.GateError):
            pipeline.check_run(self.root, self.run_id, "code")

    def test_test_gate_rejects_no_tests(self):
        self.code_ready()
        self.write("test-results.md", "RESULT: PASS\nTESTS_RUN: 0\nCOMMANDS: echo ok\nOUTPUT_LOG: test.log\n")
        self.write("test.log", "no tests run")
        with self.assertRaises(pipeline.GateError):
            pipeline.check_run(self.root, self.run_id, "test")

    def test_test_gate_requires_log(self):
        self.code_ready()
        self.write("test-results.md", "RESULT: PASS\nTESTS_RUN: 1\nCOMMANDS: echo ok\nOUTPUT_LOG: does-not-exist.log\n")
        with self.assertRaises(pipeline.GateError):
            pipeline.check_run(self.root, self.run_id, "test")

    def test_visual_gate_requires_real_images(self):
        self.write("spec.md", "OPEN_QUESTIONS: NONE\nUNREAL_REQUIRED: NO\nVISUAL_REQUIRED: YES\n")
        self.tests_ready()
        self.write("evidence.md", "EVIDENCE_STATUS: READY\nBEFORE_IMAGE: evidence/before.png\nAFTER_IMAGE: evidence/after.png\nREFERENCE: ref.png\nCAMERA_VIEWS: Gameplay and side\n")
        with self.assertRaises(pipeline.GateError):
            pipeline.check_run(self.root, self.run_id, "test")

    def test_visual_gate_rejects_identical_images(self):
        self.write("spec.md", "OPEN_QUESTIONS: NONE\nUNREAL_REQUIRED: NO\nVISUAL_REQUIRED: YES\n")
        self.tests_ready()
        self.write("evidence.md", "EVIDENCE_STATUS: READY\nBEFORE_IMAGE: evidence/before.png\nAFTER_IMAGE: evidence/after.png\nREFERENCE: ref.png\nCAMERA_VIEWS: Gameplay and side\n")
        png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32
        (self.run_dir / "evidence").mkdir()
        for name in ("before.png", "after.png"):
            (self.run_dir / "evidence" / name).write_bytes(png)
        with self.assertRaises(pipeline.GateError):
            pipeline.check_run(self.root, self.run_id, "test")

    def test_unreal_gate_requires_real_report(self):
        self.write("spec.md", "OPEN_QUESTIONS: NONE\nUNREAL_REQUIRED: YES\nVISUAL_REQUIRED: NO\n")
        self.tests_ready()
        self.write("test-results.md", "RESULT: PASS\nTESTS_RUN: 1\nCOMMANDS: UnrealEditor-Cmd.exe\nOUTPUT_LOG: actual-tests.log\nUNREAL_RESULTS: PASS\n")
        with self.assertRaises(pipeline.GateError):
            pipeline.check_run(self.root, self.run_id, "test")

    def test_review_gate_requires_verdict(self):
        self.tests_ready()
        self.assertIn("TEST PASS", pipeline.check_run(self.root, self.run_id, "test"))
        self.write("review.md", "VERDICT: NEEDS_WORK\n")
        with self.assertRaises(pipeline.GateError):
            pipeline.check_run(self.root, self.run_id, "review")
        self.write("review.md", "VERDICT: READY_FOR_OWNER_REVIEW\n")
        self.assertIn("READY FOR OWNER REVIEW",
                      pipeline.check_run(self.root, self.run_id, "review"))

    def test_invalid_run_path_rejected(self):
        with self.assertRaises(pipeline.GateError):
            pipeline.get_run_dir(self.root, "../../somewhere")

    def test_unreal_report_rejects_missing(self):
        passed, _ = run_unreal_tests.evaluate_report(self.root / "no-report.json")
        self.assertFalse(passed)

    def test_unreal_report_rejects_skipped(self):
        report = self.root / "index.json"
        report.write_text(json.dumps({
            "succeeded": 1, "succeededWithWarnings": 0, "failed": 0,
            "notRun": 1, "inProcess": 0, "tests": [{"state": "Success"}]
        }), encoding="utf-8")
        self.assertFalse(run_unreal_tests.evaluate_report(report)[0])

    def test_unreal_report_accepts_success(self):
        report = self.root / "index.json"
        report.write_text(json.dumps({
            "succeeded": 1, "succeededWithWarnings": 0, "failed": 0,
            "notRun": 0, "inProcess": 0, "tests": [{"state": "Success"}]
        }), encoding="utf-8")
        self.assertTrue(run_unreal_tests.evaluate_report(report)[0])


if __name__ == "__main__":
    unittest.main()
