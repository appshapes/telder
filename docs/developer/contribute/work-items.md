# Take a work item

Telder's work is on the Brigade Board of the team `appshapes`, which the team's repositories share with one
sequence of numbers (since 2026-11-13). A work item's number is the commit prefix, and a Telder work item carries
the tag `telder`. The board is a folder that Brigade's file sync keeps on every member's machine, so it needs the
Brigade plugin in this checkout, joined to the team ([Set up a clone](../setup/clone-and-tools.md)).

```sh
brigade work-item list                        # the board by list: Wanting (intake), Doing, Done
brigade work-item show 272                    # one work item: description, comments, history
brigade work-item add --tag telder <<'EOF'    # a new one, in Wanting
<the title, on one line>

<what is asked, and how to tell it is done>
EOF
```

In Claude Code, `/brigade:work-item` does the same in words (`/brigade:work-item 272`), and moves, assigns,
comments on, tags and edits one; `tag` sets exactly the tags given, so name the ones a work item has as well.

**`/work-item-start <number> [<collaborator session>]`** takes a work item from reading it to Done on its own,
asking you only where the work item leaves a real choice: it reads the work item, assigns it to you and moves it
to Doing, agrees the scope and the approach with you, builds under the rule files, proves each done criterion
against the running thing (`make hook-smoke` for the script, a session you start with `make plugin-dev` for a
skill or an option; a green build alone proves nothing), has the change reviewed, pushes it to `master` and
watches `ci.yml` until both jobs are green, cuts the release when the change is under `plugin/`, writes the
landing comment on the work item and moves it to Done. A second argument names another of your sessions that this
one leads over Brigade. In this repository it replaces the Brigade plugin's `/brigade:work-item-start`, which
knows none of Telder's gates.

**When a work item is finished.** Its done criteria are met and shipped (released, or on `master` with CI green
when no release carries it; a research or decision work item when its answer is on it) and nothing on it is open.
Then it gets a comment saying what shipped (the commits, the version and the release run) and moves to Done,
without being asked. It is never closed: closing is the owner's. When something is still open, the comment says
what and whose, and it stays in Doing. Never put a secret, a credential, a recipient's address or a customer's
name on a work item: the board is on every member's machine.

**Before 2026-11-13** the numbers in commits and records were cards of the AppShapes Trello board. That history
stays as it is; no card is open there, and a number of that time can name another work item on the board.

## A typical cycle

```
1.  /work-item-start 272              read, take, agree the scope, build, prove, review, push, CI, release, comment, Done
```

By hand, the same cycle:

```
1.  brigade work-item show 272        read it; assign it to yourself and move it to Doing
2.  work, in conversation             plans in .context/plans/, scratch in .ignored/, make test
3.  make plugin-dev                   try the plugin in a fresh Claude Code, from your own terminal
4.  /commit 272                       commit and push to master; watch ci.yml
5.  make release version=<v> work_item=272   when the change is under plugin/
6.  comment, move to Done             when every criterion is met and shipped
```

Step 3 runs in your own terminal, because a Claude Code session cannot start another one inside itself with a
clean environment.
