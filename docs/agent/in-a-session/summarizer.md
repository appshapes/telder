# Write a summary

The model that writes the summary is not the session's model. It is one run of `claude -p` the hook starts on the
reply's final chunk, with the reply on standard input:

```
claude -p --model <model> --output-format text --system-prompt <the instructions>
       --no-session-persistence --setting-sources "" --strict-mcp-config --tools ""
       --disable-slash-commands "Write the TL;DR of the following reply."
```

It loads no settings, no other plugin and no MCP server, has no tools, and leaves no session behind: it can only
read the reply and answer with text. It sees the reply text as shown, and nothing else from the session: not the
prompts, not the files, not the transcript, not the working directory.

## The system prompt, in layers

`instruction_parts` in the script builds it, in this order; `/tldr instructions` prints the same parts, each
under a line saying where it comes from.

1. **The plugin's own**, unless `instructions_mode` is `replace`:

   > You write the TL;DR of a reply an assistant just gave to a person. The person likely does not have much time
   > to read. Summarize the salient points using simple and concise language. Limit or omit abbreviations. Do not
   > use mannered prose. You are empowering someone to make a quick yet informed decision: highest priority items
   > first, and keep it simple and short.

2. **The user's `instructions` option**, a sentence or a few.
3. **The user's `instructions_file`**, read at every summary.
4. **The project's `.telder.md`**, at the project root, always added.
5. **The format rules**, which no layer can remove and the parser depends on:

   > Format: an unordered list only, one point per line, each line starting with '- ', at most N points, each
   > point one short sentence. No heading, no preamble, no closing line, no code. If the reply is already a list of
   > N or fewer short points, or is only a question to the person, answer with the single word NONE.

   N is the `max_points` option, 10 by default.

A `replace` that leaves nothing of the user's own falls back to the plugin's own part, with one line in the
debug log. A file that is missing, empty, not UTF-8 text or over 8 KB is ignored; a missing `instructions_file`
is logged, a missing `.telder.md` is silent.

## What the answer becomes

`clean_summary` in the script turns the answer into the list under the heading: lines beginning `- ` are kept,
in order, capped at `max_points`; heading lines are dropped; a plain line becomes a point; the single word `NONE`
means nothing is added. The heading line is the `heading` option followed by the local date and time the reply
ended (`TL;DR 10-22-2026 14:05`), taken before the nested call starts.

## When you are the summarizer

`/tldr` with no argument asks the session's model for the same thing: run `tldr-hook instructions` with the
option values as arguments, run `tldr-hook heading` for the heading line, then write the list yourself, in the
chat, under those instructions, with the heading line above it and nothing else. If the previous reply was
already a short list or a single question, say so in one line instead. That TL;DR is in the conversation, unlike
the automatic ones, because you wrote it there.
