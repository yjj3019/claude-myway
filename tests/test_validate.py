import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate_repo  # noqa: E402


VER = (ROOT / "VERSION").read_text(encoding="utf-8").strip()


class ValidateRepo(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        shutil.copytree(ROOT, self.tmp / "r", ignore=shutil.ignore_patterns(".git", "__pycache__", "tests"))
        self.r = self.tmp / "r"

    def errs(self, terms=()):
        return validate_repo.validate(self.r, terms)

    def skill(self, name="writing"):
        return self.r / "plugins/myway/skills" / name / "SKILL.md"

    def test_clean_repo_passes(self):
        self.assertEqual(self.errs(), [])

    def test_name_mismatch(self):
        p = self.skill()
        p.write_text(p.read_text(encoding="utf-8").replace("name: writing", "name: other", 1), encoding="utf-8")
        self.assertTrue(any("name" in e for e in self.errs()))

    def test_long_description(self):
        p = self.skill()
        t = p.read_text(encoding="utf-8").splitlines()
        i = next(n for n, l in enumerate(t) if l.startswith("description:"))
        t[i] = "description: " + "가" * 1100
        p.write_text("\n".join(t) + "\n", encoding="utf-8")
        self.assertTrue(any("description" in e for e in self.errs()))

    def test_yaml_unsafe_description(self):
        p = self.skill()
        t = p.read_text(encoding="utf-8").splitlines()
        i = next(n for n, l in enumerate(t) if l.startswith("description:"))
        t[i] = "description: 사용법: 이렇게 쓴다"
        p.write_text("\n".join(t) + "\n", encoding="utf-8")
        self.assertTrue(any("YAML" in e for e in self.errs()))

    def test_crlf_frontmatter_ok(self):
        p = self.skill()
        p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual(self.errs(), [])

    def test_version_mismatch(self):
        (self.r / "VERSION").write_text("9.9.9\n")
        self.assertTrue(any("버전" in e for e in self.errs()))

    def test_codex_version_mismatch(self):
        p = self.r / "plugins/myway/.codex-plugin/plugin.json"
        p.write_text(p.read_text(encoding="utf-8").replace(VER, "0.0.1"), encoding="utf-8")
        self.assertTrue(any("codex" in e for e in self.errs()))

    def test_codex_marketplace_bad_path(self):
        p = self.r / ".agents/plugins/marketplace.json"
        p.write_text(p.read_text(encoding="utf-8").replace("./plugins/myway", "./nope"), encoding="utf-8")
        self.assertTrue(any("Codex" in e for e in self.errs()))

    def test_codex_marketplace_missing(self):
        (self.r / ".agents/plugins/marketplace.json").unlink()
        self.assertTrue(any("Codex" in e for e in self.errs()))

    def test_grok_marketplace_version_and_path(self):
        p = self.r / ".grok-plugin/marketplace.json"
        raw = p.read_text(encoding="utf-8")
        p.write_text(raw.replace(VER, "0.0.1"), encoding="utf-8")
        self.assertTrue(any("grok" in e for e in self.errs()))
        p.write_text(raw.replace("./plugins/myway", "./nope"), encoding="utf-8")
        self.assertTrue(any("Grok" in e for e in self.errs()))

    def test_broken_manifest(self):
        (self.r / ".claude-plugin/marketplace.json").write_text("{")
        self.assertTrue(self.errs())

    def test_missing_reference(self):
        p = self.skill()
        p.write_text(p.read_text(encoding="utf-8") + "\n`references/nope-missing.md`\n", encoding="utf-8")
        self.assertTrue(any("nope-missing" in e for e in self.errs()))

    def test_sensitive_patterns(self):
        n = self.r / "docs" / "x.md"
        for bad in ("a" * 32, "me@" + "corp.test", "10.1." + "2.3", "/home" + "/someone/x", "ghp_" + "a" * 20, "CVE-" + "2026-12345", "RHSA-" + "2026:1234"):
            n.write_text(bad)
            self.assertTrue(any("민감" in e for e in self.errs()), bad)

    def test_safe_values_allowed(self):
        (self.r / "docs" / "x.md").write_text("203.0.113.5 and a@example.com and 127.0.0.1")
        self.assertEqual(self.errs(), [])

    def test_banned_terms(self):
        (self.r / "docs" / "x.md").write_text("Secret Corp")
        self.assertTrue(any("금지어" in e for e in self.errs(["secret corp"])))


class RhelCveExample(unittest.TestCase):
    def test_example_passes_checker(self):
        import subprocess
        d = ROOT / "plugins/myway/skills/rhel-cve"
        text = (d / "references/report-example.md").read_text(encoding="utf-8")
        body = text.split("\n<!-- REPORT START -->\n", 1)[1]
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "r.md"
            f.write_text(body, encoding="utf-8")
            r = subprocess.run([sys.executable, str(d / "scripts/check_report.py"), str(f)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)


class GradeCalc(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(ROOT / "plugins/myway/skills/admission-helper/scripts"))
        import grade_calc
        self.g = grade_calc

    def test_safe_eval_arithmetic(self):
        self.assertAlmostEqual(self.g.safe_eval("930+70*x/9.8", 9.8), 1000.0)

    def test_safe_eval_rejects_code(self):
        for bad in ("__import__('os').getcwd()", "x.__class__", "open('f')", "[1]"):
            with self.assertRaises(Exception):
                self.g.safe_eval(bad, 1.0)


class InstallCodex(unittest.TestCase):
    def test_copy_and_skip(self):
        import install_skills
        with tempfile.TemporaryDirectory() as d:
            done, skipped = install_skills.install(d)
            self.assertEqual(len(done), 5)
            self.assertTrue((Path(d) / "writing" / "SKILL.md").is_file())
            done2, skipped2 = install_skills.install(d)
            self.assertEqual((done2, len(skipped2)), ([], 5))
            done3, _ = install_skills.install(d, force=True)
            self.assertEqual(len(done3), 5)

    def test_main_target_grok_uses_dest(self):
        import install_skills
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(install_skills.main(["--dest", d]), 0)
            self.assertTrue((Path(d) / "devlog" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
