# Move from the old name

The plugin was named `tldr` through 0.3.0 and has been `telder` since 0.4.0 (2026-09-30). A plugin's name is
permanent once Anthropic's directory lists it, so it now carries the product's own name; `/tldr` and everything
it does are unchanged. An install made under the old name gets no more updates: the marketplace no longer serves
`tldr`, so Claude Code's background update finds nothing to move it to.

In a terminal:

```sh
claude plugin uninstall tldr@telder
claude plugin marketplace update telder
claude plugin install telder@telder
```

Then type `/reload-plugins` in your session. Options you had set live under the plugin's name, so set them again
under the new one, for example `Set the telder plugin's min_words to 200.` ([Set an option](../configure/set-an-option.md)).

Nothing else moves: the plugin keeps no state across the rename except the mute marker and the pieces of a reply
being shown, both in the plugin's data directory, which Claude Code removes with the old install.
