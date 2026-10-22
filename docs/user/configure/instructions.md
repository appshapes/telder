# Change the instructions

The summary follows instructions in layers, in this order. `/tldr instructions` prints the layers in effect,
each under a line saying where it comes from.

1. **The plugin's own:** summarize the salient points in simple and concise language, few or no abbreviations, no
   mannered prose, highest priority first, keep it simple and short. `instructions_mode: replace` drops this
   layer.
2. **Your `instructions` option:** a sentence or a few, for example:

   ```
   Set the telder plugin's instructions to: Write it in French. Say first what I must do next.
   ```

3. **Your `instructions_file` option:** the absolute path of a UTF-8 text file, for longer instructions. It is
   read at every summary, so an edit takes effect at once, with no new session.
4. **The project's `.telder.md`,** for instructions a team shares ([Share instructions with a project](project-file.md)).
   It is always added, whatever `instructions_mode` says.
5. **The format rules, which cannot be changed:** an unordered list of at most `max_points` points, one short
   sentence each, no heading, no preamble, no closing line, no code; a reply that is already a short list, or
   only a question to you, gets nothing.

What each layer can do is reword the summary: what it focuses on, its language, its voice, what comes first. It
cannot make the summary longer than the rules allow or turn it into prose, and it cannot reach anything but the
reply, because the model that reads it has no tools.

## `replace`

`instructions_mode: replace` drops the plugin's own layer, so your `instructions` and `instructions_file` stand
alone before the project's file and the format rules. If `replace` leaves nothing of your own, the plugin's own
instructions are used after all, with one line in Claude Code's debug log saying so.

## A file that cannot be read

A file that is missing, empty, not UTF-8 text or over 8 KB is ignored, with one line in Claude Code's debug
log (`claude --debug-file <path>`, lines beginning `tldr:`). A missing `.telder.md` is normal and is not logged.
