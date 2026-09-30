---
name: tldr
description: >-
  Write a TL;DR of your previous reply on demand, show the instructions the summaries follow, or switch the
  automatic TL;DR off and on for this machine. `/tldr` summarizes your last reply; `/tldr instructions` shows the
  instructions in effect and where each part comes from; `/tldr off` stops the automatic summaries; `/tldr on`
  starts them again; `/tldr status` says which it is. Use it when the user asks for a summary of what you just
  said, asks what the summaries follow, or asks to stop or start them.
user-invocable: true
argument-hint: "[instructions | off | on | status]"
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/tldr-hook:*)
---

# tldr

The argument is: $ARGUMENTS

## First, the instructions in effect

For no argument and for `instructions`, run exactly this command. It prints the instructions the summaries
follow, in layers, each under a line saying where it comes from: the plugin's own, the user's `instructions`
option, the user's `instructions_file`, the project's `.telder.md`, and the fixed format rules.

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tldr-hook" instructions --project-dir "${CLAUDE_PROJECT_DIR}" --instructions-file "${user_config.instructions_file}" --mode "${user_config.instructions_mode}" --max-points "${user_config.max_points}" --instructions-stdin <<'TLDR_EOF'
${user_config.instructions}
TLDR_EOF
```

## No argument: summarize your previous reply

Write the TL;DR of your previous reply yourself, in the chat, following the printed instructions exactly: the
layers in order, and the format rules last. Put the heading `${user_config.heading}` above the list. Write
nothing else. If your previous reply was already a short list or a single question, say so in one line instead.

## `instructions`: show them

Relay the command's output as it is, under a one-line lead saying these are the instructions the summaries
follow. Then say how to change them: the `instructions`, `instructions_file` and `instructions_mode` options of
the plugin (`/plugin`, then `tldr`), and a `.telder.md` file at the project root.

## `off`, `on`, `status`: the automatic summaries

Run exactly one of these commands, then relay its one line of output:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tldr-hook" off --data-dir "${CLAUDE_PLUGIN_DATA}"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tldr-hook" on --data-dir "${CLAUDE_PLUGIN_DATA}"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tldr-hook" status --data-dir "${CLAUDE_PLUGIN_DATA}"
```

`off` stops every session on this machine from adding a TL;DR until `on`; it does not need a restart. Any other
argument: say that the choices are `instructions`, `off`, `on` and `status`, and do nothing else.
