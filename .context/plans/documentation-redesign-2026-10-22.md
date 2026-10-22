# Documentation redesign: three personas and a release gate (card 127) — 2026-10-22

Card 127 on the AppShapes Trello board (`127: ...` commits). Asked by Rjae: "Review card 127. Then review the
documentation re-architecting that we did with card 110 (see `../brigade/`). When you have enough context, do
the same documentation re-architecting for this repo. Proceed autonomously, including commit and push." The
card's title was its whole brief: "Update telder documentation to take the shape of brigade's".

## 1. What Brigade's card 110 did, and what carries over

Brigade's redesign (`../brigade/.context/plans/documentation-redesign.md`, commit `a9fa483`, 2026-10-17) is a
Diátaxis-style how-to tree with a generated-reference drift check and an offline structural gate: `README.md`
names the personas; `docs/<persona>/README.md` is a persona root (an "If you want to" table, one two-sentence
section per topic); `docs/<persona>/<topic>/README.md` is a topic root (the table, one TL;DR section per action
with a `Details:` line); the leaves beside it hold the details; argued and generated documents stay where code
names them and are reached from the tree. Agents enter at `CLAUDE.md`, a short root that imports one rule file
per subject from `docs/agent/repository/`; `AGENTS.md` lists the same files. A Go package (`internal/docscheck`)
and a drift test in `make test` hold all of it, and the gate runs in CI, the release script and the release
workflow.

What carries over unchanged: the four page shapes and their limits (two sentences, twenty lines, one `Details:`
line per leaf), the rule files behind `CLAUDE.md`, `AGENTS.md`, the offline rule (external links are never
checked), the generated make-target page, the planted-violation evidence, and the four places the gate runs.

What differs, and why:

- **Three personas, not five.** Telder has no backend to own and no team to administer. The readers are the
  User (installs the plugin, reads the summaries, tunes them), the Developer (works on this repository) and the
  AI Agent (in a session: the two skills and the summarizing model; on the repository: the rule files).
- **No harness registry.** Telder is a `MessageDisplay` hook, which exists in Claude Code alone; a second
  harness is not planned, so there is nothing for a registry to hold. The gate keeps the part of Brigade's
  `harness` rule that applies: every `plugin/skills/*/SKILL.md` is named by path on the agent's skills page.
- **No command reference.** The script's command line is three verbs for the skill; the skills page names them.
- **The listing stays whole.** `plugin/README.md` is what Anthropic's directory shows to a reader who never sees
  this repository, and its privacy section is what the manifest's `privacyPolicyUrl` names. Brigade cut its
  package page to "what the package ships"; Telder keeps the listing as a reference document the User tree
  points at, and the gate requires every option to be named on the options page and in the listing both.
- **Python, not Go.** The gate is `scripts/ci/docscheck.py` (standard library, Python 3.9) and its test
  `tests/test_docscheck.py`, which `make test` runs; `make docs-check` runs the script for a person.
- **The changelog rule reads the manifest.** Telder has no `plugin/bin/VERSION`; `plugin.json`'s `version` is
  the pin.

## 2. The shape

```
README.md                           the title, badge, description and sample; "Who are you?": the three personas
docs/user/README.md                 User: install, use, configure, update, privacy
docs/developer/README.md            Developer: setup, build-and-test, change, release, contribute, documentation, evidence
docs/agent/README.md                AI Agent: in-a-session (skills, summarizer), repository (the rule files)
docs/agent/repository/*.md          conventions, invariants, gates, documentation, directory: imported by CLAUDE.md
docs/developer/reference/           make-targets.md, generated (a reference directory, no topic root)
CLAUDE.md, AGENTS.md                the agent's root and its import-free twin
```

Dissolved into the tree: the front `README.md`'s sections (install, what you see, `/tldr`, options, the
instructions, update), `docs/development.md`, `docs/claude-code-usage.md`, and every rule of the old
`CLAUDE.md`, regrouped into the five rule files with nothing dropped. Kept as reference: `plugin/README.md`,
`SECURITY.md`, `CHANGELOG.md`, the records under `.context/plans/`.

## 3. The gate (`make docs-check`; `scripts/ci/docscheck.py`, `tests/test_docscheck.py`)

Ten rules: `readme` (one H1, one H2, the three roots in order), `persona`, `topic`, `links` (the root pages,
the listing, `SECURITY.md`, `docs/**`, and `CLAUDE.md`'s imports), `reach` (every page under `docs/` from
`README.md`), `skills`, `agent`, `options` (both pages), `make` (`make docs-generate` rewrites the page),
`changelog` (the pinned version's section). The test runs the gate on the repository, on an untouched copy, and
on sixteen copies with one violation planted each, and requires every check to have been caught at least once.

Wiring: `make docs-check` and `make docs-generate` (Gates section of the Makefile); `make test` through the test
file, so `make push` runs it; `ci.yml`'s `fast` job as a step after `make plugin-check`; `release.yml`'s guard
step; `scripts/release-prep.sh` as a precondition before the bump. The `commit` skill's description of the chain
names it.

## 4. References that move

`plugin.json`'s `documentationUrl` now names the User root. The `trello-create` and `trello-read` skills named
board lists that were archived on 2026-10-22 (Doing, Deploying, Releasing, Supporting); they now name the
project lists. A `trello-done` skill is ported from Brigade (its `close.py` makes the one API call the CLI has no
flag for), because the conventions name it and the card-closing rule depends on it. The hand-off's "Where
things are" row for the docs follows the pages. `plugin/README.md` changes in one line, in its support section,
to name the documentation tree; no `$`, no icon file name, so the directory's scan has nothing new to hold.

## 5. Open after this card

- The listing and the User tree say some of the same things on purpose; the gate holds their option tables in
  step but not their sentences. A sentence-level check was not built: the listing is read by a different
  audience and is allowed to differ.
- No release is cut by this card: the change the user sees is the documentation, which the next release's
  changelog section carries under `[Unreleased]`.
