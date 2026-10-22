# Set up a clone

```sh
git clone https://github.com/appshapes/telder.git
cd telder
make setup
make test
```

`make setup` checks the tools and sets `push.autoSetupRemote`; it installs nothing. `make test` compiles the hook
script and runs the unit tests with the nested `claude -p` faked, so it needs no login and no network.

| For | You need |
| --- | --- |
| `make test`, `make push`, `make docs-check` | Python 3.9 or newer, `make`, `git` |
| `make plugin-check`, `make lint` | shellcheck (`brew install shellcheck`); CI's runner has 0.9.0, see [Run the gate](../build-and-test/gates.md) |
| `make plugin-validate` | `claude` on `PATH`, not logged in |
| `make plugin-dev`, `make hook-smoke` | `claude` on `PATH`, logged in |
| `make release` | `gh`, logged in |
| the Trello skills | the Trello CLI ([Work a card](../contribute/cards.md)) |

`make help` lists every target with its help line; the generated page [make targets](../reference/make-targets.md)
is the same list.

## Working with Claude Code

The repository is worked on with Claude Code: `CLAUDE.md` is the agent's root and loads the rule files under
`docs/agent/repository/`; the project's own skills are `/commit`, `/trello-read`, `/trello-create` and
`/trello-done` ([Contribute](../contribute/README.md)). `.claude/settings.json` names the `telder` and `brigade`
marketplaces with auto-update on, so a session in this checkout has Telder itself installed and gets a TL;DR
under its own long replies.

Next: [Try the plugin from your checkout](dev-loop.md).
