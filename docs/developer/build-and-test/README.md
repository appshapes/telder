# Build and test

## If you want to

| If you want to | Go to |
| --- | --- |
| run what a push and a release must pass | [Run the gate](#run-the-gate) |
| run the unit tests, or one of them | [Run the tests](#run-the-tests) |
| know what each CI job and script does | [Know the CI](#know-the-ci) |
| see every make target with its help line | [See every make target](#see-every-make-target) |

## Run the gate

1. `make test lint plugin-check plugin-validate docs-check`.
2. `make push` runs `test` and `plugin-check` after the pull and before the commit; CI runs all five.
3. Shell goes through shellcheck 0.9.0 in Docker as well as the local one before a push.

Details: [Run the gate](gates.md).

## Run the tests

1. `make test`: the script compiles, then `tests/` runs under `unittest` with the nested `claude -p` faked; no
   login, no network.
2. One class: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_tldr_hook.Instructions -v`.

Details: [Run the tests](tests.md).

## Know the CI

1. `ci.yml`: `fast` on Ubuntu (the whole gate), `macos` (the tests under the user platform's `python3`);
   `release.yml` on a `v*` tag.
2. The `fast` job prints the runner's tool versions in its inventory step; shellcheck is 0.9.0 there.

Details: [Know the CI](ci.md).

## See every make target

1. `make help`, or the generated page.

Details: [make targets](../reference/make-targets.md).
