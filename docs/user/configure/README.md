# Configure

Eight options, all optional, all with working defaults, read from your own Claude Code settings. The instructions
the summary follows are built in layers, and three of the layers are yours to write.

## If you want to

| If you want to | Go to |
| --- | --- |
| see every option, its default and its meaning | [Know the options](#know-the-options) |
| set an option | [Set an option](#set-an-option) |
| change what the summary focuses on, its language, its voice | [Change the instructions](#change-the-instructions) |
| give a project instructions every teammate's summaries follow | [Share instructions with a project](#share-instructions-with-a-project) |
| choose the model that writes the summary | [Choose the model](#choose-the-model) |

## Know the options

1. `min_words`, `max_points`, `model`, `heading`, `timeout`, `instructions`, `instructions_file` and
   `instructions_mode`.
2. A value outside its range is brought back inside it; a value that is not a number keeps the default.

Details: [Know the options](options.md).

## Set an option

1. Ask your session: `Set the telder plugin's min_words to 200 and max_points to 3.` It edits your user settings.
2. Or type `/plugin`, open `telder`, and set them there. A new session picks up the change.

Details: [Set an option](set-an-option.md).

## Change the instructions

1. `instructions`: a sentence or a few, for example `Write it in French. Say first what I must do next.`
2. `instructions_file`: a text file of your own, read at every summary; `instructions_mode: replace` drops the
   plugin's own part.
3. `/tldr instructions` shows the layers in effect.

Details: [Change the instructions](instructions.md).

## Share instructions with a project

1. Put a `.telder.md` at the root of the folder you open Claude Code in, for example `Name the files that changed.`
2. It is always added, after your own layers and before the format rules; commit it so the team shares it.

Details: [Share instructions with a project](project-file.md).

## Choose the model

1. `model` is a full model name, `claude-opus-5-5` by default, because choosing the points and their order is a
   judgement.
2. `claude-sonnet-5-5` is a little faster and cheaper, `claude-fable-5-1` a little slower,
   `claude-haiku-4-5-20251001` the cheapest but slow and uneven when measured.

Details: [Choose the model](model.md).
