# Developer

You work on Telder itself: one Python script, one hook, two skills and the pages around them, developed on
`master` through one gate that every push and every release passes, and scanned by Anthropic's directory at every
push.

## If you want to

| If you want to | Go to |
| --- | --- |
| set up a clone, or try the plugin from your checkout | [Set up](setup/README.md) |
| run the gate, the tests, or read what CI does | [Build and test](build-and-test/README.md) |
| change the script, an option, the directory listing, or know the layout | [Change](change/README.md) |
| cut a release | [Release](release/README.md) |
| commit, or work a card | [Contribute](contribute/README.md) |
| add or change documentation, and keep the gate green | [Documentation](documentation/README.md) |
| read the build record, the directory record and the feature records | [Evidence](evidence/README.md) |

## Set up

Python 3.9 or newer, `make`, `git`, then `make setup`. [Set up](setup/README.md) adds the dev loop that starts a
fresh Claude Code with your checkout's plugin.

## Build and test

`make test lint plugin-check plugin-validate docs-check` is the acceptance gate, login-free.
[Build and test](build-and-test/README.md) covers what each part checks and what CI runs.

## Change

The script is one stdlib file in exec form, an option lives in three places, and the listing is read by a
scanner. [Change](change/README.md) has each surface.

## Release

`make release version=<v> card=<n>` pins, renames the changelog section, commits and tags; the workflow
publishes. [Release](release/README.md) includes the recovery path.

## Contribute

`<card>: <Imperative summary>` through `make push`, merges only, a Trello card per piece of work.
[Contribute](contribute/README.md) also covers closing the card.

## Documentation

One tree for humans, one for agents, and a gate a release cannot pass without. [Documentation](documentation/README.md)
is the structure and the gate.

## Evidence

Every measurement and decision has a dated record under `.context/plans/`. [Evidence](evidence/README.md) points
at them.
