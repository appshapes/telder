# Contribute

## If you want to

| If you want to | Go to |
| --- | --- |
| commit and push a change | [Commit and push](#commit-and-push) |
| read, add or take to Done the work item the work belongs to | [Take a work item](#take-a-work-item) |

## Commit and push

1. `make push message="<work item>: <Imperative summary>"`, or `/commit <work item>` in Claude Code.
2. `master` only, merges only, never rebase; plans in `.context/plans/`, scratch in `.ignored/`.

Details: [Commit and push](commits.md).

## Take a work item

1. The number in a commit message is a work item of the team's Brigade Board, tagged `telder`:
   `brigade work-item list`, `brigade work-item show <n>`, and `brigade work-item add --tag telder` with the title
   on stdin.
2. `/work-item-start <n>` in Claude Code takes one from reading it to Done: taken, scope agreed, built, proven,
   reviewed, on `master` with CI green, released when the plugin changes, the landing comment.
3. A work item is finished when shipped and nothing on it is open: then it moves to Done, unasked, and is never
   closed.

Details: [Take a work item](work-items.md).
