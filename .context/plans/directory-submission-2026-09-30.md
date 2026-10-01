# Submitting Telder to Anthropic's plugin directory — 2026-09-30

The record of the submission work of session `45-directory-submission` (card 45). `handoff-2026-09-30.md` is the
state of the product; this page is only the directory. The portal is https://claude.ai/directory/manage; the
rules are Anthropic's [submit page](https://claude.com/docs/plugins/submit),
[pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist) and
[Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy).
Session `41-market-brigade` submitted Brigade the same day and passed on what it saw; what differs for Telder is
said here.

## State

**A draft is saved in the portal and waits for Rjae.** Everything a session may do is done; what is left are four
acknowledgements only the account's owner may give, and the Submit button.

- Draft: https://claude.ai/directory/manage/plugins/b90913e7-e905-4976-8b4c-26db9756620b (Submissions › Telder ›
  Continue). Source `appshapes/telder`, folder `plugin`, tracking `master`; a saved draft's source cannot change.
- The icon was captured when the draft was saved, from `plugin/.claude-plugin/icon.png` on `master`.
- Steps 1 to 3 are filled. Step 4, Compliance, has the contact email prefilled and four boxes unticked.
- The draft's validation report belongs to one commit. If `master` has moved since (this note's own commit moved
  it once; the session re-validated after it), select **Re-validate** on the Source step first.

### What Rjae does

1. Open the draft, **Continue submission**. On Source, **Re-validate** if the report's commit is not the tip of
   `master`. Expect: no blocking finding, 3 warnings that say "No action needed", 4 holds (below).
2. Step 3, Data handling: check the four answers under "The form's answers" below and change any you disagree
   with. They are statements made in your name.
3. Step 4, Compliance: tick the four boxes. Read the third as it is worded: "The plugin does not exfiltrate
   credentials or execute code outside its declared MCP servers." Telder has no MCP server and runs one declared
   hook script, which the listing shows to users as "This plugin runs code locally"; Brigade was submitted under
   the same sentence.
4. Step 5, Review and submit: leave auto-publish on and "GitHub push webhook" selected, **Submit for review**.
5. On the "Plugin submitted for review" page, **Set up push updates** › **Generate secret**. The page shows a
   Payload URL and a secret once. A session can then create the webhook with
   `gh api --method POST repos/appshapes/telder/hooks --input <json file>` (push event, `content_type` json, the
   secret inside the file and never on a command line); GitHub's ping shows as "Webhook connected". This needs
   admin on the repository.
6. Afterwards the portal shows Scanning, then In review. For the first version a reviewer publishes; select
   **Publish** when the version passes. Reviewer questions go to the contact email and the page's Review tab.

Also on Rjae's machine: the install made under the old name gets no more updates. In a terminal:
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

## What the portal says now (master @ f89d362)

No blocking finding. 3 warnings, all "Unrecognized field in plugin.json … No action needed" for the three link
fields only the directory reads. 4 holds, each left for the reviewer on purpose:

| Hold | Why it stays |
| --- | --- |
| Uses a credential from the user's machine | It describes something real: the hook starts `claude` with the session's environment, and `claude` reaches Anthropic under the person's login. The environment has to go whole, because it is what that `claude` signs in with (a configuration directory, a proxy, an API key). Renaming things until the scan stops matching would hide the behaviour, not change it. The README says what happens under "About your login". |
| Scripts the validator couldn't follow | The hook is Python and the plugin is a subfolder. Clearing it means a shell-only hook or a repository of the plugin alone. Neither is worth it; the report itself says waiting for the review is fine. |
| Name may be confused (author `appshapes` ~ connector `shapes`) | The publisher's real name. Brigade carries the same hold. |
| Publisher name may be confused (`appshapes` ~ `shapes`) | The same. |

The Listing details step also shows: listed on Claude Code, Cowork and the Claude apps, with "Not used here:
hooks" for the apps; "This plugin runs code locally", shown to users at install; links 5 of 6 (no
`termsOfServiceUrl`, which is optional and was left unset: the MIT license is the only terms there are).

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
  saved in this tab"). **Save and exit** creates the server-side draft and takes the icon.
- The Branch field validates any pushed branch without saving, which is how the prepared commit and the name
  were checked before `master` moved.

## Not done

- **The four acknowledgements and Submit**: Rjae's.
- **The push webhook**: after Submit, needs the secret the portal shows once.
- **Not tested**: the plugin installed from claude.ai in chat and in Cowork (it would mean uploading it to Rjae's
  account). In Cowork hooks load; whether `MessageDisplay` fires there, and whether a `claude` is on its `PATH`,
  is unknown. If it is not, the reply is shown without a summary.
- **Read from the code, not measured**: the nested call drops every variable beginning with `CLAUDE`, so a
  provider chosen by such a variable (Bedrock, Vertex) would not reach it, and `--setting-sources ""` loads no
  settings that could restore it. Worth one measurement before a user on those providers reports it.
- **No `evals/` suite**, as before.
