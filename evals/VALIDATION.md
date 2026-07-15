# Validation record — 2026-07-15

This record describes the local pre-release candidate. It is evidence about packaging and workflow contracts, not proof that scientific conclusions produced with the plugin are correct.

## Repository contracts

- 44 tests passed in the project environment.
- The same 44 tests passed in a clean virtual environment installed only from `.[dev]`; the declared extraction dependency was `pypdf>=6,<7`, with no PyMuPDF installation.
- Tests cover manifest shape, all seven skill contracts, relative links, profile-schema identity, status coverage, commit-pinned CI actions, five positive and three negative routing records, parent/child collision records, private-artifact exclusions, and the downloader security surface.
- Downloader tests are offline and cover modern and old arXiv IDs, malicious identifier input, redirect restrictions, public-DNS checks, atomic private caching, foreign-file cleanup refusal, local-source change detection, page limits, isolated extraction, CLI redaction, and absence of text previews.

## Codex validation

- All seven skills passed the current `quick_validate.py` from Codex's `skill-creator`.
- `plugins/theory-first` passed the current `validate_plugin.py` from Codex's `plugin-creator`.
- A local marketplace was added in an isolated temporary `CODEX_HOME`.
- `codex plugin add theory-first@theory-first --json` installed version `0.1.0`, and `codex plugin list` reported it enabled.
- The installed cache contained `STATUS_MODEL.md`, all seven skills, the canonical project-profile example, references, the bounded acquisition script, and its tests.

## Real-source smoke test

The acquisition path fetched the public neutral example `arxiv:1706.03762` from the fixed arXiv host:

- 2,215,244 source bytes;
- SHA-256 `bdfaa68d8984f0dc02beaca527b76f207d99b666d31d1da728ee0728182df697`;
- no absolute path or text preview in command output.

With `pypdf` available, bounded extraction completed for 15 pages and produced 40,145 navigation-text bytes in private output. The marker-owned cache cleanup removed its managed source, and the temporary extraction output was deleted. No source file or extracted text is included in this repository.

## Prompt-level forward checks

See [FORWARD_TEST_REPORT.md](FORWARD_TEST_REPORT.md). The current minimum routing corpus is [cases.json](cases.json), with parent/child boundary cases in [collisions.json](collisions.json). These are qualitative pre-release checks, not a statistical routing benchmark.

## Release-time checks still pending at this snapshot

- The public GitHub repository exists, but this candidate commit had not yet been pushed when this local record was written.
- GitHub Actions have not run on a remote commit.
- Git-based marketplace installation and ChatGPT desktop-app installation remain release-time checks.
- GitHub private vulnerability reporting must be enabled after repository creation and before inviting external users.

Complete [the release checklist](../RELEASE_CHECKLIST.md) before announcing a public release.
