# canidelete: ignore-file  (this suite is full of fixture tripwires)
import datetime as dt
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from canidelete import cli  # noqa: E402

# built at runtime so canidelete doesn't flag its own test-suite
M = "REMOVE" + "-WHEN:"
A = "REMOVE" + "-AFTER:"
TODAY = dt.date(2026, 9, 25)


def fake_fetch(table):
    calls = []

    def fetch(owner, repo, num, token):
        calls.append((owner, repo, num))
        return table.get((owner, repo, num), {"_error": "not found"})

    fetch.calls = calls
    return fetch


class Project:
    def __init__(self, files):
        self.dir = tempfile.TemporaryDirectory()
        for rel, body in files.items():
            path = os.path.join(self.dir.name, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(body)

    def run(self, fetch=None, **kw):
        findings = cli.scan(self.dir.name, **kw)
        cli.evaluate(findings, self.dir.name, today=TODAY, fetch=fetch or fake_fetch({}))
        return findings

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.dir.cleanup()


class VersionTests(unittest.TestCase):
    def test_compare(self):
        self.assertEqual(cli.vcmp("1.10.0", "1.9"), 1)
        self.assertEqual(cli.vcmp("2.0", "2.0.0"), 0)
        self.assertEqual(cli.vcmp("v3.1.4", "3.1.4"), 0)
        self.assertEqual(cli.vcmp("2.0.0rc1", "2.0.0"), -1)
        self.assertEqual(cli.vcmp("2.0.0-beta.2", "2.0.0"), -1)
        self.assertTrue(cli.satisfies("19.1.0", ">=", "19"))
        self.assertFalse(cli.satisfies("18.3.1", ">=", "19"))
        self.assertTrue(cli.satisfies("1.2", "<", "1.10"))


class ParseTests(unittest.TestCase):
    def test_marker_styles(self):
        cases = [
            "# %s requests>=2.32" % M,
            "// %s npm:react>=19 */" % M,
            "<!-- %s python>=3.12 -->" % M,
            "-- remove_when: lodash>=5",
            "/* canidelete: django>=5.0 */",
        ]
        for line in cases:
            conds = cli.scan_line(line)
            self.assertIsNotNone(conds, line)
            self.assertEqual(conds[0].kind, "version", line)
            self.assertNotIn("*/", conds[0].text)
            self.assertNotIn("-->", conds[0].text)

    def test_multiple_conditions(self):
        conds = cli.scan_line("# %s python>=3.12, https://github.com/a/and/issues/7 and 2027-01-01" % M)
        self.assertEqual([c.kind for c in conds], ["version", "github", "date"])
        self.assertEqual(conds[1].text, "https://github.com/a/and/issues/7")

    def test_bare_links_and_ignore(self):
        line = "# workaround for https://github.com/psf/requests/issues/6432"
        self.assertEqual(cli.scan_line(line)[0].kind, "github")
        self.assertIsNone(cli.scan_line(line, bare_links=False))
        self.assertIsNone(cli.scan_line(line + "  canidelete: ignore"))
        self.assertIsNone(cli.scan_line("x = 1  # nothing to see"))

    def test_prose_is_not_a_marker(self):
        self.assertIsNone(cli.scan_line("# add a REMOVE" + "-WHEN comment to your code"))
        self.assertIsNone(cli.scan_line("x = 1  # " + "canidelete: ignore"))

    def test_ignore_file(self):
        with Project({"a.py": "# canidelete: " + "ignore-file\n# %s 2020-01-01\n" % A}) as p:
            self.assertEqual(p.run(), [])

    def test_garbage_condition(self):
        c = cli.scan_line("# %s the heat death of the universe" % M)[0]
        self.assertEqual(c.kind, "unknown")


class GithubJudgeTests(unittest.TestCase):
    def test_states(self):
        self.assertEqual(cli.judge_github({"state": "open", "title": "x"})[0], cli.NO)
        self.assertEqual(cli.judge_github({"state": "closed", "state_reason": "completed",
                                           "closed_at": "2025-01-01T00:00:00Z"})[0], cli.YES)
        self.assertEqual(cli.judge_github({"state": "closed", "state_reason": "not_planned"})[0], cli.WONTFIX)
        self.assertEqual(cli.judge_github({"state": "closed", "pull_request": {"merged_at": "2025-01-01T00:00:00Z"}})[0], cli.YES)
        self.assertEqual(cli.judge_github({"state": "closed", "pull_request": {"merged_at": None}})[0], cli.WONTFIX)
        self.assertEqual(cli.judge_github({"_error": "rate limit"})[0], cli.UNKNOWN)

    def test_ago(self):
        now = dt.datetime(2026, 9, 25)
        self.assertEqual(cli.ago("2026-09-20T10:00:00Z", now), "4d ago")
        self.assertEqual(cli.ago("2025-09-25T00:00:00Z", now), "12mo ago")
        self.assertEqual(cli.ago("2023-01-01T00:00:00Z", now), "3y 8mo ago")


class EndToEndTests(unittest.TestCase):
    def test_full_project(self):
        files = {
            "package-lock.json": json.dumps({"packages": {"node_modules/react": {"version": "19.1.0"},
                                                          "node_modules/lodash": {"version": "4.17.21"}}}),
            "requirements.txt": "requests==2.31.0\nDjango[argon2]==5.1.2\n",
            "src/app.js": "\n".join([
                "// %s npm:react>=19" % M,
                "// %s lodash>=5" % M,
                "// see https://github.com/facebook/react/issues/1",
                "// see https://github.com/facebook/react/issues/1 again",
            ]),
            "src/app.py": "\n".join([
                "# %s requests>=2.32" % M,
                "# %s django>=5" % M,
                "# %s 2026-01-01" % A,
                "# %s 2027-01-01" % A,
                "# %s https://github.com/foo/bar/pull/9" % M,
                "# %s https://github.com/foo/bar/issues/10" % M,
                "# %s leftpad>=1" % M,
            ]),
            "README.md": "# %s react>=1\nhttps://github.com/x/y/issues/1\n" % M,
            "node_modules/junk/index.js": "// %s react>=1\n" % M,
        }
        table = {
            ("facebook", "react", "1"): {"state": "open", "title": "still broken"},
            ("foo", "bar", "9"): {"state": "closed", "pull_request": {"merged_at": "2026-08-01T00:00:00Z"}},
            ("foo", "bar", "10"): {"state": "closed", "state_reason": "not_planned"},
        }
        fetch = fake_fetch(table)
        with Project(files) as p:
            got = {(f.file, f.line): f.status for f in p.run(fetch=fetch)}

        self.assertEqual(got, {
            ("src/app.js", 1): cli.YES,
            ("src/app.js", 2): cli.NO,
            ("src/app.js", 3): cli.NO,
            ("src/app.js", 4): cli.NO,
            ("src/app.py", 1): cli.NO,
            ("src/app.py", 2): cli.YES,
            ("src/app.py", 3): cli.YES,
            ("src/app.py", 4): cli.NO,
            ("src/app.py", 5): cli.YES,
            ("src/app.py", 6): cli.WONTFIX,
            ("src/app.py", 7): cli.UNKNOWN,
        })
        # each unique issue is fetched once
        self.assertEqual(len(fetch.calls), len(set(fetch.calls)))
        self.assertEqual(len(fetch.calls), 3)

    def test_all_conditions_must_hold(self):
        files = {"requirements.txt": "requests==2.32.3\n",
                 "a.py": "# %s requests>=2.32, 2030-01-01\n# %s requests>=2.32, 2020-01-01\n" % (M, M)}
        with Project(files) as p:
            got = [f.status for f in sorted(p.run(), key=lambda f: f.line)]
        self.assertEqual(got, [cli.NO, cli.YES])

    def test_uv_lock(self):
        files = {"uv.lock": 'version = 1\n\n[[package]]\nname = "pydantic"\nversion = "2.9.0"\n',
                 "a.py": "# %s pydantic>=2\n" % M}
        with Project(files) as p:
            self.assertEqual(p.run()[0].status, cli.YES)

    def test_docs_opt_in(self):
        files = {"README.md": "# %s 2020-01-01\n" % A}
        with Project(files) as p:
            self.assertEqual(p.run(), [])
            self.assertEqual(len(p.run(include_docs=True)), 1)

    def test_cli_check_exit_code(self):
        with Project({"a.py": "# %s 2020-01-01\n" % A}) as p:
            self.assertEqual(cli.main(["-C", p.dir.name, "--offline", "--no-color", "--check"]), 1)
        with Project({"a.py": "# %s 2999-01-01\n" % A}) as p:
            self.assertEqual(cli.main(["-C", p.dir.name, "--offline", "--no-color", "--check"]), 0)
        with Project({"a.py": "# see https://github.com/a/b/issues/1\n"}) as p:
            self.assertEqual(cli.main(["-C", p.dir.name, "--offline", "--check"]), 0)
            self.assertEqual(cli.main(["-C", p.dir.name, "--offline", "--check", "--strict"]), 1)

    def test_render_and_markdown(self):
        with Project({"a.py": "# %s 2020-01-01\n# %s 2999-01-01\n" % (A, A)}) as p:
            findings = p.run()
        text = cli.render(findings)
        self.assertIn("DELETE IT", text)
        self.assertIn("1 not-yet tripwires hidden", text)
        self.assertIn("NOT YET", cli.render(findings, show_all=True))
        self.assertIn("| a.py:1", cli.to_markdown(findings).replace("`", ""))


if __name__ == "__main__":
    unittest.main()
