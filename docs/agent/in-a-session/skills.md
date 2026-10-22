# Know the skills

The plugin (`plugin/`) ships one hook and two skills. The skills are the model's documentation inside a session;
this page only names them.

| Skill | Who invokes it | What it carries |
| --- | --- | --- |
| [`plugin/skills/tldr/SKILL.md`](../../../plugin/skills/tldr/SKILL.md) | `/tldr`, `/tldr instructions`, `/tldr off`, `/tldr on`, `/tldr status`; or the model, when the user asks for a summary of what it just said, what the summaries follow, or to stop or start them | runs `tldr-hook instructions` with the option values as arguments and the inline instructions through a quoted heredoc; `tldr-hook heading` for the heading line; `tldr-hook off`, `on` and `status` against `CLAUDE_PLUGIN_DATA`; with no argument the model writes the TL;DR of its previous reply itself, in the chat, under the printed instructions; carries a copy of the plugin's own instructions for where the script cannot run |
| [`plugin/skills/update/SKILL.md`](../../../plugin/skills/update/SKILL.md) | `/telder:update`; or the model, when it finds the session's Telder behind its marketplace's release | `claude plugin list --json` to find each `telder@<marketplace>` install, `claude plugin marketplace update <marketplace>`, `claude plugin update telder@<marketplace> --scope <scope>` (user scope first); never adds a marketplace, never installs, never passes `-y`; ends by comparing the version the session loaded (the last part of `CLAUDE_PLUGIN_ROOT`) with the one installed and asking for `/reload-plugins` |

What the harness does around you:

- **One hook.** `plugin/hooks/hooks.json` registers `plugin/scripts/tldr-hook` on `MessageDisplay`, exec form, a
  130-second timeout, the status message "Writing the TL;DR". Claude Code runs it on each chunk of a reply it
  shows; on the final chunk the script runs the nested call and hands back the summary as display content. The
  summary is appended to what the screen shows and nowhere else: not to the transcript, not to your context, so
  a summary can never reach you as an instruction and never uses up your context.
- **The nested session** carries `TLDR_INNER=1`, so the hook returns at once there and a summary is never
  summarized. It has no tools and loads no plugin: nothing you do in a session is visible to it, and nothing it
  does is visible to you.
- **Permissions.** The `tldr` skill declares `allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/tldr-hook:*)`
  and the `update` skill `Bash(claude plugin:*)`, for the turn that loaded each. The user's `permissions` rules
  decide what else you may run.
- **Where the script cannot run** (the chat on claude.ai, a machine without `python3`), the `tldr` skill says
  what to do instead: write the TL;DR under its own copy of the instructions, and say in one line that the
  automatic summaries exist only in Claude Code. The `update` skill says the app updates its plugins itself.

What the summarizing model is given is [Write a summary](summarizer.md); what the person sees is the
[User](../../user/README.md) tree.
