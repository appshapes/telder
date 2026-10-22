# Know the layout

| Path | What |
| --- | --- |
| `plugin/.claude-plugin/plugin.json` | the manifest: name `telder`, the version pin, the listing fields, the eight options |
| `plugin/.claude-plugin/icon.png` | the listing icon, rendered from [`docs/assets/icon.svg`](../../assets/icon.svg) |
| `plugin/hooks/hooks.json` | the one hook, `MessageDisplay`, exec form |
| `plugin/scripts/tldr-hook` | the script: reads the hook input, gates on length, runs the nested `claude -p`, replies; and the `/tldr` skill's command line |
| `plugin/skills/tldr/SKILL.md` | `/tldr`, `/tldr instructions`, `/tldr off`, `/tldr on`, `/tldr status` |
| `plugin/skills/update/SKILL.md` | `/telder:update`: refresh the marketplace, update the install, ask for `/reload-plugins` |
| [`plugin/README.md`](../../../plugin/README.md) | the listing Anthropic's directory shows, and the privacy statement |
| `tests/` | the unit tests (`test_tldr_hook.py`, `test_docscheck.py`) and the sample hook input |
| `scripts/ci/` | `plugin-check.sh`, `no-secrets.sh`, `release-notes.sh`, `docscheck.py` |
| `scripts/release-prep.sh` | the release sequence |
| `.github/workflows/` | `ci.yml`, `release.yml` |
| `.claude-plugin/marketplace.json` | the `telder` marketplace that serves the plugin |
| `.claude/` | the project's skills (`/commit`, `/trello-create`, `/trello-read`, `/trello-done`) and the marketplace entries |
| `docs/` | the three persona trees (`user/`, `developer/`, `agent/`), the generated reference, the icon's source |
| `README.md`, `CLAUDE.md`, `AGENTS.md` | the human's root, the agent's root with its imports, the same files as links |
| [`CHANGELOG.md`](../../../CHANGELOG.md), [`SECURITY.md`](../../../SECURITY.md) | what changed in each release; how to report a vulnerability |
| `.context/plans/` | the plans and the records ([Evidence](../evidence/README.md)) |
| `.ignored/` | scratch, gitignored |
| `Makefile` | every target, with a help line ([make targets](../reference/make-targets.md)) |
