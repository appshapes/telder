# Telder — a TL;DR under every long Claude Code reply

When Claude Code finishes showing a reply longer than a few paragraphs, Telder adds a short list under it on your
screen: the most important points first, in simple language, for a reader with no time. A model writes the list
through the Claude Code login you already have. There is nothing to configure, no account to create and no API
key to give.

The plugin's name is `tldr`. It is one hook, one script and one skill, and it works in Claude Code.

## What you see

A reply shorter than about 300 words of prose is shown as it is. A longer one ends like this:

```
  ... Dust, smoke and water droplets can make those colors even stronger.
  ---
  TL;DR
  - Blue light scatters far more than red as sunlight crosses the air, so the sky looks blue.
  - The sun gives off less violet and our eyes see blue better, so the sky is not violet.
  - At sunrise and sunset light crosses much more air, which scatters the blue away and leaves red.
```

The summary is added to what your screen shows, and nowhere else. The conversation Claude sees is unchanged, and
so is the transcript, so a summary can never be read by Claude as an instruction and never uses up context. The
reply pauses for a few seconds at its end while the summary is written; if the model does not answer in time,
the reply is shown without one.

## Three things to try

1. **Ask something with a long answer**, for example `Explain how DNS resolution works, step by step.` The reply
   ends with a rule, the heading `TL;DR` and a list of its main points.
2. **Type `/tldr`** after any reply. Claude writes a TL;DR of its previous reply in the chat, under the same
   instructions as the automatic ones. This also works on a reply too short to get one by itself.
3. **Make the summaries your own.** Ask `Set the tldr plugin's instructions to: Write it in French. Say first
   what I must do next.`, start a new session, and type `/tldr instructions` to see the instructions now in
   effect and where each part comes from.

To pause the automatic summaries, type `/tldr off`; `/tldr on` starts them again, and `/tldr status` says which it
is. The switch covers every session on this machine and needs no restart.

## What you need

- **Claude Code.** The summary is added by a hook on the event Claude Code raises when it shows a reply. The chat
  on claude.ai does not run hooks, so the plugin adds nothing there.
- **`python3`** on the machine (macOS and Linux have it), version 3.9 or newer. The script uses the standard
  library only; nothing is installed.
- **The `claude` command**, which the Claude Code install gives you, signed in as usual.

Outside the directory, the plugin installs from its own marketplace: in Claude Code, type
`/plugin marketplace add appshapes/telder`, then `/plugin install tldr@telder`, then `/reload-plugins`.

## Options

Eight, all optional. Ask your session, for example `Set the tldr plugin's min_words to 200 and max_points to 3.`,
or type `/plugin`, open `tldr`, and set them there. A new session picks up the change.

| Option | Default | Meaning |
| --- | --- | --- |
| `min_words` | `300` | a reply with fewer words of prose gets no summary; code blocks and table rows do not count; `0` summarizes every reply |
| `max_points` | `10` | the summary has at most this many points, the most important first |
| `model` | `claude-opus-5-5` | the model that writes the summary, by its full name; `claude-sonnet-5-5` is a little faster and cheaper |
| `heading` | `TL;DR` | the line above the points |
| `timeout` | `90` | seconds to wait for the summary, 10 to 120; past it the reply is shown without one |
| `instructions` | *(empty)* | a sentence or a few of your own, added to the plugin's instructions |
| `instructions_file` | *(empty)* | absolute path to a text file of your own instructions, at most 8 KB |
| `instructions_mode` | `add` | `add` keeps the plugin's own instructions before yours; `replace` drops them |

A value outside its range is brought back inside it; a value that is not a number keeps the default.

## The instructions, in layers

The model that writes the summary follows instructions built from parts, in this order:

1. **The plugin's own**: summarize the salient points in simple and concise language, few or no abbreviations, no
   mannered prose, highest priority first, short. `instructions_mode: replace` drops this part.
2. **Your `instructions` option.**
3. **Your `instructions_file`**, read at every summary, so an edit takes effect at once.
4. **The project's `.telder.md`**, a file at the root of the folder you opened Claude Code in, for instructions a
   team shares, such as `Name the files that changed.`
5. **The format rules**, which no part can remove: an unordered list of at most `max_points` points, one short
   sentence each. If the reply is already a short list, or only a question to you, the model answers with nothing
   and nothing is added.

`/tldr instructions` prints the parts in effect, each with its source. A file that is missing, empty, not UTF-8
text or larger than 8 KB is ignored.

A `.telder.md` comes from the repository you opened, so treat it as you treat that repository's other files. It
can change the wording of the summary under a reply and nothing else: the model call that reads it has no tools,
and the summary never reaches Claude.

## What leaves your machine, and where it goes

This section is the plugin's privacy statement.

- **Fetched:** nothing. The plugin downloads nothing, when it is installed or later, and it has no network code.
- **Sent, and to where:** the text of a reply that is long enough to summarize, together with the instructions
  above (the plugin's, yours, and the project's `.telder.md`), goes to Anthropic, the same service your Claude
  Code session already talks to. It travels in one run of the `claude` program on your machine, under the login
  that program already has. Nothing goes to AppShapes or to anyone else; the plugin has no server of its own. A
  reply shorter than `min_words` is sent nowhere.
- **Never sent:** your prompts, your files, the transcript, the session's identifiers, your working directory.
- **Read on this machine:** what Claude Code hands the hook (the reply text as it is shown, and the session and
  message identifiers that keep the pieces of one reply together); the plugin's options; the file your
  `instructions_file` option names; and `.telder.md` at the project root. The script never opens the transcript
  file, Claude Code's configuration, its memory or its chat history, and it never reads a credential.
- **Written on this machine:** two things, both in the plugin's data directory and nowhere under your project.
  The pieces of the reply being shown are kept in a file that only your user can read, until the reply is
  complete. A marker file named `mute`, holding the time you typed `/tldr off`, exists until `/tldr on`. For
  Claude Code's debug log the script prints one line per summary: the word counts, the time taken and the model
  name, never the reply or the summary.
- **Run:** one program, `claude`: the executable that runs your session when Claude Code names it, otherwise the
  `claude` on your `PATH`. The script starts it directly, without a shell, with the arguments listed in the next
  section. No other program is run.
- **Kept for how long:** nothing is kept once the reply is shown. The file of pieces is deleted the moment the
  reply is complete. If a reply is interrupted, its pieces are deleted the next time a reply completes, once
  they are an hour old. Uninstalling the plugin removes its data directory, by Claude Code's default. What
  Anthropic keeps of the request is what it keeps of any other message your Claude Code sends, under the terms
  of your plan.

**About your login.** The summary is one more short message from your own Claude Code, so it runs under your own
login and counts against your plan's usage like any other short turn of the chosen model. The plugin uses your
login in that sense only. The script does not read, copy, print or store a credential. It starts `claude` with
the environment of your session, minus the variables that describe the session itself, because that environment
is what your `claude` already relies on to reach Anthropic: a configuration directory, a proxy, an API key if
you use one. The script filters it by variable name and passes the rest on without looking at a value.

## How the summary is made

The script runs this, with the reply on standard input:

```
claude -p --model <model> --output-format text --system-prompt <the instructions>
       --no-session-persistence --setting-sources "" --strict-mcp-config --tools ""
       --disable-slash-commands "Write the TL;DR of the following reply."
```

The call loads no settings, no other plugin and no MCP server, has no tools, and leaves no session behind: it
can only read the reply and answer with text. Its environment has every variable beginning with `CLAUDE` removed,
and `AI_AGENT`, apart from `CLAUDE_CONFIG_DIR`, so it is a plain new session under the same login. It carries the
marker `TLDR_INNER=1`, which makes the nested session's own copy of this hook return at once, so a summary is
never summarized.

Measured on 2026-09-30 with Claude Code 2.1.285: on a 200-word reply Opus 5.5 answered in four to five seconds,
Sonnet 5.5 in three to four and Fable 5.1 in four to six; Haiku 4.5 took seven to forty seconds. On a 350-word
reply Opus 5.5 took 27 seconds once, which is why the default wait is 90 seconds. Opus is the default because
choosing the points and their order is a judgement.

## When no summary appears

- The reply has fewer than `min_words` words of prose. Code blocks and table rows do not count.
- `/tldr off` is in effect on this machine. `/tldr status` says so.
- The model judged the reply already a short list, or a single question to you.
- The model did not answer within `timeout` seconds, or `claude` could not be run. The reply is shown as it is.

To see which, start Claude Code with `claude --debug-file <path>` and look for the lines beginning `tldr:` in
that file: each summary, and each reason for none, is one line there. If a summary never appears, check that
`python3 --version` prints 3.9 or newer and that `claude --version` works in the same terminal.

## What has been tested

The terminal, on macOS, with Claude Code 2.1.285, in an interactive session and in `-p` mode. The unit tests run
on Ubuntu and macOS on every push to `master`. Not tested yet: Windows, the desktop app's Code tab and the IDE
extensions.

## Support

- Questions and problems: [github.com/appshapes/telder/issues](https://github.com/appshapes/telder/issues)
- A suspected vulnerability, privately:
  [github.com/appshapes/telder/security](https://github.com/appshapes/telder/security/advisories/new)
- What changed in each release:
  [CHANGELOG.md](https://github.com/appshapes/telder/blob/master/CHANGELOG.md)
- The source, the tests and how to work on Telder: [github.com/appshapes/telder](https://github.com/appshapes/telder)

MIT license.
