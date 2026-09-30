#!/bin/sh
# usage: scripts/ci/release-notes.sh <version>     (prints CHANGELOG.md's section for <version> on stdout)
#
# release.yml uses it to fill the GitHub release's notes. Exits 1 when the section is missing or empty, so a tag
# whose changelog was not written is refused rather than published with nothing to say.
set -eu
v=${1:-}
[ -n "$v" ] || { printf 'usage: release-notes.sh <version>\n' >&2; exit 1; }
v=${v#v}
notes=$(awk -v v="$v" '
  $0 ~ "^## \\[" v "\\]" { on=1; next }
  /^## \[/ { on=0 }
  on { print }
' CHANGELOG.md)
printf '%s\n' "$notes" | grep -q '[^[:space:]]' || { printf 'release-notes: CHANGELOG.md has no section for %s\n' "$v" >&2; exit 1; }
printf '%s\n' "$notes"
