# Using Claude Code

How this repository is worked on with Claude Code: the slash-command skills, the daily workflow, the Trello CLI
the card numbers come from, and a reference for every command. Type any command directly in the Claude Code chat.

## Skills

Invoked via `/command`:
- `/commit <card>` - Commit, pull and push through `make push` with a `<card>: <Imperative summary>` message
- `/trello-create <title> [--board] [--list] [--from file.md]` - Create a Trello card (defaults: board AppShapes, list Wanting)
- `/trello-read <number | title | id>` - Read a Trello card: description, comments, checklists, attachments

The plugin's own skill, `/tldr`, is documented in [`plugin/README.md`](../plugin/README.md); it is the product,
not the tooling for working on it.

## Daily Workflow

Telder is developed on `master`: merges only, never rebase, and every commit goes through the `make push` gate
(pull, test, plugin-check). A card is on the AppShapes Trello board; its number is the commit prefix.

Your typical cycle for working on a card:

```
1.  /trello-read 45                     Read the card (or write one with /trello-create)
2.  Describe what you want, iterate,    Work with Claude Code; plans in .context/plans/,
    make test plugin-check              scratch in .ignored/ (gitignored)
3.  make plugin-dev                     Try the plugin in a fresh Claude Code (outside this session)
4.  /commit 45                          Commit and push to master when done
```

Steps 1 and 4 are slash commands; step 2 is normal conversation with Claude Code; step 3 runs in your own
terminal, because a Claude Code session cannot start another one inside itself with a clean environment.

## Trello CLI

The card numbers are Trello card numbers, and the two Trello skills use
[mheap/trello-cli](https://github.com/mheap/trello-cli):

1. `npm install -g trello-cli`
2. Create an API key at https://trello.com/power-ups/admin (New → API key).
3. `trello auth:api-key <key>` — it prints a token URL; open it, click Allow, copy the token.
4. `trello auth:token <token>`
5. `trello sync`
6. `trello board:list` — the AppShapes board should be listed.

The key and token live only in `~/.trello-cli/default/config.json` (and the secrets file the `trello-create`
skill names); they never appear in the repository, a card, or the chat.

## All Commands

### `/commit`

Analyze changes, generate a commit message (`<card>: <Imperative summary>`), confirm with you, then run
`make push`, which pulls, tests, checks the plugin tree, stages every working-tree change, commits and pushes. It
refuses without a numeric card number and stops on any gate failure.

Example: `/commit 45`

### `/trello-create`

Create a Trello card. Board defaults to `AppShapes`, list to `Wanting` (the other lists are Doing, Deploying, Releasing and
Supporting). With `--from file.md`, the file's first heading is the title and the rest is the description. Trello
assigns the card number; the title carries none.

Examples:
- `/trello-create Let the TL;DR heading be an option`
- `/trello-create --list Doing --from .ignored/card.md`

### `/trello-read`

Read a Trello card by number, title or id: description, comments, checklists, attachments. Search lags for a card
created in the last hour; the skill falls back to listing the board.

Example: `/trello-read 45`
