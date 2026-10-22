# Changelog

All notable changes to Telder are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **The date after the heading reads month, day, year.** The heading now ends like `TL;DR 10-22-2026 14:05`
  (it was `2026-10-22 14:05`), the order people read a date in. The time stays the hour and minute, 24-hour, in
  your machine's local time.

## [0.6.1] — 2026-10-22

### Fixed

- **`/telder:update` asks for `/reload-plugins` whenever your session runs an older Telder than is installed.**
  It said no reload was needed when the install was already current, which is also the case when Claude Code's
  background update moved the install after your session started. The session then kept running the old
  version. The skill now compares the version your session loaded with the one installed.

## [0.6.0] — 2026-10-22

### Added

- **`/telder:update` updates the plugin right now.** Claude Code updates Telder in the background when it
  refreshes the marketplace, on its own schedule, so a release can take a while to arrive. Type `/telder:update`:
  Claude refreshes the marketplace you installed from, moves your install to its current release, and asks you
  to type `/reload-plugins`. It moves an install you already have and nothing else; it never adds a marketplace
  or installs a plugin. An install from Anthropic's directory moves to the version the directory serves.

## [0.5.0] — 2026-10-22

### Added

- **The date and time after the heading.** The heading over every summary now ends with your machine's local
  date and time when the reply ended, in short form: `TL;DR 2026-10-22 14:05`. Scrolling back through a long
  session, you see when each reply landed. The `heading` option still sets the words. `/tldr` shows the same
  line, through a new `heading` command of the script. Nothing new leaves your machine.

## [0.4.2] — 2026-10-01

### Changed

- **The script no longer copies your environment.** The model call that writes the summary needs the environment
  your `claude` signs in with. The script used to copy all of it into that call; now it removes the variables
  that describe the session from its own environment, by name, and the call inherits the rest. The script reads
  the value of its own options, the project directory and its data directory, and of nothing else. What the
  summary sees and where it goes are unchanged.

## [0.4.1] — 2026-09-30

### Changed

- **`/tldr` no longer depends on the script.** Where the plugin's script cannot run, such as the chat on
  claude.ai, asking for a TL;DR of the last reply now follows a copy of the plugin's own instructions that the
  skill carries, in place of failing on the command. Nothing changes in Claude Code.

## [0.4.0] — 2026-09-30

### Added

- **A listing for Anthropic's plugin directory.** The plugin now carries an icon, the display name `Telder`, and
  links to its documentation, its support page and its privacy statement. The plugin's README is rewritten as
  that listing: what you see, three things to try, the options, and a section that says plainly what the plugin
  fetches, sends, reads, writes and runs on your machine, and for how long anything is kept.

### Changed

- **The plugin is now named `telder`** (it was `tldr`). A plugin's name is permanent once Anthropic's directory
  lists it, so it now carries the product's own name; `/tldr` and everything it does are unchanged. An install
  made under the old name gets no more updates. To move, in a terminal: `claude plugin uninstall tldr@telder`,
  `claude plugin marketplace update telder`, `claude plugin install telder@telder`, then `/reload-plugins` in your
  session. Options you had set need setting again, for example `Set the telder plugin's min_words to 200.`
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
