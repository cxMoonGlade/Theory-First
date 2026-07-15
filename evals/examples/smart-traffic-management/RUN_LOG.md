# Worked-example run log — smart traffic management

- Snapshot: 2026-07-15
- Prompt: [`STM-COMPARE-001-v1`](PROMPT.md)
- Run type: qualitative, same-prompt retrospective process comparison; no simulation and no agent-product benchmark claim

## Isolation contract

- Both arms received the frozen prompt verbatim.
- The ordinary deep-research arm could search public academic/official sources
  but did not receive Theory First's status model, templates, child-skill
  routing, or the comparison rubric.
- The Theory First arm used the seven skills shipped in this repository. It had
  no filled project profile, local domain corpus, or city calibration data, so
  generic defaults and the prompt were its only project authority.
- [`RUBRIC.md`](RUBRIC.md) was frozen before either final answer was inspected.
- The user-requested [`PRIMARY_AXES.md`](PRIMARY_AXES.md) was added after the
  landscape artifact existed but before the ordinary answer was inspected. The
  ordinary answer was not edited after generation.
- Separate read-only audit passes scored each arm without reading the other arm
  first. Their durable findings are recorded in
  [`scorecards/`](scorecards/), but the repository does not contain raw platform
  transcripts that can independently prove the blindness claim.

The timing matters: the illusion/drift axes were not preregistered before both
arms ran. They are a user-requested retrospective lens. The prompt also left the
exact queue-based-MP variant unresolved; final audit therefore rejected a
too-narrow reading that had treated “original vehicle-only Q-MP” as frozen.

## Theory First route actually executed

| Stage | Released skill | Input | Output | Gate result |
|---|---|---|---|---|
| 1 | `theory-first` | frozen decision and claim v1 | route to landscape because the domain surface was not yet mapped | continue |
| 2 | `map-research-landscape` | prompt + public discovery search | [`THEORY_FIRST_LANDSCAPE.md`](THEORY_FIRST_LANDSCAPE.md) | `ORIENTATION_ONLY / LITERATURE_NOT_CLOSED` |
| 3 | `close-literature` | E1–E9 gap ledger from the map | [`THEORY_FIRST_PACKET.md`](THEORY_FIRST_PACKET.md) | `OPEN` |
| 4 | `deep-read-paper` | assigned mechanism, limitation, observable, and baseline sources | [`source-audits/`](source-audits/) | narrow source claims reconstructed; project bridges remain open |
| 5 | `preregister-claim` | open closure packet | [`THEORY_FIRST_PREREGISTRATION_GATE.md`](THEORY_FIRST_PREREGISTRATION_GATE.md) | `CODE_BLOCKED`; no preregistration emitted |

The route stopped before code exactly where the released orchestrator says it
must stop. `CODE_BLOCKED` means “the claim is not ready to implement,” not “the
controller has been empirically disproved.”

## Source handling

- Discovery used local repository inspection first, then bounded AnySearch
  academic search and public web search.
- Search snippets routed sources but were not evidence.
- Four primary papers were acquired privately for inspection; relevant theorem,
  equation, and result pages were visually checked. Full texts are ignored and
  not distributed by this repository.
- Official live SUMO documentation was inspected as a technical specification;
  it remains an implementation gap until an executable release/commit is pinned.
- Exact searches and access limits are in the landscape and closure packet.

## Ordinary deep-research route actually executed

The comparison arm searched current academic and official sources, synthesized
one advice document, and produced
[`DEEP_RESEARCH_BASELINE.md`](DEEP_RESEARCH_BASELINE.md). It did not use Theory
First artifacts and did not run a simulation. The generated answer remains
unchanged so its source-attribution and controller-version choices can be
audited rather than repaired after scoring.

## Result boundary

This example measures two failure-containment properties in one difficult
question:

1. evidence illusion—whether unsupported certainty survives into advice; and
2. decision drift—whether the answer silently changes the frozen treatment,
   comparator, observable, regime, or threshold.

It does not measure general answer quality, average agent performance, search
recall, or empirical traffic-controller effectiveness. Repeated blinded tasks
would be required for any statistical product claim.

It also cannot establish a comparative illusion or drift **rate**: the axes were
added after one intermediate Theory First artifact existed, the exact controller
was under-specified, and no raw runner transcript is published. The committed
[`RUN_MANIFEST.json`](RUN_MANIFEST.json) provides post-run artifact identities,
not cryptographic proof of the generation order.

## Pre-release audit corrections

An isolated audit of the Theory First arm found no load-bearing illusion or
drift, but it found two local errors in the Grégoire reading note: a same-run
seed statement had been misread as ten replications, and the note had failed to
retain the manuscript's internal “3-hour” versus “7–9 a.m.” duration conflict.
Both were corrected before release. The audit also tightened three prompt line
locators in the numerical-provenance table. None of these statements had entered
the evidence matrix's gate result or the `CODE_BLOCKED` recommendation.

The isolated ordinary-arm audit found one non-load-bearing author-attribution
error. Its generated answer remains unchanged; the event is recorded in the
comparison so the baseline is not repaired after scoring.

A final cross-arm audit found that the first comparison draft had over-scored
the ordinary answer's controller choice as definite drift. Because the prompt
did not say “original vehicle-only Q-MP” and the answer visibly distinguished
the variants, the event was downgraded to an intervention-definition watch item.
The correction is reflected in both language pages and the scorecards. This is
the Theory Fix behavior the suite is meant to encourage: a favorable comparison
claim does not survive a fired trip-wire.
