#!/usr/bin/env python3
"""docscheck: the documentation gate (card 127), the structural rules every push and every release must pass,
checked offline against the tree. Ported from appshapes/brigade's internal/docscheck (card 110) to the standard
library, because this repository has no Go.

The documentation is one tree for humans and one for agents. Humans enter at README.md, which names three
personas; each persona root names its topics; each topic root names its actions with a TL;DR and a Details link;
the leaves hold the details. Agents enter at CLAUDE.md, whose @imports load the rule files under
docs/agent/repository/. Nothing here reaches the network, so a site going down is never a red build.

usage: python3 scripts/ci/docscheck.py check       (make docs-check: one finding per line, then the summary; exit 1 on any)
       python3 scripts/ci/docscheck.py generate    (make docs-generate: rewrite the generated reference page)

tests/test_docscheck.py runs `run` against the repository and against a copy with each violation planted, inside
`make test`, so `make push`, CI and the release sequence all run the gate.
"""
import json
import os
import re
import sys

# The files and directories the gate knows by name, relative to the root.
README_FILE = "README.md"
AGENTS_FILE = "AGENTS.md"
CLAUDE_FILE = "CLAUDE.md"
CHANGELOG_FILE = "CHANGELOG.md"
SECURITY_FILE = "SECURITY.md"
MAKEFILE_FILE = "Makefile"
PLUGIN_MANIFEST = "plugin/.claude-plugin/plugin.json"
PACKAGE_PAGE = "plugin/README.md"
SKILLS_DIR = "plugin/skills"
DOCS_DIR = "docs"
RULES_DIR = "docs/agent/repository"
SKILLS_PAGE = "docs/agent/in-a-session/skills.md"
OPTIONS_PAGE = "docs/user/configure/options.md"
MAKE_TARGETS_PAGE = "docs/developer/reference/make-targets.md"

# IF_YOU_WANT_TO is the heading of the navigation table every persona root and topic root carries.
IF_YOU_WANT_TO = "If you want to"
# DETAILS_PREFIX starts the line of an action section that names its leaf.
DETAILS_PREFIX = "Details:"
# MAX_OVERVIEW_SENTENCES bounds a persona root's topic section.
MAX_OVERVIEW_SENTENCES = 2
# MAX_ACTION_LINES bounds a topic root's action section: a TL;DR, not the page.
MAX_ACTION_LINES = 20
# PRE_RELEASE_VERSION is the pin of a tree that has not been released.
PRE_RELEASE_VERSION = "0.0.0"

# PERSONAS is the order README.md lists them in: (directory under docs/, the H1 of its root page).
PERSONAS = [("user", "User"), ("developer", "Developer"), ("agent", "AI Agent")]

# REFERENCE_DIRS are directories under a persona that hold generated or reference pages rather than a topic: no
# README.md, no navigation table.
REFERENCE_DIRS = {"docs/developer/reference"}

# ROOT_PAGES are the pages outside docs/ the gate reads: every relative link in them must resolve.
ROOT_PAGES = [README_FILE, AGENTS_FILE, CLAUDE_FILE, CHANGELOG_FILE, SECURITY_FILE, PACKAGE_PAGE]

# OPTION_PAGES are the pages that must name every plugin option: the options page of the tree and the listing.
OPTION_PAGES = [OPTIONS_PAGE, PACKAGE_PAGE]

FENCE_RE = re.compile(r"^\s*(```|~~~)")
CODE_RE = re.compile(r"`[^`\n]*`")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
REF_DEF_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
IMPORT_RE = re.compile(r"(?:^|\s)@([A-Za-z0-9_./-]+)")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|(\s*:?-+:?\s*\|)+\s*$")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
TARGET_RE = re.compile(r"^([A-Za-z0-9_.-]+):.*##\s*(.*)$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


class Finding:
    """One rule the tree breaks."""

    def __init__(self, check, path, message):
        self.check = check  # readme, persona, topic, links, reach, skills, agent, options, make, changelog
        self.path = path  # the file the finding is about, relative to the root
        self.message = message

    def __str__(self):
        return "%s: %s: %s" % (self.check, self.path, self.message)

    def __repr__(self):
        return "Finding(%r, %r, %r)" % (self.check, self.path, self.message)


class Summary:
    """What a passing run counted."""

    def __init__(self):
        self.pages = 0
        self.links = 0
        self.skills = 0
        self.targets = 0

    def __str__(self):
        return "%d pages, %d links, %d skills, %d make targets" % (self.pages, self.links, self.skills, self.targets)


# ---------------------------------------------------------------------------
# the markdown model


class Heading:
    def __init__(self, level, text, slug, line):
        self.level = level
        self.text = text
        self.slug = slug
        self.line = line  # 0-based


class Link:
    def __init__(self, target, line):
        self.target = target
        self.line = line


class Section:
    """A level-2 heading with the line range of its body: [start, end) in line numbers, the heading line excluded."""

    def __init__(self, heading, start, end):
        self.heading = heading
        self.text = heading.text
        self.slug = heading.slug
        self.start = start
        self.end = end


def github_slug(title):
    """GitHub's heading anchor: lowercased, punctuation dropped, spaces to hyphens."""
    out = []
    for ch in title.strip().lower():
        if ch.isalnum() or ch in "_-":
            out.append(ch)
        elif ch == " ":
            out.append("-")
    return "".join(out)


def canon(s):
    """The looser comparison that survives slug dialects: letters and digits only."""
    return "".join(ch for ch in s.lower() if ch.isalnum())


def _link_text(match):
    s = match.group(0)
    return s[s.index("[") + 1 : s.index("]")]


class Doc:
    def __init__(self, rel, data):
        self.rel = rel
        self.raw = data.replace("\r\n", "\n").split("\n")  # every line as written
        self.text = [""] * len(self.raw)  # fenced blocks blanked, inline code removed
        self.headings = []
        self.links = []
        in_fence = False
        slugs = {}
        for i, line in enumerate(self.raw):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            m = HEADING_RE.match(line)
            if m:
                title = m.group(2).replace("`", "")
                title = LINK_RE.sub(_link_text, title)
                slug = github_slug(title)
                if slug in slugs:
                    n = slugs[slug]
                    slugs[slug] = n + 1
                    slug = "%s-%d" % (slug, n)
                else:
                    slugs[slug] = 1
                self.headings.append(Heading(len(m.group(1)), title, slug, i))
            stripped = CODE_RE.sub("", line)
            self.text[i] = stripped
            for lm in LINK_RE.finditer(stripped):
                self.links.append(Link(lm.group(1), i))
            rm = REF_DEF_RE.match(stripped)
            if rm:
                self.links.append(Link(rm.group(1), i))

    def has_anchor(self, anchor):
        anchor = anchor.lower()
        return any(h.slug == anchor or canon(h.slug) == canon(anchor) for h in self.headings)

    def h1(self):
        for h in self.headings:
            if h.level == 1:
                return h
        return None

    def sections(self):
        out = []
        for i, h in enumerate(self.headings):
            if h.level != 2:
                continue
            end = len(self.raw)
            for n in self.headings[i + 1 :]:
                if n.level <= 2:
                    end = n.line
                    break
            out.append(Section(h, h.line + 1, end))
        return out

    def section(self, title):
        for s in self.sections():
            if canon(s.text) == canon(title):
                return s
        return None

    def body_links(self, start, end):
        return [l for l in self.links if start <= l.line < end]

    def table_rows(self, start, end):
        """The link targets of each data row of the first table in [start, end), one list per row, and whether a
        table was found."""
        rows = []
        seen = False
        for i in range(start, end):
            line = self.text[i]
            if not TABLE_RE.match(line):
                if seen:
                    break
                continue
            if not seen:
                seen = True
                continue  # the header row
            if TABLE_SEP_RE.match(line):
                continue
            rows.append([m.group(1) for m in LINK_RE.finditer(line)])
        return rows, seen

    def list_items(self, start, end):
        """The link targets of each list item in [start, end)."""
        items = []
        for i in range(start, end):
            line = self.text[i]
            if LIST_RE.match(line):
                items.append([m.group(1) for m in LINK_RE.finditer(line)])
        return items

    def sentences(self, start, end):
        """The sentences in [start, end): terminators followed by a space or the end of a line, link targets and
        code removed, a few abbreviations tolerated."""
        text = "\n".join(LINK_RE.sub(_link_text, self.text[i]) for i in range(start, end)) + "\n"
        for abbr in ("e.g.", "i.e.", "etc.", "vs."):
            text = text.replace(abbr, abbr.replace(".", ""))
        n = 0
        for i, ch in enumerate(text):
            if ch not in ".!?":
                continue
            if i + 1 == len(text) or text[i + 1].isspace() or text[i + 1] in ')"':
                n += 1
        return n

    def content_lines(self, start, end):
        """The non-blank lines in [start, end)."""
        return sum(1 for i in range(start, end) if self.raw[i].strip())


def resolve(rel, target):
    """Turn a link target seen in rel into a slash path relative to the root and an anchor; the third value is
    False for an external target."""
    if SCHEME_RE.match(target) or target.startswith("<") or target.startswith("//"):
        return "", "", False
    p, _, anchor = target.partition("#")
    if p == "":
        return rel, anchor, True
    if p.startswith("/"):
        return os.path.normpath(p.lstrip("/")).replace(os.sep, "/"), anchor, True
    return os.path.normpath(os.path.join(os.path.dirname(rel), p)).replace(os.sep, "/"), anchor, True


def imports(line):
    """The @path imports on one code-stripped line of CLAUDE.md: a token beginning with @ that names a path (it
    contains a slash or ends in .md), so an @handle or an address is never one."""
    return [m.group(1) for m in IMPORT_RE.finditer(line) if "/" in m.group(1) or m.group(1).endswith(".md")]


# ---------------------------------------------------------------------------
# the checker


class Checker:
    def __init__(self, root):
        self.root = root
        self.docs = {}  # every markdown file the gate reads, by slash path
        self.findings = []
        self.sum = Summary()

    def find(self, check, rel, message):
        self.findings.append(Finding(check, rel, message))

    def abs(self, rel):
        return os.path.join(self.root, *rel.split("/"))

    def exists(self, rel):
        return os.path.exists(self.abs(rel))

    def is_file(self, rel):
        return os.path.isfile(self.abs(rel))

    def is_dir(self, rel):
        return os.path.isdir(self.abs(rel))

    def read(self, rel):
        with open(self.abs(rel), encoding="utf-8") as f:
            return f.read()

    def load_doc(self, rel):
        if rel not in self.docs:
            self.docs[rel] = Doc(rel, self.read(rel))
        return self.docs[rel]

    def load(self):
        """Read every markdown file the gate checks: the root pages, the listing and docs/."""
        for rel in ROOT_PAGES:
            self.load_doc(rel)
        for dirpath, dirnames, filenames in os.walk(self.abs(DOCS_DIR)):
            dirnames.sort()
            for name in sorted(filenames):
                if name.endswith(".md"):
                    rel = os.path.relpath(os.path.join(dirpath, name), self.root).replace(os.sep, "/")
                    self.load_doc(rel)
        self.sum.pages = len(self.docs)

    def subdirs(self, rel):
        try:
            return sorted(e for e in os.listdir(self.abs(rel)) if self.is_dir(rel + "/" + e))
        except OSError:
            return []

    def leaves(self, rel):
        """The .md files beside a README in the directory rel, sorted."""
        try:
            return sorted(e for e in os.listdir(self.abs(rel)) if e.endswith(".md") and e != "README.md" and self.is_file(rel + "/" + e))
        except OSError:
            return []

    # --- 1. readme ------------------------------------------------------------

    def readme(self):
        d = self.docs[README_FILE]
        if d.h1() is None or d.headings[0].level != 1:
            self.find("readme", README_FILE, "the first heading must be the H1 title")
        for h in d.headings:
            if h.level > 2:
                self.find("readme", README_FILE, "line %d: README.md has no headings below H2; %r belongs on a persona page" % (h.line + 1, h.text))
        h2 = d.sections()
        if len(h2) != 1:
            self.find("readme", README_FILE, "README.md must have exactly one H2 section, the personas; it has %d" % len(h2))
            return
        got = []
        for item in d.list_items(h2[0].start, h2[0].end):
            if len(item) != 1:
                self.find("readme", README_FILE, "each persona item carries exactly one link, to the persona's root page; one carries %d" % len(item))
                continue
            got.append(resolve(README_FILE, item[0])[0])
        want = ["%s/%s/README.md" % (DOCS_DIR, p[0]) for p in PERSONAS]
        if got != want:
            self.find("readme", README_FILE, "the %r section must list exactly the %d persona roots in order %s; it lists %s" % (h2[0].text, len(PERSONAS), want, got))

    # --- 2. persona and topic roots ---------------------------------------------

    def personas(self):
        for pdir, title in PERSONAS:
            directory = "%s/%s" % (DOCS_DIR, pdir)
            rel = directory + "/README.md"
            d = self.docs.get(rel)
            if d is None:
                self.find("persona", rel, "the %s root page is missing" % title)
                continue
            h = d.h1()
            if h is None or canon(h.text) != canon(title):
                self.find("persona", rel, "the H1 must be %r" % title)
            topic_dirs = []
            for t in self.subdirs(directory):
                tdir = directory + "/" + t
                troot = tdir + "/README.md"
                if tdir in REFERENCE_DIRS:
                    continue
                if not self.is_file(troot):
                    self.find("persona", troot, "every topic directory has a README.md (the topic root); add it, or register %s as a reference directory" % tdir)
                    continue
                topic_dirs.append(t)
                self.topic(pdir, t, troot)
            # The navigation table.
            nav = d.section(IF_YOU_WANT_TO)
            if nav is None:
                self.find("persona", rel, "a persona root has an %r table" % ("## " + IF_YOU_WANT_TO))
            else:
                rows, found = d.table_rows(nav.start, nav.end)
                if not found:
                    self.find("persona", rel, "the %r section holds a table" % IF_YOU_WANT_TO)
                linked = set()
                for row in rows:
                    if not row:
                        self.find("persona", rel, "every %r row links to a topic root" % IF_YOU_WANT_TO)
                        continue
                    for t in row:
                        dest, _, internal = resolve(rel, t)
                        if not internal:
                            continue
                        topic = os.path.basename(os.path.dirname(dest))
                        if os.path.dirname(os.path.dirname(dest)) != directory or os.path.basename(dest) != "README.md" or topic not in topic_dirs:
                            self.find("persona", rel, "row of %r: %s is not one of this persona's topic roots" % (IF_YOU_WANT_TO, t))
                            continue
                        linked.add(topic)
                for t in topic_dirs:
                    if t not in linked:
                        self.find("persona", rel, "the %r table has no row for the topic %s/" % (IF_YOU_WANT_TO, t))
            # One section per topic, two sentences at most, linking to the topic root.
            sectioned = set()
            for s in d.sections():
                if canon(s.text) == canon(IF_YOU_WANT_TO):
                    continue
                topic = ""
                for l in d.body_links(s.start, s.end):
                    dest, _, internal = resolve(rel, l.target)
                    if not internal:
                        continue
                    t = os.path.basename(os.path.dirname(dest))
                    if os.path.dirname(os.path.dirname(dest)) == directory and os.path.basename(dest) == "README.md" and t in topic_dirs:
                        topic = t
                        break
                if topic == "":
                    self.find("persona", rel, "section %r links to no topic root of this persona; a persona root has only the %r table and one section per topic" % (s.text, IF_YOU_WANT_TO))
                    continue
                if topic in sectioned:
                    self.find("persona", rel, "section %r: the topic %s/ already has a section" % (s.text, topic))
                sectioned.add(topic)
                n = d.sentences(s.start, s.end)
                if n > MAX_OVERVIEW_SENTENCES:
                    self.find("persona", rel, "section %r has %d sentences; a topic overview has at most %d, the details belong on the topic root" % (s.text, n, MAX_OVERVIEW_SENTENCES))
            for t in topic_dirs:
                if t not in sectioned:
                    self.find("persona", rel, "the topic %s/ has no section on the persona root" % t)

    def topic(self, persona, name, rel):
        d = self.docs.get(rel)
        if d is None:
            return
        directory = os.path.dirname(rel)
        if d.h1() is None:
            self.find("topic", rel, "a topic root starts with an H1")
        nav = d.section(IF_YOU_WANT_TO)
        if nav is None:
            self.find("topic", rel, "a topic root has an %r table" % ("## " + IF_YOU_WANT_TO))
        # Actions: every H2 but the table.
        actions = []  # (section, details targets)
        for s in d.sections():
            if canon(s.text) == canon(IF_YOU_WANT_TO):
                continue
            details = []
            for i in range(s.start, s.end):
                if d.text[i].strip().startswith(DETAILS_PREFIX):
                    found = [m.group(1) for m in LINK_RE.finditer(d.text[i])]
                    details.extend(found)
                    if not found:
                        self.find("topic", rel, "section %r: the %s line carries no link" % (s.text, DETAILS_PREFIX))
            if not details:
                self.find("topic", rel, "section %r has no %r line linking to its detail page" % (s.text, DETAILS_PREFIX))
            n = d.content_lines(s.start, s.end)
            if n > MAX_ACTION_LINES:
                self.find("topic", rel, "section %r is %d lines; an action section is a TL;DR of at most %d, the rest belongs on its detail page" % (s.text, n, MAX_ACTION_LINES))
            actions.append((s, details))
        if not actions:
            self.find("topic", rel, "a topic root has at least one action section")
        # The table's rows name the actions by anchor.
        if nav is not None:
            rows, found = d.table_rows(nav.start, nav.end)
            if not found:
                self.find("topic", rel, "the %r section holds a table" % IF_YOU_WANT_TO)
            named = set()
            for row in rows:
                if not row:
                    self.find("topic", rel, "every %r row links to an action section of this page" % IF_YOU_WANT_TO)
                    continue
                for t in row:
                    dest, anchor, internal = resolve(rel, t)
                    if not internal:
                        continue
                    if dest != rel or anchor == "":
                        self.find("topic", rel, "%r row %s: a topic root's table links to its own action sections (#anchor), not elsewhere" % (IF_YOU_WANT_TO, t))
                        continue
                    hit = False
                    for s, _ in actions:
                        if s.slug == anchor.lower() or canon(s.slug) == canon(anchor):
                            named.add(s.slug)
                            hit = True
                    if not hit:
                        self.find("topic", rel, "%r row %s names no action section of this page" % (IF_YOU_WANT_TO, t))
            for s, _ in actions:
                if s.slug not in named:
                    self.find("topic", rel, "action %r has no row in the %r table" % (s.text, IF_YOU_WANT_TO))
        # No orphan leaf: every page in the directory is a Details target.
        linked = set()
        for _, details in actions:
            for t in details:
                dest, _, internal = resolve(rel, t)
                if internal:
                    linked.add(dest)
        for leaf in self.leaves(directory):
            if directory + "/" + leaf not in linked:
                self.find("topic", rel, "%s is a leaf no %s line of this topic root names (persona %s, topic %s)" % (leaf, DETAILS_PREFIX, persona, name))

    # --- 3. links ----------------------------------------------------------------

    def links(self):
        for rel in sorted(self.docs):
            d = self.docs[rel]
            for l in d.links:
                dest, anchor, internal = resolve(rel, l.target)
                if not internal:
                    continue
                self.sum.links += 1
                if not self.exists(dest):
                    self.find("links", rel, "line %d: %s does not exist" % (l.line + 1, l.target))
                    continue
                if anchor == "":
                    continue
                if not dest.endswith(".md"):
                    self.find("links", rel, "line %d: %s: an anchor on a page that is not markdown" % (l.line + 1, l.target))
                    continue
                try:
                    target = self.load_doc(dest)
                except OSError as e:
                    self.find("links", rel, "line %d: %s: %s" % (l.line + 1, l.target, e))
                    continue
                if not target.has_anchor(anchor):
                    self.find("links", rel, "line %d: %s: no heading in %s matches #%s" % (l.line + 1, l.target, dest, anchor))
        # CLAUDE.md's imports.
        for i, line in enumerate(self.docs[CLAUDE_FILE].text):
            for target in imports(line):
                if target == "./CLAUDE.user.md":
                    continue  # local-only, gitignored, absent in a fresh clone by design
                dest = resolve(CLAUDE_FILE, target)[0]
                if not self.is_file(dest):
                    self.find("links", CLAUDE_FILE, "line %d: the import @%s names no file" % (i + 1, target))

    # --- 4. reach ----------------------------------------------------------------

    def reach(self):
        seen = {README_FILE}
        queue = [README_FILE]
        while queue:
            rel = queue.pop(0)
            try:
                d = self.load_doc(rel)
            except OSError:
                continue
            for l in d.links:
                dest, _, internal = resolve(rel, l.target)
                if not internal or dest in seen or not dest.endswith(".md") or not self.is_file(dest):
                    continue
                seen.add(dest)
                queue.append(dest)
        for rel in sorted(self.docs):
            if rel.startswith(DOCS_DIR + "/") and rel not in seen:
                self.find("reach", rel, "no chain of links from README.md reaches this page; link it from a topic root or an index")

    # --- 5. skills ---------------------------------------------------------------

    def skills(self):
        """Every skill the plugin ships is named by path on the agent's skills page."""
        page = self.docs.get(SKILLS_PAGE)
        if page is None:
            self.find("skills", SKILLS_PAGE, "the skills page is missing")
            return
        text = "\n".join(page.raw)
        for name in self.subdirs(SKILLS_DIR):
            skill = "%s/%s/SKILL.md" % (SKILLS_DIR, name)
            if not self.is_file(skill):
                continue
            self.sum.skills += 1
            if skill not in text:
                self.find("skills", SKILLS_PAGE, "the skill %s is not named on the skills page" % skill)

    # --- 6. agent ------------------------------------------------------------------

    def agent(self):
        imported = set()
        for line in self.docs[CLAUDE_FILE].text:
            for target in imports(line):
                imported.add(resolve(CLAUDE_FILE, target)[0])
        linked = set()
        for l in self.docs[AGENTS_FILE].links:
            dest, _, internal = resolve(AGENTS_FILE, l.target)
            if internal:
                linked.add(dest)
        if not self.is_dir(RULES_DIR):
            self.find("agent", RULES_DIR, "the rule files are missing")
            return
        for leaf in self.leaves(RULES_DIR):
            rel = RULES_DIR + "/" + leaf
            if rel not in imported:
                self.find("agent", CLAUDE_FILE, "the rule file %s is not imported (@%s)" % (rel, rel))
            if rel not in linked:
                self.find("agent", AGENTS_FILE, "the rule file %s is not linked" % rel)

    # --- 7. options ----------------------------------------------------------------

    def options(self):
        try:
            manifest = json.loads(self.read(PLUGIN_MANIFEST))
        except (OSError, ValueError) as e:
            self.find("options", PLUGIN_MANIFEST, str(e))
            return
        keys = sorted((manifest.get("userConfig") or {}).keys())
        for rel in OPTION_PAGES:
            page = self.docs.get(rel)
            if page is None:
                self.find("options", rel, "the page is missing")
                continue
            text = "\n".join(page.raw)
            for k in keys:
                if "`%s`" % k not in text:
                    self.find("options", rel, "the option `%s` of %s is not documented" % (k, PLUGIN_MANIFEST))

    # --- 8. make targets -------------------------------------------------------------

    def make_targets(self):
        try:
            want, n = generate_make_targets(self.root)
        except OSError as e:
            self.find("make", MAKEFILE_FILE, str(e))
            return
        self.sum.targets = n
        try:
            got = self.read(MAKE_TARGETS_PAGE)
        except OSError:
            self.find("make", MAKE_TARGETS_PAGE, "the generated reference is missing; run `make docs-generate`")
            return
        if got.rstrip("\n") != want.rstrip("\n"):
            self.find("make", MAKE_TARGETS_PAGE, "stale against the Makefile's help lines; run `make docs-generate` and commit the result")

    # --- 9. changelog -----------------------------------------------------------------

    def changelog(self):
        try:
            manifest = json.loads(self.read(PLUGIN_MANIFEST))
        except (OSError, ValueError) as e:
            self.find("changelog", PLUGIN_MANIFEST, str(e))
            return
        v = str(manifest.get("version") or "").strip()
        if v in ("", PRE_RELEASE_VERSION):
            return
        if not VERSION_RE.match(v):
            self.find("changelog", PLUGIN_MANIFEST, "%r is not a version" % v)
            return
        for h in self.docs[CHANGELOG_FILE].headings:
            if h.level == 2 and h.text.startswith("[" + v + "]"):
                return
        self.find("changelog", CHANGELOG_FILE, "no `## [%s]` section for the version %s pins; a release ships with its changelog section" % (v, PLUGIN_MANIFEST))


def generate_make_targets(root):
    """The make-target reference page from the Makefile's `target: ## help` lines, in Makefile order, and the
    number of targets."""
    with open(os.path.join(root, MAKEFILE_FILE), encoding="utf-8") as f:
        data = f.read()
    out = [
        "# make targets\n\n",
        "Every target with a help line, in the Makefile's order; `make help` prints the same list. Generated by\n",
        "`make docs-generate` from the Makefile, and `make docs-check` fails when this page is stale, so edit the\n",
        "Makefile's `##` comment, never this page. A trailing ` (CI)` marks a target a workflow step runs.\n\n",
        "| Target | What it does |\n| --- | --- |\n",
    ]
    n = 0
    for line in data.split("\n"):
        m = TARGET_RE.match(line)
        if m is None:
            continue
        n += 1
        out.append("| `%s` | %s |\n" % (m.group(1), m.group(2).strip().replace("|", "\\|")))
    return "".join(out), n


def run(root):
    """Check the repository at root and return (findings, summary). An OSError is a tree the gate cannot read at
    all (no README.md), not a finding."""
    c = Checker(root)
    c.load()
    c.readme()
    c.personas()
    c.links()
    c.reach()
    c.skills()
    c.agent()
    c.options()
    c.make_targets()
    c.changelog()
    c.findings.sort(key=lambda f: (f.check, f.path))
    return c.findings, c.sum


def check(root):
    """Run the gate and format the result as the lines a person reads: one finding per line, then the summary.
    Returns (text, ok)."""
    findings, summary = run(root)
    lines = ["docs-check: %s\n" % f for f in findings]
    if findings:
        lines.append("docs-check: %s, %d finding(s)\n" % (summary, len(findings)))
        return "".join(lines), False
    lines.append("docs-check: %s, ok\n" % summary)
    return "".join(lines), True


def main(argv=None, stdout=None, stderr=None):
    argv = sys.argv[1:] if argv is None else argv
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    root = os.getcwd()
    if len(argv) != 1 or argv[0] not in ("check", "generate"):
        stderr.write("usage: docscheck.py check | generate\n")
        return 2
    try:
        if argv[0] == "check":
            text, ok = check(root)
            stdout.write(text)
            return 0 if ok else 1
        page, n = generate_make_targets(root)
        target = os.path.join(root, *MAKE_TARGETS_PAGE.split("/"))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(page)
        stdout.write("docscheck: wrote %s (%d targets)\n" % (MAKE_TARGETS_PAGE, n))
        return 0
    except OSError as e:
        stderr.write("docscheck failed (internal): %s\n" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
