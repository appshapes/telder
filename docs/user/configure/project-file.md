# Share instructions with a project

A file named `.telder.md` at the root of the folder you open Claude Code in carries instructions every summary
written in that project follows, whoever is at the keyboard: for example

```
Name the files that changed.
```

- **Where:** the project root, which is the folder Claude Code was started in (the directory Claude Code hands
  its hooks as the project directory). Commit the file so the team shares it.
- **When:** it is read at every summary, so an edit takes effect at once, and it is always added, after your own
  `instructions` and `instructions_file` and before the format rules, whatever `instructions_mode` says.
- **Limits:** UTF-8 text, at most 8 KB; a file that is empty, not text or larger is ignored. A project with no
  `.telder.md` is the normal case and nothing is logged.

A `.telder.md` comes from the repository you opened, so treat it as you treat that repository's other files. It
can change the wording of the summary under a reply and nothing else: the model call that reads it has no tools,
and the summary never reaches Claude, so the worst a hostile file can do is put a misleading list under one
reply on your screen.
