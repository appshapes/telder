# Try the plugin from your checkout

```sh
make plugin-dev                                                       # a fresh Claude Code with ./plugin loaded
make plugin-dev opts='{"model":"claude-sonnet-5-5","min_words":40}'   # with options for that one session
make plugin-dev mode=default                                          # a permission mode, passed through
make hook-smoke                                                       # the script once, on the sample reply, for real
```

**`make plugin-dev`** starts Claude Code with `--plugin-dir ./plugin`, so the session loads the plugin from the
checkout in place, under the id `telder@inline`. Run it from your own terminal, never from inside a session: a
Claude Code session cannot start another one inside itself with a clean environment, and the Makefile strips
every `CLAUDE*` and `AI_AGENT*` variable of the calling shell before launching, keeping only
`CLAUDE_CONFIG_DIR`. The strip is by prefix, never by a list of names: Brigade measured the enumerated list
short by three names, and the next release of Claude Code can add more. `CLAUDE_CONFIG_DIR` survives because it
is how a second persona on one machine keeps its own login. `opts` is the plugin's option object for that one
session, passed through `--settings`; `mode` is a permission mode.

Ask the session a long question and watch the reply end with the rule, the heading and the list. A session
started this way also has `/tldr` and `/telder:update`; the second finds no marketplace install and says so.

**`make hook-smoke`** runs `plugin/scripts/tldr-hook` once on `tests/fixtures/hook-input.json`, a 352-word sample
reply, with a real nested `claude -p` under your login, and prints the hook's JSON reply and the `tldr:` timing
line. It is the quickest way to try a change to the instructions or the model, and the only target of
`make test`'s neighbours that reaches the network.

A change to the script needs no restart of `make plugin-dev`: the hook is read from disk at every reply.
