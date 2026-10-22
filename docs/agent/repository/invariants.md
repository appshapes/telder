# Invariants: the plugin tree, the script, the nested call, secrets, configuration

- **The plugin is one command hook on `MessageDisplay`** (display-only: the summary never enters Claude's
  context; measured 2026-09-30, see `.context/plans/telder-build-2026-09-30.md` for why not `Stop` and never a
  `prompt` hook), one Python script and its two skills under `plugin/`, the listing icon, and nothing else: no
  MCP server, no channel, no binary, no `bin/` directory (a plugin with `bin/` is not installable from claude.ai
  or Cowork). `make plugin-check` enforces the `plugin/` file allowlist.
- **The hook script** is Python 3, standard library only, one file (`plugin/scripts/tldr-hook`), launched in exec
  form (`command` + `args`, never a shell string). It never writes to stdout except the hook's JSON reply;
  diagnostics go to stderr, prefixed `tldr:`.
- **The nested call.** The script spawns `claude -p` with an argument array and an environment stripped BY
  PREFIX of every variable whose name begins with `CLAUDE` — no underscore, so `CLAUDECODE` is covered — plus
  `AI_AGENT`, keeping only `CLAUDE_CONFIG_DIR`, and it sets `TLDR_INNER=1` so the nested session's own copy of the
  hook returns at once. The strip is done on the hook's own environment, by name (`leave_session`), and the
  nested call inherits it: the script never copies the environment and reads every variable by its literal
  name, because the directory's scan holds a plugin that reads the environment as a whole or by a computed name
  (measured 2026-10-01). Never `--bare` on the nested call: bare mode reads no OAuth login, so every subscription
  user would get nothing.
- **Secrets.** Never put a secret in the hook's output, in a log line, on a card or in a file under the project
  directory. The script never reads the transcript file and never reads `$CLAUDE_CONFIG_DIR/sessions/*.key`; the
  reply text it summarizes reaches it on stdin from Claude Code and goes to the summarizing model and nowhere
  else.
- **The instruction layers.** The instructions the summarizing model follows are layered in the script
  (`instruction_parts`): the plugin's own, the `instructions` option, the `instructions_file` option, the
  project's `.telder.md`, then the fixed format rules, which the parser depends on and no layer may remove. The
  `/tldr` skill gets the same layers from `tldr-hook instructions` with the option values as arguments (a model's
  Bash command carries no `CLAUDE_PLUGIN_OPTION_*`), the inline text through a quoted heredoc so any content
  survives.
- **Configuration directories.** Never hardcode `~/.claude`; use `CLAUDE_CONFIG_DIR ?? ~/.claude`. State (the
  mute marker, the pieces of a reply being shown) lives under `CLAUDE_PLUGIN_DATA`, never under
  `CLAUDE_PLUGIN_ROOT`, which changes on every update.
- **Every skill is reachable by the model.** Never add `disable-model-invocation` to a skill under
  `plugin/skills/` (`make plugin-check` enforces it, ported from Brigade's card 28 ruling: a skill the model
  cannot reach cannot help unasked).
