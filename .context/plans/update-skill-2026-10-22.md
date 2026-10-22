# The update skill — 2026-10-22

Card 124 on the AppShapes Trello board (`124: ...` commits). Asked by Rjae, used to Brigade's `/brigade:update`:
"create the `update` skill and release 0.6.0".

## Why

Auto-update is on for the `telder` marketplace, and Claude Code applies it when it refreshes the marketplace.
After the 0.5.0 release (tag at 08:04 UTC), Rjae restarted and reloaded; the session started as a resume, and no
marketplace had refreshed since 08:01 UTC, so the machine still ran 0.4.2 at 09:13 UTC. At 09:17:51 UTC Claude
Code refreshed both auto-update marketplaces (`brigade`, `telder`) on its own and moved Telder to 0.5.0: the
refresh came about five minutes into the session, not at its start. What triggers it was not settled; the docs
say "on its own schedule" and no more. The skill is the one-step update for right now.

## What it does, and why each part

- **It reads the installs first** (`claude plugin list --json`) and acts on each `telder@<marketplace>` entry.
  Brigade's skill hardcodes `brigade@brigade`; Telder is also listed in Anthropic's directory, whose installs carry
  that marketplace's name, so the id is read, not assumed.
- **It refreshes only the marketplace an install came from**, then runs `claude plugin update <id> --scope
  <scope>`, user scope first. Brigade measured (E8, Claude Code 2.1.270) that a user-scope record decides the
  version in every folder, and that `not installed at scope …` only means that scope has no install.
- **It moves an existing install and nothing else**: no marketplace added or removed, nothing installed,
  uninstalled, enabled or disabled, and never `-y`, `--yes` or `--accept-command`. A directory user who runs it
  stays on what the directory serves, so the skill cannot route anyone around the directory's review.
- **`allowed-tools: Bash(claude plugin:*)`**, as Brigade's.
- **Where no shell or `claude` exists** (claude.ai), it says the app updates its plugins and runs nothing.
- **The listing's privacy section** says what the skill fetches and runs, because `CLAUDE.md` asks that a new
  fetch or a new program be said in the same commit. It is Claude Code's own fetch, made only when typed.

## Measured

- `claude plugin marketplace update anthropic-plugin-directory --json` refreshes the directory's catalog by name
  (`outcome: ok`). At 09:16 UTC it served Telder 0.4.2 at reviewed commit `573d266`, review state `none`.
- **The skill end to end, before release**: a nested `claude -p --plugin-dir ./plugin --setting-sources ""
  --model claude-sonnet-5-5 "/telder:update"` from a folder outside the repository, with every `CLAUDE*` and
  `AI_AGENT*` variable stripped and `TLDR_INNER=1`. No settings were loaded, so the skill's `allowed-tools` was
  the only permission. It ran `claude plugin list --json`, `claude plugin marketplace update telder` and
  `claude plugin update telder@telder --scope user`, with no permission denial, in 7.3 s and four turns, and
  answered that Telder was already at 0.5.0 and no reload was needed. The background update above had moved
  the install a minute earlier, so this run saw the already-current path; the release run below sees the other.
- **After the 0.6.0 release** (tag `v0.6.0`, release run 39754518207, CI run 39754515734 green on `fast` and
  `macos`): the same run, at 09:19:34 UTC with the install at 0.5.0. `claude plugin marketplace update telder`
  moved the install to 0.6.0 by itself (the marketplace has auto-update on), so `claude plugin update` answered
  `already at the latest version (0.6.0)`. The run still asked for `/reload-plugins`, and the cache now holds
  0.6.0 with both skills.

## 0.6.1: the reload rule

The two runs exposed a defect in 0.6.0's step 3, "if every install was already current, say that instead" of
asking for the reload. An install can be current while the session runs an older version: the background update
moves the install, not the session. That was Rjae's session that morning (0.4.2 loaded, 0.5.0 installed by 09:17),
and the first run above said no reload was needed. In 0.6.1 the skill reads the loaded version from the last
part of `${CLAUDE_PLUGIN_ROOT}` (`plugins/cache/<marketplace>/telder/<version>`, measured on this machine) and
asks for the reload unless it equals the installed version, or when the path ends in no version
(`--plugin-dir`).

Measured before the 0.6.1 release, with the working-tree skill copied under folders shaped like the cache
(`.../cache/telder/telder/0.5.0` and `.../0.6.0`) and loaded with `--plugin-dir`, the install at 0.6.0, the same
nested run as above:

| Loaded from | Answer |
| --- | --- |
| a `0.5.0` folder | runs 0.5.0, installed 0.6.0, type `/reload-plugins` |
| a `0.6.0` folder | runs 0.6.0, installed 0.6.0, current, no reload needed |
| `plugin/` in the repository | no version at the end of the path, type `/reload-plugins` |

Each run made the same three calls with no permission denial, which also shows that `${CLAUDE_PLUGIN_ROOT}` is
replaced by the loaded path in the skill's text. The release's own ids are on card 124.

## Not measured

- An install from the directory being updated by `claude plugin update telder@anthropic-plugin-directory`: this
  machine has only the `telder@telder` install, and a second install would double the hook.
- A project-scope or local-scope Telder install.
