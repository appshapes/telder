# Development Guidelines

**Plans and temporary docs:**
- All plans **must** go in `.context/plans/`
- Ephemeral scratch **must** go in `.ignored/` (gitignored).

# Overrides
- @./CLAUDE.user.md (optional, local-only, gitignored — absent in fresh clones)

# Telder
- Start here: `.context/plans/handoff-2026-09-30.md` (state) and `.context/plans/telder-build-2026-09-30.md`
  (every measurement and decision).
- Telder is the product and `telder` the plugin (`/plugin install telder@telder`; it was `tldr` until 0.3.0, renamed
  for the directory, where a name is permanent and `tldr` drew three look-alike holds); `/tldr` is its skill, and the
  script, its log prefix and `TLDR_INNER` keep the old spelling. The plugin is one command hook on
  `MessageDisplay` (display-only: the summary never enters Claude's context; measured 2026-09-30, see
  `.context/plans/telder-build-2026-09-30.md` for why not `Stop` and never a `prompt` hook), one Python script and its
  skill under `plugin/`, the listing icon, and nothing else: no MCP server, no channel, no binary, no
  `bin/` directory (a plugin with `bin/` is not installable from claude.ai or Cowork). `make plugin-check` enforces
  the `plugin/` file allowlist.
- Anthropic's plugin directory takes the plugin from `plugin/` on `master` and scans every new commit there
  (`docs/development.md` › The directory listing; `.context/plans/directory-submission-2026-09-30.md` for what the
  portal found). `plugin/README.md` is the listing and its privacy statement: when the script reads, writes, sends
  or runs something new, the section "What leaves your machine, and where it goes" changes in the same commit.
  Never a dollar sign in that README and never the icon's file name (the scan holds both; `make plugin-check`
  refuses them). The name `telder` is permanent once listed.
- The hook script is Python 3, standard library only, one file (`plugin/scripts/tldr-hook`), launched in exec form
  (`command` + `args`, never a shell string). It never writes to stdout except the hook's JSON reply; diagnostics go
  to stderr. It spawns `claude -p` with an argument array and an environment stripped BY PREFIX of every variable
  whose name begins with `CLAUDE` — no underscore, so `CLAUDECODE` is covered — plus `AI_AGENT`, keeping only
  `CLAUDE_CONFIG_DIR`, and it sets `TLDR_INNER=1` so the nested session's own copy of the hook returns at once.
  Never `--bare` on the nested call: bare mode reads no OAuth login, so every subscription user would get nothing.
- Never put a secret in the hook's output, in a log line, on a card or in a file under the project directory. The
  script never reads the transcript file and never reads `$CLAUDE_CONFIG_DIR/sessions/*.key`; the reply text it
  summarizes reaches it on stdin from Claude Code and goes to the summarizing model and nowhere else.
- The instructions the summarizing model follows are layered in the script (`instruction_parts`): the plugin's
  own, the `instructions` option, the `instructions_file` option, the project's `.telder.md`, then the fixed
  format rules, which the parser depends on and no layer may remove. The `/tldr` skill gets the same layers
  from `tldr-hook instructions` with the option values as arguments (a model's Bash command carries no
  `CLAUDE_PLUGIN_OPTION_*`), the inline text through a quoted heredoc so any content survives.
- Never hardcode `~/.claude`; use `CLAUDE_CONFIG_DIR ?? ~/.claude`. State (a mute, a cache) lives under
  `CLAUDE_PLUGIN_DATA`, never under `CLAUDE_PLUGIN_ROOT`, which changes on every update.
- Every skill is reachable by the model: never add `disable-model-invocation` to a skill under `plugin/skills/`
  (`make plugin-check` enforces it, ported from Brigade's card 28 ruling).
- Commit messages: `<card>: <Imperative summary>`, the number being the AppShapes Trello card the work belongs to;
  `make push message="<card>: ..."`; merges only, never rebase. Skills: `/commit <card>`, `/trello-create`,
  `/trello-read`; `docs/claude-code-usage.md` is the usage guide.
- `make test` needs only `python3`; `make plugin-check` also needs `shellcheck`; `make plugin-validate` needs a
  `claude` on `PATH` (login-free). Run `make test plugin-check plugin-validate` before pushing anything under
  `plugin/`. CI's Ubuntu runner has shellcheck **0.9.0** (printed by `ci.yml`'s inventory step, run 36756274811) and
  this machine has 0.11, and versions disagree (0.9.0 reported SC2015 for `A && B || C`; 0.11 did not): before
  pushing a shell file run `docker run --rm -v "$PWD:/mnt" -w /mnt koalaman/shellcheck:v0.9.0 -s sh <files>` as
  well as the local one, and re-pin this sentence whenever the inventory step prints a different version.
- Releases: `make release version=X.Y.Z card=<n>` bumps `plugin/.claude-plugin/plugin.json`, moves the
  `[Unreleased]` section of `CHANGELOG.md` under the new version, commits through the push chain, tags `vX.Y.Z` and
  pushes the tag; `release.yml` then publishes the GitHub release with that changelog section as its notes. A
  published tag is never moved: bump the patch version instead.
- The plugin's dev loop is `make plugin-dev` (a fresh Claude Code with `--plugin-dir ./plugin`, outside this
  session's environment); `make plugin-dev opts='{"model":"claude-sonnet-5-5"}'` passes options.
