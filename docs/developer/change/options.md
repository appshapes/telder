# Change an option

An option is read by the script from the `CLAUDE_PLUGIN_OPTION_<NAME>` variable Claude Code exports to its hooks,
and by the `/tldr` skill from `${user_config.<name>}` in its command lines, because a model's Bash command carries
none of those variables. It lives in these places, and a change touches each:

1. **The manifest**, `plugin/.claude-plugin/plugin.json` › `userConfig`: `type`, `title`, `description`,
   `default`, and `min` and `max` for a number. What `/plugin` shows is this entry. `make plugin-validate`
   checks the shape.
2. **The script**: `DEFAULTS` and the bounds `options` applies (a value outside its range is brought back
   inside it; a value that is not a number keeps the default). A new option that the summary depends on is
   also read by `run_instructions` from an argument, so that `/tldr` follows it.
3. **The skill**, `plugin/skills/tldr/SKILL.md`, if `/tldr` needs the value: one more `--<flag>
   "${user_config.<name>}"` on the `instructions` command line.
4. **The tests**: `Options` for the default and the bounds, `Instructions` if the layering changes.
5. **The options page**, `docs/user/configure/options.md`, and **the listing**, `plugin/README.md` › Options:
   the same table in both, so the default appears in three places with the manifest. `make docs-check` fails
   when either page lacks an option the manifest declares.
6. **The changelog**, `[Unreleased]`: a new option or a changed default is a change the user sees.

Keep the count honest where it is written: the User tree and the listing say "eight options"; a ninth changes
those sentences. The listing is scanned by the directory at every push, so a new option's description there
follows the listing's rules ([Change the listing](listing.md)): no dollar sign, no icon file name.
