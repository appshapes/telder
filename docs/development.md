# Working on Telder

The developer's page: how a clone is set up, how the repository is laid out, what gates a change, and how a
release is cut. Users want the front [`README.md`](../README.md) and [`plugin/README.md`](../plugin/README.md).

## If you want to

| If you want to | Go to |
| --- | --- |
| set up a fresh clone | [Setup](#setup) |
| see every target | `make help` |
| run the tests | `make test` |
| run the whole gate | [Gates](#gates) |
| run the hook once on a sample reply, for real | `make hook-smoke` |
| try the plugin in a fresh Claude Code | `make plugin-dev`, from your own terminal — [The dev loop](#the-dev-loop) |
| commit and push | `make push message="<card>: …"`, or `/commit <card>` |
| read or create a Trello card | [`docs/claude-code-usage.md` › Trello CLI](claude-code-usage.md#trello-cli) |
| cut a release | [Releases](#releases) |
| change what Anthropic's directory lists | [The directory listing](#the-directory-listing) |
| see what a CI script does | [Layout](#layout) |

## Setup

Python 3.9 or newer, `make`, `git`, then `make setup`: it checks the tools and sets `push.autoSetupRemote`.

| For | You also need |
| --- | --- |
| `make test`, `make push` | nothing more |
| `make plugin-check`, `make lint` | shellcheck (`brew install shellcheck`) |
| `make plugin-validate`, `make plugin-dev`, `make hook-smoke` | `claude` on `PATH`; the last two logged in |
| `make release` | `gh`, logged in |
| the Trello skills | [trello-cli](claude-code-usage.md#trello-cli) |

## Gates

The acceptance gate is `make test lint plugin-check plugin-validate`. `make push` runs `test` and `plugin-check`
after the pull and before the commit; `make help` lists every target, and a trailing ` (CI)` marks the ones a
workflow step invokes.

- `make test`: the hook script compiles, and `tests/test_tldr_hook.py` runs with the nested `claude -p` faked, so
  it needs no login and no network.
- `make plugin-check`: `scripts/ci/plugin-check.sh` (the `plugin/` file allowlist, the script's mode in git, the
  version pin, no `bin/` or MCP, exec-form hooks with a timeout each, the script compiles, shellcheck, every
  skill reachable by the model, the listing icon's shape and two rules for the plugin README that the
  directory's scan enforces) and then `scripts/ci/no-secrets.sh` (nine credential shapes over every tracked and
  plugin file).
- `make plugin-validate`: `claude plugin validate` on the marketplace and, strictly, on the plugin. Login-free.

`master` only, merges only, never rebase; commit messages `<card>: <Imperative summary>`, through
`make push message="<card>: …"` — the number is the card on the AppShapes Trello board the work belongs to.
Plans live in `.context/plans/`, ephemeral scratch in `.ignored/` (gitignored).

## The dev loop

`make plugin-dev` starts a fresh Claude Code with `--plugin-dir ./plugin`, with every `CLAUDE*` and `AI_AGENT*`
variable of the calling session stripped (only `CLAUDE_CONFIG_DIR` survives), so run it from your own terminal,
never from inside a session. `make plugin-dev opts='{"model":"claude-haiku-4-5-20251001","min_words":40}'` sets
options for that one session; `mode=default` and the other permission modes pass through.

`make hook-smoke` runs the script once on `tests/fixtures/hook-input.json` with a real nested call and prints the
JSON reply and the timing line, which is the quickest way to try a prompt change.

## Releases

`make release version=X.Y.Z card=<n>` (`scripts/release-prep.sh`) bumps `plugin/.claude-plugin/plugin.json`,
renames the changelog's `[Unreleased]` section to the version and today's date under a fresh `[Unreleased]`,
commits through the push chain as `<n>: Release X.Y.Z`, tags `vX.Y.Z` and pushes the tag. `release.yml` then
checks that the manifest pins the tag, takes that changelog section (`scripts/ci/release-notes.sh`) and publishes
the GitHub release with it as the notes. Claude Code updates the plugin from the marketplace in the background
and asks for `/reload-plugins`. A published tag is never moved: bump the patch version instead. A tree that has
never been released carries `0.0.0`, which the script refuses to release.

## The directory listing

The plugin is submitted to Anthropic's plugin directory from this repository, folder `plugin`, branch `master`,
through the developer portal at `claude.ai/directory/manage`. The directory scans every new commit on `master`,
so a push is also a submission of a new version. What that asks of a change:

- **`plugin/README.md` is the listing.** The directory shows it as the description, and its section "What leaves
  your machine, and where it goes" is the privacy statement the manifest's `privacyPolicyUrl` points at. When the
  script starts to read, write, send or run something new, that section changes in the same commit. Links in it
  are absolute, because the listing is shown outside the repository. It carries its own copy of the options
  table, so an option's default changes in three places: the manifest, the front README and the plugin README.
- **No dollar sign in `plugin/README.md`, and no mention of the icon file.** The directory's scan reads a shell
  variable beside a URL as a credential leaving the machine, and holds a bundled image that a README names.
  `make plugin-check` refuses both.
- **The icon** is `plugin/.claude-plugin/icon.png`, a square PNG rendered at 1024 px from
  `docs/assets/icon.svg` in a browser (a screenshot of the `svg` element with a transparent background). The
  directory takes its copy once, the first time the submission is saved or submitted in the portal, so a new
  icon in the repository does not change the listing afterwards.
- **The name `telder` is permanent** once listed; `displayName` (`Telder`) is the label that can change.
- **Raise `version` with every release**, which `make release` does.

The checks the portal runs, and what each finding means, are in Anthropic's
[plugin pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist);
`.context/plans/directory-submission-2026-09-30.md` records what the portal said about Telder and why each
remaining hold is left for a reviewer.

## Layout

| Path | What |
| --- | --- |
| [`CHANGELOG.md`](../CHANGELOG.md) | what changed in each release |
| `plugin/.claude-plugin/plugin.json` | the manifest: name `telder`, the version pin, the options |
| `plugin/hooks/hooks.json` | the one hook, exec form |
| `plugin/scripts/tldr-hook` | the script: reads the hook input, gates on length, runs the nested `claude -p`, replies |
| `plugin/skills/tldr/SKILL.md` | `/tldr`, `/tldr off`, `/tldr on`, `/tldr status` |
| [`plugin/README.md`](../plugin/README.md) | the plugin's own page and its listing in Anthropic's directory: what it does, its options, what leaves the machine |
| `plugin/.claude-plugin/icon.png` | the listing icon, rendered from [`docs/assets/icon.svg`](assets/icon.svg) |
| `tests/` | the unit tests and the sample hook input |
| `scripts/ci/` | `plugin-check.sh`, `no-secrets.sh`, `release-notes.sh` |
| `scripts/release-prep.sh` | the release sequence |
| `.claude-plugin/marketplace.json` | the `telder` marketplace that serves the plugin |
| `.claude/` | the project's skills (`/commit`, `/trello-create`, `/trello-read`) and the marketplace entry |
| [`docs/claude-code-usage.md`](claude-code-usage.md) | how the repository is worked on with Claude Code |
| `.context/plans/` | the plans and the build notes |
