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
- **After the release**: the same run is how this machine moves to 0.6.0; its result is on card 124.

## Not measured

- An install from the directory being updated by `claude plugin update telder@anthropic-plugin-directory`: this
  machine has only the `telder@telder` install, and a second install would double the hook.
- A project-scope or local-scope Telder install.
