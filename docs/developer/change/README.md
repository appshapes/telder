# Change

## If you want to

| If you want to | Go to |
| --- | --- |
| change the hook script, the nested call, or the instruction layers | [Change the script](#change-the-script) |
| add or change a plugin option | [Change an option](#change-an-option) |
| change what Anthropic's directory lists, or the privacy statement | [Change the listing](#change-the-listing) |
| know where things are | [Know the layout](#know-the-layout) |

## Change the script

1. One file, `plugin/scripts/tldr-hook`, Python 3 standard library, launched in exec form; stdout carries the
   hook's JSON reply and nothing else.
2. The nested `claude -p` runs with an argument array and the hook's own environment stripped by prefix; never
   `--bare`, never a copy of the environment.
3. `instruction_parts` is the layering; a change to a layer changes `/tldr instructions`, the tests and the pages
   that list the layers.

Details: [Change the script](script.md).

## Change an option

1. The manifest's `userConfig`, then `DEFAULTS` and the bounds in the script, which reads each option from its
   `CLAUDE_PLUGIN_OPTION_<NAME>` variable.
2. The default appears in three places: the manifest, `docs/user/configure/options.md` and `plugin/README.md`;
   the gate holds the two pages.

Details: [Change an option](options.md).

## Change the listing

1. `plugin/README.md` is what the directory shows, and its privacy section is what `privacyPolicyUrl` names;
   when the script reads, writes, sends or runs something new, that section changes in the same commit.
2. Never a dollar sign in it, never the icon's file name; links in it are absolute.

Details: [Change the listing](listing.md).

## Know the layout

1. `plugin/` ships; everything else is the repository around it.

Details: [Know the layout](layout.md).
