# Know the CI

| Workflow | When | Jobs |
| --- | --- | --- |
| `ci.yml` | every push and pull request | `fast` (Ubuntu: `make test`, `make lint`, `make plugin-check`, `make docs-check`, then Claude Code installed with npm, never authenticated, for `make plugin-validate`); `macos` (the primary user platform: `make test` under its `python3`) |
| `release.yml` | a `v*` tag | checks the tag is not already published; guards that the manifest pins the tag, the changelog has the tag's section and `make docs-check` passes; publishes the GitHub release with that section as its notes (`--prerelease` for a tag with a hyphen) |

Both jobs of `ci.yml` start with a "Runner image inventory" step that prints the image and the versions of
shellcheck, `python3`, `node` and `gh` into the job summary. It never gates; its value is that shellcheck
releases disagree with each other, and the version it prints is the one pinned in the agent's
[Gates](../../agent/repository/gates.md) rule file.

What the workflows share, ported from Brigade: every job sets `timeout-minutes`, because GitHub's default is
360 and a hung job would burn six hours; no constant-false `if:` anywhere, so a green conclusion means every step
passed; `release.yml` queues a duplicate delivery of a tag push behind the first run and does nothing when the
release exists, because GitHub delivers a push event at least once.

The scripts the workflows run live in `scripts/ci/`: `plugin-check.sh` and `no-secrets.sh` (`make plugin-check`),
`docscheck.py` (`make docs-check`), `release-notes.sh` (the changelog section for a version, which `release.yml`
turns into the release notes and which refuses an empty section). `scripts/release-prep.sh` is the release
sequence `make release` runs on the developer's machine ([Cut a release](../release/cut-a-release.md)).

Not ported from Brigade, on purpose: the agentic loop and the release-notes email, which need secrets and
Blacksmith runners; Telder's workflows run on plain `ubuntu-latest` and `macos-latest`.
