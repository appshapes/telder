# Documentation

One tree for humans, entered at `README.md`; one for agents, entered at `CLAUDE.md`; and a gate, `make docs-check`,
that a push and a release must pass. The rules themselves are the agent's
[Documentation](../../agent/repository/documentation.md) rule file; this topic is how to work with them.

## If you want to

| If you want to | Go to |
| --- | --- |
| add or change a page in the right place and shape | [Know the structure](#know-the-structure) |
| run the gate and read what it reports | [Run the gate](#run-the-gate) |

## Know the structure

1. README → persona root → topic root → detail page; `docs/<persona>/<topic>/<action>.md`.
2. A persona root: an `If you want to` table and one two-sentence section per topic. A topic root: the table and
   one TL;DR section per action with a `Details:` line. A detail page: the details, nothing else.
3. The listing, `SECURITY.md`, `CHANGELOG.md` and the records under `.context/plans/` are reference documents,
   reached from the tree and never copied into it.

Details: [Know the structure](structure.md).

## Run the gate

1. `make docs-check`; `make docs-generate` after a Makefile help line changes.
2. It runs in `make test`, CI's `fast` job, `scripts/release-prep.sh` and `release.yml`.

Details: [Run the gate](gate.md).
