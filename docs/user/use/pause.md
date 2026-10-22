# Pause and resume

```
/tldr off
/tldr on
/tldr status
```

`/tldr off` stops the automatic summaries on this machine, in every session, until `/tldr on`. It takes effect
at once and needs no restart: the next reply in any session is shown without a summary. `/tldr status` says
which of the two is in effect.

The switch is a marker file named `mute` in the plugin's data directory, holding the time you typed `/tldr off`.
It is the only thing the plugin keeps between replies, and it is under your Claude Code plugin data, never under
a project. Uninstalling the plugin removes it.

While the summaries are off, `/tldr` still writes one on demand ([Get a TL;DR right now](on-demand.md)).

In the chat on claude.ai, where the plugin's script cannot run, `off`, `on` and `status` answer in one line
that the automatic summaries exist only in Claude Code.
