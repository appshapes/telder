# Set an option

Three ways, all ending in your own Claude Code settings. A running session keeps the values it started with, so
start a new session for a change to take effect.

## Ask your session

```
Set the telder plugin's min_words to 200 and max_points to 3.
```

Claude edits the plugin's options in your user settings and tells you to start a new session.

## The plugin menu

Type `/plugin`, open `telder`, and set the options there. Each one shows its title, its meaning and its default.

## On the command line

For one session, pass the options with `--settings`; the key is the plugin's id, `telder@telder` for an install
from the marketplace (`telder@anthropic-plugin-directory` for one from the directory, `telder@inline` for
`--plugin-dir`):

```sh
claude --settings '{"pluginConfigs":{"telder@telder":{"options":{"model":"claude-sonnet-5-5","min_words":40}}}}'
```

## What a value can be

A number option (`min_words`, `max_points`, `timeout`) outside its range is brought back inside it, and a value
that is not a number keeps the default; `instructions_mode` is `add` unless it is exactly `replace`; `model` is
passed to `claude` as it is, so it must be a full model name. Every option and its range is on
[Know the options](options.md).
