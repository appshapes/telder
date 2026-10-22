"""The documentation gate (card 127). scripts/ci/docscheck.py holds the rules; this file is what proves each of
them can FAIL, which is the only property a check really has: the gate runs against the repository itself (and
must pass), and against a copy of the tree with one violation planted at a time (and must name it). `make test`
runs both, so the gate bites in `make push`, in CI and in the release sequence before anything is tagged."""
import importlib.machinery
import importlib.util
import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SCRIPT = os.path.join(REPO, "scripts", "ci", "docscheck.py")


def load_script():
    loader = importlib.machinery.SourceFileLoader("docscheck", SCRIPT)
    spec = importlib.util.spec_from_loader("docscheck", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


docscheck = load_script()

# The parts of the repository the copy leaves out: the git directory, caches and scratch. Everything the gate reads
# or a link names is in it.
SKIP = shutil.ignore_patterns(".git", ".ignored", "__pycache__", ".pytest_cache", ".ruff_cache", ".playwright-cli", "worktrees", ".DS_Store")


def read(root, rel):
    with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as f:
        return f.read()


def write(root, rel, body):
    path = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)


def replace(root, rel, old, new):
    """Rewrite the first occurrence of old in rel, and fail loudly when old is absent: a mutation that changed
    nothing would make the failure test vacuous."""
    text = read(root, rel)
    if old not in text:
        raise AssertionError("the mutation's target %r is not in %s, so the mutation would prove nothing" % (old, rel))
    write(root, rel, text.replace(old, new, 1))


def append(root, rel, text):
    write(root, rel, read(root, rel) + text)


def pin_version(root, version):
    manifest = read(root, docscheck.PLUGIN_MANIFEST)
    new = re.sub(r'^(\s*"version":\s*)"[^"]+"', r'\1"%s"' % version, manifest, count=1, flags=re.M)
    if new == manifest:
        raise AssertionError("the manifest's version line was not found")
    write(root, docscheck.PLUGIN_MANIFEST, new)


MUTATIONS = [
    ("readme: a persona dropped from the list", "readme",
     lambda root: replace(root, docscheck.README_FILE, "- **[Developer](docs/developer/README.md)**", "- **Developer**")),
    ("readme: a second H2", "readme",
     lambda root: append(root, docscheck.README_FILE, "\n## Install\n\nType `/plugin install telder@telder`.\n")),
    ("persona: a topic overview of three sentences", "persona",
     lambda root: replace(root, "docs/user/README.md", "## Install\n\n", "## Install\n\nOne sentence more. ")),
    ("persona: a topic with no section", "persona",
     lambda root: (write(root, "docs/user/extra/README.md", "# Extra\n\n## If you want to\n\n| If you want to | Go to |\n| --- | --- |\n| do it | [Do it](#do-it) |\n\n## Do it\n\n1. Done.\n\nDetails: [Do it](do-it.md).\n"),
                   write(root, "docs/user/extra/do-it.md", "# Do it\n\nDone.\n"))),
    ("topic: an action with no Details line", "topic",
     lambda root: replace(root, "docs/user/install/README.md", "Details: [Install the plugin](install.md).", "See the page.")),
    ("topic: an orphan leaf", "topic",
     lambda root: write(root, "docs/user/install/stray.md", "# Stray\n\nNobody names this page.\n")),
    ("topic: an action over twenty lines", "topic",
     lambda root: replace(root, "docs/user/install/README.md", "## Install the plugin\n", "## Install the plugin\n" + "- one more line of detail that belongs on the leaf\n" * 21)),
    ("links: a missing page", "links",
     lambda root: append(root, "docs/user/install/install.md", "\nSee [nowhere](nowhere.md).\n")),
    ("links: a missing anchor", "links",
     lambda root: append(root, "docs/user/install/install.md", "\nSee [a section](uninstall.md#no-such-heading).\n")),
    ("links: a CLAUDE.md import that names no file", "links",
     lambda root: append(root, docscheck.CLAUDE_FILE, "\n@docs/agent/repository/missing.md\n")),
    ("reach: a page nothing links", "reach",
     lambda root: write(root, "docs/lost.md", "# Lost\n\nNo chain of links reaches this page.\n")),
    ("skills: a skill missing from the skills page", "skills",
     lambda root: write(root, "plugin/skills/extra/SKILL.md", "---\nname: extra\n---\n")),
    ("agent: a rule file CLAUDE.md does not import", "agent",
     lambda root: replace(root, docscheck.CLAUDE_FILE, "@docs/agent/repository/gates.md\n", "")),
    ("options: an option with no row", "options",
     lambda root: replace(root, docscheck.PLUGIN_MANIFEST, '"userConfig": {', '"userConfig": {\n    "brand_new_option": {"type": "string", "description": "undocumented"},')),
    ("make: a stale make-targets page", "make",
     lambda root: append(root, docscheck.MAKE_TARGETS_PAGE, "| `imaginary` | a target the Makefile does not have |\n")),
    ("changelog: a pinned version with no section", "changelog",
     lambda root: pin_version(root, "9.9.9")),
]


class DocsGate(unittest.TestCase):
    def copy_tree(self):
        dst = tempfile.mkdtemp(prefix="telder-docs-")
        self.addCleanup(shutil.rmtree, dst, True)
        shutil.copytree(REPO, dst, ignore=SKIP, dirs_exist_ok=True)
        return dst

    def test_passes_on_the_repository(self):
        """The gate as CI runs it."""
        findings, summary = docscheck.run(REPO)
        self.assertEqual([], [str(f) for f in findings])
        self.assertGreater(summary.pages, 0)
        self.assertGreater(summary.links, 0)
        self.assertGreaterEqual(summary.skills, 2)
        self.assertGreater(summary.targets, 0)

    def test_passes_on_an_unmutated_copy(self):
        """The positive control: the same code path on an untouched copy, and silence."""
        root = self.copy_tree()
        findings, _ = docscheck.run(root)
        self.assertEqual([], [str(f) for f in findings])

    def test_fails_on_planted_violations(self):
        """Every check can fail, one planted violation at a time, and the finding names the check it belongs to."""
        checks = set()
        for name, check, mutate in MUTATIONS:
            with self.subTest(name):
                root = self.copy_tree()
                mutate(root)
                findings, _ = docscheck.run(root)
                self.assertTrue(findings, "the mutation changed nothing the gate can see, so the check %r is vacuous" % check)
                self.assertIn(check, {f.check for f in findings}, "the gate reported %r, none of them under the check %r" % ([str(f) for f in findings], check))
                checks.add(check)
        self.assertEqual({"readme", "persona", "topic", "links", "reach", "skills", "agent", "options", "make", "changelog"}, checks)

    def test_output_shape(self):
        """`docscheck.py check` prints one finding per line and a summary line, and exits 1."""
        root = self.copy_tree()
        write(root, "docs/lost.md", "# Lost\n")
        text, ok = docscheck.check(root)
        self.assertFalse(ok)
        self.assertIn("docs-check: reach: docs/lost.md:", text)
        self.assertIn("finding(s)", text)
        cwd = os.getcwd()
        os.chdir(root)
        try:
            out, err = io.StringIO(), io.StringIO()
            self.assertEqual(1, docscheck.main(["check"], out, err))
            self.assertIn("docs-check: reach: docs/lost.md:", out.getvalue())
            self.assertEqual(2, docscheck.main(["bogus"], out, err))
        finally:
            os.chdir(cwd)

    def test_generate_writes_the_page_the_check_expects(self):
        root = self.copy_tree()
        os.remove(os.path.join(root, *docscheck.MAKE_TARGETS_PAGE.split("/")))
        findings, _ = docscheck.run(root)
        self.assertIn("make", {f.check for f in findings})
        cwd = os.getcwd()
        os.chdir(root)
        try:
            out = io.StringIO()
            self.assertEqual(0, docscheck.main(["generate"], out, io.StringIO()))
            self.assertIn("docscheck: wrote " + docscheck.MAKE_TARGETS_PAGE, out.getvalue())
        finally:
            os.chdir(cwd)
        findings, _ = docscheck.run(root)
        self.assertNotIn("make", {f.check for f in findings})
        page = read(root, docscheck.MAKE_TARGETS_PAGE)
        self.assertIn("| `test` |", page)
        self.assertIn("| `docs-check` |", page)

    def test_the_manifest_is_the_pin_the_changelog_rule_reads(self):
        version = json.loads(read(REPO, docscheck.PLUGIN_MANIFEST))["version"]
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        self.assertIn("## [%s]" % version, read(REPO, docscheck.CHANGELOG_FILE))


if __name__ == "__main__":
    unittest.main()
