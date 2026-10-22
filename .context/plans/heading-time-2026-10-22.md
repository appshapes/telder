# The date and time after the heading — 2026-10-22

Card 123 on the AppShapes Trello board (`123: ...` commits). Asked by Rjae: "add short-form date and time to the
TL;DR heading, in local time", then release.

## What was decided, and why

- **The format is fixed: `YYYY-MM-DD HH:MM`**, local time, 24-hour, no seconds, no zone name. Short, sortable
  and readable in every locale. The C library's locale short forms (`%x %X`) were not used: the hook runs with
  whatever locale the session has, often none, and `%X` carries seconds.
- **The time is taken when the reply ends, not when the summary does.** Both handlers read the clock before the
  nested model call, which takes 5 to 30 seconds. A reader scrolling back sees when the reply landed.
- **The `heading` option sets the words only**; the stamp follows whatever it says. No option switches the stamp
  off: the feature is the stamp, and the option count stays at eight.
- **`/tldr` gets the same line through `tldr-hook heading [--heading TEXT]`**, because Claude does not know the
  clock. The skill runs it for the no-argument case and puts its one line over the list. Where the script cannot
  run (claude.ai), the heading stays the option's words alone.
- **Rendering.** `MessageDisplay` shows `**TL;DR** 2026-10-22 14:05`: the words bold, the stamp plain. `Stop`
  shows `TL;DR 2026-10-22 14:05` as plain text.
- **Nothing new leaves the machine.** The privacy statement's "Read on this machine" names the clock, since
  `CLAUDE.md` asks that reading something new be said in the same commit.

## Measured

- `make hook-smoke` (the `Stop` fixture, 352 words, Opus 5.5): `TL;DR 2026-10-22 04:02` over nine points in
  6.1 s.
- `tldr-hook heading` under `TZ=Asia/Tokyo` printed 17:02 while the machine (EDT) printed 04:02: local time is
  the process's zone.
- `make test` runs 46 tests.

## Release

`0.5.0`, 2026-10-22, cut by session `telder-1b` with `make release version=0.5.0 card=123`: the feature commit is
`cbd8d94`, the release commit `24f620a`, the tag `v0.5.0`; `release.yml` run 39744979763 published
https://github.com/appshapes/telder/releases/tag/v0.5.0, marked latest, with the changelog section as its notes.
`ci.yml` run 39744975460 on the release commit was green on both jobs (`fast`, `macos`); the run on `cbd8d94`
was cancelled, superseded by the release push. The runner's inventory step still prints shellcheck 0.9.0.
