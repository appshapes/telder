# Security

## Reporting a vulnerability

Report it privately through GitHub: **Security → Report a vulnerability** on
[appshapes/telder](https://github.com/appshapes/telder/security/advisories/new). Please do not open a public
issue for a suspected vulnerability, and do not include a credential in the report — describe where it would
leak, not its value.

## What to expect

A maintainer reads the report and answers in the advisory thread. Telder is a small project with no security team
and no response-time commitment; what it does promise is that a confirmed vulnerability is fixed in a release
before the advisory is published, and that the fix is recorded in [`CHANGELOG.md`](CHANGELOG.md).

## Supported versions

The latest release only. Claude Code updates the plugin in the background from the marketplace, so a fix ships as
a new release and users move to it with `/reload-plugins`.

## What the plugin sees, and where it goes

The hook receives the text of each reply Claude Code shows you, and nothing else from your session: not your
prompts, not the transcript file, not your credentials. It sends that text to one model call through your own
`claude` login, as a nested `claude -p`, to write the summary; the summary is display-only and never enters the
conversation Claude sees. The script writes no file under your project and keeps no copy of any reply.
