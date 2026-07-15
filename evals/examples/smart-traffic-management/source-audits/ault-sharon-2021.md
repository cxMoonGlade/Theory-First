# Ault and Sharon 2021 — auditable close-reading note

## Assignment

- Target evidence rows: E2, E3, E6.
- Claim or bridge under review: what a public SUMO traffic-signal benchmark
  actually measures and whether its fixed-time/MP arms close the frozen claim.
- Consequence if wrong: a recognized benchmark could lend false authority to
  vehicle-only metrics or a non-recalibrated fixed-time comparator.
- Required fidelity: state/reward definitions, controller identities, scenario
  construction, and result-selection procedure.
- Acceptance condition: identify both reusable benchmark practice and target
  quantities absent from it.
- Failure condition: present RESCO as validation of person/pedestrian outcomes.

## Source identity and provenance

| Field | Value |
|---|---|
| Title | Reinforcement Learning Benchmarks for Traffic Signal Control |
| Authors | James Ault; Guni Sharon |
| Venue or repository | NeurIPS 2021 Datasets and Benchmarks Track |
| DOI, arXiv ID, or stable identifier | [proceedings paper](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/f0935e4cd5920aa6c7c996a5ee53a70f-Abstract-round1.html) |
| Version and date | proceedings version, 2021 |
| Supplement or correction | None inspected |
| Artifact SHA-256 | `a5f63be76a2453f4402f92339fee1cebf649912ef02e0c9f45161b8233ce1e48` |
| Access date | 2026-07-15 |
| Evidence class | primary |
| Implementation locator and commit | [Pi-Star-Lab/RESCO](https://github.com/Pi-Star-Lab/RESCO); commit not pinned |

The inspected PDF is not redistributed with this repository.

## Source map

| Section or artifact | Purpose | Relevance to assignment | Read depth |
|---|---|---|---|
| §3.1–3.4, pp. 4–6 | state, reward, scenarios, baselines | E2/E3/E6 | close-read; p. 5 visually verified |
| §4, pp. 7–9 | experiment and reported metrics | selection/uncertainty | close-read; pp. 8–9 visually verified |
| §5, p. 9 | conclusions | transfer boundary | close-read |

## Notation ledger

The source exposes benchmark features and metrics in prose rather than a
load-bearing theorem. Its state includes vehicle counts/queues and signal phase;
its reported objectives are vehicle traffic quantities. No person or pedestrian
state is defined in the inspected benchmark interface.

## Assumption ledger

| Assumption | Exact locator | Used by | Project satisfies it? | Failure consequence |
|---|---|---|---|---|
| extracted Cologne/Ingolstadt SUMO scenarios and their calibrated demands represent the benchmark tasks | pp. 5–6, §3.3 | evaluation tasks | no | benchmark outcomes do not transfer to the corridor |
| fixed-time intervals come from each SUMO scenario | p. 6, §3.4 | fixed-time baseline | unknown / no | it is not evidence of a newly recalibrated comparator |
| state/reward observations are vehicle-oriented | p. 5, §§3.1–3.2 | controller evaluation | no for frozen multimodal claim | person and pedestrian endpoints are absent |

## Equation and definition ledger

| Item | Exact locator | Paper statement | Reconstruction | Checks | Status |
|---|---|---|---|---|---|
| reward/metric vector | p. 5, §3.2 | system travel time, approximated signal delay, vehicle wait, average queue, and pressure | all are vehicle traffic measures in the defined state | person/pedestrian fields absent | verified |
| fixed-time baseline | p. 6, §3.4 item 1 | phases run for scenario-defined fixed durations in a cycle | reusable baseline implementation, not a calibration method | comparator identity checked | verified |
| max-pressure baseline | p. 6, §3.4 item 2 | phase combination with maximal joint pressure | implementation follows a cited RL-era formulation | not equation-matched to Varaiya here | ambiguous for frozen treatment |

## Theorem and proof ledger

No theorem is used for the frozen claim.

## Figure and table ledger

| Item | Locator | Visual facts | Caption claim | Author inference | Project inference | Visual status |
|---|---|---|---|---|---|---|
| Fig. 4 | p. 8 | learning curves over five seeds with one-standard-deviation bands; best episodes marked | compares training behavior | some algorithms diverge | selection must be frozen | verified |
| Table 1 | pp. 8–9 | delay, trip time, wait, and queue are vehicle metrics; best episode can precede divergence | reports best episode over five seeds | best-episode summaries can differ from final behavior | confirmatory selection cannot use best observed run | verified |

## Algorithm and implementation reconstruction

- Inputs and outputs: vehicle/signal observations in, phase action out.
- Scenario selection: extracted realistic SUMO networks with calibrated demand.
- Baselines: scenario-defined fixed-time, max-pressure, and greedy control.
- Metrics: average vehicle delay, trip time, wait, and queue.
- Randomness and seeds: five random seeds for learning curves/results.
- Selection: Table 1 reports the best-performing episode, not necessarily final
  performance (p. 8).
- Missing implementation details for this claim: people/occupancies,
  pedestrians, P95 endpoints, incident, fixed-time recalibration protocol, and
  confirmatory controller selection.

## Claim ledger

| Label | Claim | Exact evidence or derivation | Assumptions | Falsifier | Status |
|---|---|---|---|---|---|
| `[source]` | RESCO supplies standardized SUMO tasks and baseline implementations | §3 | source scenarios/code | repository does not match paper | verified |
| `[source]` | the evaluated state and reported metrics are vehicle-oriented | p. 5; Table 1 | source interface | person/pedestrian definition in inspected interface | verified |
| `[source]` | best-episode reporting can mask later divergence | p. 8 discussion of Fig. 4/Table 1 | training evaluation | final episode equals selected episode | verified |
| `[project-inference]` | RESCO is useful as an implementation cross-check | benchmark code must be pinned | formulation may differ | hand calculation disagrees | inference-only |
| `[conflict]` | RESCO closes the frozen person/pedestrian/fixed-time-calibration rows | required objects are absent or scenario-defined | none | exact source definitions appear | contradicted |

## Adversarial checks

- Metric substitution: vehicle average delay cannot be called person delay.
- Baseline substitution: “fixed-time included” does not mean “recalibrated on a
  declared training surface.”
- Selection bias: best episode is incompatible with a frozen confirmatory arm.
- External validity: realistic source scenarios are not local corridor data.

## Unresolved items and access limits

The code commit, current maintenance state, and scenario licenses were not
audited. A discovery attempt initially associated the benchmark title with
`arXiv:2103.01115`; the downloaded file at that identifier was an unrelated
economics paper. Source-title verification caught the mismatch before it entered
the evidence matrix. That arXiv identifier is excluded.

## Evidence-row disposition

- E2: `CONTRADICTED` as direct support: target person and pedestrian observables
  are absent.
- E3: `MISSING`: the fixed plan is scenario-defined, not a transferable
  recalibration procedure.
- E6: `INFERENCE_ONLY`: the benchmark offers useful implementation patterns, but
  no version-pinned corridor bundle exists.

This does not make RESCO a poor benchmark. It establishes that benchmark status
cannot substitute for target-observable and local-calibration fidelity.

## Minimal quotation ledger

No verbatim quotation is needed; all source statements above are paraphrased.
