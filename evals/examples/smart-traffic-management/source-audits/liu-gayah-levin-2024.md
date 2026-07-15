# Liu, Gayah, and Levin 2024 — auditable close-reading note

## Assignment

- Target evidence rows: E2, E3, E5, E8.
- Claim or bridge under review: whether vehicle-only queue MP controls person
  delay and pedestrian waiting, and what the pedestrian-aware alternative proves.
- Consequence if wrong: vehicle metrics or average pedestrian delay could be
  substituted for the frozen person and P95-crossing-wait endpoints.
- Required fidelity: controller equations/theorem, person-delay construction,
  visually checked result figures, and sensing limitations.
- Acceptance condition: keep PQ-MP and Q-MP distinct and preserve every metric
  mismatch or internal numerical conflict.
- Failure condition: import the paper's tuned values or average results into the
  corridor without a new claim version.

## Source identity and provenance

| Field | Value |
|---|---|
| Title | A Max Pressure Algorithm for Traffic Signals Considering Pedestrian Queues |
| Authors | Hao Liu; Vikash V. Gayah; Michael W. Levin |
| Venue or repository | arXiv manuscript; later *Transportation Research Part C* 169, 104865 |
| DOI, arXiv ID, or stable identifier | [arXiv:2406.19305v1](https://arxiv.org/abs/2406.19305); [10.1016/j.trc.2024.104865](https://doi.org/10.1016/j.trc.2024.104865) |
| Version and date | arXiv v1, 27 June 2024 |
| Supplement or correction | Journal-version differences not inspected |
| Artifact SHA-256 | `a38dd97842bad544d6993a4e3073c5fb1e651b49eef3c912ffe9a83db43f5ad9` |
| Access date | 2026-07-15 |
| Evidence class | primary |
| Implementation locator and commit | none identified |

The inspected manuscript is not redistributed with this repository.

## Source map

| Section or artifact | Purpose | Relevance to assignment | Read depth |
|---|---|---|---|
| §2, pp. 4–8 | vehicle/pedestrian dynamics and PQ-MP | mechanism | close-read; p. 8 visually verified |
| §4.1–4.2, pp. 14–16 | simulation and treatments | regime/controller identity | close-read; p. 15 visually verified |
| §4.3, pp. 17–23 | delays and measurement error | E2/E5/E8 | close-read; pp. 19–21 and 23 visually verified |
| §5, pp. 23–24 | conclusions and practical limits | E8 | close-read; p. 24 visually verified |

## Notation ledger

| Symbol | Paper meaning | Type or shape | Units | Domain | First definition | Project mapping |
|---|---|---|---|---|---|---|
| `x^v_{h,i,j}` | vehicles in a movement queue | nonnegative scalar | vehicles | point queue | §2.1 | vehicle pressure state |
| `x^p_{i,alpha,beta}` | pedestrians queued for a crosswalk movement | nonnegative scalar | persons | pedestrian node | §2.2 | pedestrian pressure state, not crossing-wait tail |
| `lambda` | pedestrian weight/coefficient in adjusted saturation/pressure | scalar | model-dependent | positive tested grid | eq. (7), §4.2 | controller tuning value, not a universal fact |
| `tau` | first-arrival wait threshold for rule-based MP | scalar | seconds | tested values | §4.2 | competing controller parameter |
| `d_v`, `p_in` | vehicle and pedestrian demand objects | vectors | rates | feasible demand sets | Theorem 1 | local corridor values absent |

## Assumption ledger

| Assumption | Exact locator | Used by | Project satisfies it? | Failure consequence |
|---|---|---|---|---|
| vehicle links use infinite-capacity store-and-forward point queues | p. 4, §2.1 | dynamics and theorem | no / unknown | incident spillback is not covered |
| pedestrian nodes have infinite occupancy and sidewalk walkers move at free-flow speed | p. 5, §2.2 assumptions 2–3 | pedestrian dynamics | unknown | crowding and walking delay differ |
| adjusted right-turn saturation-flow distribution is fixed | p. 8, Theorem 1 | maximum-stability theorem | unknown | theorem cannot be transferred |
| per-crosswalk pedestrian queue counts are available | p. 15, §4.2; p. 24, §5 | PQ-MP implementation | unknown | field-realizability and delay degrade |
| average vehicle occupancy is 1.3 persons/vehicle | p. 19, §4.3.2 | total person-delay comparison | no | source person weighting is not portable |

## Equation and definition ledger

| Item | Exact locator | Paper statement | Reconstruction | Checks | Status |
|---|---|---|---|---|---|
| PQ-MP policy | pp. 7–8, eqs. (5)–(9) | joint vehicle/pedestrian pressure determines the signal | distinct from original Q-MP because crosswalk queues enter state/action score | controller identity checked | verified |
| maximum stability | p. 8, Theorem 1 | PQ-MP stabilizes under stated vehicle/pedestrian feasible-demand conditions | throughput property for the paper's model | hypotheses and controller checked | verified |
| total person delay | p. 19, §4.3.2 | combine vehicle delay using 1.3 persons/vehicle with pedestrian delay | source-specific weighted total | units checked | verified in source scope |
| P95 pedestrian crossing wait | absent | paper reports average/total pedestrian delay, not the frozen tail estimator | no derivation exists in this source | nearby observable rejected | missing |

## Theorem and proof ledger

| Result | Locator | Hypotheses and quantifiers | Conclusion | Dependency or proof route | Project applicability |
|---|---|---|---|---|---|
| Theorem 1 | p. 8 | equations (5)–(9), combined feasible demand interior, fixed adjusted right-turn saturation distribution | PQ-MP maximizes joint vehicle/pedestrian throughput in the model | drift proof developed through §3 | unknown / violated |

The result is about **PQ-MP**, not original vehicle-only **Q-MP**, and it does
not impose a P95-wait non-inferiority bound.

## Figure and table ledger

| Item | Locator | Visual facts | Caption claim | Author inference | Project inference | Visual status |
|---|---|---|---|---|---|---|
| Fig. 8 | p. 19 | vehicle and pedestrian delay vary oppositely with `lambda`; tested tick values include 0.0005, 0.001, 0.002, 0.004, 0.006, 0.008, 0.01, 0.05, 0.1 | delay from PQ-MP | tuning reflects a trade-off | no universal coefficient | verified |
| Fig. 9 | pp. 20–21 | both alternative models reduce vehicle delay but increase pedestrian delay relative to Q-MP; PQ-MP has lower person delay than rule-based MP in tested cases | reductions relative to Q-MP | multimodal state improves the tested trade-off | average trade-off does not close P95 | verified |
| Fig. 11 | p. 23 | pedestrian performance degrades with queue-measurement error; at highest demand person delay can exceed the rule-based baseline | measurement-error impact | sensing matters | perfect SUMO state would overstate field readiness | verified |

## Algorithm and implementation reconstruction

- Inputs and outputs: vehicle queues, pedestrian crosswalk queues, turning and
  service objects in; selected phase out.
- State and update order: signal update every 20 s in the source simulation.
- Preprocessing and data selection: a synthetic 5×5 grid, four vehicle demand
  levels, ten starting seeds.
- Objective and estimator: source evaluates average/total vehicle, pedestrian,
  and person delay; it does not optimize the frozen P95 endpoint.
- Tuning: a grid of `lambda` and rule thresholds is inspected, then selected
  models are compared. This is exploratory tuning, not the frozen corridor's
  train/confirmatory separation.
- Negative controls and ablations: Q-MP and rule-based MP are comparisons;
  pedestrian measurement noise is a valuable stress test.
- Missing implementation details: no recalibrated fixed-time arm, four-signal
  corridor, recurring-peak/incident pair, P95 crossing wait, or P95 side-street
  queue.

## Claim ledger

| Label | Claim | Exact evidence or derivation | Assumptions | Falsifier | Status |
|---|---|---|---|---|---|
| `[source]` | PQ-MP has a maximum-stability result in its joint model | p. 8, Theorem 1 | theorem ledger | failed hypothesis or proof | verified |
| `[source]` | source person delay assumes 1.3 persons/vehicle | p. 19, §4.3.2 | source weighting | different occupancy model | verified |
| `[source]` | both PQ-MP and rule-based MP increase pedestrian delay relative to Q-MP in Fig. 9 | pp. 20–21, Fig. 9(b) and discussion | source grid and tuning | opposite plotted sign | verified |
| `[conflict]` | selected `lambda` is unambiguous | p. 19 prose gives `0.0006`, which is absent from the tested grid; Fig. 9 labels `0.006` | manuscript v1 | journal correction or code resolves it | ambiguous |
| `[project-inference]` | a pedestrian-aware claim version may be more credible than original Q-MP | source mechanism plus frozen guardrail | new treatment must be declared | original and new versions are conflated | inference-only |
| `[unknown]` | PQ-MP satisfies the frozen 5% P95 guardrail | no tail result | corridor data and estimator absent | confirmatory tail failure | missing |

## Adversarial checks

- Observable alternative: average pedestrian delay cannot substitute for P95
  crossing wait.
- Controller alternative: PQ-MP cannot be introduced as an implementation
  detail of Q-MP.
- Numerical conflict: p. 19 prose says `0.0006`, while the tested grid and Fig. 9
  identify `0.006`; neither may be copied without resolution.
- Regime failure: infinite vehicle storage is especially inappropriate for the
  incident stratum.
- Measurement corruption: source Fig. 11 shows that noisy pedestrian counts can
  reverse a high-demand comparison.

## Unresolved items and access limits

The journal version, code, and any correction were not inspected. The prompt
contains no occupancy, pedestrian-demand, sensing-error, or local calibration
artifact. The exact crossing-wait event estimator remains absent.

## Evidence-row disposition

- E2: `MISSING` for both network-wide person-delay construction in the local
  population and P95 crossing-wait semantics.
- E3: `MISSING`; there is no recalibrated fixed-time comparator.
- E5: `MISSING` for the 10%/5% numerical proposition.
- E8: `INFERENCE_ONLY`; the source motivates pedestrian-count and corruption
  checks but does not instantiate them for the corridor.

This note establishes neither a corridor effect nor a preferred treatment. It
does expose two high-risk illusion routes: average-to-tail substitution and an
internally inconsistent tuning value.

## Minimal quotation ledger

No verbatim quotation is needed; all source statements above are paraphrased.
