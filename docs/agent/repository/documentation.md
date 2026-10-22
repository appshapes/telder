# Documentation: where a page goes, and the gate that holds it

The documentation is one tree for humans and one for agents (card 127,
`.context/plans/documentation-redesign-2026-10-22.md`, the shape of Brigade's card 110).

- **Humans enter at `README.md`**, which has two parts only: the title, description and sample; and the three
  personas, each a link to its root. The roots are `docs/user/`, `docs/developer/` and `docs/agent/`, each a
  `README.md`.
- **A persona root** has an `## If you want to` table whose rows link to the persona's topic roots, then one H2
  per topic: at most two sentences and a link to the topic's `README.md`. Nothing else.
- **A topic root** (`docs/<persona>/<topic>/README.md`) has an `## If you want to` table whose rows link to its
  own action sections, then one H2 per action: the TL;DR (the shortest listing that gets it done, at most 20
  lines) and a `Details:` line linking to the action's page. Every `.md` beside the README is such a page and is
  named by exactly one `Details:` line; a page nothing names fails the gate.
- **A detail page** is the leaf: the details, concise, in one logical order, no mannered prose, no restating of
  the TL;DR. It may link to a reference document instead of repeating it.
- **Reference documents stay where code and manifests name them** and are reached from the tree:
  `plugin/README.md` (the directory listing and the privacy statement `privacyPolicyUrl` names; its headings
  are anchors the manifest and the tree depend on), `SECURITY.md`, `CHANGELOG.md`, the records under
  `.context/plans/`, and the generated `docs/developer/reference/make-targets.md`. A directory under a persona
  that holds reference pages rather than a topic is registered in the gate's `REFERENCE_DIRS`.
- **Agents enter at `CLAUDE.md`**, whose `@docs/agent/repository/<file>.md` imports load every rule file; a rule
  belongs in one of those files, never in `CLAUDE.md` itself, and every file under `docs/agent/repository/` must
  be imported there and linked from `AGENTS.md`. Inside a session, the plugin's skills are the agent's
  documentation: `docs/agent/in-a-session/skills.md` names each skill by path.
- **The gate** is `make docs-check` (`scripts/ci/docscheck.py`, `tests/test_docscheck.py`), offline, standard
  library only, in `make test`, CI's `fast` job, `scripts/release-prep.sh` and `release.yml`. Its rules: the
  README shape; the persona and topic shapes above; every relative link and `#anchor` in the root pages, the
  listing and `docs/**` resolves, and every `@` import in `CLAUDE.md` names a file; every page under `docs/` is
  reachable from `README.md`; every `plugin/skills/*/SKILL.md` is named on the skills page; the rule files'
  imports and links; every `userConfig` option of `plugin/.claude-plugin/plugin.json` named in
  `docs/user/configure/options.md` and in `plugin/README.md`; `docs/developer/reference/make-targets.md` equal to
  what `make docs-generate` writes from the Makefile's `##` help lines; and a `## [<version>]` changelog section
  for the version the manifest pins. External links are never checked: a site going down is not a bug in this
  repository.
- **When you change** a `make` target's help line, run `make docs-generate`. When you add or change an option,
  its default changes in three places: the manifest, the options page and the listing. When you add a skill,
  add its row to the skills page. When you add a page, name it from a `Details:` line. When a procedure
  changes, change the leaf and the TL;DR together, and the listing where it says the same.
