# Commit and push

Telder is developed on `master`: merges only, never rebase, and every commit goes through one chain:

```sh
make push message="127: Redesign the documentation around three personas"
```

`make commit` pulls (`git pull --no-edit`, a plain merge), runs the tests (the documentation gate among them)
and `plugin-check`, stages **every** working-tree change (`git add --verbose :/ .`) and commits; `make push`
adds the push. In a shared checkout, check `git status` first: another session's edits are staged too.

**A merge conflict** in the pull is resolved in place, never escaped with `git merge --abort`, a rebase or a
force-push. Keep what both sides meant (`git log --merge -p` shows the commits on each side), stage the files the
resolution touched but not your own uncommitted work, run the gates on the merged tree, and conclude the merge with
a commit that names each file and how it was resolved; then push:

```sh
git add Makefile docs/developer/README.md
make test plugin-check
git commit -m "297: Merge origin/master: Makefile: kept both targets; docs/developer/README.md: both rows"
make pull && git push       # or make push message="...", when your work is still uncommitted
```

When the pull refuses because an uncommitted change would be overwritten, no merge has started: `git stash`,
`make pull`, `git stash pop`, resolve the markers the pop leaves, `git reset -q`, `git stash drop`, and `make push`
again, its message naming what conflicted. When what a side meant cannot be told from the code, its commits and its
work item, ask whoever wrote it, and leave the merge in progress meanwhile. The agent's rule is
[Conventions](../../agent/repository/conventions.md); a Claude Code session follows it on its own and asks you only
in that last case.

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
