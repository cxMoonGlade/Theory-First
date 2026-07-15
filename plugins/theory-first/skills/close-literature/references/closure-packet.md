# Literature-closure packet

Use one packet per frozen claim version.

## Header

```text
charter_id:
claim_version:
frozen_claim:
decision_supported:
project_profile_version:
evidence_snapshot_date:
search_languages:
access_constraints:
closure_status: CLOSED | OPEN | CONTRADICTED | SEARCH_EXHAUSTED_GAP
```

## Evidence matrix

| Row ID | Function | Proposition that must be supported | Evidence locator | Evidence kind | Regime | Status | Conflict or next action |
|---|---|---|---|---|---|---|---|
| E1 | mechanism |  |  | source claim / project fact / project inference |  | closed / missing / ambiguous / inference-only / contradicted / search-exhausted-gap |  |

The `Function` column should cover mechanism, observable, bridge, validity regime, metric/baseline, numerical value, implementation fidelity, and disconfirmation whenever they are load-bearing. Add rows rather than compressing different propositions into one citation.

An evidence locator identifies the exact equation, theorem, figure, table, section, dataset record, specification clause, or durable artifact. A URL or paper title alone is not a locator.

## Numerical provenance

| Value ID | Value and units | Role | Source kind | Exact locator | Transformation chain | Regime compatibility | Status |
|---|---|---|---|---|---|---|---|

Useful source kinds include source-measured, source-derived, dataset-measured, calibrated, project-design, convenience, and numerical-only. Flag any composite assembled across sources with incompatible conventions or regimes.

## Search ledger

| Date | Corpus or database | Query family | Filters and language | Results screened | Relevant leads | Access limits |
|---|---|---|---|---:|---:|---|

## Scoped search-exhausted gap

Create this block only when needed:

```text
row_id:
proposition_not_found:
corpora_and_databases:
exact_query_families:
search_date:
languages:
year_filters:
backward_and_forward_citation_depth:
access_or_indexing_limits:
near_misses_and_why_they_fail:
smallest_search_that_could_change_status:
```

The valid conclusion is “not found within this recorded search surface,” not “no such evidence exists.”

## Source inventory

For each selected source, record stable identity, version, access date, assigned evidence rows, deep-read-note path, correction/retraction status, and redistribution constraints. Do not embed the paper or its full extracted text.
