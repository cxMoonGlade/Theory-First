# Usage Guide

English | [简体中文](USAGE.zh-CN.md)

[Back to the project README](../README.md)

This guide shows how to route concrete research tasks through the seven-skill
suite. Install the complete suite first. The examples below are prompt
templates, not claims that a particular source exists or that a workflow will
pass its gates. Replace every angle-bracketed field before use.

## Before choosing a case

Use the orchestrator unless the input already satisfies a child skill's
preconditions:

- use `theory-first` before a new claim-bearing experiment or implementation;
- use `theory-fix` after a result exists and before its interpretation
  propagates;
- use `map-research-landscape` directly for broad orientation only;
- use `close-literature` directly only for a frozen claim with explicit
  load-bearing evidence rows;
- use `deep-read-paper` directly for exactly one identified source and one
  assigned question;
- use `preregister-claim` directly only with a complete closed-literature
  packet; and
- use `stress-test-claim` directly only with a closed packet, the original
  preregistration, and the raw result artifacts.

No scientific status authorizes file edits, execution, network access, data
access, spending, or any other action outside the user's request and the host's
permissions.

## Case 1 — Ground a new experiment with theory-first

Use this route when an experiment, model, mechanism, observable, metric, or
prediction would otherwise be implemented from an unclosed scientific premise.

### Copyable prompt

```text
Use theory-first for a new claim-bearing experiment.

Decision: <decision this experiment will support>
Draft claim: <exact claim to freeze>
Mechanism: <proposed mechanism or governing operation>
Observable: <measured or computed quantity>
Regime: <population, scale, assumptions, and boundary conditions>
Known sources: <source identifiers or "none">
Project profile: <profile path or "none">
Retrieval boundary: <local-only or authorized external sources>

Do not write or run claim-bearing code, and do not inspect results, until the workflow returns its scoped code gate.
```

### Why it routes here

The result has not been inspected, and the task would create a new scientific
claim. `theory-first` therefore freezes the question, optionally maps unstable
terminology, closes the load-bearing literature, and preregisters predictions
before deciding whether claim-bearing code may begin.

### Expected artifacts

- a versioned charter with the claim, consequence, regime, rivals, kill
  condition, and non-goals;
- a landscape-map reference or an explicit reason it was skipped;
- a closure matrix and references to any load-bearing deep-reading notes;
- unresolved contradiction and scoped-gap records;
- a preregistration identifier and pass/fail ledger; and
- one scoped `CODE_BLOCKED` or `CODE_PERMITTED` record.

### Stop conditions

- A missing required child returns `SUITE_INCOMPLETE`; install the complete
  seven-skill suite before continuing.
- Any load-bearing row that is missing, ambiguous, inference-only,
  contradicted, inaccessible, or a `search-exhausted-gap` returns
  `CODE_BLOCKED`.
- A failed preregistration gate also returns `CODE_BLOCKED`.
- `CODE_PERMITTED` applies only to the frozen claim version, regime, and
  implementation boundary. It is not a truth certificate or action permission.

## Case 2 — Map broadly, then close the literature

Use this two-step route when vocabulary is unstable, several formalisms
compete, or the initial search is likely to be too narrow. The map chooses the
reading path; it does not close evidence.

### Copyable landscape prompt

```text
Use map-research-landscape before narrowing this research question.

Decision: <decision the map will inform>
Current draft claim: <claim or question>
Mechanism and observable: <current formulation>
Known synonyms or neighboring fields: <terms or "unknown">
Scope limits: <time, language, access, and confidentiality boundaries>
Project profile: <profile path or "none">

Return an orientation map, explicit no-go boundaries, and a minimal candidate reading set. Label every source as a discovery lead and do not claim literature closure.
```

Once the map has made the evidence rows explicit, freeze the claim and hand it
to `close-literature`:

```text
Use close-literature on the frozen claim below, using the landscape map only as routing input.

Charter ID: <frozen charter identifier>
Decision: <decision this claim will support>
Frozen claim: <exact claim>
Mechanism: <mechanism>
Observable: <observable and measurement procedure>
Regime: <assumptions, scale, and boundaries>
Landscape map: <artifact path or identifier>
Known sources: <source identifiers>
Project profile: <profile path or "none">

Build the coverage matrix first. Assign every load-bearing source to an evidence row and invoke deep-read-paper where equation, theorem, figure, data, or implementation fidelity is required. Do not preregister or write experiment code.
```

### Why it routes here

`map-research-landscape` is the wide scan: terminology lattice, source
clusters, formulation crosswalk, benchmarks, implementations, and no-go
boundaries. `close-literature` is the narrow audit against a frozen claim. It
selects only sources that carry a mechanism, observable, bridge, validity,
metric, numerical, implementation, or disconfirmation row.

### Expected artifacts

- an orientation map, candidate reading set, search ledger, and evidence rows;
- a closure packet with a source inventory and row-by-row status;
- exact deep-read-note references for load-bearing equations, theorems,
  figures, data semantics, or implementation details;
- contradiction and numerical-provenance ledgers; and
- `CLOSED`, `OPEN`, `CONTRADICTED`, or `SEARCH_EXHAUSTED_GAP` from literature
  closure.

### Stop conditions

- Mapping stops at orientation saturation; it must not drift into a claim of
  comprehensive coverage.
- `close-literature` returns `SUITE_INCOMPLETE` if `deep-read-paper` is not
  discoverable.
- `OPEN`, `CONTRADICTED`, and `SEARCH_EXHAUSTED_GAP` block the theory-first
  evidence gate. They are not permission to preregister a positive premise.

## Case 3 — Deep-read one load-bearing paper

Use `deep-read-paper` when one exact source must be checked at equation,
theorem, figure, or implementation fidelity. Do not use it to discover a field
or select among many ambiguous citations.

### Copyable prompt

```text
Use deep-read-paper for exactly one source.

Source: <local PDF, exact title plus DOI, or arXiv identifier and version>
Assigned evidence row or question: <one precise question>
Target claim: <claim that would use this source>
Consequence if wrong: <downstream consequence>
Required fidelity: <equation, theorem, figure, table, algorithm, or implementation>
Project mapping: <symbols, quantities, or operation to compare>

Do not survey the field or execute source code. Separate source claims, reconstruction, project inference, unknowns, and conflicts, and attach exact locators to every load-bearing use.
```

### Why it routes here

The source and assignment are already identified. A field survey belongs to
`map-research-landscape`; multi-source discovery and selection belong to
`close-literature`.

### Expected artifacts

- fixed source identity, version, acquisition date, and digest;
- a source map and notation ledger;
- reconstruction of the assigned equations, theorem conditions, figures,
  tables, algorithms, or implementation details;
- a claim ledger separating `[source]`, `[reconstructed]`,
  `[project-inference]`, `[unknown]`, and `[conflict]`; and
- `CLOSED`, `INFERENCE_ONLY`, `MISSING`, `AMBIGUOUS`, or `CONTRADICTED` for each
  assigned evidence row.

### Stop conditions

- If the citation does not identify one source and version, supply an exact
  title plus DOI/arXiv identifier or the source file; do not guess.
- A load-bearing figure that cannot be inspected remains
  `VISUALLY_UNVERIFIED` and cannot close its row.
- `CLOSED` is local to the assigned row. It does not establish field-wide
  closure, accept the project claim, or authorize code.

## Case 4 — Audit a result with theory-fix or direct stress testing

Use `theory-fix` by default when a result is surprising, unusually clean,
hoped-for, summary-derived, sensitive to formulation, or about to become a
premise. Freeze it before changing code, parameters, exclusions, plots, or
wording.

### Copyable theory-fix prompt

```text
Use theory-fix before this result propagates.

Claim ID and exact wording: <identifier and frozen wording>
Statement type and intended confidence class: <registered values>
Code, configuration, data, environment, and result artifacts: <immutable identifiers>
Original charter and preregistration: <identifiers or recorded absence>
Observed metrics, uncertainty, exclusions, and stopping decision: <values and conventions>
Result-to-claim bridge: <why the result is said to support the claim>
Alternative explanations: <known rivals>
Downstream consumers: <definitions, designs, reports, or planned runs>

Freeze the artifacts and mark downstream consumers PROPAGATION_PAUSED. Reopen the load-bearing literature before stress testing. Do not edit code, rerun, or rewrite the claim during this audit.
```

Invoke `stress-test-claim` directly only when its complete prerequisite packet
already exists:

```text
Use stress-test-claim directly. The required refreshed closure packet, original preregistration, and raw result artifacts are already available.

Frozen claim: <exact wording and claim ID>
Consequence and downstream consumers: <decision and propagation sites>
Statement type and confidence class: <registered values>
Closed literature packet: <artifact identifier>
Original preregistration: <artifact identifier>
Raw artifacts and exact configuration: <immutable identifiers>
Alternative formulations and invariants: <registered alternatives>

Run every applicable trip-wire against the actual artifacts. Do not acquire literature, edit the preregistration, repair code, or launch a replacement experiment.
```

### Why it routes here

`theory-fix` owns the post-result sequence: freeze propagation, reopen evidence,
delegate hostile checks, and classify the top-level outcome. Direct
`stress-test-claim` is only valid after literature closure has already been
refreshed and all required artifacts are present.

### Expected artifacts

- a frozen claim and artifact manifest;
- a downstream propagation ledger and evidence-delta ledger;
- a wire-by-wire stress-test record and preregistration deviations;
- contrary evidence, residual risks, and forbidden extrapolations; and
- exactly one top-level `STOP`, `REPAIR`, `REOPEN_EVIDENCE`, or
  `ACCEPT_WITH_CLASS` decision from `theory-fix`.

### Stop conditions

- A hard wire, irreproducibility, invalid provenance, or direct contradiction
  returns `STOP` unless a defect is localized, bounded, and testable as
  `REPAIR` on a fresh artifact.
- Missing literature, a recoverable artifact, or an obtainable independent
  check returns `REOPEN_EVIDENCE`; direct stress testing may report `PENDING`.
- `REPAIR` does not validate the repaired result; it requires a new version and
  fresh test under the unchanged acceptance rule.
- Only `ACCEPT_WITH_CLASS` can resume propagation, and only within its exact
  class and regime. “Survives current wires” is not proof.

## Case 5 — Handle a known literature gap honestly

Use this route for a frozen claim whose load-bearing premise is already known
to lack adequate support. The task is to audit the search surface and define
the smallest next action, not to turn absence into positive evidence.

### Copyable prompt

```text
Use close-literature to audit a known load-bearing literature gap without turning absence into evidence.

Charter ID: <frozen charter identifier>
Decision and frozen claim: <decision and exact claim>
Load-bearing row: <mechanism, observable, bridge, regime, metric, value, implementation, or disconfirmation>
Proposition not yet supported: <exact proposition>
Known sources and prior searches: <identifiers and query records>
Search boundary: <corpora, query families, date, languages, year filters, citation depth, and access limits>
External retrieval authority: <authorized services or local-only>

Search for supporting and contrary primary evidence. If no adequate source is found, record the scoped search-exhausted-gap and return the correct closure status. Do not use the gap as a positive premise, preregister the claim, or write claim-bearing code.
```

### Why it routes here

The claim and missing row are already frozen, so the problem is evidence
closure rather than landscape orientation. A scoped `search-exhausted-gap`
records where the search looked; it never asserts that the whole field lacks
an answer.

### Expected artifacts

- the updated coverage matrix and source inventory;
- the exact search ledger, access failures, and contrary-evidence search;
- the proposition not found and the complete boundary of the recorded search;
- `OPEN`, `CONTRADICTED`, or `SEARCH_EXHAUSTED_GAP` when the row cannot close;
  and
- the smallest next action, such as obtaining access, expanding the approved
  search surface, or versioning and narrowing the claim.

### Stop conditions

- External search without authorization stops at the local boundary and leaves
  the row open.
- `search-exhausted-gap` does not close a load-bearing row; theory-first remains
  `CODE_BLOCKED`.
- Narrowing or changing the claim requires a new charter version and change
  ledger, never a silent rewrite.

## Case 6 — Requests that should not trigger this suite

These tasks do not, by themselves, require a scientific evidence gate:

```text
Rename this internal helper and update its existing unit tests without changing behavior.
```

```text
Translate this README while preserving its commands and links.
```

```text
Fix this deterministic CLI argument-parsing exception against the existing specification.
```

```text
Give me a short, non-claim-bearing summary of the abstract I supplied for personal orientation.
```

### Why they do not route here

They are ordinary engineering, documentation, or lightweight summarization
tasks with no new scientific premise, claim-bearing experiment, load-bearing
source verification, or result-to-claim propagation.

### Expected artifacts

Return the artifact appropriate to the ordinary task: a scoped code change and
tests, a translation, a bug fix, or a clearly limited summary. Do not fabricate
a Theory First status when the suite was not invoked.

### Escalation condition

Stop the ordinary route and select the appropriate skill if the task begins to
depend on an unclosed scientific premise, asks what one paper actually proves,
designs a claim-bearing experiment, or promotes a result into a downstream
claim.

## Case 7 — Invoke the same workflow on Codex, Claude Code, or OpenCode

Install all seven skills and start a new task. Select the case prompt first,
then prepend the host's native invocation. Skill names are identifiers for the
host's skill mechanism, not shell commands.

### Codex

```text
Use $<skill-name>.
<paste the selected case prompt here>
```

For the primary pre-result and post-result workflows, replace `<skill-name>`
with `theory-first` or `theory-fix`. Direct child names are valid only under the
preconditions stated earlier in this guide.

### Claude Code

```text
/theory-first:<skill-name>
<paste the selected case prompt here>
```

For example, the namespaced entry points are
`/theory-first:theory-first` and `/theory-first:theory-fix`.

### OpenCode

```text
Load and follow the <skill-name> skill before doing the task.
<paste the selected case prompt here>
```

OpenCode resolves the named skill through its native skill tool. Do not invent
a slash-command surface when the installed host exposes skill loading instead.

### Expected behavior and stops

All three hosts load the same canonical skill directories and should produce
the same routing and status semantics. If a dependency-bearing skill cannot
discover a named child, it returns `SUITE_INCOMPLETE` rather than improvising a
replacement workflow. Reinstall the complete suite and begin a new task before
retrying.

## Reading the final status

The full transition table is in the [status
model](../plugins/theory-first/STATUS_MODEL.md). The practical rule is short:

- before results, only a scoped `CODE_PERMITTED` clears the scientific gate;
- after results, `STOP`, `REPAIR`, and `REOPEN_EVIDENCE` keep propagation
  paused;
- `ACCEPT_WITH_CLASS` records survival within a named attack surface and exact
  regime, not universal truth; and
- every gap, pending wire, access limit, and project inference remains visible
  in the output packet.

For a complete same-prompt run, including a frozen rubric, equation-level
reading notes, a failed preregistration gate, and an illusion/drift comparison
against ordinary deep research, see the [smart-traffic worked
example](../evals/examples/smart-traffic-management/README.md).
