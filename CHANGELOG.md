# Changelog

All notable changes to Telder are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
