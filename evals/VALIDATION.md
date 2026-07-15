# Validation record — 2026-07-15

This record separates release-specific packaging evidence. It is evidence about
skill and host contracts, not proof that scientific conclusions produced with
the suite are correct.

## v0.2.0 cross-platform release

### Open standard and repository contracts

- All seven skills passed `agentskills validate` from the Agent Skills
  reference package `skills-ref==0.1.1`.
- The 49-test repository gate passed, including Agent Skills frontmatter,
  relative-resource confinement, synchronized portable status models,
  full-suite child dependency preflights, common Codex/Claude metadata, and
  native marketplace paths.
- All seven skills passed the current Codex `quick_validate.py`; the Codex
  plugin validator passed; both Claude marketplace and plugin manifests passed
  `claude plugin validate --strict`.
- `python scripts/sync_portable_resources.py --check` confirmed that each
  portable orchestrator directory contains a byte-identical copy of the
  canonical status-transition table. Orchestrator execution still requires the
  complete seven-skill suite.

### Isolated host installation matrix

| Host surface | Version tested | Result |
|---|---:|---|
| Codex native marketplace | `codex-cli 0.144.2` | Installed `theory-first@theory-first` at `0.2.0`, enabled it, and retained the portable status model. |
| Claude Code native marketplace | `2.1.207` | Strict validation and isolated install passed; `plugin details` discovered all seven namespaced skills and no unintended agents, hooks, MCP, or LSP components. |
| OpenCode through the Agent Skills CLI | OpenCode `1.18.2`, `skills` `1.5.17` | A clean `--skill '*'` copy installation exposed all seven skills through `opencode debug skill`; both orchestrator status models matched the canonical bytes. A separate single-skill probe confirmed why orchestrators must not be installed alone. |

These checks establish packaging, discovery, and resource integrity. They do
not establish identical model behavior across hosts, models, permission
policies, or tool configurations.

### Published-source checks

- GitHub `main` at packaging commit
  `ee7772920341fad398a7f465b086e2a2ac7657ba` passed the complete CI run:
  Python 3.10, 3.11, and 3.12 repository gates plus the isolated
  `skills@1.5.17` full-suite installation job.
- A fresh isolated Codex marketplace checkout of that commit installed and
  enabled plugin version `0.2.0`; its cache contained all seven skills.
- A fresh isolated Claude Code marketplace checkout of that commit installed
  and enabled plugin version `0.2.0`; `plugin details` reported seven skills
  and zero agents, hooks, MCP servers, or LSP servers.
- A fresh isolated Agent Skills installation from GitHub found exactly seven
  suite skills. OpenCode `1.18.2` discovered all seven, including both entry
  points, and both installed status models matched the canonical bytes.
- The repository description and topics now identify the cross-platform
  surface, and GitHub private vulnerability reporting remains enabled.

The release tag is cut from the validation-bearing commit only after its own CI
run passes.

### Remaining behavioral limit

Prompt-level Claude Code and OpenCode behavior was not exercised with a model
provider in this environment. Packaging, installation, discovery, and resource
integrity are verified; identical model behavior across hosts, models,
permission policies, and tool configurations is not claimed. The shared routing
corpus remains the minimum behavioral contract.

## v0.1.0 published baseline

### Repository contracts

- 44 tests passed in the project environment.
- The same 44 tests passed in a clean virtual environment installed only from `.[dev]`; the declared extraction dependency was `pypdf>=6,<7`, with no PyMuPDF installation.
- Tests cover manifest shape, all seven skill contracts, relative links, profile-schema identity, status coverage, commit-pinned CI actions, five positive and three negative routing records, parent/child collision records, private-artifact exclusions, and the downloader security surface.
- Downloader tests are offline and cover modern and old arXiv IDs, malicious identifier input, redirect restrictions, public-DNS checks, atomic private caching, foreign-file cleanup refusal, local-source change detection, page limits, isolated extraction, CLI redaction, and absence of text previews.

### Codex validation

- All seven skills passed the current `quick_validate.py` from Codex's `skill-creator`.
- `plugins/theory-first` passed the current `validate_plugin.py` from Codex's `plugin-creator`.
- A local marketplace was added in an isolated temporary `CODEX_HOME`.
- `codex plugin add theory-first@theory-first --json` installed version `0.1.0`, and `codex plugin list` reported it enabled.
- The installed cache contained `STATUS_MODEL.md`, all seven skills, the canonical project-profile example, references, the bounded acquisition script, and its tests.

### Real-source smoke test

The acquisition path fetched the public neutral example `arxiv:1706.03762` from the fixed arXiv host:

- 2,215,244 source bytes;
- SHA-256 `bdfaa68d8984f0dc02beaca527b76f207d99b666d31d1da728ee0728182df697`;
- no absolute path or text preview in command output.

With `pypdf` available, bounded extraction completed for 15 pages and produced 40,145 navigation-text bytes in private output. The marker-owned cache cleanup removed its managed source, and the temporary extraction output was deleted. No source file or extracted text is included in this repository.

### Prompt-level forward checks

See [FORWARD_TEST_REPORT.md](FORWARD_TEST_REPORT.md). The current minimum routing corpus is [cases.json](cases.json), with parent/child boundary cases in [collisions.json](collisions.json). These are qualitative pre-release checks, not a statistical routing benchmark.

### Published-source checks

- The reviewed source was pushed to the public `cxMoonGlade/Theory-First` repository, and the README, manifest, privacy-policy, and repository URLs resolved from `main`.
- GitHub Actions passed the 44-test repository gate on Python 3.10, 3.11, and 3.12.
- A fresh isolated `CODEX_HOME` added `cxMoonGlade/Theory-First` as a Git marketplace, installed `theory-first@theory-first` at version `0.1.0`, and reported it enabled.
- The repository description and discovery topics were set, and GitHub private vulnerability reporting was enabled.

### Remaining environment-specific check

- Installation through the ChatGPT desktop-app interface was not exercised in this environment. This does not affect the verified Git-based Codex installation path, but it remains an explicit unverified surface.

Use [the release checklist](../RELEASE_CHECKLIST.md) again for every future tag.
