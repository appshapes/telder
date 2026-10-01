#!/bin/sh
# usage: scripts/ci/plugin-check.sh          (run from the repository root; no arguments)
#
# Static checks of the shipped plugin tree (`make plugin-check` runs this and then no-secrets.sh). Ported from
# appshapes/brigade. Exits non-zero on the FIRST failure, so a red line is always the whole story. One `ok: …`
# line per check.
#
# 1  plugin/ holds only allow-listed paths            5  hooks.json is exec-form, its commands exist and are
# 2  plugin/scripts/tldr-hook is 100755 in git           executable, and every hook sets a timeout
# 3  plugin.json "version" is one version token       6  the hook script compiles under python3
# 4  no bin/, no mcpServers, no channels under plugin/ 7  sh -n and shellcheck -s sh on every shell script
#                                                     8  no skill declares disable-model-invocation
#                                                     9  the listing icon is a square PNG the directory accepts,
#                                                        and the plugin README stays clear of two directory holds
#
# Why textual JSON checks: hooks.json and plugin.json are small hand-written manifests, jq is not on every host
# that runs `make plugin-check`, and the schema half is covered by `make plugin-validate` (`claude plugin validate
# --strict`, which Brigade measured as login-free but blind to a missing hook command -- hence check 5).
set -eu

die() { printf 'plugin-check: %s\n' "$1" >&2; exit 1; }
ok() { printf 'ok: %s\n' "$1"; }

[ -d plugin ] || die "run me from the repository root: no plugin/ directory here"

plugin_json=plugin/.claude-plugin/plugin.json
hooks_json=plugin/hooks/hooks.json
hook_script=plugin/scripts/tldr-hook

# ---- 1. the plugin/ file allowlist -------------------------------------------------------------------------------
# find, not `git ls-files`: an untracked stray (a .DS_Store, a __pycache__) would be packaged by --plugin-dir just
# the same, so the check has to see the working tree.
find plugin -type f -print | LC_ALL=C sort | while IFS= read -r f; do
  rel=${f#plugin/}
  case $rel in
    .claude-plugin/plugin.json|.claude-plugin/icon.png|hooks/hooks.json|scripts/tldr-hook|README.md) ;;
    skills/*/*) ;;   # a skill directory and whatever it carries beside its SKILL.md
    *) die "not allow-listed under plugin/: $f" ;;
  esac
done
ok "plugin/ contains only allow-listed paths"

# ---- 2. the hook script's mode as git records it (the exec-form hook runs the file directly) -----------------------
git rev-parse --git-dir >/dev/null 2>&1 || die "not a git repository: cannot check the recorded file modes"
modes=$(git ls-files -s plugin) || die "git ls-files failed"
[ -n "$modes" ] || die "git tracks no file under plugin/"
printf '%s\n' "$modes" | grep -q "^100755 .*	$hook_script\$" || die "git does not track $hook_script as 100755 (git update-index --add --chmod=+x $hook_script)"
ok "$hook_script is 100755 in git"

# ---- 3. the version pin ------------------------------------------------------------------------------------------
[ -f "$plugin_json" ] || die "missing $plugin_json"
manifest=$(sed -nE 's/^[[:space:]]*"version":[[:space:]]*"([^"]+)".*/\1/p' "$plugin_json" | head -n 1)
[ -n "$manifest" ] || die "$plugin_json declares no \"version\" on a line of its own"
case $manifest in
  [0-9]*.[0-9]*.[0-9]*) ;;
  *) die "$plugin_json version is not MAJOR.MINOR.PATCH: '$manifest'" ;;
esac
ok "$plugin_json pins version $manifest"

# ---- 4. no bin/, no MCP, no channels ----------------------------------------------------------------------------
# A plugin with a top-level bin/ is not installable from claude.ai or Cowork; check 1's allowlist already refuses
# the directory, so what is left is the content half: an mcpServers or channels key inside an allow-listed file.
if grep -rlE '"mcpServers"|"channels"' plugin >/dev/null 2>&1; then
  grep -rnE '"mcpServers"|"channels"' plugin >&2 || true
  die "an mcpServers or channels key appears under plugin/"
fi
ok "no bin/, no mcpServers and no channels anywhere under plugin/"

# ---- 5. hooks.json: exec form, every command there and executable, every hook with a timeout ---------------------
[ -f "$hooks_json" ] || die "missing $hooks_json"
types=$(awk '{ n += gsub(/"type"[[:space:]]*:/, "") } END { print n + 0 }' "$hooks_json")
cmds=$(awk '{ n += gsub(/"command"[[:space:]]*:[[:space:]]*"/, "") } END { print n + 0 }' "$hooks_json")
timeouts=$(awk '{ n += gsub(/"timeout"[[:space:]]*:/, "") } END { print n + 0 }' "$hooks_json")
[ "$types" -gt 0 ] || die "$hooks_json declares no hook \"type\""
[ "$types" = "$cmds" ] || die "$hooks_json has $types \"type\" keys but $cmds \"command\" strings: every hook must be exec form"
[ "$types" = "$timeouts" ] || die "$hooks_json has $types hooks but $timeouts \"timeout\" keys: every hook sets its own timeout (the nested model call outlives the default)"
bad=$(grep -oE '"type"[[:space:]]*:[[:space:]]*"[^"]*"' "$hooks_json" | grep -cv '"command"$' || true)
[ "$bad" = 0 ] || die "$hooks_json has $bad hook entries whose \"type\" is not \"command\""
grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' "$hooks_json" |
  sed -e 's/^"command"[[:space:]]*:[[:space:]]*"//' -e 's/"$//' |
  while IFS= read -r cmd; do
    [ -n "$cmd" ] || die "$hooks_json has an empty \"command\""
    rest=${cmd#\$\{CLAUDE_PLUGIN_ROOT\}}
    case $rest in
      "$cmd")
        case $cmd in /*) ;; *) die "$hooks_json command '$cmd' is neither absolute nor \${CLAUDE_PLUGIN_ROOT}-rooted" ;; esac
        resolved=$cmd ;;
      /*) resolved=plugin$rest ;;
      *) die "$hooks_json command '$cmd' must continue with / after \${CLAUDE_PLUGIN_ROOT}" ;;
    esac
    case $cmd in
      *[\ \	\;\|\&\<\>\(\)\`\"\']*) die "$hooks_json command '$cmd' is a shell string, not exec form: put arguments in \"args\"" ;;
    esac
    [ -f "$resolved" ] || die "$hooks_json names a hook command that does not exist: $cmd -> $resolved"
    [ -x "$resolved" ] || die "$hooks_json names a hook command that is not executable: $cmd -> $resolved"
  done
args_bad=$(grep -oE '"args"[[:space:]]*:[[:space:]]*[^[:space:]]' "$hooks_json" | grep -cv '\[$' || true)
[ "$args_bad" = 0 ] || die "$hooks_json has an \"args\" value that is not a JSON array"
ok "$hooks_json is exec form, every hook command exists and is executable, every hook sets a timeout"

# ---- 6. the hook script compiles -------------------------------------------------------------------------------
[ -f "$hook_script" ] || die "missing $hook_script"
head -n 1 "$hook_script" | grep -q '^#!/usr/bin/env python3$' || die "$hook_script must start with #!/usr/bin/env python3"
# compile(), not py_compile: py_compile would drop a __pycache__ under plugin/, which check 1 rightly refuses.
python3 -c 'import sys; compile(open(sys.argv[1]).read(), sys.argv[1], "exec")' "$hook_script" || die "$hook_script does not compile"
ok "$hook_script compiles under $(python3 --version 2>&1)"

# ---- 7. every shell script parses, and shellcheck agrees ----------------------------------------------------------
set -- scripts/ci/*.sh scripts/*.sh
for f in "$@"; do
  [ -f "$f" ] || continue
  sh -n "$f" || die "sh -n $f failed"
done
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck -s sh "$@" || die "shellcheck reported problems"
  ok "shellcheck -s sh clean: $*"
elif [ -n "${CI:-}" ]; then
  die "shellcheck is not installed and CI is set: the runner image preinstalls it, so this is a real failure"
else
  printf 'plugin-check: WARNING: shellcheck is not installed; skipping (CI enforces it)\n' >&2
  ok "shellcheck skipped with a warning (not CI)"
fi

# ---- 8. no skill disables model invocation --------------------------------------------------------------------
# Ported from Brigade (card 28): a skill the model cannot reach on its own is a skill that cannot help unasked.
disabled=""
for f in plugin/skills/*/SKILL.md; do
  [ -f "$f" ] || continue
  if grep -qE '^[[:space:]]*disable-model-invocation[[:space:]]*:' "$f"; then
    disabled="$disabled $f"
  fi
done
[ -z "$disabled" ] || die "disable-model-invocation is declared in:$disabled -- every skill stays reachable by the model"
ok "no skill declares disable-model-invocation"

# ---- 9. what Anthropic's plugin directory checks, and `claude plugin validate` does not -----------------------------
# The directory takes the listing icon from .claude-plugin/icon.png: a square PNG, 512 to 2048 px a side, under
# 2 MB. The size is read from the PNG header (bytes 16 to 23 of the file), so no image library is needed.
icon=plugin/.claude-plugin/icon.png
[ -f "$icon" ] || die "missing $icon (the directory's listing icon)"
python3 - "$icon" <<'PY' || die "$icon is not a square PNG of 512 to 2048 px a side and under 2 MB"
import struct
import sys

data = open(sys.argv[1], "rb").read()
ok = data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR" and len(data) < 2 * 1024 * 1024
if ok:
    width, height = struct.unpack(">II", data[16:24])
    ok = width == height and 512 <= width <= 2048
sys.exit(0 if ok else 1)
PY
# The directory's scan holds a plugin whose README names a shell variable beside a URL ("uses a credential from
# the user's machine"; Brigade measured it on `$PWD`), and one that names a bundled image in backticks.
readme=plugin/README.md
[ -f "$readme" ] || die "missing $readme (the directory shows it as the listing)"
if grep -n '\$' "$readme" >&2; then
  die "$readme contains a dollar sign: the directory's scan reads a shell variable there as a credential"
fi
if grep -n 'icon\.png' "$readme" >&2; then
  die "$readme names the icon file: the directory's scan holds a bundled image that a README names"
fi
ok "$icon is a square PNG the directory accepts, and $readme has no dollar sign and does not name the icon"

printf 'plugin-check: all checks passed\n'
