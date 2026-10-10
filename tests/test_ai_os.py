"""Offline regression tests for memory/skills behavior."""
import json
from pathlib import Path
import tempfile
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ai_os


class TestAgentMemory(unittest.TestCase):
    def test_route_precise_animation(self):
        found = ai_os.route("harvest Mifune montage with audio capture", [
            {"id": "animation-harvest", "path": "somewhere", "priority": 10,
             "triggers": ["harvest", "audio capture", "mifune"]},
            {"id": "unreal-verify", "path": "other", "priority": 1,
             "triggers": ["unreal", "visual verification"]}])
        self.assertEqual(found[0]["skill"], "animation-harvest")
        self.assertIn("audio capture", found[0]["matched"])

    def test_route_avoids_partial_word(self):
        skills = [{"id": "ship", "path": "x", "triggers": ["rig"], "priority": 0}]
        self.assertEqual(ai_os.route("original texture", skills), [])

    def test_learn_recall_and_propose(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp)
            first = ai_os.learn(store, "Mifune retarget", "foot slide", "root mismatch",
                                "check root profile", "unverified", "animation-harvest",
                                known_skills={"animation-harvest"})
            second = ai_os.learn(store, "Tree color", "bark too brown", "wrong palette",
                                 "use teal palette", "reference comparison", "unreal-verify",
                                 kind="success", confidence="verified")
            self.assertNotEqual(first["id"], second["id"])
            self.assertEqual(len(ai_os.read_lessons(store)), 2)
            self.assertEqual(ai_os.recall("Mifune foot slide", ai_os.read_lessons(store))[0]["id"], first["id"])
            proposal = ai_os.propose(store, first["id"], {"animation-harvest": ".claude/skills/animation-harvest/SKILL.md"})
            self.assertTrue(proposal.exists())
            self.assertIn("NOT APPLIED", proposal.read_text())
            with self.assertRaises(FileExistsError):
                ai_os.propose(store, first["id"], {"animation-harvest": "x"})

    def test_verified_requires_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                ai_os.learn(Path(tmp), "t", "s", "c", "r", "unverified", "ship",
                            confidence="verified", known_skills={"ship"})

    def test_audit_detects_missing_link_and_bad_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AI_OS" / "areas").mkdir(parents=True)
            (root / "AI_OS" / "MAP.md").write_text("[missing](oops.md)\n")
            (root / "AI_OS" / "areas" / "art.md").write_text("# art\n## Projects\n")
            (root / "AI_OS" / "skill_registry.json").write_text(json.dumps({"skills": []}))
            report = ai_os.audit(root)
            self.assertTrue(any("broken link" in err for err in report))
            self.assertTrue(any("six ordered sections" in err for err in report))

    def test_no_log_exists_means_no_recorded_lessons(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(ai_os.read_lessons(Path(tmp)), [])


if __name__ == "__main__":
    unittest.main()
