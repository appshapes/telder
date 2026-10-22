# Run the tests

```sh
make test                                                                      # everything, in seconds
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_tldr_hook.Instructions -v   # one class
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v         # what make test runs
```

`make test` first compiles `plugin/scripts/tldr-hook` (with `compile()`, not `py_compile`, which would drop a
`__pycache__` under `plugin/` that the allowlist rightly refuses), then runs every `tests/test_*.py` under
`unittest`. Nothing reaches the network and nothing needs a login: the nested `claude -p` is a fake that records
its arguments and answers what the test says.

| File | What it proves |
| --- | --- |
| `tests/test_tldr_hook.py` | the script, loaded as a module: word counting outside code and tables; the options, their bounds and garbage; the environment strip by prefix and a real child inheriting it; the command shape of the nested call; the cleaning of the model's answer; the two events (`MessageDisplay` chunks accumulating to one summary on the final chunk, the pieces readable by this user only, stale pieces swept; `Stop`); the heading's local date and time, taken when the reply ends; the `off`, `on`, `status`, `instructions` and `heading` command line; every instruction layer in order and the file rules; the skill's own copy of the instructions matching the script's |
| `tests/test_docscheck.py` | the documentation gate: green on the repository, green on an untouched copy, and one planted violation per check caught under that check's name ([Run the gate](../documentation/gate.md)) |
| `tests/fixtures/hook-input.json` | a `Stop` event with a 352-word reply, the input of `make hook-smoke` |

The tests set `sys.dont_write_bytecode` and `make test` sets `PYTHONDONTWRITEBYTECODE=1`, for the same reason as
the compile step: the plugin tree is an allowlist, and `--plugin-dir` would ship a cache.

For one real run of the hook, with a real model, `make hook-smoke` ([Try the plugin from your checkout](../setup/dev-loop.md)).
