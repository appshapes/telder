# Telder

[![release](https://img.shields.io/github/v/release/appshapes/telder)](https://github.com/appshapes/telder/releases/latest)

A TL;DR under every long Claude Code reply. When a reply runs past a few paragraphs, the `tldr` plugin adds a
short list under it: the most important points first, in simple language, for a reader with no time. A small
model writes it through your own `claude` login. Nothing to configure, no API key.

## If you want to

| If you want to | Go to |
| --- | --- |
| install the plugin | [Install](#install) |
| see what a TL;DR looks like | [What you see](#what-you-see) |
| get a TL;DR of the last reply right now, or pause the summaries | [`/tldr`](#tldr) |
| change how long a reply must be, how many points, which model | [Options](#options) |
| update the plugin | [Update](#update) |
| know what the plugin sees, and where it goes | [`plugin/README.md` › What the plugin sees](plugin/README.md#what-the-plugin-sees) |
| see what changed in a release | [`CHANGELOG.md`](CHANGELOG.md) |
| work on Telder | [`docs/development.md`](docs/development.md) |

## Install

1. Open Claude Code.
2. Type `/plugin marketplace add appshapes/telder`.
3. Type `/plugin install tldr@telder`. When it asks where to install, choose **user**.
4. Type `/reload-plugins`.

You need `python3` on your machine (macOS and Linux have it) and the `claude` command on your `PATH`, which the
Claude Code install gives you.

## What you see

A reply shorter than about 120 words of prose is shown as it is. A longer one ends like this:

```
  ... Dust, smoke and water droplets can make those colors even stronger.
  ---
  TL;DR
  - Blue light scatters far more than red as sunlight crosses the air, so the sky looks blue.
  - The sun gives off less violet and our eyes see blue better, so the sky is not violet.
  - At sunrise and sunset light crosses much more air, which scatters the blue away and leaves red.
```

The summary is added to what your screen shows, and nowhere else: the conversation Claude sees is unchanged, and
so is the transcript. The reply pauses for a few seconds at its end while the summary is written; if the model
does not answer in time, the reply is shown without one.

## `/tldr`

- `/tldr` — Claude writes a TL;DR of its previous reply, in the chat.
- `/tldr off` — no more automatic summaries on this machine, in every session, until `/tldr on`.
- `/tldr on` — start them again.
- `/tldr status` — which it is.

## Options

Ask your session, for example:

```
Set the tldr plugin's min_words to 200 and max_points to 3.
```

It edits your user settings; start a new session for the change to take effect. Or type `/plugin`, open `tldr`,
and set them there.

| Option | Default | Meaning |
| --- | --- | --- |
| `min_words` | `120` | a reply with fewer words of prose gets no summary; code and tables do not count; `0` summarizes every reply |
| `max_points` | `5` | at most this many points, the most important first |
| `model` | `claude-opus-5-5` | the model that writes the summary, by its full name: `claude-sonnet-5-5` is a little faster and cheaper, `claude-fable-5-1` a little slower, `claude-haiku-4-5-20251001` the cheapest but slow and uneven when measured |
| `heading` | `TL;DR` | the line above the points |
| `timeout` | `40` | seconds to wait for the summary before showing the reply without one |

## Update

Nothing to do. Claude Code updates the plugin in the background and tells you to type `/reload-plugins`; do that.

## More

- [plugin/README.md](plugin/README.md) — what the plugin ships, what it sees, and how the summary is made
- [docs/development.md](docs/development.md) — working on Telder: setup, gates, the dev loop, releases, layout
- [docs/claude-code-usage.md](docs/claude-code-usage.md) — working on Telder with Claude Code: skills, the Trello CLI
- [CHANGELOG.md](CHANGELOG.md) — what changed in each release
