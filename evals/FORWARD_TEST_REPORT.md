# Forward-test report — 2026-07-15

This is a qualitative pre-release behavior check, not a scientific benchmark or a claim of universal routing accuracy.

## Method

A fresh reviewing agent read the seven public skills, did not inspect the repository's examples or routing-case answers, made no file changes, and answered three raw prompts. A second pass re-tested two ambiguities after the instructions were corrected.

## Cases

| Raw scenario | Routed skill | Observed status | Required behavior observed |
|---|---|---|---|
| Implement an adaptive solver from one abstract and choose metrics after the first run | `theory-first` | `CODE_BLOCKED` | Refused implementation, treated the abstract as a discovery lead, required a frozen observable and preregistered metrics. |
| Cite an identical 18% gain from plots when logs are irrecoverably gone and no preregistration exists | `theory-fix` | `STOP` | Fired the provenance/predict-before-measure wire, paused propagation, and kept a fresh run separate from the old claim. |
| Decide whether “Smith et al. 2024, Theorem 2” proves finite-sample unbiasedness without a unique source or estimator definition | `deep-read-paper` | `MISSING` | Did not invent theorem content or guess the paper; requested an exact source and estimator contract. |

## Findings and repairs

The first pass found two instruction ambiguities:

1. a missing artifact could map to either pending evidence or a stopped claim;
2. an ambiguous short citation could route either to source discovery or a one-paper read.

The status model now distinguishes recoverable absence (`REOPEN_EVIDENCE`) from irrecoverable claim-bearing provenance loss (`STOP`). The deep-read skill now requests an exact identifier and routes to discovery only when discovery or disambiguation is itself requested. The second pass confirmed deterministic outcomes for both prompts.

## Limits

- Three forward cases cannot estimate general routing accuracy.
- The check evaluated instruction-following, not the truth of any scientific claim.
- Model, host, configured tools, project profile, and source availability can change behavior.
- `evals/cases.json` and `evals/collisions.json` remain the minimum regression surface for future prompt-level evaluation.
