# Theory First landscape — smart traffic management

> - Status: **ORIENTATION_ONLY / LITERATURE_NOT_CLOSED**
> - Workflow stage: released `map-research-landscape` skill only
> - Snapshot: 2026-07-15
> - Frozen prompt: [`STM-COMPARE-001-v1`](PROMPT.md)
>
> This document is a discovery map, not a study protocol, preregistration,
> simulation result, or pilot go/no-go decision. Every cited paper is still a
> candidate lead until its load-bearing equations, definitions, and regimes are
> checked by close reading.

## 1. Decision and scope

```text
decision_supported: whether a city lab should advance a queue-based
  max-pressure (MP) signal controller to a calibrated four-intersection SUMO
  comparison against a recalibrated fixed-time controller, and eventually to a
  pilot decision
draft_claim_or_topic: >=10% reduction in network-wide mean person delay, with
  <=5% increases in P95 pedestrian waiting time and P95 side-street queue length,
  under one recurrent peak profile and one predeclared incident perturbation
scope_and_non_goals: orient terminology, formulations, observables, baselines,
  implementation surfaces, and failure regimes; do not choose controller
  equations, define local numerical inputs, run SUMO, close evidence, or decide
  pilot readiness
project_profile_version: none; the frozen prompt is the sole authority and the
  repository contains only an example project-profile template
snapshot_date: 2026-07-15
languages_and_access_limits: English-language public metadata, abstracts,
  open manuscripts, and official documentation; no authenticated databases;
  no redistribution of papers; no local calibration or confidential city data
orientation_stop_reason: targeted searches now recur in six stable clusters;
  the remaining uncertainty is expressible as specific evidence rows
```

The immediate decision is therefore **which exact claims and definitions must
be closed before a defensible experiment can be specified**. It is not yet
whether MP wins or whether the city should pilot it.

## 2. Terminology lattice

| Term | Meaning in this map | Synonyms or neighboring terms | Often-confused term | Equivalence status | Search role |
|---|---|---|---|---|---|
| max-pressure (MP) control | Feedback signal control selecting phases or green allocations from local upstream/downstream pressure | back-pressure, max-weight; queue-based MP (Q-MP) | every controller with a “pressure” reward | suspected family relation; formulas and guarantees vary | central mechanism |
| queue-based MP | Pressure computed primarily from vehicle queue counts and movement service rates | classical MP, Q-MP | capacity-aware, delay-based, position-weighted, cyclic, pedestrian-aware MP | not equivalent | candidate intervention requiring a frozen variant |
| throughput / maximum stability | Bounded queues for feasible long-run demand under a stated queueing model | stability region, capacity region | lower finite-horizon mean delay | not equivalent | theorem-to-claim boundary |
| fixed-time control | Preset cycle, phase sequence, splits, and offsets | pre-timed, static TLS, time-of-day plan | SUMO's auto-generated 90 s equal-split plan; an optimized corridor plan | not equivalent | comparator definition |
| recalibrated fixed-time | Fixed plan retimed for a declared calibration demand and objective, then frozen before evaluation | optimized pre-timed plan | retuning on the evaluation seed or incident result | unresolved | baseline fairness |
| person delay | Delay accumulated by individual travelers, potentially including vehicle occupancies and pedestrians | passenger-weighted delay, person time loss | vehicle mean `timeLoss`, vehicle waiting time, door-to-door travel time | disputed until the estimator and denominator are fixed | primary observable |
| pedestrian waiting time | Time from arrival at a controlled crossing queue to permitted/actual crossing start | curb wait, crossing delay | SUMO walk-stage `timeLoss`; `waitingTime` for a ride | not equivalent | safety/equity observable |
| side-street queue length | Physical or count queue on predeclared minor approaches | jam length, halting count | link occupancy, total link vehicles, network queue sum | not equivalent | spillback guardrail |
| P95 queue / wait | 95th percentile over a predeclared sampling unit | near-worst-case tail | the 95th percentile of per-cycle maxima, pooled time steps, or seed summaries | not equivalent | aggregation ambiguity |
| recurrent peak profile | Repeated time-varying arrival pattern over the analysis horizon | time-of-day demand | iid stationary arrivals used by some theory | not equivalent | regime bridge |
| incident perturbation | One frozen non-recurring change such as lane blockage or saturation-flow reduction | capacity loss, link blockage, event scenario | a demand surge or routing intervention | not equivalent | disconfirmation regime |
| finite storage / spillback | Downstream link capacity can block upstream discharge | blocking, queue propagation | infinite point queues | not equivalent | no-go boundary |

Hypotheses needing source verification: traffic MP is historically derived from
network back-pressure/max-weight control; Q-MP is the frozen prompt's intended
variant; and SUMO queue observations can faithfully instantiate the queue state
used in the selected theorem. None is treated as established for this project
yet.

## 3. Cluster map

All sources below are **discovery leads**, not closed evidence.

| Cluster | Defining question | Mechanism | Observable | Regime | Standard methods / metrics | Rival or boundary | Primary-source leads | Relevance |
|---|---|---|---|---|---|---|---|---|
| A. Store-and-forward MP foundations | Under what assumptions does local pressure control stabilize a signalized network? | Phase selection from movement queue differentials, turn ratios, and saturation flows | Long-run bounded mean queue / feasible-demand throughput | Point queues; classical formulation uses unlimited storage and stated arrival/routing assumptions | Lyapunov stability and capacity region | A stability theorem does not yield a 10% finite-run delay effect | [Varaiya 2013](https://doi.org/10.1016/j.trc.2013.08.014); [Kouvelas et al. 2014](https://doi.org/10.3141/2421-15) | Defines the anchor mechanism and its theorem boundary |
| B. Corridor timing and coordination | Does local adaptive control retain corridor progression and legal cyclic operation? | Cycle, phase sequence, split, offset, update period, yellow/all-red and lost time | Queue, travel time, delay, progression quality | Closely spaced arterial intersections, recurrent peaks | Existing and retimed fixed-time plans; cyclic/acyclic MP | A poorly optimized or uncoordinated fixed-time arm is a strawman | [Tascikaraoglu et al. 2015, PointQ](https://arxiv.org/abs/1507.08082); [Barman & Levin 2022](https://doi.org/10.1177/03611981211072807) | The proposed four-intersection object is a corridor, not four isolated junctions |
| C. Finite capacity, spillback, and incidents | What happens when a blocked or short downstream link fills? | Capacity-normalized pressure, occupancy, work conservation | Physical queue, blocked discharge, spillback, completed trips | Finite links and capacity-reducing incidents | Capacity-aware pressure; lane/blockage stress tests | Classical back-pressure can become non-work-conserving and propagate congestion in finite-capacity models | [Grégoire et al. 2015](https://doi.org/10.1109/TCNS.2014.2378871) ([open manuscript](https://arxiv.org/abs/1309.6484)) | Directly threatens the side-street P95 guardrail and incident claim |
| D. Pedestrians and person objectives | Can a vehicle-queue policy protect pedestrian service and optimize people rather than vehicles? | Joint vehicle/pedestrian queues, protected/permissive movements, possible occupancy weights | Person delay and pedestrian queue/wait | Mixed vehicle–pedestrian networks | Person-weighted delay; pedestrian delay tails; mode-stratified reporting | Vehicle-only Q-MP need not control pedestrian waiting; right-turn yielding matters | [Liu, Gayah & Levin 2024](https://doi.org/10.1016/j.trc.2024.104865) ([open manuscript](https://arxiv.org/abs/2406.19305)) | The proposed primary metric and first guardrail are multimodal |
| E. Baseline, metrics, and statistical evaluation | What makes the two-arm comparison fair and decision-grade? | Calibration/validation split, frozen alternatives, repeated stochastic runs | Person/vehicle delay, P95 queues, confidence intervals | Calibrated traffic microsimulation | Paired seeds, initialization handling, multiple runs, CI and sensitivity analysis | No local calibration data means simulation output cannot yet support a city-pilot claim | [FHWA Traffic Signal Timing Manual](https://ops.fhwa.dot.gov/publications/fhwahop08024/fhwa_hop_08_024.pdf); [FHWA Traffic Analysis Toolbox Vol. III](https://ops.fhwa.dot.gov/publications/fhwahop18036/fhwahop18036.pdf) | Supplies standard signal metrics, fixed-time practice, calibration, and alternatives-analysis conventions |
| F. SUMO implementation and observability | Which simulator state and output implements each theoretical object? | Static TLS or TraCI-controlled phases; E2 detectors; trip/person/TLS output | `timeLoss`, `waitingTime`, person stages, jam length, TLS state | Version-pinned microscopic simulation | Official output schemas, saved TLS transitions, unfinished-trip policy | Development docs drift; default fixed timing, teleports, censored trips, and metric aliases can bias comparison | [SUMO traffic-light docs](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html); [TripInfo/person output](https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html); [TLS output](https://sumo.dlr.de/docs/Simulation/Output/Traffic_Lights.html); [official source](https://github.com/eclipse-sumo/sumo) | Defines the operational bridge and audit trail |

## 4. Formulation and observable crosswalk

| Formulation | Object transformed | Quantity expected invariant across arms | Observable actually reported | Required bridge | Known mismatch |
|---|---|---|---|---|---|
| Classical point-queue MP | Movement queue vector and admissible signal stage | Demand, routing/turn ratios, saturation rates, legal stage set | Queue stability or aggregate queue in its source model | Show that chosen SUMO queue estimator and phase service reproduce the source equation | Infinite point queues omit finite storage, vehicle positions, and spillback |
| Capacity-aware MP | Queue/occupancy normalized by downstream storage | Geometry and storage capacities | Queue, work conservation, congestion propagation | Map SUMO lane capacity and jam state to the normalized pressure term | It is a different intervention from unqualified Q-MP |
| Recalibrated fixed-time corridor | Cycle, splits, offsets, phase order | Same demand, routes, safety clearances, horizon, and incident | Delay, queue, progression | Freeze the calibration data, objective, optimizer, and final plan before evaluation | SUMO defaults are not a recalibrated corridor baseline |
| Pedestrian-aware MP | Vehicle and pedestrian queues and conflicts | Same pedestrian arrivals, crossing geometry, walk/clearance timing, and yielding model | Person delay and pedestrian delay/queue | Define traveler weights and derive crossing wait from auditable events | Vehicle Q-MP, pedestrian-aware MP, and occupancy-weighted MP are distinct policies |
| SUMO microscopic experiment | Individual vehicles/persons, lanes, routes, and TLS states | Exact scenario files and paired stochastic inputs, differing only in controller arm | Vehicle `timeLoss`/`waitingTime`; walk/ride stages; E2 jam measures | Predeclare estimands, censored-trip handling, aggregation units, and controller-state logs | SUMO's similarly named fields are not the prompt's estimands by default |

The most important invariant is the **scenario surface**: geometry, demand and
route realizations, vehicle/person attributes, safety phases, simulation horizon,
warm-up, incident, and random seeds must be identical between arms. Only the
frozen controller may differ. That invariance is a proposed evaluation contract,
not something established by this map.

## 5. Discovery-lead shortlist

| Lead | Candidate role | What the scan indicates | Why it is not yet evidence |
|---|---|---|---|
| [Varaiya 2013](https://doi.org/10.1016/j.trc.2013.08.014) | foundation anchor | Introduces traffic MP and a maximum-throughput/stability result in a store-and-forward point-queue model | Exact pressure equation, theorem quantifiers, admissible controls, and finite-storage remarks have not been reconstructed |
| [Kouvelas et al. 2014](https://doi.org/10.3141/2421-15) | arterial application | Tests MP on a signalized arterial queue model | Transfer to a four-intersection SUMO corridor, person metrics, and incident regime is unverified |
| [Tascikaraoglu et al. 2015](https://arxiv.org/abs/1507.08082) | calibration/incident bridge | Uses a calibrated arterial queue model and compares existing/retimed fixed-time with MP, including diversion around a capacity-reducing incident | It is an open preprint/working-paper surface using PointQ rather than SUMO; exact comparison and calibration limitations require close reading |
| [Grégoire et al. 2015](https://doi.org/10.1109/TCNS.2014.2378871) | limitation / alternative | Identifies finite-capacity failure modes and proposes capacity-aware pressure | Need exact counterexample regime and whether its remedy preserves the intended Q-MP identity |
| [Liu, Gayah & Levin 2024](https://doi.org/10.1016/j.trc.2024.104865) | multimodal bridge | Extends MP to pedestrian queues and reports person-delay simulations | Need the exact person-delay estimator, pedestrian service constraints, comparison arms, and tail behavior |
| [FHWA Traffic Signal Timing Manual](https://ops.fhwa.dot.gov/publications/fhwahop08024/fhwa_hop_08_024.pdf) | metric/baseline authority | Names person/vehicle delay and 50th/95th-percentile queues; discusses fixed-time, Webster/HCM timing, coordination, and pedestrian trade-offs | It is guidance, not evidence for the proposed 10%/5% numerical thresholds |
| [FHWA Traffic Analysis Toolbox Vol. III (2019)](https://ops.fhwa.dot.gov/publications/fhwahop18036/fhwahop18036.pdf) | microsimulation evaluation authority | Covers calibration, validation, multiple runs, initialization, bias, confidence intervals, hypothesis tests, and sensitivity analysis | Exact applicable procedures and required local inputs have not been extracted |
| [SUMO official documentation](https://sumo.dlr.de/docs/) | implementation/observable authority | Defines static/TraCI TLS control and vehicle/person/TLS outputs | Online docs track the development version; a release and source commit must be pinned before implementation |

## 6. No-go and artifact boundaries visible from the map

1. **Theorem–outcome mismatch.** Maximum stability or throughput optimality is
   not a theorem that MP reduces finite-horizon mean person delay by 10%, nor
   that either P95 guardrail is non-inferior.
2. **Finite-storage mismatch.** Classical point queues and physical SUMO lanes
   are different objects. A capacity-reducing incident can produce spillback,
   blocking, and non-work-conserving behavior precisely where the original
   guarantee is least transferable.
3. **Controller identity ambiguity.** Classical Q-MP, capacity-aware MP,
   cyclic MP, phase-switch-loss MP, pedestrian-aware MP, and occupancy-weighted
   MP cannot be mixed after results are seen. One intervention must be frozen.
4. **Vehicle–person mismatch.** Averaging vehicle `timeLoss` is not automatically
   network-wide mean person delay. Vehicle occupancies, pedestrians, unfinished
   travelers, and the denominator must be declared.
5. **Pedestrian metric aliasing.** SUMO's walk-stage `timeLoss`, ride
   `waitingTime`, stationary time, curb arrival, signal permission, and actual
   crossing start describe different events. P95 crossing wait likely needs a
   derived, validated event estimator.
6. **Queue metric aliasing.** Halting number, jam length in vehicles, jam length
   in metres, link occupancy, and all vehicles on a lane are not interchangeable.
   P95 over time steps is not P95 over cycle maxima or run summaries.
7. **Censoring and gridlock artifacts.** SUMO writes vehicle trip information on
   arrival by default. Excluding unfinished or never-inserted travelers can make
   the more congested arm look better. Teleport and collision policies can erase
   the very queues being compared.
8. **Strawman baseline risk.** An auto-generated static plan with a default
   cycle/equal split is not “recalibrated fixed-time.” Conversely, optimizing
   fixed timing on evaluation realizations leaks test information.
9. **Signal-safety and switching-loss risk.** Yellow/all-red, minimum green,
   pedestrian WALK/clearance, permitted turns, and cyclic expectations must be
   held legal in both arms. Directly setting signal states can silently move
   these obligations into custom code.
10. **Pilot external-validity boundary.** With the prompt's explicit absence of
    local calibration data, a simulated effect cannot by itself establish city
    pilot readiness. Geometry, saturation flow, turning movements, demand,
    routing, pedestrian arrivals, occupancies, and incident capacity loss remain
    unset local inputs.
11. **Numerical-threshold provenance.** The scan found no source establishing
    the prompt's 10% benefit or 5% harm margins as universal standards. They are
    currently decision thresholds supplied by the prompt, not literature facts.

## 7. Minimal six-source close-reading set

This set is chosen for coverage and contrast, not citation count. A later
`close-literature` stage may replace or add sources when an assigned question
cannot be answered.

| Priority | Source identity | Role | Assigned close-reading question | Expected evidence rows | Access status |
|---:|---|---|---|---|---|
| 1 | [Varaiya, “Max pressure control of a network of signalized intersections” (2013)](https://doi.org/10.1016/j.trc.2013.08.014) | anchor | What exact pressure, queue dynamics, controller timing, information, feasibility set, and assumptions support the stability theorem, and what does it *not* say about delay? | E1, E4, E5 | DOI/abstract accessible; publisher full text not verified in this scan |
| 2 | [Grégoire et al., “Capacity-Aware Backpressure Traffic Signal Control” (2015)](https://doi.org/10.1109/TCNS.2014.2378871) | disconfirmation | Construct the exact finite-capacity failure mechanism for classical MP; identify when normalized pressure is required and which guarantees survive. | E4, E5, E8 | DOI metadata plus [open manuscript](https://arxiv.org/abs/1309.6484) accessible |
| 3 | [Liu, Gayah & Levin, “A Max Pressure Algorithm for Traffic Signals Considering Pedestrian Queues” (2024)](https://doi.org/10.1016/j.trc.2024.104865) | mechanism-to-observable bridge | How are pedestrian queues, vehicle–pedestrian conflicts, person delay, and comparison policies defined; are pedestrian tail waits constrained or only averages reported? | E2, E3, E8 | DOI plus [open manuscript](https://arxiv.org/abs/2406.19305) accessible |
| 4 | [FHWA Traffic Signal Timing Manual, FHWA-HOP-08-024](https://ops.fhwa.dot.gov/publications/fhwahop08024/fhwa_hop_08_024.pdf) | metric/baseline | Which definitions and aggregation units apply to person delay and P95 queue; what inputs and coordination choices make a fixed-time corridor plan a fair baseline? | E2, E3 | Official 274-page PDF accessible; relevant routing locators include pp. 40, 48, 72–75, 189–192 |
| 5 | [FHWA Traffic Analysis Toolbox Vol. III, FHWA-HOP-18-036 (2019)](https://ops.fhwa.dot.gov/publications/fhwahop18036/fhwahop18036.pdf) | evaluation / calibration | What calibration/validation, warm-up, replication, confidence-interval, alternatives-analysis, and bias controls are required for this decision class? | E6, E7, E9 | Official PDF and [HTML contents](https://ops.fhwa.dot.gov/trafficanalysistools/tat_vol3/list_contents.htm) accessible |
| 6 | [SUMO official traffic-light and output documentation](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html) | implementation / observable | For a pinned SUMO release, which state variables and event logs implement each pressure term and estimand; how are unfinished trips, teleports, pedestrian waits, queues, and legal phase transitions audited? | E2, E6, E7 | Official [TripInfo/person](https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html), [TLS output](https://sumo.dlr.de/docs/Simulation/Output/Traffic_Lights.html), and source available; online docs are not release-pinned |

The PointQ corridor paper and Kouvelas/Barman corridor studies remain reserve
leads. They should enter the reading set if the six sources above do not close
the calibrated-corridor and incident-transfer rows.

## 8. Evidence rows to hand to `close-literature`

| ID | Load-bearing question | Needed evidence | Current status |
|---|---|---|---|
| E1 | What exact controller does “queue-based MP” denote? | Equation-level policy, queue state, turn-ratio/service inputs, update interval, phase order, minimum/maximum green, switching clearances | `OPEN` |
| E2 | What are the three estimands? | Equations for mean person delay, P95 pedestrian crossing wait, and P95 side-street queue; population, units, spatial and temporal aggregation, censoring | `OPEN` |
| E3 | What is a fair recalibrated fixed-time arm? | Calibration-only data, objective, cycle/split/offset/sequence method, corridor coordination, pedestrian timing, frozen-plan record | `OPEN` |
| E4 | Does the source regime cover this corridor and incident? | Storage capacities, spillback, nonstationary peak, fixed or changing turn ratios, incident type/duration/location, demand feasibility | `OPEN` |
| E5 | Which source claim bridges to the proposed numerical prediction? | Explicit separation of stability/throughput, average delay, person delay, and tail non-inferiority; no unsupported theorem leap | `OPEN` |
| E6 | How will SUMO artifacts be controlled? | Pinned release/commit; warm-up/end; unfinished and uninserted travelers; teleports/collisions; paired seeds; deterministic scenario manifest | `OPEN` |
| E7 | What statistical comparison supports 10%/5% decisions? | Unit of replication, paired design, run-count rule, uncertainty interval, multiplicity, simultaneous benefit and non-inferiority decision rule | `OPEN` |
| E8 | Are physical queues and pedestrian service observable and controlled? | Validated queue detector against ground truth; curb-arrival/crossing-start events; queue-measurement noise; capacity normalization | `OPEN` |
| E9 | What can support a city pilot decision without local data? | Minimum local calibration/validation packet and a scoped rule distinguishing method feasibility from local effect/pilot readiness | `OPEN`; likely prerequisite gate |

No row is marked confirmed by this map.

## 9. Exact search ledger and access limits

Local discovery first: no domain literature corpus, RAG index, or filled project
profile was present in this standalone release repository; only the frozen prompt
and an example profile template were available. External search was authorized
by the worked-example request. Queries contained only public, generic topic
terms.

| ID | Lane | Service / filter | Exact query | Result used for routing |
|---|---|---|---|---|
| S00 | capability discovery | AnySearch `get_sub_domains`, `academic` | `academic` | Selected `academic.search` and `academic.preprint`; no required query parameters |
| S01 | foundations | AnySearch academic / Engineering / relevance | `max pressure traffic signal control urban networks queue stability Varaiya` | MP/back-pressure family, arterial applications, phase variants |
| S02 | foundation identity | AnySearch academic / Engineering / relevance | `Max pressure control of a network of signalized intersections Pravin Varaiya 2013` | Routed to Varaiya and neighboring MP papers; exact DOI verified on publisher metadata |
| S03 | foundations + official evaluation + implementation | Web search | `site:sciencedirect.com "Max pressure control of a network of signalized intersections"` | Varaiya publisher record and DOI |
| S04 | multimodal observable | Web search | `max pressure traffic signals pedestrian waiting queue paper` | Liu–Gayah–Levin pedestrian-aware MP lead |
| S05 | calibration / statistics | Web search | `FHWA Traffic Analysis Toolbox Volume III microsimulation calibration validation multiple runs official PDF` | FHWA official 2019 guide and contents |
| S06 | implementation / observable | Web search | `SUMO official documentation person delay waiting time queue traffic light TraCI` | SUMO output, TripInfo/person, TLS, teleport surfaces |
| S07 | finite-capacity boundary | AnySearch academic / Engineering / relevance | `capacity aware backpressure traffic signal control finite queue spillback` | Capacity-aware and position-weighted variants |
| S08 | exact limitation identity | AnySearch academic / Engineering / relevance | `Capacity-aware backpressure traffic signal control Grégoire Frazzoli de La Fortelle 2014` | DOI `10.1109/TCNS.2014.2378871` and OA manuscript |
| S09 | multimodal bridge | AnySearch academic / Engineering / date | `A Max Pressure Algorithm for Traffic Signals Considering Pedestrian Queues Liu Gayah Levin` | Current journal DOI found through arXiv metadata |
| S10 | exact multimodal identity | AnySearch academic preprint / title / English / OA | `A Max Pressure Algorithm for Traffic Signals Considering Pedestrian Queues` | arXiv record and journal link |
| S11 | metrics/baselines | AnySearch academic / Engineering / relevance | `traffic signal performance measures person delay pedestrian waiting time 95th percentile queue length fixed time baseline` | Low precision; retained no load-bearing result |
| S12 | official baseline | Web search | `site:ops.fhwa.dot.gov traffic signal timing manual fixed-time Webster delay queue pedestrian performance measures PDF` | FHWA timing manual |
| S13 | official metrics | Web search | `site:ops.fhwa.dot.gov traffic signal performance measures pedestrian delay queue length official` | FHWA signal-performance sources |
| S14 | SUMO metric semantics | Web search | `site:sumo.dlr.de/docs TripInfo personInfo waitingTime timeLoss lanearea jam length official` | Official field definitions and censoring behavior |
| S15 | SUMO controller surface | Web search | `site:sumo.dlr.de/docs traffic light TraCI max pressure fixed time official` | Static TLS, adaptation tools, TraCI phase control |
| S16 | incident boundary | AnySearch academic / Engineering / relevance | `max pressure traffic signal control incident lane blockage robustness recurrent demand corridor` | Sparse direct MP results; reinforced incident-transfer gap |
| S17 | corridor evidence | AnySearch academic / Engineering / relevance | `Maximum pressure controller for stabilizing queues in signalized arterial networks Kouvelas 2014` | PointQ and arterial/corridor leads |
| S18 | exact corridor identity | Web search | `"Maximum pressure controller for stabilizing queues in signalized arterial networks" DOI` | DOI `10.3141/2421-15` |
| S19 | cyclic implementation | Web search | `"Max-pressure signal control with cyclical phase structure" DOI` | Cyclic-phase lead; exact journal identity not closed |
| S20 | calibrated comparator | Web search | `"PointQ model of an arterial network: calibration and experiments" DOI journal` | Confirmed stable arXiv identity; no journal DOI found |
| S21 | implementation repositories | Web search | `site:github.com max pressure traffic signal SUMO implementation` | Official SUMO tutorial/source and third-party libraries; third-party code not promoted to evidence |

Access and quality limits:

- AnySearch queries were sent to `https://api.anysearch.com`; web queries used
  public search and source hosts. No confidential terms or local paths were sent.
- The Varaiya publisher abstract was accessible, but full-text access was not
  established. Open versions were available for Grégoire and Liu et al.
- FHWA documents and SUMO pages were accessible. The live SUMO documentation
  explicitly tracks the latest development version, so exact implementation
  claims require a pinned release/commit.
- Search results also returned reviews, generated summaries, unrelated papers,
  Wikipedia, Reddit, vendor pages, and recent unreplicated implementations.
  They were used only, if at all, as routing hints and are not cited as evidence.
- No citation-graph exhaustiveness claim was attempted. “No source found” in
  this scan means only “not found by the bounded queries above,” never field-wide
  absence.

## Handoff

Orientation is saturated enough to narrow: the central choices are classical
versus capacity-/pedestrian-aware MP, point-queue versus finite-link dynamics,
vehicle versus person observables, and genuinely recalibrated fixed-time versus
SUMO defaults. The next authorized stage should assign E1–E9 to
`close-literature`/`deep-read-paper`. Until those rows close, there is no
literature-closed claim, preregistered protocol, simulation authorization, or
pilot decision.
