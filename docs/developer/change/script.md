# Change the script

`plugin/scripts/tldr-hook` is the whole plugin at run time: Claude Code runs it as the `MessageDisplay` hook, and
the `/tldr` skill runs it as a small command line. The rules it keeps are the agent's
[Invariants](../../agent/repository/invariants.md); this page is where each one lives in the file and what to run
after a change.

## The shape

- **One file, standard library only, Python 3.9 or newer.** No package is installed on a user's machine, and
  `make plugin-check` refuses anything under `plugin/` the allowlist does not name.
- **Exec form.** `plugin/hooks/hooks.json` names the script as `command` with an empty `args` array and a
  130-second `timeout`; never a shell string. `plugin-check` holds the form, the mode (100755 in git) and the
  timeout.
- **Stdout is the hook's JSON reply and nothing else.** Diagnostics go to stderr through `warn`, prefixed
  `tldr:`, which Claude Code's debug file records.
- **Two events are understood.** `HANDLERS` maps `MessageDisplay` (in use: the summary goes on the message's
  final display chunk, display-only) and `Stop` (the summary as a `systemMessage`, which Claude sees on the next
  turn: an injection path, so not used; the build record has the measurements). Changing the event means
  changing `hooks.json`, the handler and the listing's "What leaves your machine" section.

## The nested call

`summarize_command` builds the argument array; `claude_command` picks the executable, the one running the
session when Claude Code names it, else `claude` on `PATH`; `leave_session` removes from the hook's own
environment every variable whose name begins with `CLAUDE` (so `CLAUDECODE` and `CLAUDE_CODE_*` together) plus
`AI_AGENT`, keeping `CLAUDE_CONFIG_DIR`, and sets `TLDR_INNER=1`; the child then inherits that environment. The
script never copies the environment and reads each variable by its literal name, because the directory's scan
holds a plugin that reads the environment as a whole or by a computed name. Never `--bare`: bare mode reads no
OAuth login, so every subscription user would get nothing. `tests/test_tldr_hook.py` pins the command shape and
runs a real child to prove the strip.

## The instruction layers

`instruction_parts` returns the parts in order: the plugin's own (`BUILT_IN`, unless `instructions_mode` is
`replace` and something of the user's exists), the `instructions` option, the `instructions_file` option, the
project's `.telder.md` (`project_dir_of`: `CLAUDE_PROJECT_DIR`, else the hook input's `cwd`), then
`FORMAT_RULES` with `max_points` and `NONE` filled in. `read_instructions_file` ignores a file that is missing,
empty, not UTF-8 or over `MAX_INSTRUCTIONS_BYTES`. `run_instructions` prints the same parts for the skill, each
under its source, from the values the skill passes as arguments and the inline text on stdin. A change to a
layer changes the tests (`Instructions`), the skill's own copy of the built-in text (`SkillFallback` pins the
two equal), and the pages that list the layers: the user's [Change the instructions](../../user/configure/instructions.md),
the agent's [Write a summary](../../agent/in-a-session/summarizer.md), and the listing.

## State and secrets

`data_dir` is `CLAUDE_PLUGIN_DATA` (kept across updates), else a per-user temporary directory; `mute_path` is the
`/tldr off` marker; `accumulator_path` is the file of a reply's pieces, created by `private_dir` for this user
only and deleted on the final chunk; `sweep_stale` removes pieces older than an hour. Nothing is written under
the project. The script never reads the transcript file, never reads `$CLAUDE_CONFIG_DIR/sessions/*.key`, and
never puts a secret in its output or its log line.

## After a change

```sh
make test                 # the fake nested call; seconds
make hook-smoke           # one real nested call on the sample reply
make plugin-dev           # a fresh Claude Code with the checkout's plugin, from your own terminal
make plugin-check         # the tree, the mode, the form
```

Then the pages: a new read, write, send or run changes `plugin/README.md`'s privacy section in the same commit
([Change the listing](listing.md)), and a changed behaviour changes its leaf and TL;DR in the User tree and the
`[Unreleased]` section of `CHANGELOG.md`.
