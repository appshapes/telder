# Privacy

The plugin has no server and no network code of its own. What it sends is the reply being summarized, through
the `claude` you already use, to Anthropic. The statement itself is in the plugin's listing, which is what
Anthropic's directory shows and what the manifest's privacy link names; this page is the way into it.

## If you want to

| If you want to | Go to |
| --- | --- |
| know what the plugin fetches, sends, reads, writes and runs, and for how long anything is kept | [Know what leaves your machine](#know-what-leaves-your-machine) |
| know how the summary is made, and what your login is used for | [Know how the summary is made](#know-how-the-summary-is-made) |
| report a suspected vulnerability | [Report a vulnerability](#report-a-vulnerability) |

## Know what leaves your machine

1. Sent: the text of a reply long enough to summarize, with the instructions, to Anthropic through one run of
   `claude` under your own login. Nothing to AppShapes or anyone else; a reply under `min_words` is sent nowhere.
2. Never sent: your prompts, your files, the transcript, the session's identifiers, your working directory.
3. Fetched: nothing by the plugin itself. Written: two files in the plugin's data directory, never under a project.

Details: [What leaves your machine, and where it goes](../../../plugin/README.md#what-leaves-your-machine-and-where-it-goes).

## Know how the summary is made

1. One `claude -p` with no settings, no other plugin, no MCP server, no tools and no session left behind; it can
   only read the reply and answer with text.
2. It inherits your session's environment with every variable beginning `CLAUDE` removed, except
   `CLAUDE_CONFIG_DIR`, so it is a plain new session under the same login; the script reads no credential.

Details: [How the summary is made](../../../plugin/README.md#how-the-summary-is-made).

## Report a vulnerability

1. Privately, through Report a vulnerability on the repository's Security tab; no credential in the report.
2. A confirmed vulnerability is fixed in a release before the advisory is published, and recorded in the changelog.

Details: [SECURITY.md](../../../SECURITY.md).
