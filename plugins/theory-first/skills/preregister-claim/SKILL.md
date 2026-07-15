---
name: preregister-claim
description: Convert a literature-closed computational-science claim into a falsifiable preregistration before claim-bearing code is written or results are inspected. Use after close-literature, or when a complete closure packet already exists, to freeze the question, mechanism-to-observable bridge, standard metrics, numerical provenance, prediction bands, independent ground truth, constraint falsifiers, controls, bounded simplifications, and decision rules. This skill checks a prerequisite gate; it does not search literature, run experiments, or authorize code by itself.
---

# Preregister Claim

Turn a closed evidence packet into bets that cannot be silently rewritten after measurement.

## Hard boundary

Do not write or run claim-bearing experiment code. Do not inspect results that could inform the predictions. Existing platform code may be named as an implementation target, but it is not evidence for its own correctness.

Require a `close-literature` packet. Every load-bearing premise must be `closed`:

- `missing`, `ambiguous`, `inference-only`, or `contradicted` blocks the gate.
- A `search-exhausted-gap` may motivate the question, but it cannot support a positive premise.
- An abstract, search snippet, citation count, or retrieval hit is not a closed premise.

If the preconditions fail, emit `preregistration gate: fail`, name the exact rows, and stop.

## Workflow

1. **Freeze the question charter.** State the decision and consequence, why the question is important and attackable now, the reusable object or test it could produce, at least two formulations, their invariants, and the kill condition. Difficulty, novelty, and prestige do not establish importance.
2. **Bind mechanism to observable.** Name the causal or mathematical mechanism, the measured object, and every bridge needed between them. Cite exact locations in reading notes. Explicitly list nearby quantities that do not answer the question.
3. **Bind a standard metric.** Prefer a field-standard metric with its exact convention, units, aggregation, uncertainty, and reference. A project-defined metric is allowed only as declared debt when no suitable standard exists; never silently replace the target with a convenient proxy.
4. **Create the numerical-provenance ledger.** For every claim-bearing constant, range, threshold, prior, and tolerance, record source kind, exact locator, units and regime, transformations, compatibility assumptions, and uncertainty. Cross-source composites require an explicit compatibility argument.
5. **Freeze predictions and decisions.** Register sign, direction, scaling, and magnitude bands where justified. For each prediction, state the null, strongest competing explanation, decision rule, multiple-comparison policy when relevant, and what observation would disconfirm the preferred claim. Do not invent precision unsupported by the evidence.
6. **Choose independent ground truth.** Use a raw artifact, closed form, hand reconstruction, or genuinely different method with a different blind spot. A second wrapper around the same implementation is circular.
7. **Register constraints and corruption falsifiers.** Enumerate every theorem, invariant, conservation law, schema constraint, or limiting case the implementation must satisfy. For each, define an assertion and a deliberately broken input that must make the test fail. A clean-input pass alone is not a falsifier.
8. **Bound simplifications.** Give each approximation, truncation, surrogate, discretization, and convenience assumption a domain and error bound against the faithful target. An unbounded load-bearing simplification blocks the gate.
9. **Register controls and non-degeneracy.** Define inert, positive, negative, shuffled, or corrupted controls as applicable. Prove that the intervention changes the measured object rather than only configuration metadata. Freeze exact assertions and tolerances.
10. **Separate statement types from claim confidence.** Label statements as `(a) exact` theorem/identity, `(b) registered prediction`, or `(c) heuristic gate`. Undeclared statements default to `(c)`. A successful heuristic does not become an exact premise. Separately freeze the maximum project-defined claim-confidence class each possible outcome could earn.
11. **Write the preregistration.** Read `references/preregistration-template.md` completely and fill every applicable field. Mark non-applicable fields with a reason rather than deleting them.

## Gate and handoff

Return the preregistration location plus this ledger:

`premises closed | mechanism-observable bridge bound | standard metric bound | value provenance complete | predictions frozen | independent ground truth | corruption falsifiers | simplifications bounded | controls non-degenerate | preregistration gate`

Emit `preregistration gate: pass` only when every hard item passes. Otherwise emit `fail` with exact blockers and the owning upstream skill. This child skill never emits `CODE_PERMITTED`; the `theory-first` orchestrator owns that final decision.

A later miss is a finding. Preserve the original registration and append outcomes; never edit the original band, metric, or decision rule to fit the result.
