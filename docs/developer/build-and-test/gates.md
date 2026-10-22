# Run the gate

```sh
make test lint plugin-check plugin-validate docs-check
```

The acceptance gate. `make push` runs `test` and `plugin-check` after the pull and before the commit; CI's `fast`
job runs all five on every push. `make help` lists every target, and a trailing ` (CI)` marks the ones a workflow
step invokes.

| Target | Checks | Needs |
| --- | --- | --- |
| `make test` | the hook script compiles; `tests/test_tldr_hook.py` with the nested `claude -p` faked; `tests/test_docscheck.py`, the documentation gate against the tree and against copies with a violation planted | `python3` |
| `make lint` | `shellcheck -s sh` on every shell script under `scripts/` | shellcheck |
| `make plugin-check` | `scripts/ci/plugin-check.sh`: the `plugin/` file allowlist, the script's mode in git, the version pin, no `bin/` or MCP, exec-form hooks with a timeout each, the script compiles, `sh -n` and shellcheck, every skill reachable by the model, the listing icon's shape, and the two rules for the listing README the directory's scan enforces; then `scripts/ci/no-secrets.sh`, nine credential shapes over every tracked and plugin file | shellcheck |
| `make plugin-validate` | `claude plugin validate` on the marketplace and, strictly, on the plugin; login-free | `claude` |
| `make docs-check` | `scripts/ci/docscheck.py check`: the same rules `make test` runs, printed one finding per line ([Run the gate](../documentation/gate.md)) | `python3` |

## shellcheck is pinned

CI's Ubuntu runner has shellcheck **0.9.0**, printed by `ci.yml`'s inventory step (run 36756274811); this machine
has 0.11, and versions disagree (0.9.0 reported SC2015 for `A && B || C`; 0.11 did not). Before pushing a shell
file, run CI's version as well as the local one:

```sh
docker run --rm -v "$PWD:/mnt" -w /mnt koalaman/shellcheck:v0.9.0 -s sh scripts/ci/*.sh scripts/*.sh
```

The pin lives in the agent's [Gates](../../agent/repository/gates.md) rule file; re-pin it whenever the
inventory step prints a different version.

## Before pushing anything under plugin/

Run all five. Every push to `master` is also a submission of a new version to Anthropic's directory
([Change the listing](../change/listing.md)), so the tree that leaves your machine is the tree the directory
scans.
