# On this repository

The rules an agent follows when it changes Telder. `CLAUDE.md` imports every page below, so a Claude Code
session has them before its first prompt; `AGENTS.md` lists them for a harness that reads no imports. Each page is
one subject and is the only place its rules live.

## If you want to

| If you want to | Go to |
| --- | --- |
| commit, push, open or close a card, place a plan or a scratch file, name the thing | [Follow the conventions](#follow-the-conventions) |
| touch the plugin tree, the script, the nested call, a secret or a configuration directory | [Keep the invariants](#keep-the-invariants) |
| know what must pass before a push and before a release | [Pass the gates](#pass-the-gates) |
| add or change a page, an option's row, or the documentation gate | [Write documentation](#write-documentation) |
| change anything the directory lists or scans: the listing README, the icon, the manifest | [Respect the directory](#respect-the-directory) |

## Follow the conventions

1. `master`, merges only, never rebase; `make push message="<card>: <Imperative summary>"` or `/commit <card>`.
2. Plans in `.context/plans/`, scratch in `.ignored/`; `handoff-2026-09-30.md` is the state, `telder-build-2026-09-30.md` the record.
3. A card is done when shipped and nothing on it is open; then `/trello-done <card>`, unasked.
4. Telder is the product, `telder` the plugin; `/tldr` and `/telder:update` its skills; the script keeps the old spelling.

Details: [Conventions](conventions.md).

## Keep the invariants

1. One hook on `MessageDisplay`, one stdlib Python script in exec form, two skills, the icon; nothing else ships.
2. The nested `claude -p` runs with an argument array and the hook's own environment stripped by prefix; never `--bare`.
3. Never a secret in the output, a log, a card or a file under the project; never the transcript, never `sessions/*.key`.
4. `CLAUDE_CONFIG_DIR ?? ~/.claude`; state under `CLAUDE_PLUGIN_DATA`; every skill reachable by the model.

Details: [Invariants](invariants.md).

## Pass the gates

1. `make test lint plugin-check plugin-validate docs-check` before pushing anything under `plugin/`.
2. shellcheck 0.9.0 through Docker as well as the local one before pushing a shell file.
3. `make release version=X.Y.Z card=<n>`; a published tag is never moved.

Details: [Gates](gates.md).

## Write documentation

1. README → persona root → topic root → detail page; one `Details:` line names every leaf.
2. A plugin option is a row on the options page and in the listing; a `make` help line is `make docs-generate`.
3. `make docs-check` fails on the shape, a broken link, an orphan, an unlisted skill, an undocumented option or a
   missing changelog section.

Details: [Documentation](documentation.md).

## Respect the directory

1. Every push to `master` is a new version for Anthropic's directory, which scans it.
2. `plugin/README.md` is the listing and the privacy statement: a new read, write, send or run changes it in the
   same commit; never a dollar sign in it, never the icon's file name.
3. The name `telder` is permanent.

Details: [The directory](directory.md).
