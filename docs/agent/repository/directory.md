# The directory: what Anthropic's plugin directory asks of every push

Anthropic's plugin directory takes the plugin from `plugin/` on `master` and scans every new commit there, so a
push is also a submission of a new version (`.context/plans/directory-submission-2026-09-30.md` records what the
portal found and why each remaining hold is left for a reviewer). What that asks of a change:

- **`plugin/README.md` is the listing.** The directory shows it as the description, and its section "What leaves
  your machine, and where it goes" is the privacy statement the manifest's `privacyPolicyUrl` points at. When the
  script starts to read, write, send or run something new, that section changes in the same commit. Links in it
  are absolute, because the listing is shown outside the repository. It carries its own copy of the options
  table.
- **No dollar sign in `plugin/README.md`, and no mention of the icon file.** The directory's scan reads a shell
  variable beside a URL as a credential leaving the machine, and holds a bundled image that a README names.
  `make plugin-check` refuses both.
- **The icon** is `plugin/.claude-plugin/icon.png`, a square PNG rendered at 1024 px from `docs/assets/icon.svg`
  in a browser. The directory takes its copy once, the first time the submission is saved or submitted in the
  portal, so a new icon in the repository does not change the listing afterwards.
- **The name `telder` is permanent** once listed; `displayName` (`Telder`) is the label that can change.
- **Raise `version` with every release**, which `make release` does. An install from the directory moves to the
  version the directory serves, which can trail this repository while a new version is reviewed; `/telder:update`
  never routes anyone around that review.
- **The checks the portal runs**, and what each finding means, are in Anthropic's
  [plugin pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist).
