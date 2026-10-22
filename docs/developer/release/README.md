# Release

The current release is the one `plugin/.claude-plugin/plugin.json` pins. A release is one command on a clean
`master`, published by the workflow the tag triggers, and served to users by Claude Code's background update,
and by Anthropic's directory once it has reviewed the push.

## If you want to

| If you want to | Go to |
| --- | --- |
| cut a release | [Cut a release](#cut-a-release) |

## Cut a release

1. Write the `[Unreleased]` section of `CHANGELOG.md`; `make docs-check` must pass. A patch for a fix, a minor
   for a feature; `1.0.0` not yet.
2. `make release version=<v> card=<n>` on a clean `master` with `gh` logged in: pins the manifest, renames the
   section, commits `<n>: Release <v>` through `make push`, tags `v<v>`, pushes the tag.
3. `release.yml` guards and publishes; `gh run list --workflow release.yml` watches it. Comment the card with the
   version and close it.

Details: [Cut a release](cut-a-release.md).
