# Know why no summary appeared

One of four things, in the order to check them:

1. **The reply has fewer than `min_words` words of prose.** Code blocks and table rows do not count, so a reply
   that is mostly code or a table stays under the threshold. The default is 300; `0` summarizes every reply
   ([Know the options](../configure/options.md)).
2. **`/tldr off` is in effect** on this machine. `/tldr status` says so, and `/tldr on` ends it.
3. **The model judged the reply already a short list, or a single question to you**, and answered with nothing.
   That is by instruction: the format rules tell it to.
4. **The model did not answer within `timeout` seconds, or `claude` could not be run.** The reply is shown as it
   is. The default wait is 90 seconds, because Opus 5.5 took 27 seconds once on a 350-word reply when measured
   ([Choose the model](../configure/model.md)).

To see which, start Claude Code with a debug file and look for the plugin's lines in it:

```sh
claude --debug-file /path/to/claude-debug.log
grep 'tldr:' /path/to/claude-debug.log
```

Each summary, and each reason for none, is one line there beginning `tldr:`: the word counts, the time taken and
the model name, never the reply or the summary.

If a summary never appears in any session, check in the same terminal that `python3 --version` prints 3.9 or
newer and that `claude --version` works. The hook needs both on the `PATH` Claude Code runs with.
