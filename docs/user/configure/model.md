# Choose the model

The `model` option names the model that writes the summary, by its full name; the nested `claude -p` does not
accept a short alias such as `opus` or `haiku`. It runs through your own `claude` login, sees only the reply
being summarized, and counts against your plan's usage like any other short turn of that model.

| Model | Measured on a 200-word reply | Notes |
| --- | --- | --- |
| `claude-opus-5-5` | four to five seconds | the default: choosing the points and their order is a judgement |
| `claude-sonnet-5-5` | three to four seconds | a little faster and cheaper |
| `claude-fable-5-1` | four to six seconds | a little slower |
| `claude-haiku-4-5-20251001` | seven to forty seconds | the cheapest, but slow and uneven |

Measured on 2026-09-30 with Claude Code 2.1.285. On a 350-word reply Opus 5.5 took 27 seconds once, which is why
the default `timeout` is 90 seconds; a reply the model does not answer within `timeout` is shown without a
summary, and the hook's own limit is 130 seconds, above the option's cap of 120.

```
Set the telder plugin's model to claude-sonnet-5-5.
```

Changing the model changes nothing about what leaves your machine: the same reply and the same instructions go
to Anthropic, through the same login ([Privacy](../privacy/README.md)).
