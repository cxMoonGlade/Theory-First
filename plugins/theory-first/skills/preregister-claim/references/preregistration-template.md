# Claim preregistration template

Copy this template into the project's declared evidence location. Complete it before claim-bearing implementation or result inspection. Keep the original immutable after execution begins; append an outcome record instead.

```markdown
# <Claim or experiment> — preregistration

Status: PRE-REGISTERED
Registered at: <ISO-8601 timestamp>
Registered by: <person or agent>
Execution has not begun: <yes/no; explain if no>
Results have not been inspected: <yes/no; explain if no>

## 1. Question charter

- Frozen claim:
- Decision and consequence:
- Importance × attackability:
- Reusable object or test:
- Alternative formulations:
- Invariants across formulations:
- Kill condition:
- Explicitly out of scope:

## 2. Evidence closure

| premise | closure row | exact source locator | status | role in claim |
|---|---|---|---|---|
| | | | closed | |

Unresolved gaps used only as motivation, never as positive premises:

## 3. Mechanism → observable bridge

| link | input object | operation or theorem | output object | source locator | failure mode |
|---|---|---|---|---|---|
| | | | | | |

Nearby quantities that must not substitute for the target:

## 4. Metric contract

- Field-standard metric and reference:
- Exact convention, units, aggregation, and uncertainty:
- Target population or regime:
- Forbidden proxies:
- Project-defined metric debt, if unavoidable:

## 5. Numerical provenance

| value or range | source kind | exact locator | original units/regime | transformation chain | compatibility and uncertainty |
|---|---|---|---|---|---|
| | source-measured / source-derived / dataset-measured / calibrated / project-design / convenience / numerical-only | | | | |

Cross-source composite compatibility argument:

## 6. Frozen predictions and decisions

| id | observable | prediction or null | statement type | magnitude band | decision rule | strongest competitor | disconfirming observation |
|---|---|---|---|---|---|---|---|
| P1 | | | (a)/(b)/(c) | | | | |

- Multiple-comparison or model-selection policy:
- Missing-data and exclusion policy:
- Stopping rule:
- Sensitivity analyses fixed in advance:

## 7. Independent ground truth

| prediction | reference method or raw artifact | why its blind spot differs | comparison rule |
|---|---|---|---|
| | | | |

## 8. Constraint and corruption ledger

| theorem, invariant, or limiting case | exact assertion | falsifying test | deliberately broken input | required trip evidence |
|---|---|---|---|---|
| | | | | |

## 9. Controls and non-degeneracy

- Negative or inert control and expected failure:
- Positive control and expected response:
- Corruption or shuffle control:
- Proof the intervention moves the measured object:
- Seed, split, or leakage controls:

## 10. Bounded simplifications

| simplification | faithful target | domain | error bound | validation method | action if bound fails |
|---|---|---|---|---|---|
| | | | | | STOP / REPAIR |

## 11. Statement-type and confidence ledger

- (a) exact theorem, identity, or zero-tolerance constraint:
- (b) registered prediction bands:
- (c) heuristic go/no-go gates:
- Maximum project-defined claim-confidence class for each outcome:
- Claims that this experiment cannot support:

## 12. Execution and outcome appendices

- Planned implementation owner and artifact locations:
- Raw-data immutability policy:
- Reproducibility commands or environment contract:
- Outcome append-only location:
- Downstream work blocked until outcome review:
```

## Source-kind meanings

- `source-measured`: measured in a cited primary source.
- `source-derived`: derived in a cited source from stated premises.
- `dataset-measured`: computed directly from an identified raw dataset.
- `calibrated`: fitted on declared calibration data.
- `project-design`: chosen because it defines the study.
- `convenience`: chosen for expedience and not evidence-backed.
- `numerical-only`: imposed for stability or precision.

Convenience and numerical-only values may be operationally necessary, but they cannot be presented as empirical facts. Record sensitivity ranges for every load-bearing value of either kind.
