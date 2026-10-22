# Cut a release

```sh
make release version=0.8.0 card=127          # on a clean master, gh logged in
```

`scripts/release-prep.sh` does, in order:

0. **Preconditions**: a `MAJOR.MINOR.PATCH` version without the `v` (`0.0.0` is the pre-release sentinel and is
   refused), a card number, the repository root, a clean tree (untracked files included: step 3 stages
   everything), `master`, no local tag `v<v>`, a `## [Unreleased]` section in `CHANGELOG.md` that holds a line
   (a release says what changed), `make docs-check` green, then `git pull --no-edit`.
1. **Bump the pin**: `plugin/.claude-plugin/plugin.json` › `version`.
2. **The changelog**: `## [Unreleased]` becomes `## [<v>] — <today>` under a fresh `## [Unreleased]`.
3. **Commit**: `make push message="<card>: Release <v>"`, which pulls, runs the tests with the documentation
   gate (the new pin now needs its `## [<v>]` section, which step 2 wrote), runs `plugin-check`, commits and
   pushes.
4. **Tag**: `git tag -a v<v> && git push origin v<v>`.

`release.yml` then checks that the tag is not already published (GitHub delivers a tag push at least once), guards
that the manifest pins the tag, takes the tag's changelog section with `scripts/ci/release-notes.sh` (which refuses
an empty one) and runs `make docs-check`, and publishes the GitHub release with the section as its notes:
`--latest` for a plain version, `--prerelease` for one with a hyphen. There are no binaries: the release is the
tag.

```sh
gh run list --workflow release.yml
```

## After

- Claude Code moves every install from the marketplace in the background and asks for `/reload-plugins`;
  `/telder:update` does it at once ([Update right now](../../user/update/update-now.md)).
- Anthropic's directory scans the push and serves the version once reviewed, which can take a while
  ([Change the listing](../change/listing.md)).
- Comment the card with the version, the commit, the tag and the run ids, and close it when its criteria are met
  ([Work a card](../contribute/cards.md)).

## Recovery

- If `release.yml` fails after the tag exists, fix the cause, delete the never-published tag
  (`git tag -d v<v> && git push --delete origin v<v>`) and tag again by hand
  (`git tag -a v<v> -m v<v> && git push origin v<v>`); the script cannot be rerun on a tree that is already
  pinned. A **published** tag is never rewritten: bump the patch version instead.
- `DRY_RUN=1 card=<n> scripts/release-prep.sh <v>` does steps 1 and 2 for real, prints 3 and 4, and stops; revert
  the two files afterwards.
