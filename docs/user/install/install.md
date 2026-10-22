# Install the plugin

Telder installs from its own marketplace, which is this repository, with two commands typed in a Claude Code
session. It is also listed in Anthropic's plugin directory.

## From the marketplace

```
/plugin marketplace add appshapes/telder
/plugin install telder@telder
/reload-plugins
```

- The first command adds the `telder` marketplace: this public repository, cloned by Claude Code; no GitHub key is
  needed. A folder whose committed `.claude/settings.json` already names the marketplace skips it.
- Choose **user** when the second command asks where to install: one install for every folder under this Claude
  account, which one update moves. If it shows the plugin's options instead of asking, Telder is already
  installed.
- The marketplace has auto-update on, so Claude Code refreshes it on its own schedule and moves your install to
  the current release; [Update](../update/README.md) says how to do that right now.

## From Anthropic's directory

Telder is listed in Anthropic's plugin directory. An install made from there is named
`telder@anthropic-plugin-directory` and moves to the version the directory serves, which can trail this
repository while a new version is reviewed. `/telder:update` moves it to that version and no further.

## What you need

- **Claude Code**, in the terminal. The summary is added by a hook on the event Claude Code raises when it shows
  a reply. The chat on claude.ai runs no hooks, so no summary is added by itself there; asking for a TL;DR of the
  last reply still gets one, written under the plugin's own instructions.
- **`python3`**, 3.9 or newer, which macOS and Linux have. The script uses the standard library only; nothing is
  installed.
- **The `claude` command**, which the Claude Code install gives you, signed in as usual. The summary runs through
  that login, as one more short message from your own Claude Code, and counts against your plan's usage like
  any other short turn of the chosen model.

## What has been tested

The terminal, on macOS, with Claude Code 2.1.285, in an interactive session and in `-p` mode. The unit tests run
on Ubuntu and macOS on every push to `master`. Not tested yet: Windows, the desktop app's Code tab, the IDE
extensions, Cowork, and the chat on claude.ai.

## From a checkout

`claude --plugin-dir ./plugin` from a clone of this repository loads the plugin in place for that one session;
its options key is `telder@inline` instead of `telder@telder`. The developer's way to do that is
[Try the plugin from your checkout](../../developer/setup/dev-loop.md).

Next: [See what you get](../use/what-you-see.md).
