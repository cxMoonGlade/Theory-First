# Claim stress-test trip-wires

Run every applicable wire. Preserve `pending` when the required evidence is unavailable.

## 1. Theorem, symmetry, and limiting-case wire

Write the governing theorems, symmetries, conservation laws, bounds, dimensional constraints, and limiting cases for the complete configuration: intervention, initial or boundary conditions, dynamics, estimator, and observable.

Ask whether a transformation `T` forces an observable relation such as `O(x) = O(Tx)`, `O(x) = -O(Tx)`, a zero, or a bound. Test those relations numerically and analytically where possible. A forbidden result is a fired wire, not a small discrepancy.

## 2. Formulation and bridge wire

Express the claim in every frozen formulation and compare at the measured-object level. Check each mechanism → latent quantity → observable → metric bridge separately.

A source's result for a rate, state variable, surrogate, or asymptotic regime does not automatically govern a finite-sample record statistic. Shared terminology is not a bridge. Unexplained disagreement fires the wire or reopens evidence.

## 3. Independent-ground-truth wire

Ask whether the reference and implementation could share the same error. Prefer a raw artifact, hand derivation, closed form, constructive null, alternative discretization, or independently implemented representation.

A second wrapper, re-export, or refactor around the same engine is circular and leaves this wire `pending`.

## 4. Non-degeneracy wire

Prove that the intervention changes the object actually measured. Compare the test point with a null point using a preregistered object-level tolerance.

Check for no-op parameters, clipped ranges, equivalent operators, inert components, data leakage, identical random streams, stale caches, byte-identical outputs, and metrics insensitive to the claimed change. A degenerate design fires the wire.

## 5. Measurement-lens wire

For weak, absent, or unexpectedly clean results, enumerate every basis choice, projection, aggregation, filter, truncation, regularizer, split, selection rule, and plotting choice between the underlying object and headline metric.

Test whether any lens can erase, manufacture, or reverse the signal. A result visible only after an unregistered lens change fires the wire; an immature or suppressing lens cannot support an intrinsic-system conclusion.

## 6. Un-led adversarial-reproduction wire

Give an independent reviewer only the frozen problem, goal, claim, and raw artifacts. Require reconstruction of load-bearing quantities and active search for counterexamples. Do not reveal the suspected diagnosis or expected answer.

If independence is impossible, document why and leave the wire `pending`.

## 7. Predict-before-measure wire

Compare the interpretation with the immutable preregistration and its `(a) exact / (b) registered prediction / (c) heuristic gate` classes.

Check for changed bands, metrics, exclusions, seeds, stopping rules, subgroups, thresholds, or headline observables after result inspection. A miss remains a finding. Undeclared post-selection fires the wire and must be labeled exploratory.

## 8. Propagation wire

Search project artifacts for the exact claim and its aliases. Classify each consumer as a definition, premise, derivation, design choice, experiment, decision, or narrative mention.

When any wire fires, block and repair premise-bearing consumers first. Preserve the failed claim and correction trail. A local correction with unexamined downstream consumers leaves this wire fired.

## Wire ledger

For each wire record:

| wire | status | object tested | method | exact evidence locator | counterexample or limitation | next action |
|---|---|---|---|---|---|---|
| 1–8 | survives / fires / pending / not applicable | | | | | |

An empty counterexample column does not establish survival; the method and evidence must show that the stated failure mode was actually challenged.
