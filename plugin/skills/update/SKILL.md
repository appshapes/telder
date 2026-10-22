---
name: update
description: >-
  Move the Telder plugin to its marketplace's current release from inside this session, then have the user run
  /reload-plugins. Use when the user asks to update Telder or the TL;DR plugin, or when you find this session's
  Telder is behind its marketplace's release and moving it is the next useful step.
user-invocable: true
allowed-tools: Bash(claude plugin:*)
---

# Update Telder

Run every command below from this session, one per Bash call, so it acts on this session's configuration
directory. Relay each command's result in a line.

## 1. Find the install

Run exactly this command:

```
claude plugin list --json
```

It prints the installs as a JSON array. Telder's are the entries whose `id` is `telder@<marketplace>`:
`telder@telder` for the plugin's own marketplace, another marketplace name for an install from Anthropic's
directory. Note each one's `id`, `scope` and `version`.

If there is no such entry, say in one line that Telder is not installed from a marketplace in this configuration
(a session started with `--plugin-dir`, for one), so there is nothing to update, and stop.

## 2. Refresh the marketplace, then update the install

For each marketplace among those ids, once:

```
claude plugin marketplace update <marketplace>
```

Then for each install, the `user` scope first:

```
claude plugin update telder@<marketplace> --scope <scope>
```

An answer of `not installed at scope …` is not a failure: a `project` or `local` install belongs to one folder
and is updated from a session in that folder. Say so in one clause and go on. An install from Anthropic's
directory moves to the version the directory serves, which can trail the plugin's own marketplace while a new
version is reviewed.

This skill moves an install that already exists and nothing else. Never add or remove a marketplace, and never
install, uninstall, enable or disable a plugin. Never pass `-y`, `--yes` or `--accept-command`: if a command asks
to confirm a command that a marketplace declares, stop and show the person what it asked.

## 3. The reload

This session runs the Telder it loaded when it started, from `${CLAUDE_PLUGIN_ROOT}`. For an install from a
marketplace, the last part of that path is the version this session runs. The installed version can be newer:
a marketplace with auto-update on moves the install when it refreshes, during step 2 or before this skill ran,
and the update then answers `already at the latest version` although this session runs an older one.

A new version loads only when the user runs `/reload-plugins` or starts a new session; nothing you can run does
that. End with one line: the version this session runs, the version now installed, and that they type
`/reload-plugins`. Say that Telder is current and no reload is needed only when the two versions are the same;
when the path does not end in a version (a session started with `--plugin-dir`), ask for the reload.

## If the command cannot be run

Where there is no shell or no `claude` command (the chat on claude.ai, for one), do not look for another way to
run it. Say in one line that the app updates its plugins itself, so there is nothing to run here.
