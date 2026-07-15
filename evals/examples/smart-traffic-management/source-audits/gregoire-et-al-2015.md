# Grégoire et al. 2015 — auditable close-reading note

## Assignment

- Target evidence rows: E4, E5, E8.
- Claim or bridge under review: whether ordinary back-pressure remains a faithful
  intervention under finite road storage and an incident.
- Consequence if wrong: the study could select an action that cannot discharge,
  then mistake spillback artifacts for controller performance.
- Required fidelity: theorem/counterexample, normalized-pressure remedy, and
  SUMO comparison implementation.
- Acceptance condition: identify the exact finite-capacity failure and keep the
  proposed remedy distinct from classical queue-based MP.
- Failure condition: silently rename capacity-aware control as the frozen
  queue-based controller.

## Source identity and provenance

| Field | Value |
|---|---|
| Title | Capacity-Aware Backpressure Traffic Signal Control |
| Authors | Jean Grégoire; Xiangjun Qian; Emilio Frazzoli; Arnaud de La Fortelle; Tichakorn Wongpiromsarn |
| Venue or repository | *IEEE Transactions on Control of Network Systems* 2(2), 164–173 |
| DOI, arXiv ID, or stable identifier | [10.1109/TCNS.2014.2378871](https://doi.org/10.1109/TCNS.2014.2378871); [arXiv:1309.6484v3](https://arxiv.org/abs/1309.6484) |
| Version and date | arXiv v3, 22 April 2014; journal issue June 2015 |
| Supplement or correction | None inspected |
| Artifact SHA-256 | `849afe245f918d64f4a866c9b906e697e17ebbd13a91f3fecd6a1e26874491a7` |
| Access date | 2026-07-15 |
| Evidence class | primary |
| Implementation locator and commit | not supplied by paper |

The inspected manuscript is not redistributed with this repository.

## Source map

| Section or artifact | Purpose | Relevance to assignment | Read depth |
|---|---|---|---|
| §§II–III, pp. 2–4 | bounded-queue model and failure | E4/E8 | close-read; p. 4 visually verified |
| §IV, pp. 4–7 | capacity-aware pressure | alternative mechanism | mapped; load-bearing definitions close-read |
| §V, pp. 7–9 | SUMO implementation and results | baseline/regime transfer | close-read; pp. 7–9 visually verified |
| §VI, p. 9 | conclusions and limits | E4/E5 | close-read and visually verified |

## Notation ledger

| Symbol | Paper meaning | Type or shape | Units | Domain | First definition | Project mapping |
|---|---|---|---|---|---|---|
| `Q_a(k)` | occupancy/queue at node `a` in slot `k` | bounded scalar | vehicles | `[0,C_a]` | §II | physical storage-dependent state |
| `C_a` | maximum queue capacity | scalar | vehicles | positive finite | §II | lane length and vehicle/gap model |
| `P_a` | pressure at node `a` | scalar | normalized score | pressure function | §II | differs from unbounded linear queue pressure |
| `f_ab(k)` | feasible transfer from `a` to `b` | scalar | vehicles/slot | link movement | §II | blocked when downstream is full |

## Assumption ledger

| Assumption | Exact locator | Used by | Project satisfies it? | Failure consequence |
|---|---|---|---|---|
| each queue has known finite capacity | §II | bounded model and normalized pressure | unknown | capacity-aware policy cannot be instantiated |
| movement is infeasible when downstream is full | §II; p. 4 counterexample | Theorem 1 | expected in physical SUMO links | classical pressure can select a non-discharging phase |
| SUMO lane capacity is lane length divided by 7.5 m | p. 7, §V-A | source simulation | not transferable without local vehicle mix | source convenience becomes invented calibration |
| 15 s control slots include 4 s yellow | p. 7, §V-A | source simulation | not specified | outcome depends on switching contract |

## Equation and definition ledger

| Item | Exact locator | Paper statement | Reconstruction | Checks | Status |
|---|---|---|---|---|---|
| bounded linear-pressure saturation | p. 4, before §III-B | linear pressure saturates at different values when capacities differ | a full downstream queue can retain lower pressure than a larger upstream queue | finite-capacity limit checked | verified |
| work conservation | p. 4, §III-B | if some input-output pair can transfer, a work-conserving controller makes the junction work | separates selected phase from feasible discharge | counterexample checked | verified |
| normalized pressure | §IV, eq. (5) | use a convex pressure normalized by capacity | full queues reach a common normalized limit | recovers original behavior as capacities grow | verified for source model |

## Theorem and proof ledger

| Result | Locator | Hypotheses and quantifiers | Conclusion | Dependency or proof route | Project applicability |
|---|---|---|---|---|---|
| Theorem 1 | p. 4, §III-B | bounded queue constraints; ordinary linear-pressure back-pressure | not work-conserving in the general case | explicit four-node counterexample, Fig. 4 | directly relevant disconfirmation |

## Figure and table ledger

| Item | Locator | Visual facts | Caption claim | Author inference | Project inference | Visual status |
|---|---|---|---|---|---|---|
| Figs. 4–6 | p. 4 | selected movement is blocked; another feasible movement is not selected; congestion can propagate/deadlock | illustrates loss of work conservation and propagation | bounded queues create failure | incident makes this a required stress test | verified |
| Figs. 12–14 | pp. 8–9 | advantage of capacity-aware control appears as load rises; blocked turn example shown | source simulation comparison | ordinary pressure degrades near capacity | magnitude is not transferable | verified |

## Algorithm and implementation reconstruction

- Inputs and outputs: queue occupancies and capacities in; phase choice out.
- State and update order: 15 s slot in the source SUMO study, including 4 s
  yellow; queue lengths retrieved and signal program updated via TraCI.
- Objective and estimator: compare ordinary linear pressure with convex
  capacity-normalized pressure.
- Preprocessing and data selection: population varied from 10,000 to 39,000.
  The manuscript calls the morning peak 3 hours but labels it 7–9 a.m. (2
  hours), so the duration is internally inconsistent and is not imported.
- Baselines: the fixed cycle is explicitly non-optimized (p. 7), with a 60 s
  cycle and paper-selected phase durations. It is not the frozen recalibrated
  fixed-time comparator.
- Randomness and seeds: the same ActivityGen seed is used across controllers
  within a source test run; a replication count and frozen paired-seed decision
  rule are not supplied.
- Missing implementation details: no transferable corridor calibration,
  pedestrian/person estimand, P95 guardrail, or incident protocol.

## Claim ledger

| Label | Claim | Exact evidence or derivation | Assumptions | Falsifier | Status |
|---|---|---|---|---|---|
| `[source]` | ordinary back-pressure is not generally work-conserving with bounded queues | p. 4, Theorem 1 and Figs. 4–6 | bounded storage | general proof error or infeasible counterexample | verified |
| `[source]` | capacity-normalized pressure mitigates the identified propagation mechanism | §IV; §VI | known capacity and source model | remedy fails its work-conservation criteria | verified in source scope |
| `[source]` | the paper's fixed cycle is non-optimized | p. 7, §V-A item 3 | source setup | an optimization/calibration record | verified |
| `[project-inference]` | a declared incident is a high-value finite-capacity falsifier | source mechanism plus prompt | incident must reduce usable storage/service | no occupancy or spillback response | inference-only |
| `[conflict]` | the source comparison validates a recalibrated fixed-time baseline | p. 7 says non-optimized | none | calibration artifact | contradicted |

## Adversarial checks

- Alternative formulation: capacity-aware pressure is a distinct controller,
  not a harmless implementation detail.
- Observable mismatch: vehicle count/time in network is not person delay or a
  pedestrian tail.
- Limiting case: normalized pressure approaches the ordinary form as capacities
  grow; the frozen incident moves the study in the opposite direction.
- Numerical portability: 7.5 m per vehicle and the timing values are source
  design choices, not local corridor facts.

## Unresolved items and access limits

The journal correction history and implementation source were not inspected.
The project has no capacity calibration, exact incident, or selected MP variant.

## Evidence-row disposition

- E4: `CONTRADICTED` for an unqualified classical-MP transfer into a finite-link
  incident regime.
- E5: `MISSING` for the proposed 10%/5% outcomes.
- E8: `INFERENCE_ONLY`; finite storage supplies a falsifier, but its SUMO
  instrumentation is not yet defined.

This note does not prove that capacity-aware MP meets the frozen claim. It shows
why substituting it after seeing a failure would be decision drift.

## Minimal quotation ledger

No verbatim quotation is needed; all source statements above are paraphrased.
