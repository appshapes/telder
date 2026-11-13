# Conventions: git, commits, work items, plans, names

- **Branch and history.** Work on `master`. Merges only: never `git rebase`, never `git pull --rebase`, never a
  force-push of pushed history. Integrate with `git pull --no-edit`.
- **A merge conflict is the session's to resolve, in place** (the owner's global rule, made this repository's on
  2026-11-13, work item 297). A pull conflicts when origin and local commits it has not seen change the same lines.
  1. Read what each side meant (`git log --merge -p`, and the work items its commits name), keep both, and leave
     no marker; fix as well what the merged tree breaks beyond the markers (a file that merged cleanly but fails
     combined).
  2. Stage the files the resolution touched, and none of the work's own uncommitted changes, then run the gates on
     the merged tree (`make test plugin-check`, and `make lint` for a shell file) until they pass.
  3. Conclude the merge with a commit that names every file that conflicted and how it was resolved:
     `git commit -m "<work item>: Merge origin/master: <file>: <how>; <file>: <how>"`.
  4. Push: `make push message="…"` when the work itself is still uncommitted, otherwise `make pull` then
     `git push`. If origin moved again, its new conflict is resolved the same way.

  When the pull refuses because an uncommitted change would be overwritten, no merge has started: `git stash`,
  `make pull`, `git stash pop`; resolve the markers the pop leaves as in step 1, clear the unmerged state with
  `git reset -q`, `git stash drop`, and run `make push` again with a message that also names each file that
  conflicted and how. Never `git merge --abort` to escape a conflict, never a rebase or a force-push to resolve
  one. When what one side meant cannot be told from the code, its
  commits and its work item, ask the user at once and leave the merge in progress, never aborted: until it is
  concluded, no other session in the checkout can pull.
- **Commit messages** are `<work item>: <Imperative summary>`, the number being the Brigade Board work item the
  work belongs to. Commit and push through `make push message="<work item>: …"` (pull, test, plugin-check, stage
  every working-tree change, commit, push) or the `/commit <work item>` skill, which is a port of it and runs it
  without asking for approval. `make push` stages everything in the checkout, including another session's edits:
  check `git status` first in a shared checkout.
- **Plans** go in `.context/plans/`; **ephemeral scratch** in `.ignored/` (gitignored) or the session's scratchpad.
  Never a stray file in the repository root. `.context/plans/handoff-2026-09-30.md` is the state of the work
  (append to it when a piece of work lands) and `telder-build-2026-09-30.md` the record of every measurement and
  decision; a feature gets a dated record page of its own beside them.
- **Work items.** Telder's work is on the Brigade Board of the team `appshapes`, which the team's repositories
  share with one sequence of numbers (since 2026-11-13, work item 272); a Telder work item carries the tag
  `telder`. `brigade work-item list` shows the board, `/brigade:work-item <number>` reads or changes one, and
  `brigade work-item add --tag telder`, the title on stdin, adds one in Wanting. `/work-item-start <number>
  [<collaborator session>]` takes one from reading it to Done: read, assigned to the user and moved to Doing, the
  scope agreed, built, proven, reviewed, on `master` with CI green, released when it changes what the plugin
  ships, the landing comment, moved to Done. In this repository it is the way to start a work item, not the
  plugin's `/brigade:work-item-start`, which knows none of these gates. A work item is finished when its done
  criteria are met and shipped (released, or on `master` with CI green when no release carries it; a research or
  decision work item when its answer is on it) and nothing on it is open. Then comment on it with what shipped
  and move it to Done without being asked. Never close it: closing is the owner's word. A comment carries no
  `Session stamp:` line, because the board records the member and the session. When something is still open,
  say what it is and leave it in Doing; never report a work item as done without having moved it. Never put a
  secret, a credential, a recipient's address or a customer's name on a work item: the board is a folder on
  every teammate's machine. Numbers in commits and records before 2026-11-13 are cards of the AppShapes Trello
  board, which holds no open card; they are history, and the same number on the board can be another piece of
  work.
- **Skills of this repository** live in `.claude/skills/`: [`commit`](../../../.claude/skills/commit/SKILL.md) and
  [`work-item-start`](../../../.claude/skills/work-item-start/SKILL.md). Each is linked here, and `make docs-check`
  fails on one that is not and on a link to one that is gone. The plugin's own skills (`plugin/skills/`) are the
  product.
- **Names.** Telder is the product and `telder` the plugin (`/plugin install telder@telder`; it was `tldr` until
  0.3.0, renamed for the directory, where a name is permanent and `tldr` drew three look-alike holds); `/tldr`
  and `/telder:update` are its skills; the script `tldr-hook`, its log prefix `tldr:` and `TLDR_INNER` keep the
  old spelling.
- **Dates** in plans and records are absolute (`2026-10-22`), never relative.
