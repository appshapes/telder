# See what you get

A reply shorter than about 300 words of prose is shown as it is. A longer one ends like this:

```
  ... Dust, smoke and water droplets can make those colors even stronger.
  ---
  TL;DR 10-22-2026 14:05
  - Blue light scatters far more than red as sunlight crosses the air, so the sky looks blue.
  - The sun gives off less violet and our eyes see blue better, so the sky is not violet.
  - At sunrise and sunset light crosses much more air, which scatters the blue away and leaves red.
```

- **The threshold** is the `min_words` option, 300 by default. Words inside code blocks and table rows do not
  count, so a reply that is mostly code gets no summary however long it is.
- **The heading** is the `heading` option, `TL;DR` by default, shown in bold, followed by your machine's local
  date and time when the reply ended: month, day, year, then the hour and minute, 24-hour. Scrolling back
  through a long session, you see when each reply landed. The time is taken when the reply ends, not when the
  summary is written.
- **The points** are at most `max_points`, 10 by default, the most important first, one short sentence each,
  in simple language with few or no abbreviations.
- **The rule** above the heading is a literal `---` line in the terminal.

The summary is added to what your screen shows, and nowhere else. The conversation Claude sees is unchanged, and
so is the transcript, so a summary can never be read by Claude as an instruction and never uses up context. The
reply pauses for a few seconds at its end while the summary is written: the status line says "Writing the
TL;DR"; if the model does not answer in time, the reply is shown without one.

The words are the summarizing model's, under instructions you can change: what it focuses on, its language, its
voice ([Change the instructions](../configure/instructions.md)).
