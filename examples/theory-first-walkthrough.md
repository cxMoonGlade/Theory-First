# Synthetic theory-first walkthrough

This is a routing and output example, not a scientific claim. The scenario,
numbers, source identifiers, and excerpts are invented. `SRC-A` and `SRC-B` are
placeholders, not citations.

## Before

A researcher starts with this request:

> Implement an adaptive spectral filter for our time-dependent PDE solver. I
> expect at least 20% lower steady-state error, and it should preserve mass.

The request combines a mechanism, an outcome, a numerical threshold, and a
constraint, but none is yet pinned to a definition or an independent check. The
initial record is therefore:

```yaml
claim: adaptive spectral filtering reduces steady-state error by at least 20%
constraint: conserved mass is unchanged
observable: unspecified
comparison: unspecified
evidence_status: open
preregistration_status: absent
decision: CODE_BLOCKED
```

`$theory-first` asks what consequence makes the question worth answering and
what observation would kill the mechanism claim. It maps nearby method families
before selecting a small, load-bearing reading set.

## Evidence closure

The synthetic closure ledger might become:

| Evidence row | Required bridge | Synthetic record | Status |
| --- | --- | --- | --- |
| Mechanism | Filter operation to damping of unresolved modes | `SRC-A`, Eq. 7 and assumptions | closed |
| Observable | Discrete solution to normalized steady-state error | `SRC-B`, Sec. 3.2 | closed |
| Constraint | Update rule to discrete mass balance | No adequate source within the recorded boundary | search-exhausted-gap |
| Threshold | Why 20% is scientifically meaningful | Project preference only | inference-only |

The gap record contains the synthetic databases, queries, search date,
languages, citation depth, and access limits. It does not claim that no mass
preservation result exists anywhere.

At this point the original claim remains blocked. The researcher narrows it:

> Test whether the declared filter reduces normalized steady-state error versus
> the frozen unfiltered baseline. Treat 20% as a decision threshold, not a
> literature-backed constant. Require mass drift below the solver's independently
> measured numerical floor.

## Preregistration

Before implementation or result inspection, the synthetic preregistration fixes:

```yaml
primary_metric: normalized steady-state error at fixed grid, step budget, and wall-clock cap
comparison: frozen unfiltered solver with identical initialization
prediction_band: relative error change <= -0.20
constraint_falsifier: absolute mass drift exceeds independently measured floor
independent_ground_truth: higher-resolution reference using a different integration path
negative_control: identity filter
corruption_test: reverse the filter weights; the primary metric must worsen
statement_type: "(b) registered prediction"
maximum_claim_confidence_if_passed: "project-supported numerical result"
```

The threshold's provenance is recorded as `project-design`, not disguised as a
published value. The conservation rule is testable even though its literature
row remains a scoped gap.

## After

The final gate is conditional and explicit:

```yaml
evidence_packet: closed_for_narrowed_claim
open_gap:
  kind: search-exhausted-gap
  scope: theoretical mass-preservation proof
  effect: blocks_theorem_claim_but_not_declared_numerical_test
preregistration_status: pass
decision: CODE_PERMITTED
permitted_scope: run the preregistered numerical comparison only
still_blocked:
  - claim of a general conservation theorem
  - claim that 20% is a literature-established constant
```

The change from `CODE_BLOCKED` to `CODE_PERMITTED` came from narrowing the claim,
closing its observable and mechanism bridges, declaring value provenance, and
making the remaining gap's consequences explicit—not from assuming the hoped-for
result is true.
