# Change the listing

The plugin is submitted to Anthropic's plugin directory from this repository, folder `plugin`, branch `master`,
through the developer portal at `claude.ai/directory/manage`. The directory scans every new commit on `master`,
so a push is also a submission of a new version: a push that passes the scan goes live, and one that draws a
hold waits for a reviewer. The rules are the agent's [The directory](../../agent/repository/directory.md) rule
file; this page is what to do when you change one of the things it names.

## The listing README

`plugin/README.md` is what the directory shows as the plugin's description. It is written for a reader who
never sees this repository: what you see, three things to try, what you need, the options, the instructions in
layers, what leaves your machine, how the summary is made, when no summary appears, what has been tested,
support. Links in it are absolute. It carries its own copy of the options table, so an option's default
changes there as well as in the manifest and the options page ([Change an option](options.md)).

Its section "What leaves your machine, and where it goes" is the privacy statement: the manifest's
`privacyPolicyUrl` points at that heading, so the heading's wording is an anchor and does not change. When the
script starts to read, write, send or run something new, the section changes in the same commit, with the
bullets it has: fetched, sent and to where, never sent, read on this machine, written on this machine, run,
kept for how long.

Two things the directory's scan holds, which `make plugin-check` refuses before a push: a dollar sign anywhere
in the README (the scan reads a shell variable beside a URL as a credential leaving the machine; Brigade
measured it on `PWD` with its sigil), and the icon's file name (the scan holds a bundled image that a README
names).

## The manifest

`plugin/.claude-plugin/plugin.json` carries the listing fields: `displayName` (`Telder`, the label that can
change; `name` is `telder` and is permanent once listed), `description`, `author`, `homepage`, `repository`,
`documentationUrl` (the User tree), `supportUrl` (the issues page), `privacyPolicyUrl` (the section above),
`license`, `keywords`, and `version`, which `make release` raises.

## The icon

`plugin/.claude-plugin/icon.png` is a square PNG, 512 to 2048 px a side and under 2 MB (`plugin-check` reads the
size from the PNG header), rendered at 1024 px from `docs/assets/icon.svg` in a browser: a screenshot of the
`svg` element with a transparent background. The directory takes its copy once, the first time the submission
is saved or submitted in the portal, so a new icon in the repository does not change the listing afterwards.

## What the portal checks

Anthropic's [plugin pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist) lists
the checks and what each finding means. `.context/plans/directory-submission-2026-09-30.md` records what the
portal said about Telder, which holds were cleared and how (the rename to `telder`, the environment read by
name), and why each remaining warning is left for a reviewer.
