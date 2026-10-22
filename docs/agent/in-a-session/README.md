# In a session

Telder's hook runs outside your turn: Claude Code calls it when it shows your reply, the summary goes to the
screen, and nothing comes back to you. What you can do is run the two skills when asked.

## If you want to

| If you want to | Go to |
| --- | --- |
| know the skills the plugin loads, and what each runs | [Know the skills](#know-the-skills) |
| know what the model that writes the summary is given, and what it must answer | [Write a summary](#write-a-summary) |

## Know the skills

1. `/tldr [instructions | off | on | status]` runs `tldr-hook` for the instructions in effect, the heading line
   or the mute switch; with no argument you write the TL;DR of your previous reply yourself.
2. `/telder:update` runs Claude Code's own plugin commands, moves an existing install and nothing else, and ends
   by asking for `/reload-plugins`.

Details: [Know the skills](skills.md).

## Write a summary

1. The summarizing model is a nested `claude -p` with no tools and no settings; it reads the reply on stdin under
   a system prompt built in layers and answers with a list, or the word `NONE`.
2. `/tldr` with no argument puts you in its place: the same layers, printed by `tldr-hook instructions`, under
   the heading line `tldr-hook heading` prints.

Details: [Write a summary](summarizer.md).
