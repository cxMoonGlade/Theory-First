# Should the city pilot max-pressure control on the four-intersection corridor?

## Bottom line

**Recommendation now: no-go for a live traffic-signal pilot, but go for a locked, confirmatory SUMO comparison.** The literature makes max-pressure a credible candidate, particularly when demand is variable or disrupted, but it does not establish this corridor-specific numerical claim. The foundational result is a queue-stability/throughput result under a stylized store-and-forward model; it is not a guarantee of a 10% reduction in mean person delay, and it says still less about pedestrian or minor-street tail outcomes. Those three quantities must be estimated on a locally calibrated model.

The field-pilot decision should be conditional. Advance only if a held-out simulation experiment shows, with one-sided 95% uncertainty bounds, that max-pressure:

1. reduces network-wide mean person delay by **at least 10%**;
2. increases the 95th-percentile pedestrian crossing wait by **no more than 5%**; and
3. increases the 95th-percentile side-street queue by **no more than 5%**;

and if the model, controller, and hardware-readiness checks described below all pass. A favorable point estimate alone is insufficient. Until those data exist, the proposed effect is a hypothesis, not a result.

My recommended candidate is a **cyclic, pedestrian-queue-aware max-pressure controller with finite-storage safeguards**, compared against a genuinely reoptimized and coordinated fixed-time plan. That is more pilot-relevant than unconstrained textbook max-pressure. The exact controller version must be named and frozen before evaluation; original vehicle-only queue max-pressure, pedestrian-queue max-pressure, occupancy-weighted max-pressure, and coordinated max-pressure are different treatments and must not be interchanged after results are seen.

## What the literature supports—and what it does not

Pravin Varaiya's foundational max-pressure paper proves maximum stability for a signalized queueing network: informally, if an admissible signal policy can stabilize feasible demand, the max-pressure policy can do so as well. The model assumes movement-specific point queues, fixed mean turning probabilities, stochastic arrivals and service, and effectively unlimited queue storage. The result supports the controller's mechanism—serve movements with high upstream pressure toward less-congested downstream links—but does not imply a particular reduction in delay on a finite four-signal corridor ([Varaiya, 2013](https://doi.org/10.1016/j.trc.2013.08.014)). A later review finds that calibrated microsimulation studies have mostly reported favorable results while emphasizing the many practical variants developed for cycles, measurement error, realistic flows, and alternative modes ([Levin, 2023](https://doi.org/10.1061/JTEPBS.TEENG-7578)).

That distinction matters here:

- **Finite links and spillback.** Classical back-pressure can behave poorly when physical links fill because the point-queue theorem omits storage. Capacity-aware pressure was proposed specifically to address non-work-conserving behavior and congestion propagation under finite capacities ([Grégoire et al., 2015](https://doi.org/10.1109/TCNS.2014.2378871)). Position-weighted back-pressure explicitly represents where vehicles are on a link and reported better recovery and incident response than standard back-pressure and optimized fixed timing in its tested simulations, but that evidence remains model- and network-specific ([Li and Jabari, 2019](https://doi.org/10.1016/j.trb.2019.08.005)). An incident on a short corridor makes this caveat central rather than peripheral.

- **Practical phase operation.** Original max-pressure may select phases in an arbitrary order, creating phase skipping and potentially long waits. A cyclic version was developed because practitioners considered arbitrary phase order unacceptable; it requires an approved phase order and bounded cycle while retaining a stability result within the constrained policy class, at some cost in performance ([Levin, Hu, and Odell, 2020](https://doi.org/10.1016/j.trc.2020.102828)).

- **Pedestrians.** A 2024 pedestrian-queue max-pressure algorithm includes both vehicle and pedestrian queues in phase pressure and models conflicts such as right-turn yielding. Its microsimulation experiments found lower person delay than original vehicle-queue max-pressure and a rule-based pedestrian variant under the conditions tested; the paper also proves a stability property in its model ([Liu, Gayah, and Levin, 2024](https://doi.org/10.1016/j.trc.2024.104865); [open author manuscript](https://arxiv.org/abs/2406.19305)). This supports testing a pedestrian-aware version; it does not prove this corridor's 5% tail-wait guardrail.

- **Person versus vehicle objectives.** Standard queue max-pressure treats a car and a crowded bus as vehicles. Occupancy-weighted max-pressure was developed because vehicle throughput is not the same objective as passenger performance; its simulations found benefits for high-occupancy movement under tested conditions ([Ahmed, Liu, and Gayah, 2024](https://doi.org/10.1016/j.trc.2024.104795)). Consequently, a claim about *person* delay requires explicit occupancies and pedestrian trips. Vehicle time loss mislabeled as person delay would not answer the question.

- **Corridor coordination.** A well-timed fixed plan can create progression through closely spaced intersections, while independent phase decisions can break a green wave. A recent coordinated max-pressure variant uses queue and platoon-speed information and performed well in arterial microsimulation ([Ahmed, Liu, and Gayah, 2025](https://doi.org/10.1016/j.trb.2025.103308)). It is relevant context, but it is a different controller from plain queue max-pressure. Use it only as a separately declared secondary treatment unless it is chosen as the candidate before the study.

- **Deployment evidence is encouraging but still thin.** A Minnesota project demonstrated queue-based max-pressure on North American controller hardware in a hardware-in-the-loop SUMO testbed. The report identified queue sensing, pedestrian calls, flashing operation, emergency preemption, and a staged single-intersection-then-corridor rollout as remaining deployment work ([Hao and Stern, 2024](https://rosap.ntl.bts.gov/view/dot/79015)). A 2025 study reports an on-road experiment at an isolated T-intersection for a *travel-time-based* cyclic max-pressure variant, not the queue-based four-intersection treatment proposed here ([Zoabi and Haddad, 2025](https://doi.org/10.1016/j.trc.2025.105070)). Neither establishes the present claim.

The appropriate reading of this evidence is therefore: **strong enough to justify a careful simulation study, not strong enough to skip it or to assert the target effect.**

## Freeze the treatment and comparator

### Recommended max-pressure treatment

At each intersection, define movement queue $q_{ij}(t)$, estimated turning proportions $r_{jk}$, and saturation flow $s_{ij}$. The transparent queue-pressure core is

\[
w_{ij}(t)=q_{ij}(t)-\sum_k r_{jk}q_{jk}(t),
\qquad
P_\phi(t)=\sum_{(i,j)\in\phi}s_{ij}w_{ij}(t),
\]

with the highest-pressure currently admissible phase receiving service. The study specification must also freeze all details that can materially change behavior:

- movement-level versus lane-level queue aggregation;
- detector coverage, update interval, smoothing, missing-data behavior, and queue-estimation error;
- turning proportions and how often, if ever, they update;
- saturation flows;
- tie-breaking;
- phase order, minimum and maximum greens, yellow and all-red clearances, pedestrian WALK and clearance intervals, and phase-call logic;
- handling of a full or blocked receiving link;
- communication latency, missed updates, and fail-safe fallback.

For the pilot candidate, use an approved cyclic/ring-barrier phase sequence, legal clearances, mandatory service of called phases, and an agency-approved maximum time to pedestrian service. Vehicle pressure should never be allowed to create an unsafe transition or defeat pedestrian clearance. The current federal MUTCD is the 11th Edition with Revision 1; among other requirements, priority operation may not shorten yellow/red clearances or pedestrian intervals below the applicable requirements ([FHWA MUTCD current edition](https://mutcd.fhwa.dot.gov/)). The same locally approved safety timings must apply to both controllers.

Because pedestrian tail waiting is a named decision endpoint, I would choose the published pedestrian-queue max-pressure concept for the primary candidate rather than add a post hoc starvation override to vehicle-only max-pressure. Couple that pedestrian pressure with the cyclic and finite-storage operational constraints above, then document that the resulting engineering implementation is a specific composite controller whose performance must be established empirically. If the lab's proposal specifically means original vehicle-only Q-MP, test that exact algorithm instead and label it honestly; do not substitute the pedestrian-aware version after the original fails a guardrail.

Do **not** add bus occupancy weights, platoon coordination weights, or delay-based pressure during confirmatory evaluation unless they were part of the frozen candidate. Those are defensible future variants, but changing the objective changes the treatment.

The pressure calculation used in the confirmatory model must consume only signals obtainable in a field installation. Perfect SUMO ground-truth queues extending beyond the planned camera or loop coverage would give the adaptive controller an unrealizable advantage. Run a secondary ideal-sensor analysis to measure the information penalty, but use realistic sensing for the primary comparison.

### Strong recalibrated fixed-time comparator

The comparator should not be the legacy plan or SUMO's generated default. Recalibrate it using only training-period recurring-peak data:

- optimize feasible cycle length, splits, phase sequence if agency rules permit, and offsets across all four intersections;
- use the same phase library, yellow/all-red times, pedestrian call/recall rules, and legal minimums as the candidate;
- optimize the registered person-delay objective subject to the same pedestrian and side-street operational constraints, rather than optimizing arterial vehicle throughput alone;
- choose timings across a set of training demand realizations, not the one realization later used for testing;
- freeze the plan before applying the held-out incident and final random seeds.

SUMO's `tlsCycleAdaptation.py` can provide a Webster-based split/cycle starting point and `tlsCoordinator.py` can optimize offsets, but the documentation warns that the former uses static hourly flows and does not itself coordinate intersections. Use those tools as initializers, followed by a documented constrained search on the training set ([SUMO traffic-light tools](https://sumo.dlr.de/docs/Tools/tls.html)). Give both alternatives a documented and reasonable tuning budget. Report the current field plan as an additional descriptive comparator, not as the primary baseline.

An incident-specific fixed plan may be useful as a secondary “best prepared fixed-time” benchmark. It should not replace the primary recurring-peak fixed plan unless the agency actually has a rule that would detect this incident and invoke that plan in practice.

## Make the claim mathematically unambiguous

The phrase “under a recurrent peak-demand profile and one predeclared incident perturbation” can mean either one incident-inclusive scenario or success in both normal and disrupted peaks. Do not pool the two: pooling can hide a failure in one condition. The conservative and operationally useful interpretation is two locked scenario strata:

1. **Peak:** the recurrent peak profile with no incident.
2. **Peak + incident:** the same profile and stochastic realization with the one frozen incident added.

Require the claim to pass in each stratum. If the intended claim concerns only the incident-inclusive run, say so before calibration and make the no-incident case secondary.

For controller $c\in\{MP,FT\}$ and scenario $s$, define:

- $D_{c,s}$: network-wide mean person delay;
- $W_{c,s}$: network-wide 95th-percentile pedestrian crossing wait;
- $Q_{c,s,a}$: 95th-percentile queue length for predeclared side-street approach $a$.

The effects are ratios:

\[
R_D(s)=\frac{D_{MP,s}}{D_{FT,s}},\qquad
R_W(s)=\frac{W_{MP,s}}{W_{FT,s}},\qquad
R_Q(s)=\max_a\frac{Q_{MP,s,a}}{Q_{FT,s,a}}.
\]

The last definition is intentionally approach-protective: pooling every side-street sample can let a severe deterioration at one short approach disappear among many benign observations. Also report the pooled network side-street p95 if stakeholders want the literal aggregate, but do not let it override the worst predeclared approach. The success thresholds are

\[
R_D(s)\le 0.90,\qquad R_W(s)\le1.05,\qquad R_Q(s)\le1.05.
\]

If a fixed-time guardrail denominator is zero, a relative increase is not estimable; do not insert an arbitrary epsilon. Report the absolute difference and treat the relative claim as unsubstantiated unless the decision-maker replaces it, in advance, with a defensible absolute margin.

## Operational definitions and SUMO measurement

FHWA guidance treats delay as additional travel time experienced by a driver, passenger, or pedestrian and identifies delay and queues as core signal-performance measures. It also explicitly lists per-person delay and 95th-percentile queue length among common signal-timing measures ([FHWA Traffic Signal Timing Manual, Chapters 2–3](https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter2.htm)). The following definitions turn those concepts into reproducible simulation endpoints.

### 1. Network-wide mean person delay

The analysis population is every person whose *intended* departure falls inside the locked measurement window, regardless of whether that person departs or finishes before the nominal end. For person $p$, define

\[
d_p=(\text{actual arrival}-\text{intended departure})
      -(\text{frozen reference travel time on the same route and modes}).
\]

The reference contains ideal/free-flow movement and any scheduled activity or transit dwell that should not count as traffic delay. It is calculated once using the same route and traveler attributes, not reoptimized by controller. The network mean is $\sum_p d_p/N_p$.

Model occupancies explicitly. If travelers are represented as vehicles rather than SUMO persons, multiply each vehicle's delay by its frozen occupancy, include the driver, add pedestrian-person delays, and divide by the total represented persons. Do not count a transit vehicle once and call the result person delay. Avoid double-counting explicit passengers and their carrier vehicle.

SUMO's trip information distinguishes `departDelay`, `waitingTime`, and `timeLoss`; `timeLoss` is loss from traveling below ideal speed and does not replace insertion/departure delay. Person records also provide stage information, with ride-stage time loss inherited from the vehicle ([SUMO TripInfo documentation](https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html)). Use `departDelay + timeLoss` as an auditable cross-check against the traveler-level reference calculation, not as an unexplained metric substitution.

Run a common clearance tail after demand ends until the measurement cohort completes. Also enable unfinished and undeparted output. SUMO otherwise writes trip information only for arrivals, which can make a gridlocked controller look artificially good by excluding its missing trips; its documentation explicitly warns about fair comparisons with unfinished vehicles ([SUMO Statistic Output](https://sumo.dlr.de/docs/Simulation/Output/StatisticOutput.html)). If any cohort member remains unfinished at a predeclared hard clearance cap, report the available lower-bound delay and treat that controller/scenario as an automatic no-go rather than inventing a favorable completion time.

### 2. 95th-percentile pedestrian waiting time

Measure one observation per crossing episode, not total trip waiting and not a snapshot count. The wait starts when a pedestrian reaches the curb/walking area with the crossing as the next edge and is unable to enter; it ends when the pedestrian first enters that crossing. SUMO's pedestrian crossing tutorial shows how `edge.getLastStepPersonIDs`, `person.getNextEdge`, and `person.getWaitingTime` identify this state ([SUMO TraCI pedestrian crossing tutorial](https://sumo.dlr.de/docs/Tutorials/TraCIPedCrossing.html)). Log the event timestamps directly so a later reset of cumulative waiting cannot alter the endpoint.

Compute the p95 across all eligible crossing episodes in the scenario, while retaining crosswalk and intersection identifiers. Report the registered network value plus p95 by crosswalk, the maximum individual wait, unserved calls, and any pedestrian teleport/abort. If an episode remains unserved at the hard clearance cap, do not drop it; record its observed lower-bound wait and make the scenario an automatic no-go.

### 3. 95th-percentile side-street queue length

Before running, enumerate every side-street inbound approach and state whether the approach queue is the maximum lane queue or another fixed lane-group rule. Measure in metres, which maps to storage and spillback more meaningfully than a heterogeneous vehicle count. Sample at a fixed interval, preferably each simulated second after warm-up. For each approach and time, record the back-of-queue distance using a detector that covers the full physical storage area. SUMO E2 lane-area detectors are designed for standing/jammed queues and report jam length in vehicles and metres ([SUMO E2 documentation](https://sumo.dlr.de/docs/Simulation/Output/Lanearea_Detectors_%28E2%29.html)). A detector shorter than the possible queue right-censors the endpoint and invalidates the test.

Freeze the halting speed, minimum halt time, intra-vehicle gap, detector length, sampling interval, and multi-lane aggregation. Then compute each approach's p95 over its time samples within each replication. Also report the share of samples at physical storage, turn-bay overflow, downstream blocking, and maximum queue. Those diagnostics cannot rescue a failed p95 but can expose a misleading pass caused by detector saturation.

## Scenario construction and local data needed

No credible numerical result can be produced without local data. Build the model and demand generator from data that are temporally separated from the final evaluation.

### Network and boundaries

Code the four controlled intersections, actual lane/channelization geometry, grade and speed limits, stop lines, crosswalks, bus stops, legal turns, existing phase plans, detector locations, storage lengths, and saturation constraints. Include enough uncontrolled approach and downstream buffer outside the four-intersection evaluation area that queues are not clipped by artificial source/sink boundaries. The evaluation network remains the four intersections, but its simulation boundary must be wider.

Verify connection priorities, permissive turns, right-turn/pedestrian yielding, lane choice, car following, lane changing, discharge headways, pedestrian speeds, and crossing behavior by animation and targeted traces before calibration.

### Demand population

Use multiple observed recurring peak days. Preserve time-varying origin-destination or route demand, movement turn proportions, pedestrian crossing arrivals, vehicle classes, transit schedules, passenger occupancy distributions, and day-to-day variation. Divide whole days—not individual vehicles—into:

- model calibration/training days;
- independent validation days; and
- held-out confirmatory demand realizations or a demand generator fitted without those days.

The recurrent profile should be a distribution of plausible days, not one perfectly repeated flow file. Pre-generate every traveler, route, desired departure, behavior draw, and occupancy for a replication, and feed the identical file to both controllers. Dynamic rerouting can create a legitimate treatment response, but it also changes the estimand. For the primary signal-control comparison, freeze routes or freeze a common route-choice policy; study adaptive rerouting separately.

FHWA's 2019 microsimulation guidance emphasizes that an uncalibrated model has no assurance of predictive value, calls for representative-day variation envelopes, and calibrates capacity, route choice, then system performance such as travel time and queues ([FHWA Traffic Analysis Toolbox Volume III, Chapter 5](https://ops.fhwa.dot.gov/publications/fhwahop18036/chapter5.htm)). Set local acceptability criteria before fitting. Validate not only counts but also the outcomes most likely to decide this study: time-dependent travel times, discharge flow, queue profiles/spillback, pedestrian arrivals and waits, and side-street performance.

### The one incident

Select the perturbation from the city's incident logs or operational risk register, not because it makes max-pressure look good. A suitable rule is the most frequent consequential *lane-blocking* incident class on an internal corridor link. Before controller tuning, freeze:

- affected edge, direction, and lane(s);
- capacity/speed effect and whether the lane is completely closed;
- onset relative to the peak profile;
- duration and recovery rule;
- traveler information and rerouting availability;
- whether responders block any adjacent movement.

If no local incident distribution is available, the operations team should specify a credible drill scenario and explicitly label it as a designed stress test rather than “representative.” This answer does not invent a location, duration, or severity. Pair the exact same incident with both controllers. Do not search incident parameters for the case that maximizes the treatment effect.

## Experimental protocol

### Phase A: model acceptance, before alternatives

1. Create a versioned base network reproducing the observed fixed-time/current-control condition.
2. Verify conservation, routes, signal conflicts, clearances, pedestrian service, detector coverage, and incident actuation with small deterministic tests.
3. Calibrate on training days and validate on untouched days against the locked local criteria.
4. Reject or repair unstable model variants—teleports, unresolved collisions, impossible queues, systematic route failures, or strong seed sensitivity are not harmless noise.
5. Obtain an independent traffic engineer's acceptance of the base model and measurement definitions before alternative tuning.

### Phase B: tune, then freeze

1. Optimize the coordinated fixed-time baseline on training realizations; confirm its choice on validation realizations.
2. Tune only the declared max-pressure parameters—such as decision interval, pedestrian pressure weight, queue smoothing, cycle cap, and allowed maximum service interval—on the same training/validation split.
3. Use the same safety constraints but do not force identical operational parameters where the controller classes inherently differ.
4. Freeze source code, SUMO version, configuration, detector model, fixed timing, pressure formulation, parameter values, demand generator, incident, seed list, endpoints, censoring, statistics, and decision rule. Hash the input bundle.
5. Run implementation unit tests on hand-calculated queue states and phase choices. Test full receiving links, zero demand, tied pressure, stuck/missing detector, pedestrian call, emergency preemption, communication timeout, controller restart, and fallback to the safe fixed plan.

### Phase C: paired confirmatory runs

Use a controller-by-scenario design: two controllers crossed with peak and peak-plus-incident. For each stochastic replication, use common random numbers and the same pre-generated traveler/behavior input for both controllers. Merely giving SUMO the same master seed can be insufficient if different control trajectories consume random numbers in a different order; pre-generating stochastic inputs makes the pairing auditable. SUMO supports explicit repeatable seeds and documents repeated-seed operation ([SUMO randomness documentation](https://sumo.dlr.de/docs/Simulation/Randomness.html)).

Randomize run order, conceal treatment labels during metric extraction, and run each simulation in a fresh process. Record the software/container identifier, machine, command, wall-clock/controller computation times, seed, checksums, warnings, teleports, unfinished trips, and output checksums.

Use a warm-up long enough for the corridor state to represent the start of the recurring peak, then a locked measurement cohort and a common clearance tail. Do not estimate the warm-up separately for each controller. Include the same initial queues if the observed peak starts with residual demand.

FHWA recommends multiple alternative runs with differing seeds and an initial set of four runs to estimate stochastic variability, followed by the required number of replications and statistical testing ([FHWA Volume III, Chapter 6](https://ops.fhwa.dot.gov/publications/fhwahop18036/chapter6.htm)). Four is a variance pilot, not an adequate default sample size for tail non-inferiority. Use pilot runs that are excluded from confirmatory estimation—or a fully predeclared blinded sample-size re-estimation—to estimate the paired variance of all three ratios. Choose *N* to provide at least 90% joint power under explicit design alternatives that are far enough beyond the decision margins to be worth detecting, with a prespecified maximum *N*. Power cannot be 90% when the true effect lies exactly on a tested margin. Do not keep adding seeds after looking at which endpoint narrowly failed.

### Statistical analysis

Treat the day/replication as the independent cluster. Individual people and one-second queue samples inside a run are not independent replicates. For each scenario:

1. estimate all three max-pressure/fixed-time ratios from the paired runs;
2. use a paired hierarchical bootstrap, resampling replication/day clusters and recalculating the mean or p95 from their underlying observations;
3. report point estimates, absolute changes, percent changes, and one-sided 95% upper confidence bounds;
4. run implementation-independent checks with a paired randomization or permutation test where appropriate.

The exact claim passes only when the upper confidence bounds satisfy

\[
U_{0.95}[R_D(s)]\le0.90,\qquad
U_{0.95}[R_W(s)]\le1.05,\qquad
U_{0.95}[R_Q(s)]\le1.05
\]

for every confirmatory scenario stratum. Requiring all component tests to pass is an intersection-union decision: a failure or inconclusive interval on any component means the joint claim is not established. No favorable average can compensate for a failed harm guardrail. If analysts inspect multiple alternative endpoint definitions, incident choices, subgroups, or controller versions, those are exploratory and need multiplicity handling; they cannot replace the locked result.

Report distributions as well as ratios. At minimum show run-paired differences, person-delay histograms by mode, pedestrian waits by crosswalk, queue trajectories by approach, throughput/completion, phase service and switching, spillback duration, and incident recovery time. Inspect whether the mean benefit is concentrated in arterial car occupants while pedestrians, buses, or one side street bear the cost.

### Robustness analyses that cannot rescue the primary result

After the locked analysis, repeat or reweight across plausible calibrated parameter sets, detector noise/dropout and latency, occupancy uncertainty, route-choice behavior, demand near the validation envelope's limits, and modest incident timing/duration uncertainty. A 2024 global sensitivity analysis of a three-intersection SUMO model found delay and travel-time outputs sensitive to car-following acceleration, deceleration, headway, speed-factor distribution, and impatience, underscoring the need to calibrate and vary these parameters rather than treating defaults as truth ([Schrader and Bittle, 2024](https://doi.org/10.1109/TITS.2024.3372334)).

Also run pure Q-MP, the chosen pedestrian-aware candidate, and—if corridor progression is a concern—a separately frozen coordinated-MP diagnostic. These analyses explain mechanism and inform a future controller; they do not change the primary treatment after the fact.

## Decision rule

### Conditional go

Authorize only a limited, reversible field pilot if all of the following are true:

- independent reviewers accept the calibrated/validated base model and confirm that no evaluator-only SUMO state is unavailable to the proposed field controller;
- all registered one-sided confidence bounds pass in every required scenario;
- there are no teleports, censored queues, missing-trip bias, unsafe/illegal phases, unserved pedestrian calls, or unacceptable physical-storage overflows that undermine the result;
- benefit direction and guardrails remain credible under the predeclared calibration and detector-uncertainty checks;
- hardware-in-the-loop tests reproduce phase commands, timing constraints, latency, failover, pedestrian operation, preemption, flashing modes, and cabinet conflict monitoring;
- the agency confirms that sensing coverage and maintenance can support the queue estimates used in the primary simulation.

Then proceed in stages: shadow operation with no signal authority; hardware-in-the-loop and cabinet testing; a single-intersection off-peak trial with operator override and automatic fallback; and only then a short four-intersection corridor pilot. Use an independent safety/operations review and a prewritten stop rule for excessive pedestrian wait, side-street spillback, detector failure, communications failure, or anomalous phases. A SUMO pass supports an operational pilot; it does not establish crash safety.

### No-go or inconclusive

Do not pilot this controller version if any threshold fails, if an interval crosses its margin, or if the model/hardware validity checks fail. “Inconclusive” is a no-go for the stated claim, not evidence of equivalence. Do not lower the 10% target, widen a 5% harm margin, choose a more favorable incident, remove unfinished travelers, or retune after seeing confirmatory results. A materially revised controller can be evaluated as a new study.

## Important limitations

- **Simulation validity dominates.** Calibration can make SUMO resemble selected field measures without guaranteeing correct counterfactual response to a novel adaptive policy.
- **The theorem is not the estimand.** Maximum stability under a queueing model is neither mean-delay optimality nor pedestrian/side-street non-inferiority.
- **One incident has narrow external validity.** Passing one blockage does not establish performance for crashes, weather, special events, emergency preemption, detector outages, or incidents elsewhere.
- **Four signals are an open system.** Boundary demand, downstream congestion outside the model, and rerouting can reverse the apparent benefit.
- **Tail metrics are noisy and definition-sensitive.** P95 estimates require substantially more information than a mean; sampling interval, detector length, crosswalk aggregation, and censoring must be frozen.
- **Sensors can erase simulated gains.** Queue occlusion, finite field of view, movement misclassification, communications latency, and failed detectors may change phase decisions. Minnesota's hardware-in-the-loop work specifically found sensing integration to be a deployment issue.
- **Mode equity is not automatic.** Vehicle-queue control can improve throughput while shifting delay to people in high-occupancy vehicles, pedestrians, or minor approaches.
- **Operational and safety questions remain.** Driver expectancy, controller/cabinet interoperability, cybersecurity, maintenance, pedestrian accessibility, emergency response, and crash risk are not resolved by mobility metrics.

## Advice to the lab

Treat the 10%/5%/5% statement as a demanding joint claim. The most informative near-term investment is not a live pilot or a more elaborate controller; it is accurate pedestrian, occupancy, movement, queue, and incident data plus a credible fixed-time reoptimization. If the locked simulation passes, the evidence supports a carefully staged pilot. If it does not, the study will still reveal whether the limiting issue is corridor progression, finite storage, pedestrian service, occupancy mismatch, sensing, or simply lack of a 10% opportunity against a strong baseline.

As of the evidence reviewed here, **the justified decision is go for the confirmatory study and no-go for field authority until it passes.**

## Search and source ledger

Search date: **2026-07-15**. No simulation was run and no local calibration values were assumed.

- Academic searches: “max-pressure traffic signal control queue finite capacity spillback incident,” “queue-based max pressure pedestrian waiting,” “occupancy/person max-pressure,” “cyclic max-pressure phase structure,” and “SUMO traffic microsimulation sensitivity.” Discovery used academic metadata search and direct publisher/author manuscripts.
- Foundational/review sources: [Varaiya 2013](https://doi.org/10.1016/j.trc.2013.08.014) for the original mechanism and theorem boundary; [Levin 2023](https://doi.org/10.1061/JTEPBS.TEENG-7578) for the methodological and empirical review.
- Practical variants: [capacity-aware pressure](https://doi.org/10.1109/TCNS.2014.2378871), [position-weighted/incident-responsive pressure](https://doi.org/10.1016/j.trb.2019.08.005), [cyclic phase structure](https://doi.org/10.1016/j.trc.2020.102828), [pedestrian-queue pressure](https://doi.org/10.1016/j.trc.2024.104865), [occupancy-weighted pressure](https://doi.org/10.1016/j.trc.2024.104795), and [coordinated corridor pressure](https://doi.org/10.1016/j.trb.2025.103308).
- Deployment evidence: [Minnesota hardware-in-the-loop report](https://rosap.ntl.bts.gov/view/dot/79015) and [2025 isolated-intersection travel-time-based experiment](https://doi.org/10.1016/j.trc.2025.105070).
- Official protocol/metric sources: [FHWA Traffic Analysis Toolbox Volume III](https://ops.fhwa.dot.gov/publications/fhwahop18036/index.htm), [FHWA Traffic Signal Timing Manual](https://ops.fhwa.dot.gov/publications/fhwahop08024/), and the [current MUTCD](https://mutcd.fhwa.dot.gov/).
- Official simulator sources: SUMO documentation for [traffic-light timing tools](https://sumo.dlr.de/docs/Tools/tls.html), [TripInfo](https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html), [Statistic Output](https://sumo.dlr.de/docs/Simulation/Output/StatisticOutput.html), [E2 queue detectors](https://sumo.dlr.de/docs/Simulation/Output/Lanearea_Detectors_%28E2%29.html), [pedestrian crossing instrumentation](https://sumo.dlr.de/docs/Tutorials/TraCIPedCrossing.html), and [randomness/seeds](https://sumo.dlr.de/docs/Simulation/Randomness.html).
- Model uncertainty: [Schrader and Bittle 2024](https://doi.org/10.1109/TITS.2024.3372334) for sensitivity of SUMO performance measures to behavioral and fleet inputs.
