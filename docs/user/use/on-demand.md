# Get a TL;DR right now

```
/tldr
```

Claude writes a TL;DR of its previous reply, in the chat, under the same instructions as the automatic ones: the
plugin's own, yours, the project's, then the format rules ([Change the instructions](../configure/instructions.md)).
It puts the heading line over it, with the local date and time, and nothing else. If the previous reply was
already a short list or a single question, it says so in one line instead.

Two differences from the automatic summary:

- **It works on any reply**, including one too short to get a summary by itself, and while `/tldr off` is in
  effect.
- **It is in the conversation.** Claude wrote it there, so it is in the transcript and in what Claude sees from
  then on, like anything else Claude writes. The automatic summary is on your screen only.

```
/tldr instructions
```

prints the instructions the summaries follow, in layers, each under a line saying where it comes from: the
plugin's own, your `instructions` option, your `instructions_file`, the project's `.telder.md`, and the format
rules. Then it says how to change them.

## Where the plugin's script cannot run

In the chat on claude.ai, and on a machine without `python3`, the skill cannot run the plugin's script. `/tldr`
still writes the summary, under a copy of the plugin's own instructions that the skill carries, with the heading
alone and no date and time. `/tldr instructions` shows that copy. `/tldr off`, `on` and `status` say in one line
that the automatic summaries exist only in Claude Code, so there is nothing to switch there.
