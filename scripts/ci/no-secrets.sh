#!/bin/sh
# usage: scripts/ci/no-secrets.sh            (run from the repository root; no arguments)
#
# Fails, naming the file and line, when a credential shape reaches something we ship or track. Ported from
# appshapes/brigade, where a real personal-access-token prefix once reached a public repository through a test
# fixture built from a credential that was in the session's context: the lesson is to scan everything, with no
# length floor on the prefix-shaped patterns.
#
# Patterns, everywhere in scope (every file under plugin/ and every tracked file):
#   * an Anthropic API key           sk-ant-<8+>
#   * a JWT-shaped triple            eyJ<8+>.eyJ<8+>.<8+>
#   * a Supabase secret key or PAT   sb_secret_<8+>   sbp_<20+ hex>
#   * a GitHub token                 ghp_<20+>   github_pat_<8+>
#   * an AWS access key id           AKIA<16 upper/digits>
#   * a Resend API key               re_<8+>_<8+>
#   * a private key block            -----BEGIN ... PRIVATE KEY-----
# The scanned file count is printed, so a run that read nothing is visible instead of vacuously green.
set -eu

die() { printf 'no-secrets: %s\n' "$1" >&2; exit 1; }

[ -d plugin ] || die "run me from the repository root: no plugin/ directory here"

anthropic='sk-ant-[A-Za-z0-9_-]\{8,\}'
jwt='eyJ[A-Za-z0-9_-]\{8,\}\.eyJ[A-Za-z0-9_-]\{8,\}\.[A-Za-z0-9_-]\{8,\}'
sbsecret='sb_secret_[A-Za-z0-9_-]\{8,\}'
sbpat='sbp_[0-9a-f]\{20,\}'
ghp='ghp_[A-Za-z0-9]\{20,\}'
ghpat='github_pat_[A-Za-z0-9_]\{8,\}'
aws='AKIA[0-9A-Z]\{16\}'
resend='re_[A-Za-z0-9]\{8,\}_[A-Za-z0-9]\{8,\}'
pem='-----BEGIN [A-Z ]*PRIVATE KEY-----'

tmp=$(mktemp -t no-secrets.XXXXXX) || die "cannot create a temporary file"
trap 'rm -f "$tmp"' EXIT HUP INT TERM

{
  find plugin -type f -print
  git ls-files
} | LC_ALL=C sort -u | while IFS= read -r f; do
  [ -f "$f" ] || continue
  printf '%s\n' "$f"
done > "$tmp"

count=$(grep -c . "$tmp" || true)
[ "$count" -gt 0 ] || die "the scan found no files at all: refusing to pass vacuously"

hits=0
while IFS= read -r f; do
  if grep -aHn -e "$anthropic" -e "$jwt" -e "$sbsecret" -e "$sbpat" -e "$ghp" -e "$ghpat" -e "$aws" -e "$resend" -e "$pem" "$f" >&2; then
    hits=$((hits + 1))
  fi
done < "$tmp"
[ "$hits" = 0 ] || die "$hits file(s) above contain a credential-shaped string"

printf 'no-secrets: scanned %s tracked/plugin file(s) for nine credential shapes: clean\n' "$count"
