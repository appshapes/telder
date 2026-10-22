# Uninstall

In a terminal:

```sh
claude plugin uninstall telder@telder
```

Then type `/reload-plugins` in any session that is open, or start a new one. An install from Anthropic's
directory is `telder@anthropic-plugin-directory` instead.

What goes with it:

- **The plugin's data directory**, by Claude Code's default: the mute marker from `/tldr off` and any pieces of
  a reply that was being shown. Nothing was written under your projects, so there is nothing to clean there.
- **Nothing else.** The plugin installed no program and changed no file of yours. A `.telder.md` you put at the
  root of a project is a file of that project, and stays until you remove it.

To stop the summaries without uninstalling, `/tldr off` holds them on this machine until `/tldr on`
([Pause and resume](../use/pause.md)).
