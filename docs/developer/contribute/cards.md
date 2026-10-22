# Work a card

A ticket is a card on the AppShapes Trello board, and its number is the commit prefix. Three skills in Claude
Code use [mheap/trello-cli](https://github.com/mheap/trello-cli):

| Skill | Does |
| --- | --- |
| `/trello-read <number \| title \| id>` | the card's description, comments, checklists, attachments; search lags for a card created in the last hour, so the skill falls back to listing the board |
| `/trello-create <title> [--board] [--list] [--label] [--from file.md]` | a card; defaults: board AppShapes, list Wanting, label Telder. Every card carries exactly one project label, one of the board's. Plain titles; Trello assigns the number. `--from file.md` takes the title from the first heading and the description from the rest |
| `/trello-done <number \| id>` | the closing comment (what shipped, the version or commit, the date, what was left out and where it went), the complete check, the archive |

**The board.** Its open lists are project lists, one per product (Brigade, Cavalry, Website, Canary), plus
Wanting for intake and Hibernating for work set aside; a Telder card goes in Wanting with the label Telder.

**When a card is done.** Its done criteria are met and shipped (released, or merged when no release carries it;
a research or decision card when its answer is on the card) and nothing on it is open. Then run
`/trello-done <card>` without being asked. When something is still open, say what it is and leave the card;
never report a card as done without having run it. Never put a secret, a credential, a recipient's address or
a customer's name on a card: the board is as public as the repository.

## Setting up the CLI

1. `npm install -g trello-cli`
2. Create an API key at https://trello.com/power-ups/admin (New → API key).
3. `trello auth:api-key <key>`: it prints a token URL; open it, Allow, copy the token.
4. `trello auth:token <token>`
5. `trello sync`
6. `trello board:list` should list AppShapes.

The key and token live only in `~/.trello-cli/default/config.json`; they never appear in the repository, a card or
the chat. If a command says `no such table: boards`, run `trello sync` once and retry.

## A typical cycle

```
1.  /trello-read 127                  read the card (or write one with /trello-create)
2.  work, in conversation             plans in .context/plans/, scratch in .ignored/, make test
3.  make plugin-dev                   try the plugin in a fresh Claude Code, from your own terminal
4.  /commit 127                       commit and push to master
5.  /trello-done 127                  when every criterion is met and shipped
```

Steps 1, 4 and 5 are slash commands; step 2 is normal conversation with Claude Code; step 3 runs in your own
terminal, because a Claude Code session cannot start another one inside itself with a clean environment.
