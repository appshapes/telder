# tldr — a TL;DR under every long reply

The plugin half of Telder. When Claude Code finishes showing a reply longer than a few paragraphs, a short list is
added under it on your screen: the most important points first, in simple language, for a reader with no time.
The front [README](../README.md) has the install steps and the options; this page says what ships and what it does.

## What this plugin ships

- **One hook**, on `MessageDisplay` (`hooks/hooks.json`, exec form, no shell). Claude Code runs it for every piece
  of reply text it shows, and once more when a message is complete. The script keeps the pieces, and on that
  last call, when the message has enough prose, asks a small model for the summary and hands back the text to
  show. The hook is display-only by Claude Code's own contract: the transcript and what Claude sees keep the
  original text, so the summary can never be read by Claude as an instruction and never grows the context.
- **One script**, `scripts/tldr-hook`: Python 3, standard library only. It reads the hook's JSON on stdin, counts
  the words of prose (fenced code and table rows do not count), and when there are at least `min_words`, runs
  `claude -p` with the chosen model and the reply on its stdin. The instructions it gives the model: summarize
  the salient points in simple and concise language, few or no abbreviations, no mannered prose, highest priority
  first, an unordered list of at most `max_points` points, short. If the reply is already a short list, or only a
  question to you, the model answers with nothing and nothing is added.
- **One skill**, `/tldr`: with no argument, Claude writes a TL;DR of its previous reply itself, under the same
  instructions as the automatic ones; `instructions` prints those instructions in layers; `off`, `on` and
  `status` control the automatic summaries on this machine.
- **No MCP server, no channel, no binary, no `bin/`.** CI enforces the file list.

## What the plugin sees

The hook receives the text of each reply as Claude Code shows it, and the session and message identifiers it
needs to keep the pieces of one message together. It does not receive your prompts, does not read the transcript
file, and never reads a credential. The reply text goes to one nested `claude -p` call, under your own login, and
nowhere else; that call loads no settings, no other plugin, no MCP server and no tool. The pieces of a message are
kept in a file under the plugin's data directory only until the message is complete, then deleted; a piece left
behind by an interrupted message is deleted an hour later. The script writes nothing under your project.

## How the summary is made

`claude -p --model <model> --output-format text --system-prompt <the instructions> --no-session-persistence
--setting-sources "" --strict-mcp-config --tools "" --disable-slash-commands`, with the reply on stdin, in an
environment from which every variable of your session that begins with `CLAUDE` (and `AI_AGENT`) has been removed,
apart from `CLAUDE_CONFIG_DIR`, so the nested call is a plain new session under the same login. It carries
`TLDR_INNER=1`, which makes the nested session's own copy of this hook return at once. Measured on 2026-09-30 with
Claude Code 2.1.285, on a 200-word reply: Opus 5.5 answered in four to five seconds, Sonnet 5.5 in three to four,
Fable 5.1 in four to six; Haiku 4.5 took seven to forty seconds and once ran past the timeout. Opus is the default
because the points and their order are a judgement, and one second is cheap. The nested call counts against your
plan's usage like any other short turn of that model.

## The instructions, in layers

The system prompt of the nested call is built from parts, in this order, joined by blank lines: the plugin's
own instructions (unless `instructions_mode` is `replace`), the `instructions` option, the `instructions_file`
option's text, the project's `.telder.md` (read from `CLAUDE_PROJECT_DIR`, which Claude Code exports to its
hooks, else the hook input's `cwd`), and last the format rules, which the script's parser depends on and which
no layer can remove. A file is read at every summary, must be UTF-8 and at most 8 KB, and is ignored with a
debug line otherwise; a missing `.telder.md` is silent. `replace` with nothing else given falls back to the
plugin's own, with a debug line. `tldr-hook instructions …` prints the same layers with their sources; the
`/tldr` skill runs it with the option values as arguments, because the model's Bash commands do not carry the
`CLAUDE_PLUGIN_OPTION_*` variables the hook gets.

A `.telder.md` comes from the repository you opened, so treat it as you treat that repository's other files:
it can change the wording of the summary under a reply, and nothing else, because the nested call has no
tools and the summary never reaches Claude.

## When nothing is added

- The reply has fewer than `min_words` words of prose.
- `/tldr off` is in effect on this machine.
- The model did not answer within `timeout` seconds, or `claude` could not be run: the reply is shown as it is,
  and one line says why in Claude Code's debug log (`claude --debug-file <path>`).
- The model judged the reply already short, or a single question.

## Options

Eight, all optional: `min_words`, `max_points`, `model`, `heading`, `timeout`, `instructions`, `instructions_file`
and `instructions_mode`. Their meanings and defaults are
in the front [README › Options](../README.md#options). The plugin reads them from the `CLAUDE_PLUGIN_OPTION_*`
variables Claude Code gives its hooks; a value outside its range is clamped, a value that is not a number keeps
the default and says so in the debug log.
