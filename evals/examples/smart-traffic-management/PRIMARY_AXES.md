# Primary comparison axes — illusion and drift

Added at the user's request on 2026-07-15, after the Theory First landscape
map was written but before the ordinary deep-research answer was inspected.
The original frozen [`RUBRIC.md`](RUBRIC.md) remains unchanged and supplies
diagnostic detail. These two axes determine the retrospective headline audit.

They were **not frozen before both arms ran**, so this example cannot establish
a causal workflow advantage on either axis. In addition, the prompt names a
“queue-based max-pressure” family but does not say “original vehicle-only
Q-MP.” The audit must preserve that ambiguity instead of retroactively narrowing
the intervention to make one arm look worse.

This is one worked example, not a statistical benchmark of agents or products.

## Axis A — evidence illusion

An **illusion event** is a sentence or decision that looks evidence-backed but
has not earned that status. Record each event with an exact answer locator and
classify it as:

1. `source-identity`: nonexistent, mismatched, or unverified source presented as
   the cited work;
2. `source-entailment`: a source is real but does not establish the proposition
   attached to it;
3. `bridge`: a theorem, mechanism, or neighboring observable is silently
   promoted into the target outcome;
4. `numerical-provenance`: a threshold, calibration value, effect size, or local
   parameter is treated as empirical without a valid origin;
5. `metric-semantics`: a similarly named field or aggregate is substituted for
   the declared estimand;
6. `false-completion`: an unresolved prerequisite is hidden behind a confident
   go/no-go conclusion.

Also record **caught illusion hazards**: tempting errors that the arm explicitly
detects, labels, and prevents from propagating. A longer list of declared gaps is
not itself a penalty. The main judgment is whether unsupported certainty enters
the recommendation.

Headline labels:

- `CONTROLLED`: no load-bearing illusion event survives into the recommendation;
- `LEAKED`: at least one load-bearing event survives, but uncertainty elsewhere
  limits its reach;
- `DOMINANT`: the recommendation substantially depends on unsupported premises.

## Axis B — decision drift

A **drift event** is an unannounced change to a frozen object that makes the
question easier or different. Check these invariants sentence by sentence:

| Frozen object | Must remain fixed | Typical silent substitution |
|---|---|---|
| decision | whether the study is ready to specify/run, then whether its result could support a pilot | recommending deployment from literature alone |
| intervention | queue-based max-pressure family; exact variant unresolved in the prompt | an unannounced switch after an exact variant has been selected |
| comparator | recalibrated fixed-time corridor plan | SUMO default or arbitrary fixed cycle |
| primary estimand | network-wide mean **person** delay | mean vehicle delay, vehicle waiting time, or throughput |
| guardrail 1 | P95 pedestrian crossing wait | mean pedestrian delay or ride waiting time |
| guardrail 2 | P95 side-street queue length | network mean queue, occupancy, or total vehicles |
| regimes | one recurrent peak and one predeclared incident | stationary demand, no incident, or post-hoc stress cases |
| numerical rules | 10% benefit and 5% harm margins | qualitative improvement or different thresholds |
| evidence boundary | no invented local calibration and no simulation run | fabricated geometry, demand, seeds, or results |

A proposed alternative is not drift when it is labeled as a separate claim
version and the original version is stopped rather than silently overwritten.
When the prompt itself leaves the exact variant open, selecting and naming one
is an intervention-definition **watch item**, not automatically a drift event.
The scorer must check whether the choice and alternatives remain visible.

Headline labels:

- `ANCHORED`: all load-bearing invariants are preserved or explicit version
  changes stop the original claim;
- `WOBBLED`: one or more substitutions occur, but the final scope mostly returns
  to the frozen decision;
- `DRIFTED`: the recommendation answers a materially different question.

## Reporting rule

For each arm, report:

1. headline label for each axis;
2. an exact event ledger, including zero events if none are found;
3. caught hazards and the mechanism that caught them;
4. practical cost: searches, close reads, artifacts, and time-to-advice;
5. the original ten safeguards from `RUBRIC.md` as a secondary table.

Do not count cautious wording alone as illusion control. A claim is controlled
only when its source, bridge, metric, numerical provenance, and unresolved status
remain traceable to an artifact or an explicit gap.
