# Telder

A TL;DR under every long Claude Code reply: one Claude Code plugin (`plugin/`), which is one command hook on
`MessageDisplay`, one Python script and two skills, served from this repository's own marketplace and listed in
Anthropic's plugin directory. This file is the agent's root. The rule files below load with it; each is one
subject, and a rule lives in exactly one of them. Humans start at [README.md](README.md); the agent persona's own
page is [docs/agent/README.md](docs/agent/README.md).

@docs/agent/repository/conventions.md
@docs/agent/repository/invariants.md
@docs/agent/repository/gates.md
@docs/agent/repository/documentation.md
@docs/agent/repository/directory.md

# Overrides
- @./CLAUDE.user.md (optional, local-only, gitignored — absent in fresh clones)
