# Know the structure

```
README.md                              the title, description and sample; the three personas
docs/<persona>/README.md               persona root
docs/<persona>/<topic>/README.md       topic root
docs/<persona>/<topic>/<action>.md     detail page (the leaf)
CLAUDE.md                              the agent's root: @imports of docs/agent/repository/*.md
AGENTS.md                              the same files as links, for a harness without imports
plugin/README.md                       the listing: a reference document the tree points at
```

The personas, in README order: `user`, `developer`, `agent`. The shape is Brigade's (its card 110), with three
personas instead of five because Telder has no backend to own and no team to administer.

## The three page shapes

**A persona root** has an H1 with the persona's name, a `## If you want to` table whose rows link to the
persona's topic roots, and then exactly one H2 per topic directory: at most two sentences, one of them linking to
the topic's `README.md`. Nothing else: no procedures, no commands.

**A topic root** has an H1, a `## If you want to` table whose rows link to its own action sections (`#anchor`), and
then one H2 per action. An action section is the TL;DR: the shortest listing that gets the action done, at most 20
non-blank lines, usually a numbered list, and a last line `Details: [<title>](<page>.md)`. Every `.md` beside the
README is such a page and is named by a `Details:` line; a page nothing names is an orphan and fails the gate. A
`Details:` line may name a reference document instead of a sibling page when the details already exist there
(the User's privacy topic does this with the listing's privacy section, the update topic with `CHANGELOG.md`).

**A detail page** is the leaf. The details in one logical order, concise, no mannered prose, no restating of the
TL;DR; headings as needed; links to the reference documents for what they already say. It may link across
personas: the developer's script page links the agent's summarizer page.

## Reference documents

Stay where code and manifests name them and are reached from the tree: `plugin/README.md` (the directory listing
and the privacy statement; its headings are anchors the manifest's `privacyPolicyUrl` and the tree depend on),
`SECURITY.md`, `CHANGELOG.md`, the records under `.context/plans/`, and the generated
`docs/developer/reference/make-targets.md`. A directory under a persona that holds reference pages rather than a
topic is registered in the gate's `REFERENCE_DIRS`.

The listing says some of what the User tree says, on purpose: the directory shows the listing to a reader who
never sees this repository. When a procedure changes, change the leaf, the TL;DR and the listing's sentence
together.

## Style

- Lead with what the reader does; say the result they see.
- One idea per sentence. Short lists for parallel items. A table when there are columns.
- Commands in fenced blocks; a value a reader copies in backticks.
- Numbers that came from a measurement name the record (`.context/plans/…`) and its date.
- Dates absolute. No secrets, no addresses, no local paths of a real machine.
- In the listing: no dollar sign, no icon file name, absolute links ([Change the listing](../change/listing.md)).
