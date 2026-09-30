# Development Guidelines

**Plans and temporary docs:**
- All plans **must** go in `.context/plans/`
- Ephemeral scratch **must** go in `.ignored/` (gitignored).

# Overrides
- @./CLAUDE.user.md (optional, local-only, gitignored — absent in fresh clones)

# Telder
- Telder is the product; `tldr` is the plugin (`/plugin install tldr@telder`). The plugin is one command hook on
  `MessageDisplay` (display-only: the summary never enters Claude's context; measured 2026-09-30, see
  `.context/plans/telder-build-2026-09-30.md` for why not `Stop` and never a `prompt` hook), one Python script and its
  skill under `plugin/`, and nothing else: no MCP server, no channel, no binary, no
  `bin/` directory (a plugin with `bin/` is not installable from claude.ai or Cowork). `make plugin-check` enforces
  the `plugin/` file allowlist.
- The hook script is Python 3, standard library only, one file (`plugin/scripts/tldr-hook`), launched in exec form
  (`command` + `args`, never a shell string). It never writes to stdout except the hook's JSON reply; diagnostics go
  to stderr. It spawns `claude -p` with an argument array and an environment stripped BY PREFIX of every variable
  whose name begins with `CLAUDE` — no underscore, so `CLAUDECODE` is covered — plus `AI_AGENT`, keeping only
  `CLAUDE_CONFIG_DIR`, and it sets `TLDR_INNER=1` so the nested session's own copy of the hook returns at once.
  Never `--bare` on the nested call: bare mode reads no OAuth login, so every subscription user would get nothing.
- Never put a secret in the hook's output, in a log line, on a card or in a file under the project directory. The
  script never reads the transcript file and never reads `$CLAUDE_CONFIG_DIR/sessions/*.key`; the reply text it
  summarizes reaches it on stdin from Claude Code and goes to the summarizing model and nowhere else.
- Never hardcode `~/.claude`; use `CLAUDE_CONFIG_DIR ?? ~/.claude`. State (a mute, a cache) lives under
  `CLAUDE_PLUGIN_DATA`, never under `CLAUDE_PLUGIN_ROOT`, which changes on every update.
- Every skill is reachable by the model: never add `disable-model-invocation` to a skill under `plugin/skills/`
  (`make plugin-check` enforces it, ported from Brigade's card 28 ruling).
- Commit messages: `<card>: <Imperative summary>`, the number being the AppShapes Trello card the work belongs to;
  `make push message="<card>: ..."`; merges only, never rebase. Skills: `/commit <card>`, `/trello-create`,
  `/trello-read`; `docs/claude-code-usage.md` is the usage guide.
- `make test` needs only `python3`; `make plugin-check` also needs `shellcheck`; `make plugin-validate` needs a
  `claude` on `PATH` (login-free). Run `make test plugin-check plugin-validate` before pushing anything under
  `plugin/`. The CI runner's shellcheck may disagree with the local one; when it does, the runner's version, printed
  by `ci.yml`'s inventory step, wins.
- Releases: `make release version=X.Y.Z card=<n>` bumps `plugin/.claude-plugin/plugin.json`, moves the
  `[Unreleased]` section of `CHANGELOG.md` under the new version, commits through the push chain, tags `vX.Y.Z` and
  pushes the tag; `release.yml` then publishes the GitHub release with that changelog section as its notes. A
  published tag is never moved: bump the patch version instead.
- The plugin's dev loop is `make plugin-dev` (a fresh Claude Code with `--plugin-dir ./plugin`, outside this
  session's environment); `make plugin-dev opts='{"model":"claude-sonnet-5-5"}'` passes options.
