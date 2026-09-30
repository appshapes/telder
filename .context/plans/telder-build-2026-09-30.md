# Telder build record — 2026-09-30

What was reviewed, what was measured, what was decided, and what is open. The first session's record; later
sessions append.

## The ask

A Claude Code plugin (marketing name Telder, plugin name `tldr`) that puts a TL;DR under every reply: salient
points, simple and concise language, few or no abbreviations, no mannered prose, highest priority first, an
unordered list, short — for a person deciding quickly. Port from Brigade whatever is meaningful. Start from the
research note `~/Downloads/claude-code-response-simplifier-hooks.md`.

## The research note, reviewed

The note is right on the two candidate events and their contracts, and right that a `Stop` hook can only append,
never replace. Three things it did not say, all measured below and all decisive:

1. A `type: "prompt"` hook on `Stop` cannot write the summary. The note suggests it as the way to "generate the
   summary without calling the API yourself". On Claude Code 2.1.285 the prompt is wrapped as *"Based on the
   conversation transcript above, has the following stopping condition been satisfied? … Condition: <your
   prompt>"*, the whole transcript is sent (21 messages for a one-turn session), and the model answers a fixed
   schema `{ok, reason, impossible}` — the `systemMessage` the docs list for prompt hooks never appears. Two
   runs, two models, both the same. The `haiku` alias is also rejected there (404 `model: haiku`).
2. A `Stop` hook's `systemMessage` is shown to Claude on the next turn as well as to the person. For a summary
   that lists "next steps", that is an instruction-injection path (claude-mem issue #987 hit exactly this).
3. `MessageDisplay` fires once per chunk *with a `message_id`*, so the chunks of one message can be joined, and
   its `timeout` can be raised above the 10-second default. That makes it usable for a model-written summary,
   which the note called "awkward".

The two existing plugins: `mk1332/tldr-nudge` (Stop hook, Python, counts words, *asks* whether you want a TL;DR
and writes it with `claude -p --model haiku` only on request, one extra turn each time) and `itsdevcoffee/tldr`
(a `/tldr` command only, the main model summarizes on demand). Neither is automatic; both leave the choice of
event unmeasured.

## Measurements (Claude Code 2.1.285, macOS, this account)

| Probe | Result |
| --- | --- |
| Stop + prompt hook, `model: haiku` | hook error: 404 `model: haiku` |
| Stop + prompt hook, full Haiku id, and no model | model answers `{ok:true, reason:…, impossible:false}`; no systemMessage possible |
| Stop + command hook, headless `-p` | `system/informational` event, `Stop says: ` prefixed on every line |
| Stop + command hook, interactive | renders under the reply as `⎿ Stop says: TL;DR` with the points indented; issue #50542 (plugin-scope systemMessage not rendered) is gone |
| Stop + command hook, `async: true` | turn ends at once; the hook is backgrounded; its reply never reaches the screen, not at 75 s |
| MessageDisplay + command hook, headless `-p` | one call, `final: true`, `delta` = the whole message; `displayContent` replaces the printed result |
| MessageDisplay + command hook, interactive | three chunks then a final empty one, same `message_id`; the summary renders inside the reply as markdown (`---`, bold heading, bullets) |
| `--bare` on the nested call | exits 1: bare mode reads no OAuth login |
| Nested `claude -p`, Haiku 4.5 | 6.0 s, 6.4 s, 6.8 s, 11.7 s, 32.8 s, timeout (> 40 s) |
| Nested `claude -p`, Sonnet 5.5 | 3.5 s, 2.7 s, 2.8 s, 3.1 s, 3.7 s, 3.3 s |
| Nested `claude -p`, Opus 5.5 | 3.7 s, 3.9 s, 4.7 s |
| Nested `claude -p`, Fable 5.1 | 4.0 s, 4.4 s, 6.3 s |

## Decisions

- **Event: `MessageDisplay`**, not `Stop`. Display-only (no injection path, no context growth), rendered as
  markdown inside the reply, and visible in `-p` output too. The cost is that every long text block of a turn
  gets a summary, not only the last; intermediate narration is rarely 120 words. The script still understands
  `Stop` (tested), so a fork that prefers the notice style changes one line of `hooks.json`.
- **Mechanism: a command hook running a nested `claude -p`.** Uses the person's own login; no API key. Not a
  prompt hook (cannot emit text), not an agent hook (same wrapper, slower), not the API (needs a key).
- **Default model: `claude-opus-5-5`** (Rjae: "Opus at a minimum"; measured one second behind Sonnet, which is
  nothing beside the reply). Sonnet, Fable and Haiku are options; Haiku works but unpredictably.
- **Language: Python 3, standard library**, one file with a shebang, mode 755, exec-form hook. The closest prior
  art chose Python; `node` is not on `PATH` for the native Claude Code install; POSIX sh cannot parse JSON safely
  without `jq`, which is not on every host.
- **Ported from Brigade:** CLAUDE.md conventions (plans, scratch, commit format, never rebase); the `make push`
  chain; `plugin-check.sh` (allowlist, mode in git, version pin, no bin/MCP/channels, exec-form hooks, shellcheck,
  every skill model-reachable) and `no-secrets.sh` (nine shapes, no length floor on prefixes); `ci.yml` with the
  runner-inventory step and timeouts; a cut-down `release.yml` and `release-prep.sh` (no binaries, so the
  changelog section is the notes); the `commit`, `trello-create` and `trello-read` skills (Trello lists updated to
  Wanting, Doing, Deploying, Releasing, Supporting); the marketplace entry with `autoUpdate`; the environment
  strip by prefix; keep-a-changelog; SECURITY.md; the "If you want to" README tables.
- **Not ported (open question for Rjae):** the agentic loop (`claude.yml`, `review-pull-request.yml`,
  `auto-merge.yml`, the monthly agents, `_create-claude-issue.yml`) and the release-notes email. Both need
  repository secrets (`CLAUDE_CODE_OAUTH_TOKEN`, `GH_ACTIONS_TOKEN`, `RESEND_API_KEY`) and Blacksmith runners.

## Adjustable instructions (built in the same session, second commit)

Rjae asked for it after the initial build. Design: the system prompt is layered — the plugin's own voice
guidance, the `instructions` option (inline), the `instructions_file` option (type `file`, read at every
summary, 8 KB cap), the project's `.telder.md` (from `CLAUDE_PROJECT_DIR`, else the hook input's `cwd`; always
added; a repository file, so it can only change the summary's wording), then the fixed format rules. `replace`
mode drops the first layer only. `/tldr` follows the same layers through `tldr-hook instructions`, which takes
the option values as arguments because a model's Bash command has no `CLAUDE_PLUGIN_OPTION_*`; the inline text
travels through a quoted heredoc. `/tldr instructions` shows the layers with their sources. Not built: a
project-level switch to refuse `.telder.md` (display-only blast radius did not justify a ninth option).

## State at the end of the first session

Two commits on `master` of the public `github.com/appshapes/telder` (created this session, private
vulnerability reporting on): `9ebb6d5 45: Create the tldr plugin` and `6f05619 45: Let the person adjust the
instructions`. Card 45 on the AppShapes board. Green locally: `make test` (39 tests), `make lint`,
`make plugin-check`, `make plugin-validate`; `make hook-smoke` produced a real summary; the finished plugin was
run headless and interactively with options set through `--settings`. The first CI run failed on the runner's
shellcheck 0.9.0 (SC2015 on `A && B || C`, which the local 0.11 does not report); the second commit fixed it and its run
(36756679977) was green on both jobs. The hand-off for the next session is `handoff-2026-09-30.md`.

## Open

- (Done, second commit.) Rjae wanted to discuss letting the person adjust the instructions that drive the summary (and `/tldr`) once
  the initial implementation is done. Candidate design: an `instructions_file` option (userConfig type `file`,
  user-level, read by the hook and quoted by the skill) plus a per-project `.tldr.md` read from the hook's
  `cwd`, each either replacing or extending the built-in guidance; plugin options are user-level only (Claude
  Code reads `pluginConfigs` from user, `--settings` and managed settings, never project settings), which is
  why a project needs a file.
- Port the agentic loop and the release-notes email, or not (Rjae, 2026-09-30: wait for now).
- A `claude plugin eval` suite (`evals/`) once there is something to score.
- Not measured: Windows (the shebang and `python3` assumption), the Desktop app and IDE extensions (their
  `MessageDisplay` rendering), a reply made of several long text blocks in one turn.
