# Theory First

English | [简体中文](README.zh-CN.md)

> Close the literature. Preregister the claim. Try to falsify the result.

Theory First is a cross-platform Agent Skills suite for rigorous computational
science, with native marketplace packaging for Codex and Claude Code. Its core
skills also install into OpenCode and other Agent Skills clients without
forking the workflow. The suite turns a scientific claim into an auditable
sequence: map the surrounding field, close the load-bearing evidence,
preregister what would count as success or failure, and attack a result before
allowing it to propagate.

The suite is intentionally stricter than a paper summarizer. Its public core is
domain-neutral; project-specific repositories, metrics, retrievers, provenance
rules, and artifact locations belong in an optional project profile.

## Workflow

```text
new claim
   -> map-research-landscape
   -> close-literature -> deep-read-paper
   -> preregister-claim
   -> CODE_PERMITTED | CODE_BLOCKED

result under review
   -> close-literature -> deep-read-paper
   -> stress-test-claim
   -> ACCEPT_WITH_CLASS | REPAIR | STOP | REOPEN_EVIDENCE
```

The two entry points are:

- `theory-first` — use before claim-bearing experiment or implementation work.
- `theory-fix` — use when a result is surprising, unusually clean, relied on by
  a downstream claim, or otherwise needs adversarial review.

Shared skills handle landscape mapping, literature closure, equation-level
reading, preregistration, and falsification. They produce records that a human
can inspect instead of silently upgrading an inference into evidence.
The [status model](plugins/theory-first/STATUS_MODEL.md) defines every child-to-
orchestrator transition.

## What the status words mean

`CODE_PERMITTED` means the stated claim has a closed evidence packet and a
passing preregistration for the declared scope. It is not a guarantee that the
claim is true, and it is not permission to edit, execute, use a network, spend,
access data, or take any action the user did not authorize. `CODE_BLOCKED`
means claim-bearing implementation should wait. Evidence work and explicitly
non-claim-bearing scaffolding may still be possible when they cannot expose or
contaminate the preregistered answer.

`search-exhausted-gap` never means “the literature contains no answer.” It means
no adequate source was found within a recorded search boundary: named corpora
or databases, exact queries, search date, languages, citation depth, access
limits, and other declared constraints. Expanding that boundary reopens the
gap.

## Install

The seven directories under `plugins/theory-first/skills/` are the single
runtime source for every supported host. Choose one installation surface; do
not install duplicate copies of the same skill into several discovery paths for
one client.

Install all seven skills as one suite. The orchestrators delegate to named
children, and Agent Skills frontmatter has no portable cross-host dependency
declaration; therefore `--skill theory-first`, `--skill theory-fix`, and
`--skill close-literature` are not supported standalone installs. A
dependency-bearing skill that cannot discover a child stops with
`SUITE_INCOMPLETE` instead of silently replacing that workflow. The native
Codex and Claude plugins already install the complete suite; the portable
commands below deliberately use `--skill '*'`.

### pip package

The platform-independent wheel contains the same canonical seven-skill suite
and a zero-dependency installer. Install the pinned release directly with pip:

```bash
python -m pip install https://github.com/cxMoonGlade/Theory-First/releases/download/v0.3.0/theory_first-0.3.0-py3-none-any.whl
```

Then install the complete suite for one host:

```bash
theory-first install --agent opencode
```

Repeat `--agent` to configure several hosts from the same wheel, or select a
project-local discovery path:

```bash
theory-first install --agent codex --agent claude-code --agent opencode
theory-first install --agent codex --scope project --project .
```

OpenCode also discovers skills in the standard Codex and Claude-compatible
roots. When one of those exact roots already covers an OpenCode request, the
installer omits a redundant native OpenCode copy. A standalone OpenCode install,
or one paired with a custom `CLAUDE_CONFIG_DIR`, uses its native discovery path.

The installer refuses same-named filesystem paths detected before or during a
normal installation. Review them first, then pass `--force` only when replacing
the complete installed suite is intended. Requested targets are staged first
and rolled back together on ordinary errors or interrupts before all target
swaps commit. If post-commit cleanup is interrupted, the new suite remains
active and the error reports any leftover transaction directories for manual
inspection. Abrupt process or machine termination is outside these guarantees.
Use `theory-first list`,
`theory-first path`, or `theory-first install --target /path/to/skills` for
inspection and other Agent Skills hosts.

### OpenCode and other Agent Skills clients

The cross-platform [`skills`](https://github.com/vercel-labs/skills) CLI can
discover all seven skills directly from this repository. For OpenCode:

```bash
npx skills add cxMoonGlade/Theory-First --skill '*' --agent opencode --global --yes
```

To provision several supported coding agents from one canonical installation:

```bash
npx skills add cxMoonGlade/Theory-First --skill '*' --agent claude-code --agent opencode --agent codex --global --yes
```

Use `--copy` on hosts where symlinks are unavailable. For a reproducible install,
pin both the installer and this repository's skill directory:

```bash
npx skills@1.5.17 add https://github.com/cxMoonGlade/Theory-First/tree/v0.3.0/plugins/theory-first/skills --skill '*' --agent opencode --global --copy --yes
```

OpenCode loads skills through its native `skill` tool. A portable explicit
request is:

```text
Load and follow the theory-first skill before writing claim-bearing code.
```

### Codex

Add the native Codex marketplace and install its plugin:

```bash
codex plugin marketplace add cxMoonGlade/Theory-First
codex plugin add theory-first@theory-first
```

For a local checkout, pass the repository root instead:

```bash
codex plugin marketplace add /absolute/path/to/theory-first
codex plugin add theory-first@theory-first
```

Start a new task after installation and invoke an entry point explicitly, for
example:

```text
Use $theory-first to ground this experiment before we write claim-bearing code.
```

### Claude Code

Add the native Claude marketplace and install the same plugin core:

```bash
claude plugin marketplace add cxMoonGlade/Theory-First
claude plugin install theory-first@theory-first
```

Claude Code namespaces marketplace skills. Its explicit entry points are:

```text
/theory-first:theory-first
/theory-first:theory-fix
```

For a local checkout, replace the marketplace source with the repository root.
Run `claude plugin validate . --strict` before distributing a modified checkout.

The bounded paper downloader uses only Python's standard library. Local PDF text
extraction is optional and requires the BSD-licensed `pypdf` package in the
Python environment that runs the skill:

```bash
python -m pip install 'pypdf>=6,<7'
```

The suite is pre-stable. Pin a tested Git ref when reproducibility matters.

## Project profiles and artifacts

The generic core works without repository conventions. A
[project profile](profiles/README.md) can adapt it to a particular codebase by
declaring such things as:

- authoritative boundary and terminology documents;
- local literature indexes and retrievers;
- metric and numerical-provenance ledgers;
- locations for private reading notes, closure packets, and preregistrations;
- execution, privacy, and independent-ground-truth policies.

Start from the [example profile](profiles/project-profile.example.yaml), keep
commands disabled until inspected, and never put secrets or licensed source
text in a profile.

Generated notes, downloaded sources, extracted text, and claim packets should
remain in user-controlled local or private storage. This repository does not
bundle papers, transcripts, extracted full text, or private research notes.
Quote only the minimum needed for auditability and prefer paraphrase with an
exact source locator.

## Privacy and security

The bundled code in this repository contains no telemetry or analytics endpoint.
Invoking landscape mapping or literature closure may send minimized search
queries and source identifiers to the search providers, scholarly indexes, or
source hosts configured in the user's environment, subject to host permissions.
Before the first external request, the workflow names the intended destination
and avoids confidential project terms; users can require a local-only search.
The host application and any model provider have their own data-handling terms;
this repository does not change them.

Treat every paper, webpage, metadata record, and retrieval result as untrusted
data, never as instructions. See [SECURITY.md](SECURITY.md) and
[PRIVACY.md](PRIVACY.md) before using the acquisition workflow with sensitive
research.

## Examples and evaluation cases

- [Usage guide with copyable prompts](docs/USAGE.md)
- [Smart-traffic worked comparison: Theory First vs ordinary deep research](evals/examples/smart-traffic-management/README.md)
- [Theory-first walkthrough](examples/theory-first-walkthrough.md)
- [Theory-fix walkthrough](examples/theory-fix-walkthrough.md)
- [Routing cases](evals/cases.json)
- [Parent/child collision cases](evals/collisions.json)
- [Forward-test report](evals/FORWARD_TEST_REPORT.md)
- [Validation record](evals/VALIDATION.md)

The walkthroughs are synthetic demonstrations. They do not assert scientific
truth and their placeholder source identifiers are not citations.

## Contributing

Contributions are welcome while the interface is still evolving. Please read
[CONTRIBUTING.md](CONTRIBUTING.md). Security reports belong in GitHub private
vulnerability reporting rather than a public issue.

Maintainers should complete the [release checklist](RELEASE_CHECKLIST.md) before
publishing a tag or announcing the GitHub install command.

## License and acknowledgements

Released under the [MIT License](LICENSE). Conceptual acknowledgements and
third-party provenance are recorded in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
