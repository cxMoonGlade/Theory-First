# Theory First status model

This file is the canonical transition table for the plugin. Child statuses describe evidence or a check; only the two orchestrators issue top-level workflow outcomes.

## Two separate classification axes

- **Statement type** is fixed before measurement: `(a) exact constraint`, `(b) registered prediction`, or `(c) heuristic gate`.
- **Claim-confidence class** is project-defined wording for how strongly a reviewed conclusion may be presented within an exact scope, such as `tentative` or `supported`.

Surviving a check never changes a statement type automatically and never upgrades claim confidence without an explicit `theory-fix` decision.

## Deep read → closure row

| `deep-read-paper` disposition | `close-literature` row status | Consequence |
|---|---|---|
| `CLOSED` | `closed` | The assigned row may close at the recorded fidelity and scope. |
| `INFERENCE_ONLY` | `inference-only` | Useful project reasoning, but not a closed premise. |
| `MISSING` | `missing` | Evidence was absent or inaccessible. |
| `AMBIGUOUS` | `ambiguous` | Material readings remain unresolved. |
| `CONTRADICTED` | `contradicted` | The source conflicts with the frozen proposition. |

Retrieval hits, abstracts, snippets, and summaries never enter this table as closed evidence.

## Closure rows → closure packet

Apply this precedence:

1. Any credible load-bearing `contradicted` row yields `CONTRADICTED`.
2. Otherwise, any `missing`, `ambiguous`, `inference-only`, or inaccessible row yields `OPEN`.
3. Otherwise, if the only unresolved row is a fully scoped `search-exhausted-gap`, yield `SEARCH_EXHAUSTED_GAP`.
4. Only all-`closed` load-bearing rows yield `CLOSED`.

`SEARCH_EXHAUSTED_GAP` means “not found within the recorded search surface,” never field-wide absence.

## Theory First gate

| Closure packet | Preregistration | Top-level outcome |
|---|---|---|
| `CLOSED` | `pass` | `CODE_PERMITTED` for the exact claim version and implementation boundary |
| `CLOSED` | `fail` or absent | `CODE_BLOCKED` with preregistration blockers |
| `OPEN`, `CONTRADICTED`, or `SEARCH_EXHAUSTED_GAP` | any value | `CODE_BLOCKED` with the smallest reopening action |

`CODE_PERMITTED` is scientific-workflow clearance only. It never grants user authorization to edit files, execute code, use a network, spend money, access data, message people, or exceed host permissions. The user's request and the host's safety controls remain authoritative.

## Stress child → Theory Fix outcome

| `stress-test-claim` child outcome | Additional condition | `theory-fix` outcome |
|---|---|---|
| `STOP — wire fired` | Every fired defect is localized, bounded, and testable on a fresh artifact under the unchanged acceptance rule | `REPAIR` |
| `STOP — wire fired` | Any defect is irrecoverable, unbounded, contradictory, provenance-invalid, or lacks a defensible repair | `STOP` |
| `PENDING` | Required artifact or independent check is recoverable or obtainable | `REOPEN_EVIDENCE` |
| `REOPEN_EVIDENCE` | A named closure row is unresolved | `REOPEN_EVIDENCE` |
| `SURVIVES CURRENT WIRES` | Refreshed closure is `CLOSED`, no wire is pending, and scope is fixed | `ACCEPT_WITH_CLASS` |
| `SURVIVES CURRENT WIRES` | Any parent gate remains incomplete | `REOPEN_EVIDENCE` |

Credible load-bearing contradiction found during evidence reopening maps directly to `STOP`; do not pass an unclosed packet into the stress child. Irrecoverable loss of claim-bearing provenance or predict-before-measure records is a fired wire, not `PENDING`.

## Propagation

`CODE_BLOCKED`, `STOP`, `REPAIR`, and `REOPEN_EVIDENCE` keep affected downstream scientific claims paused. `CODE_PERMITTED` and `ACCEPT_WITH_CLASS` apply only to the named version, scope, confidence wording, and next action; neither is universal validation.
