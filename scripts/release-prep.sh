#!/bin/sh
# usage: card=<n> scripts/release-prep.sh <version>          (run by `make release version=0.1.0 card=<n>`)
#        DRY_RUN=1 card=<n> scripts/release-prep.sh <version>  -- steps 1-2 for real, then stop and PRINT 3-4
#
# The release sequence, ported from appshapes/brigade and cut down: no binaries, no checksums, so the tag is the
# release and release.yml publishes it with the changelog section as its notes.
#
#   preconditions   a MAJOR.MINOR.PATCH version, a card number, the repository root, a clean tree, master
#   1  bump the pin        plugin/.claude-plugin/plugin.json "version"
#   2  the changelog       CHANGELOG.md: rename `## [Unreleased]` to `## [<v>] — <today>` under a fresh
#                          `## [Unreleased]`; refuse an empty Unreleased section (a release says what changed)
#   3  commit              make push message="<card>: Release <v>"
#   4  tag                 git tag -a v<v> && git push origin v<v>  ->  release.yml publishes the GitHub release
#
# A PUBLISHED tag is never rewritten: bump the patch version instead. A tag that release.yml refused (version
# mismatch) is deleted with `git tag -d v<v> && git push --delete origin v<v>` before the next attempt.
set -eu

die() { printf 'release-prep: %s\n' "$1" >&2; exit 1; }
say() { printf 'release-prep: %s\n' "$1"; }

plugin_json=plugin/.claude-plugin/plugin.json
changelog=CHANGELOG.md

v=${1:-}
card=${card:-}
case ${DRY_RUN:-0} in
  ''|0|no|false) dry_run=0 ;;
  *)             dry_run=1 ;;
esac

# ---- preconditions -------------------------------------------------------------------------------------------
[ -n "$v" ] || die "usage: scripts/release-prep.sh <version>   (make release version=X.Y.Z card=<n>)"
case $v in
  v*)                   die "pass the version without the leading 'v' (got '$v'); the script tags v<version> itself" ;;
  0.0.0)                die "0.0.0 is the pre-release sentinel and cannot be released: pass make release version=X.Y.Z" ;;
  *[!0-9.]*)            die "not a MAJOR.MINOR.PATCH version: '$v'" ;;
  [0-9]*.[0-9]*.[0-9]*) ;;
  *)                    die "not a MAJOR.MINOR.PATCH version: '$v'" ;;
esac
case $card in
  '')        die "usage: make release version=X.Y.Z card=<n>: card is the AppShapes Trello card the release belongs to" ;;
  *[!0-9]*)  die "card must be a Trello card number (got '$card')" ;;
esac
if [ ! -f "$plugin_json" ] || [ ! -f "$changelog" ]; then
  die "run this from the repository root (no $plugin_json / $changelog here)"
fi
git rev-parse --git-dir >/dev/null 2>&1 || die "not a git repository"

dirty=$(git status --porcelain --untracked-files=normal)
if [ -n "$dirty" ]; then
  printf '%s\n' "$dirty" >&2
  die "tree not clean: commit or discard your changes first (step 3's 'make push' runs 'git add :/ .')"
fi
branch=$(git branch --show-current)
[ "$branch" = master ] || die "release from master, not '$branch'"
git tag -l "v$v" | grep -q . && die "tag v$v already exists locally"

grep -q '^## \[Unreleased\]' "$changelog" || die "$changelog has no '## [Unreleased]' section"
# The Unreleased section is everything between its heading and the next '## [' heading; it must hold a line.
unreleased=$(awk '/^## \[Unreleased\]/ {on=1; next} /^## \[/ {on=0} on' "$changelog" | grep -c '[^[:space:]]' || true)
[ "$unreleased" -gt 0 ] || die "$changelog's Unreleased section is empty: a release says what changed"

if [ "$dry_run" = 1 ]; then
  say "DRY_RUN=1: skipping 'git pull --no-edit'"
else
  git pull --no-edit
fi

# ---- 1. bump the pin --------------------------------------------------------------------------------------------
sed -i.bak -E "s/^([[:space:]]*\"version\":[[:space:]]*)\"[^\"]+\"/\1\"$v\"/" "$plugin_json"
rm -f "$plugin_json.bak"
manifest=$(sed -nE 's/^[[:space:]]*"version":[[:space:]]*"([^"]+)".*/\1/p' "$plugin_json" | head -n 1)
[ "$manifest" = "$v" ] || die "the bump did not take in $plugin_json (its version reads as '$manifest'): \"version\" must start its own line"
say "1. pinned $plugin_json to $v"

# ---- 2. the changelog -------------------------------------------------------------------------------------------
today=$(date +%Y-%m-%d)
awk -v v="$v" -v d="$today" '
  /^## \[Unreleased\]/ && !done { print "## [Unreleased]"; print ""; print "## [" v "] — " d; done=1; next }
  { print }
' "$changelog" > "$changelog.new" && mv "$changelog.new" "$changelog"
grep -q "^## \[$v\] — $today" "$changelog" || die "the changelog rename did not take"
say "2. $changelog: Unreleased is now [$v] — $today"

if [ "$dry_run" = 1 ]; then
  say "DRY_RUN=1: stopping before the commit. A real run would now:"
  say "  3. make push message=\"$card: Release $v\""
  say "  4. git tag -a v$v -m v$v && git push origin v$v"
  exit 0
fi

# ---- 3. commit --------------------------------------------------------------------------------------------------
make push message="$card: Release $v"
say "3. committed and pushed the release commit"

# ---- 4. tag -----------------------------------------------------------------------------------------------------
git tag -a "v$v" -m "v$v"
git push origin "v$v"
say "4. pushed v$v; release.yml now publishes the GitHub release with the changelog section as its notes"
