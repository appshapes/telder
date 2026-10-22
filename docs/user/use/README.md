# Use

Nothing to start: once the plugin is installed, every reply long enough gets its list. These are the things you
see and the things you can type.

## If you want to

| If you want to | Go to |
| --- | --- |
| know what a TL;DR looks like and when it appears | [See what you get](#see-what-you-get) |
| get a TL;DR of the last reply right now, in any session | [Get a TL;DR right now](#get-a-tldr-right-now) |
| stop the automatic summaries for a while, and start them again | [Pause and resume](#pause-and-resume) |
| know why a reply got no summary | [Know why no summary appeared](#know-why-no-summary-appeared) |

## See what you get

1. A reply shorter than about 300 words of prose is shown as it is; a longer one ends with a rule, the heading
   `TL;DR` with your local date and time, and a list of its points, the most important first.
2. The list is added to your screen only: the conversation Claude sees and the transcript are unchanged.

Details: [See what you get](what-you-see.md).

## Get a TL;DR right now

1. Type `/tldr`. Claude writes a TL;DR of its previous reply in the chat, under the same instructions as the
   automatic ones, even for a reply too short to get one by itself.
2. `/tldr instructions` shows the instructions in effect and where each part comes from.

Details: [Get a TL;DR right now](on-demand.md).

## Pause and resume

1. `/tldr off` stops the automatic summaries on this machine, in every session, at once.
2. `/tldr on` starts them again; `/tldr status` says which it is.

Details: [Pause and resume](pause.md).

## Know why no summary appeared

1. The reply was under `min_words` words of prose, `/tldr off` is in effect, the model judged the reply a short
   list or a question, or it did not answer within `timeout` seconds.
2. `claude --debug-file <path>` records one `tldr:` line per reply saying which.

Details: [Know why no summary appeared](no-summary.md).
