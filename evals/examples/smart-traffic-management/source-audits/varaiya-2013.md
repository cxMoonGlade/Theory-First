# Varaiya 2013 — auditable close-reading note

## Assignment

- Target evidence rows: E1, E4, E5.
- Claim or bridge under review: the exact classical max-pressure controller,
  its guarantee, and whether that guarantee supports the frozen 10%/5% claim.
- Consequence if wrong: a throughput theorem could be misreported as a delay or
  non-inferiority theorem.
- Required fidelity: equations, theorem hypotheses, and limitation section.
- Acceptance condition: reconstruct the controller and state only the theorem's
  actual conclusion.
- Failure condition: any unclosed bridge from point queues to the three SUMO
  estimands.

## Source identity and provenance

| Field | Value |
|---|---|
| Title | Max pressure control of a network of signalized intersections |
| Authors | Pravin Varaiya |
| Venue or repository | *Transportation Research Part C* 36 (2013), 177–195 |
| DOI, arXiv ID, or stable identifier | [10.1016/j.trc.2013.08.014](https://doi.org/10.1016/j.trc.2013.08.014) |
| Version and date | Accepted manuscript/publication version; November 2013 |
| Supplement or correction | None inspected |
| Artifact SHA-256 | `b7a971218bfe69c836ce7e056acc76201b684d3be99063696022c20b8e5f4240` |
| Access date | 2026-07-15 |
| Evidence class | primary |
| Implementation locator and commit | none |

The inspected PDF is not redistributed with this repository.

## Source map

| Section or artifact | Purpose | Relevance to assignment | Read depth |
|---|---|---|---|
| Abstract and §1, pp. 177–179 | model and contribution boundary | assumptions | close-read |
| §3.1–3.2, pp. 183–184 | queue dynamics, stability, MP equations | E1/E5 | close-read and visually verified |
| §4.4–4.5, pp. 186–187 | long links and finite storage | E4 | close-read |
| §6, pp. 194–195 | limitations and future work | E4/E5 | close-read |

## Notation ledger

| Symbol | Paper meaning | Type or shape | Units | Domain | First definition | Project mapping |
|---|---|---|---|---|---|---|
| `x(l,m)(t)` | queue for turn movement from link `l` to `m` | nonnegative scalar | vehicles | point queue | p. 183, §3.1 | candidate movement-queue state, not yet a SUMO detector |
| `r(m,p)` | fixed turn ratio from `m` to `p` | probability | dimensionless | outgoing movements | pp. 179, 183 | requires calibrated or measured route proportions |
| `c(l,m)` | mean saturation flow | nonnegative scalar | vehicles/period | movement | p. 179 | requires a declared SUMO service estimator |
| `S(l,m)` | whether a movement is actuated | binary matrix entry | dimensionless | admissible stage | p. 183 | must include legal stage and clearance logic |
| `D`, `D⁰` | feasible demand set and its interior | set | vehicles/period | mean demand vectors | §2 | frozen recurrent profile is not automatically a member |

## Assumption ledger

| Assumption | Exact locator | Used by | Project satisfies it? | Failure consequence |
|---|---|---|---|---|
| bounded iid exogenous demand, turn movements, and saturation flow; mutual independence | p. 183, “Random demand, turns, saturation flow” | queue process and Theorem 2 | no / unknown | recurrent peak and incident do not inherit the theorem |
| fixed turn probabilities | abstract; pp. 178–179 | equations (18), (21), proof | unknown | pressure and feasible set change |
| separate point queue for every turn movement | abstract; §3.1 | state and update | no | shared lanes and head-of-line blocking are omitted |
| unlimited storage | abstract; p. 194, §6 | theorem model | no | spillback and de-facto red can invalidate the bridge |
| average demand lies in `D⁰` | p. 184, Theorem 2 | stability guarantee | unknown | theorem conclusion cannot be invoked |

## Equation and definition ledger

| Item | Exact locator | Paper statement | Reconstruction | Checks | Status |
|---|---|---|---|---|---|
| mean stability | p. 184, definition 3, eq. (20) | time-average expected total queue is bounded | this is a long-run queue property, not finite-horizon person delay | units and quantifier checked | verified |
| phase weight | p. 184, eq. (21) | upstream movement queue minus turn-ratio-weighted downstream queues | `w(l,m)=x(l,m)-sum_p r(m,p)x(m,p)` | exit-link limit checked | verified |
| stage pressure | p. 184, eq. (22) | saturation-flow-weighted sum of actuated movement weights | `gamma(S)=sum c(l,m)w(l,m)S(l,m)` | units are vehicle-like score per period | verified |
| MP policy | p. 184, eq. (23) | select an admissible signal matrix maximizing pressure | `u*(X)=argmax_S gamma(S)(X)` | tie-breaking and switching implementation not fixed | verified, implementation unresolved |

## Theorem and proof ledger

| Result | Locator | Hypotheses and quantifiers | Conclusion | Dependency or proof route | Project applicability |
|---|---|---|---|---|---|
| Theorem 2 | p. 184 | source queueing model and average demand `d` in `D⁰` | MP stabilizes the queue process; no controller stabilizes demand outside `D` | Lyapunov drift, eqs. (24)–(25) | violated / unknown |

## Figure and table ledger

No figure is load-bearing for the frozen numerical claim. Equations (20)–(25)
and Theorem 2 on p. 184 were visually checked against the PDF.

## Algorithm and implementation reconstruction

- Inputs and outputs: adjacent movement queues, mean turn ratios, saturation
  flows, and admissible stages in; one maximizing stage out.
- State and update order: choose the feedback control at a period boundary from
  the current queue vector; apply it during the next period (§3.1).
- Objective and estimator: maximize equation (22), not delay.
- Initialization and stopping rule: theorem is asymptotic; no finite SUMO
  horizon or stopping rule is supplied.
- Randomness and seeds: iid source model; no project seed protocol.
- Negative controls and ablations: examples show nearby local controllers can
  be unstable, but do not test the frozen three-estimand claim.
- Missing implementation details: queue detector, stage duration, clearances,
  minimum green, shared lanes, finite storage, incident representation, and
  tie-breaking.

## Claim ledger

| Label | Claim | Exact evidence or derivation | Assumptions | Falsifier | Status |
|---|---|---|---|---|---|
| `[source]` | classical MP maximizes throughput in the stated model | p. 184, eqs. (20)–(25), Theorem 2 | source model; `d in D⁰` | unbounded expected queues under a feasible source-model demand | verified |
| `[source]` | finite storage is a major limitation and can cause blocking | pp. 194–195, §6 | physical finite links | a faithful finite-link mapping with no blocking risk | verified |
| `[source]` | delay, utilization, and stop performance require further study | p. 195, §6 | none beyond paper scope | a result elsewhere, not this theorem | verified |
| `[project-inference]` | equation (23) is a plausible controller family for the corridor | equation-level mapping | implementation bridge still missing | detector/stage audit fails | inference-only |
| `[conflict]` | Theorem 2 proves a 10% mean-person-delay benefit and 5% tail non-inferiority | no such result; §6 explicitly leaves delay study open | none | source locator supporting those quantities | contradicted |

## Adversarial checks

- Dimensional/observable check: a bounded expected vehicle-queue sum is not a
  percentage change in seconds of person delay.
- Failed theorem hypothesis: finite storage, nonstationary peak demand, and a
  capacity-reducing incident are outside or unresolved.
- Implementation ambiguity: the source policy does not fully specify a legal
  SUMO signal program.
- Reversal condition: spillback can prevent the selected movement from
  discharging even when its source-model pressure is maximal.

## Unresolved items and access limits

No correction or implementation was inspected. The project has no calibrated
turn ratios, saturation rates, storage capacities, or detector-to-queue mapping.

## Evidence-row disposition

- E1: `INFERENCE_ONLY` for the project. The source controller is reconstructed,
  but the exact executable intervention is not frozen.
- E4: `CONTRADICTED` as a direct theorem transfer: core finite-storage and demand
  assumptions are violated or unknown.
- E5: `CONTRADICTED` as support for the numerical outcome. The theorem establishes
  stability/throughput only.

This does not establish that max pressure performs poorly; it establishes that
this source cannot supply the proposed outcome bridge.

## Minimal quotation ledger

No verbatim quotation is needed; all source statements above are paraphrased.
