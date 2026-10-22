# Telder

[![release](https://img.shields.io/github/v/release/appshapes/telder)](https://github.com/appshapes/telder/releases/latest)

A TL;DR under every long Claude Code reply. When a reply runs past a few paragraphs, the `telder` plugin adds a
short list under it: the most important points first, in simple language, for a reader with no time. A model
writes it through your own `claude` login, Opus by default. Nothing to configure, no API key.

```
  ... Dust, smoke and water droplets can make those colors even stronger.
  ---
  TL;DR 10-22-2026 14:05
  - Blue light scatters far more than red as sunlight crosses the air, so the sky looks blue.
  - The sun gives off less violet and our eyes see blue better, so the sky is not violet.
  - At sunrise and sunset light crosses much more air, which scatters the blue away and leaves red.
```

## Who are you?

- **[User](docs/user/README.md)** — you use Claude Code and want the long replies summarized: install the plugin,
  read what it adds, tune what it focuses on, update it, know what leaves your machine.
- **[Developer](docs/developer/README.md)** — you work on Telder itself: set up a clone, pass the gates, change
  the script or the listing, cut a release, write the documentation.
- **[AI Agent](docs/agent/README.md)** — you are the model: in a session, the plugin's skills are your
  documentation; on this repository, `CLAUDE.md` and `AGENTS.md` are.
