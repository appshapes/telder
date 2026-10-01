# Submitting Telder to Anthropic's plugin directory — 2026-09-30

The record of the submission work of session `45-directory-submission` (card 45). `handoff-2026-09-30.md` is the
state of the product; this page is only the directory. The portal is https://claude.ai/directory/manage; the
rules are Anthropic's [submit page](https://claude.com/docs/plugins/submit),
[pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist) and
[Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy).
Session `41-market-brigade` submitted Brigade the same day and passed on what it saw; what differs for Telder is
said here.

## State

**Submitted for review on 2026-10-01**, by this session on Rjae's instruction ("complete the submission
yourself"; asked how the four Compliance acknowledgements should be ticked, she answered "You tick them for me").

- The plugin's page: https://claude.ai/directory/manage/plugins/b90913e7-e905-4976-8b4c-26db9756620b. Source
  `appshapes/telder`, folder `plugin`, tracking `master`. Status after Submit: Scanning.
- Submitted at `master` @ `97a28b5` (0.4.2), which validated with no blocking finding, 3 warnings that say "No
  action needed" and 3 holds. The portal first queued the commit the draft was saved at (`f89d362`, 0.4.1), so
  **Check for new commits** was selected right after Submit; the push of this note is the first push the webhook
  carries.
- The push webhook is GitHub hook `690373636` on `appshapes/telder` (push event, json, signed with the secret
  the portal showed once; the secret was written to a private file, used once and deleted). GitHub's ping
  returned 200 and the page shows "Webhook connected".
- The icon was captured when the draft was first saved, from `plugin/.claude-plugin/icon.png`.

### What happens next, and who acts

1. Anthropic: the security scan, then a reviewer for the three holds. Nothing is asked of anyone meanwhile.
2. Rjae: reviewer questions come to the contact email and the page's Review tab. When the version passes, select
   **Publish**; for a first version that is a request a reviewer carries out.
3. Any session: every push to `master` is now a new version for the directory, within minutes.

On Rjae's machine the install made under the old name gets no more updates. In a terminal:
`claude plugin uninstall tldr@telder`, `claude plugin marketplace update telder`,
`claude plugin install telder@telder`, then `/reload-plugins`.

## What the portal said, before any change (master @ aca54aa)

Validate, 7 checks: no blocking finding, 1 warning, 7 holds for a reviewer. Validate alone creates no draft.

| Finding | Kind | What the report said |
| --- | --- | --- |
| No icon | warning | add a square PNG at `.claude-plugin/icon.png`, 512 to 2048 px, under 2 MB; the file "may become the listing icon only once: the first time the plugin is saved or submitted in the developer portal" |
| Uses a credential from the user's machine (`MCP_FORWARDS_CREDENTIAL_ENV`) | hold | "this plugin reads the installer's environment (printenv / env / export -p / set) (file scripts/tldr-hook) and can send data off the machine (file scripts/tldr-hook: a command assembled at run time)" |
| Scripts the validator couldn't follow (`COMMAND_SCRIPT_NOT_FOLLOWED`) | hold | the validator follows only plain shell scripts; `scripts/tldr-hook` is Python, so a reviewer reads it |
| Name may be confused with an existing listing (`NAME_CONFUSABLE`) | hold, 4 findings | `tldr` is one or two characters from connector `timr`, connector `tldv` and plugin `tlgr`; author `appshapes` resembles connector `shapes` |
| Publisher name may be confused with another (`PUBLISHER_CONFUSABLE`) | hold | `appshapes` resembles connector `shapes`; Brigade has the same hold |

## What changed, and why

| Change | Why | Commit |
| --- | --- | --- |
| The icon, `plugin/.claude-plugin/icon.png`, 1024 px, from `docs/assets/icon.svg` | the warning; the listing takes it once | `ce1dd1d` |
| Manifest: `displayName` `Telder`, `author.url`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl`; "Claude Code" in the description | the listing's label and links; policy 3.A and 3.B ask for a privacy link and a support channel | `ce1dd1d` |
| `plugin/README.md` rewritten as the listing | the directory shows it as the description; policy 3.C and 3.E ask for how it works, how to troubleshoot and three examples; the section "What leaves your machine, and where it goes" is the privacy statement, and "About your login" answers the credential hold in words | `ce1dd1d` |
| The file of reply pieces is 0600 in a 0700 folder | it held reply text under the machine's default mode; a privacy statement that says "only your user" has to be true | `ce1dd1d` |
| `make plugin-check` check 9: the icon's shape; no dollar sign and no icon file name in the plugin README | two things the directory's scan holds and nothing local caught | `ce1dd1d` |
| The plugin is named `telder` (was `tldr`) | Rjae's decision, on a measurement: a throwaway branch named `telder` validated with 4 holds against 7; the three `tldr` look-alikes went away. The name is permanent once listed | `f8db740` |
| Release 0.4.0 | the rename and the listing | `aec6d25`, tag `v0.4.0`, run 36801122620 |
| `/tldr` carries the plugin's own instructions for where the script cannot run | the portal lists the plugin on Claude Code, Cowork and the Claude apps, and derives that by itself; in chat only the skill's own folder is copied, so the script is not there. Tested in Claude Code with the shell tool denied: `/telder:tldr` wrote the summary | `fd76390` |
| Release 0.4.1 | the skill change | `f89d362`, tag `v0.4.1`, run 36801323751; CI run 36801321988 green on both jobs |
| The script reads each variable by its literal name, and the nested `claude` inherits the hook's environment after `leave_session` removed the session's variables from it by name; nothing copies the environment any more | Rjae asked for the Source step's findings to be resolved. This is what cleared "Uses a credential from the user's machine" (see "How the credential hold was cleared") | `e82ea99`, `69d455e` |
| Release 0.4.2 | the environment change | `97a28b5`, tag `v0.4.2`; release and CI runs green |

## What the portal says now (master @ 97a28b5)

No blocking finding. 3 warnings, all "Unrecognized field in plugin.json … No action needed" for the three link
fields only the directory reads; removing them would remove the listing's privacy, support and documentation
links. 3 holds, each left for the reviewer:

| Hold | Why it stays |
| --- | --- |
| Scripts the validator couldn't follow | The hook is Python and the plugin is a subfolder. Clearing it means a shell-only hook or a repository that holds the plugin alone. Neither is worth it; the report itself says waiting for the review is fine. |
| Name may be confused (author `appshapes` ~ connector `shapes`) | Rjae's decision, 2026-10-01: keep `appshapes`. Measured: another `author.name` clears this one. |
| Publisher name may be confused (`appshapes` ~ `shapes`) | The publisher is the GitHub owner, not `author.name` (measured: changing the author left this hold). Brigade carries the same one. |

The Listing details step also shows: listed on Claude Code, Cowork and the Claude apps, with "Not used here:
hooks" for the apps; "This plugin runs code locally", shown to users at install; links 5 of 6 (no
`termsOfServiceUrl`, which is optional and was left unset: the MIT license is the only terms there are).

## How the credential hold was cleared

The hold read: "this plugin reads the installer's environment (printenv / env / export -p / set) (file
scripts/tldr-hook) and can send data off the machine (file scripts/tldr-hook: a command assembled at run time)".
Six throwaway branches were validated through the Branch field, nothing saved, all deleted afterwards:

| Probe | Result |
| --- | --- |
| no `$` character anywhere in the script | no change |
| the literal word `claude` in place of the computed executable | no change |
| `author.name` changed | NAME_CONFUSABLE gone, PUBLISHER_CONFUSABLE stays |
| named reads through `os.environ[name]` with `name` a loop variable | the text became "reads the installer's an environment variable named at run time" |
| only literal reads, but a variable still called `env` holding them and the old copying function still in the file | the first text again |
| the change that shipped | the hold is gone |

So the scan holds a script that reads the environment as a whole, or reads a variable whose name is computed.
What shipped is a real change and not a renaming: the script used to copy every value into a dictionary and hand
it to the nested call; it now deletes the session's variables from its own environment by name and the nested
call inherits the rest, so no value other than the plugin's own options, the project directory and the data
directory is ever read. `tests/test_tldr_hook.py` has a test that starts a real child and checks what it
inherits. The README's "About your login" says the same in words. The reviewer still reads the script, because
of the script hold.

The portal answered "Could not validate: Too many validations" on the fourth Validate inside about three
minutes; three minutes later it accepted one again.

## The form's answers (step 3, saved in the draft)

| Question | Answer | Why |
| --- | --- | --- |
| Does the plugin read or store personal data? | **Reads only** | it reads the text of replies, which can hold a name or an address; it stores nothing past the moment the reply is shown |
| Does any skill send data to a service other than the declared connectors? | **Yes — listed in README** | the reply text goes to Anthropic through the person's own `claude`; that is not a declared connector, and the README lists it. "No" was defensible (nothing leaves the platform), but the README says "Sent", so the answer agrees with it |
| How long does your service retain data received from Claude? | **Not retained** | there is no service |
| Is the plugin intended for users under 18? | **No** | |

## Driving the portal from a session

- The signed-in browser is the playwright-cli session `directory`, which Rjae signed in to for Brigade. Session
  `41-market-brigade` uses it every 30 minutes; ask it to pause before using it and say when it is free. Do not
  copy its sign-in to another browser: that is a credential copy nobody asked for.
- Run playwright-cli from a directory outside the repository; `.playwright-cli/` is gitignored as well.
  `snapshot main` leaves the chat sidebar out of the output.
- **Validate** and **Re-validate** create nothing on the server. **Next** keeps a draft in the tab only ("Draft
  saved in this tab"). **Save and exit** creates the server-side draft and takes the icon. A saved draft keeps
  the Data handling answers.
- After **Submit for review** the page offers **Set up push updates**: a dialog, **Generate secret**, then a
  Payload URL and a secret in two text fields, shown once. Read them from the page into a private file, build
  the hook's JSON from it, `gh api --method POST repos/appshapes/telder/hooks --input <file>`, delete the files;
  never print the secret.
- The Branch field validates any pushed branch without saving, which is how the prepared commit and the name
  were checked before `master` moved.

## Not done

- **Publish**, once the version passes: Rjae's, on the plugin's page.
- **Not tested**: the plugin installed from claude.ai in chat and in Cowork (it would mean uploading it to Rjae's
  account). In Cowork hooks load; whether `MessageDisplay` fires there, and whether a `claude` is on its `PATH`,
  is unknown. If it is not, the reply is shown without a summary.
- **Read from the code, not measured**: the nested call drops every variable beginning with `CLAUDE`, so a
  provider chosen by such a variable (Bedrock, Vertex) would not reach it, and `--setting-sources ""` loads no
  settings that could restore it. Worth one measurement before a user on those providers reports it.
- **No `evals/` suite**, as before.
