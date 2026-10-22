# Set up

## If you want to

| If you want to | Go to |
| --- | --- |
| set up a fresh clone and its tools | [Set up a clone](#set-up-a-clone) |
| try the plugin in a fresh Claude Code, or run the hook once for real | [Try the plugin from your checkout](#try-the-plugin-from-your-checkout) |

## Set up a clone

1. Python 3.9 or newer, `make`, `git`; shellcheck for `make lint` and `make plugin-check`; `claude` on `PATH`
   for `make plugin-validate`; `gh` logged in for `make release`.
2. `make setup` checks them and sets `push.autoSetupRemote`; `make test` runs in seconds with no login.

Details: [Set up a clone](clone-and-tools.md).

## Try the plugin from your checkout

1. `make plugin-dev` from your own terminal, never from inside a session: a fresh Claude Code with
   `--plugin-dir ./plugin`, the session's variables stripped.
2. `make plugin-dev opts='{"model":"claude-sonnet-5-5","min_words":40}'` sets options for that one session.
3. `make hook-smoke` runs the script once on the sample reply, for real, and prints the JSON reply and the
   timing line.

Details: [Try the plugin from your checkout](dev-loop.md).
