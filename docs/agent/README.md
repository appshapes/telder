# AI Agent

You are the model. In a Claude Code session with Telder installed, the plugin's two skills are your documentation,
and a second model, called by the hook, writes the summaries; on this repository you are a contributor, and
`CLAUDE.md` is your root.

## If you want to

| If you want to | Go to |
| --- | --- |
| act in a session: `/tldr`, `/telder:update`, and what the summarizing model is asked | [In a session](in-a-session/README.md) |
| work on this repository: the rules, the gates, the cards, the documentation | [On this repository](repository/README.md) |

## In a session

The hook runs without you: the summary is shown to the person and never enters your context.
[In a session](in-a-session/README.md) names the two skills and what the summarizing model follows.

## On this repository

`CLAUDE.md` imports one rule file per subject from `docs/agent/repository/`, and `AGENTS.md` lists the same files
for a harness that reads no imports. [On this repository](repository/README.md) is the index of those rules.
