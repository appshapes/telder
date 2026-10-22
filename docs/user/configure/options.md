# Know the options

Eight options, all optional, all with working defaults. Values are read from your own Claude Code settings, never
from a project; how to set one is [Set an option](set-an-option.md).

| Option | Default | Meaning |
| --- | --- | --- |
| `min_words` | `300` | a reply with fewer words of prose gets no summary; code blocks and table rows do not count; `0` summarizes every reply |
| `max_points` | `10` | the summary has at most this many points, the most important first; 1 to 10 |
| `model` | `claude-opus-5-5` | the model that writes the summary, by its full name: `claude-sonnet-5-5` is a little faster and cheaper, `claude-fable-5-1` a little slower, `claude-haiku-4-5-20251001` the cheapest but slow and uneven when measured ([Choose the model](model.md)) |
| `heading` | `TL;DR` | the words above the points; the local date and time the reply ended follow them |
| `timeout` | `90` | seconds to wait for the summary, 10 to 120; past it the reply is shown without one |
| `instructions` | *(empty)* | a sentence or a few of your own, added to the plugin's instructions ([Change the instructions](instructions.md)) |
| `instructions_file` | *(empty)* | absolute path to a UTF-8 text file of your own instructions, at most 8 KB, added after `instructions`; read at every summary, so an edit takes effect at once |
| `instructions_mode` | `add` | `add` keeps the plugin's own instructions before yours; `replace` drops them; a project's `.telder.md` is always added and the format rules always apply |

A value outside its range is brought back inside it; a value that is not a number keeps the default. The
plugin's own instructions and the format rules the layers end with are on the page about
[changing the instructions](instructions.md).
