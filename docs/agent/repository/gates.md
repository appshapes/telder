# Gates: what runs before a push, and what a release needs

- **The acceptance gate** is `make test lint plugin-check plugin-validate docs-check`. `make test` needs only
  `python3` (the nested `claude -p` is faked, so no login and no network); `make lint` and `make plugin-check`
  also need `shellcheck`; `make plugin-validate` needs a `claude` on `PATH` (login-free). `make push` runs `test`
  (the documentation gate is one of its tests) and `plugin-check` after the pull and before the commit; CI's
  `fast` job runs all five. Run all five before pushing anything under `plugin/`.
- **shellcheck is pinned.** CI's Ubuntu runner has shellcheck **0.9.0** (printed by `ci.yml`'s inventory step,
  run 36756274811) and this machine has 0.11, and versions disagree (0.9.0 reported SC2015 for `A && B || C`;
  0.11 did not): before pushing a shell file run
  `docker run --rm -v "$PWD:/mnt" -w /mnt koalaman/shellcheck:v0.9.0 -s sh <files>` as well as the local one,
  and re-pin this sentence whenever the inventory step prints a different version.
- **The documentation gate** (`make docs-check`, card 127) runs inside `make test` through
  `tests/test_docscheck.py`, in CI's `fast` job, as a precondition of `scripts/release-prep.sh` and as a guard
  step of `release.yml`. Its rules are in [documentation.md](documentation.md). A release with no
  `## [<version>]` changelog section does not leave the developer's machine.
- **Releases.** `make release version=X.Y.Z card=<n>` bumps `plugin/.claude-plugin/plugin.json`, moves the
  `[Unreleased]` section of `CHANGELOG.md` under the new version, commits through the push chain, tags
  `vX.Y.Z` and pushes the tag; `release.yml` then publishes the GitHub release with that changelog section as
  its notes. A published tag is never moved: bump the patch version instead. A tree that has never been released
  carries `0.0.0`, which the script refuses to release.
- **The dev loop** is `make plugin-dev` (a fresh Claude Code with `--plugin-dir ./plugin`, outside this
  session's environment: run it from your own terminal, never from inside a session);
  `make plugin-dev opts='{"model":"claude-sonnet-5-5"}'` passes options. `make hook-smoke` runs the script once
  on the sample reply with a real nested call.
