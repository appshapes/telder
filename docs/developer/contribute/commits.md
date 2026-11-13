# Commit and push

Telder is developed on `master`: merges only, never rebase, and every commit goes through one chain:

```sh
make push message="127: Redesign the documentation around three personas"
```

`make commit` pulls (`git pull --no-edit`, a plain merge), runs the tests (the documentation gate among them)
and `plugin-check`, stages **every** working-tree change (`git add --verbose :/ .`) and commits; `make push`
adds the push. In a shared checkout, check `git status` first: another session's edits are staged too. On a
merge conflict, stop and hand it back; never `git merge --abort` into a rebase, never a force-push.

- **The message** is `<work item>: <Imperative summary>`, the number being the Brigade Board work item the work
  belongs to ([Take a work item](work-items.md)). `/commit <work item>` in Claude Code writes the message from the
  diff, prints the command and runs the chain without asking; it refuses without a numeric work item and stops
  for anything in the diff that looks like a secret.
- **Plans** go in `.context/plans/`, **scratch** in `.ignored/` (gitignored); never a stray file in the root. A
  piece of work that lands appends its lines to `.context/plans/handoff-2026-09-30.md`, the state of the work,
  and a feature gets a dated record page beside it ([Evidence](../evidence/README.md)).
- **Shell** goes through shellcheck 0.9.0 in Docker before a push ([Run the gate](../build-and-test/gates.md)).
- **Every push is a submission.** Anthropic's directory scans each commit on `master`, so a change under
  `plugin/` passes the whole gate first ([Change the listing](../change/listing.md)).
- **Documentation** moves with the change: a changed procedure changes its leaf and its TL;DR; a new `make`
  help line runs `make docs-generate`; a new option gets its row on two pages; a change the user sees gets
  its `[Unreleased]` entry ([Documentation](../documentation/README.md)).
