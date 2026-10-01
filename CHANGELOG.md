# Changelog

All notable changes to Telder are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **A listing for Anthropic's plugin directory.** The plugin now carries an icon, the display name `Telder`, and
  links to its documentation, its support page and its privacy statement. The plugin's README is rewritten as
  that listing: what you see, three things to try, the options, and a section that says plainly what the plugin
  fetches, sends, reads, writes and runs on your machine, and for how long anything is kept.

### Changed

- **The reply being shown is kept for your user only.** While a reply is on its way to the screen, its pieces
  wait in a file under the plugin's data directory. That file and its folder are now readable by your user alone
  (they followed the machine's default before, which on most machines lets other local users read them). The file
  is still deleted the moment the reply is complete.

## [0.3.0] — 2026-09-30

### Changed

- **A longer wait for the summary.** The default `timeout` is now `90` seconds (was `40`). Opus 5.5 took 27 seconds
  on a 350-word reply when measured, so a longer reply could have run past the old limit and been shown with no
  summary. The option still accepts 10 to 120.

## [0.2.0] — 2026-09-30

### Changed

- **Higher defaults.** `min_words` is now `300` (was `120`): a reply needs about three hundred words of prose
  before it gets a summary, so short and medium replies are shown as they are. `max_points` is now `10` (was
  `5`), the most the option allows, so a long reply's summary can carry more of its points. Both stay options.

## [0.1.0] — 2026-09-30

### Added

- **A TL;DR under every long reply.** When Claude Code finishes a reply longer than a few paragraphs, the `tldr`
  plugin appends a short summary: the most important points first, as a plain list, in simple language, for a
  reader with no time. A model writes it through your own `claude` login, Opus by default; nothing to configure, no API key.
- **Your own instructions for the summary.** The `instructions` option takes a sentence or a few, the
  `instructions_file` option a text file, and a `.telder.md` at the project root carries a team's; each is
  added to the plugin's own instructions, or `instructions_mode: replace` drops those. `/tldr instructions` shows
  the layers in effect, and `/tldr` follows the same ones.
