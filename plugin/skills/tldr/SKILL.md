---
name: tldr
description: >-
  Write a TL;DR of your previous reply on demand, or switch the automatic TL;DR off and on for this machine.
  `/tldr` summarizes your last reply; `/tldr off` stops the automatic summaries; `/tldr on` starts them again;
  `/tldr status` says which it is. Use it when the user asks for a summary of what you just said, asks for
  shorter answers, or asks to stop or start the summaries.
user-invocable: true
argument-hint: "[off | on | status]"
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/tldr-hook:*)
---

# tldr

The argument is: $ARGUMENTS

## No argument: summarize your previous reply

Write the TL;DR of your previous reply yourself, in the chat, and nothing else. Follow these rules:

- Summarize the salient points using simple and concise language. Limit or omit abbreviations. No mannered prose.
- The reader likely does not have much time: highest priority items first, and keep it simple and short.
- An unordered list of at most 5 points, one short sentence each, under a `TL;DR` heading. No preamble, no
  closing line, no code.
- If your previous reply was already a short list or a single question, say so in one line instead.

## `off`, `on`, `status`: the automatic summaries

Run exactly one of these commands, then relay its one line of output:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tldr-hook" off --data-dir "${CLAUDE_PLUGIN_DATA}"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tldr-hook" on --data-dir "${CLAUDE_PLUGIN_DATA}"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tldr-hook" status --data-dir "${CLAUDE_PLUGIN_DATA}"
```

`off` stops every session on this machine from adding a TL;DR until `on`; it does not need a restart. Any other
argument: say that the choices are `off`, `on` and `status`, and do nothing else.
