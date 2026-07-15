# Theory First

> Close the literature. Preregister the claim. Try to falsify the result.

Theory First is a pre-release Codex plugin containing agent skills for rigorous
computational science. It turns a scientific claim into an auditable sequence:
map the surrounding field, close the load-bearing evidence, preregister what
would count as success or failure, and attack a result before allowing it to
propagate.

The plugin is intentionally stricter than a paper summarizer. Its public core is
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

- `$theory-first` — use before claim-bearing experiment or implementation work.
- `$theory-fix` — use when a result is surprising, unusually clean, relied on by
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

This repository is laid out as a Codex marketplace containing one plugin. Add
its marketplace source with:

```bash
codex plugin marketplace add cxMoonGlade/Theory-First
codex plugin add theory-first@theory-first
```

For a local checkout, pass the marketplace root directory instead:

```bash
codex plugin marketplace add /absolute/path/to/theory-first
codex plugin add theory-first@theory-first
```

The first command registers the marketplace; the second installs its plugin.
You can also inspect or install it from the plugin directory in the ChatGPT
desktop app. Start a new task after installation and invoke an entry-point skill
explicitly, for example:

```text
Use $theory-first to ground this experiment before we write claim-bearing code.
```

The bounded paper downloader uses only Python's standard library. Local PDF text
extraction is optional and requires the BSD-licensed `pypdf` package in the
Python environment that runs the skill:

```bash
python -m pip install 'pypdf>=6,<7'
```

The plugin is pre-release. Pin a tested Git ref when reproducibility matters.

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

The plugin code in this repository contains no telemetry or analytics endpoint.
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
