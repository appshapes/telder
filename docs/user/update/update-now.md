# Update right now

```
/telder:update
/reload-plugins
```

Claude runs Claude Code's own plugin commands in your session, where you see them, and relays each result in a
line:

1. `claude plugin list --json`, to find your installs: `telder@telder` for the plugin's own marketplace,
   `telder@anthropic-plugin-directory` for one from Anthropic's directory.
2. `claude plugin marketplace update <marketplace>`, once per marketplace those installs came from.
3. `claude plugin update telder@<marketplace> --scope <scope>` for each install, the user scope first. An answer
   of `not installed at scope …` is not a failure: a project or local install belongs to one folder and is
   updated from a session in that folder.
4. One line saying which version this session runs, which is now installed, and that you type
   `/reload-plugins`. A new version loads only when you do, or when you start a new session. It says no reload
   is needed only when the two versions are the same.

The skill moves an install that already exists and nothing else: it never adds or removes a marketplace, never
installs, uninstalls, enables or disables a plugin, and never answers a confirmation for you. An install from
Anthropic's directory moves to the version the directory serves, which can trail this repository while a new
version is reviewed.

## The background update

The marketplace entry has auto-update on. Claude Code refreshes it on its own schedule, which is not at every
session start: on 2026-10-22 a resumed session ran the old version for five minutes before the refresh came, and
an update that arrives after a session starts leaves that session on the version it loaded. When it refreshes,
it moves the install and tells you to type `/reload-plugins`. `/telder:update` is the same move, right now.

## In a terminal

The same two commands by hand, for an install from the marketplace:

```sh
claude plugin marketplace update telder
claude plugin update telder@telder
```

Then `/reload-plugins` in your session.
