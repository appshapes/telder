# Install

Telder is a Claude Code plugin: one hook, one script, two skills. Nothing is compiled, nothing is downloaded by
the plugin itself, and no account is created.

## If you want to

| If you want to | Go to |
| --- | --- |
| install the plugin in Claude Code | [Install the plugin](#install-the-plugin) |
| move an install made under the old name, `tldr` | [Move from the old name](#move-from-the-old-name) |
| remove the plugin | [Uninstall](#uninstall) |

## Install the plugin

1. Open Claude Code.
2. Type `/plugin marketplace add appshapes/telder`.
3. Type `/plugin install telder@telder`. When it asks where to install, choose **user**.
4. Type `/reload-plugins`.

You need `python3`, 3.9 or newer (macOS and Linux have it), and the `claude` command on your `PATH`, which the
Claude Code install gives you.

Details: [Install the plugin](install.md).

## Move from the old name

1. In a terminal: `claude plugin uninstall tldr@telder`, `claude plugin marketplace update telder`,
   `claude plugin install telder@telder`.
2. Type `/reload-plugins` in your session, and set the options you had again under the new name.

Details: [Move from the old name](old-name.md).

## Uninstall

1. In a terminal: `claude plugin uninstall telder@telder`, then `/reload-plugins` in your session.
2. The plugin's data directory goes with it; nothing was written under your projects.

Details: [Uninstall](uninstall.md).
