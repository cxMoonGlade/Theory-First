# SUMO output documentation — auditable technical-source note

## Assignment

- Target evidence rows: E2, E6, E7, E8.
- Claim or bridge under review: whether built-in SUMO fields directly implement
  mean person delay, pedestrian crossing wait, and side-street queue length.
- Consequence if wrong: similarly named outputs can create a fully reproducible
  but wrong result.
- Required fidelity: official field definitions, inclusion/censoring behavior,
  person-stage semantics, and version boundary.
- Acceptance condition: identify fields that are direct, derived, or unsuitable.
- Failure condition: equate `waitingTime` or vehicle `timeLoss` with a frozen
  person/pedestrian estimand without an event-level bridge.

## Source identity and provenance

| Field | Value |
|---|---|
| Title | SUMO TripInfo, output overview, pedestrian, and lane-area-detector documentation |
| Authors | Eclipse SUMO project |
| Venue or repository | official SUMO documentation |
| DOI, arXiv ID, or stable identifier | [TripInfo](https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html); [output overview](https://sumo.dlr.de/docs/Simulation/Output/index.html); [pedestrians](https://sumo.dlr.de/docs/Simulation/Pedestrians.html); [E2](https://sumo.dlr.de/docs/Simulation/Output/Lanearea_Detectors_%28E2%29.html) |
| Version and date | live documentation snapshot accessed 2026-07-15; release not pinned |
| Supplement or correction | live pages can change |
| Artifact SHA-256 | not retained; version-pinned source is a prerequisite |
| Access date | 2026-07-15 |
| Evidence class | primary technical specification |
| Implementation locator and commit | [eclipse-sumo/sumo](https://github.com/eclipse-sumo/sumo); commit absent |

## Source map

| Section or artifact | Purpose | Relevance to assignment | Read depth |
|---|---|---|---|
| TripInfo “Generated Output” | vehicle field semantics | E2/E7 | close-read |
| TripInfo “Output for vehicles that have not arrived” | censoring | E6/E7 | close-read |
| TripInfo “Person and Container Output” | person-stage fields | E2/E8 | close-read |
| output overview “Aggregated Traffic Measures” | denominator defaults | E2/E7 | close-read |
| E2 lane-area detector output | jam/queue fields | E8 | mapped; release-specific behavior unresolved |

## Notation ledger

| Field | Official meaning in inspected page | Units | Project mapping |
|---|---|---|---|
| vehicle `waitingTime` | time with vehicle speed at or below 0.1 m/s, excluding scheduled stops | seconds | nearby vehicle metric, not person or crossing delay |
| vehicle `timeLoss` | time lost from travel below individual ideal speed | seconds | possible component/cross-check, not a complete person estimand |
| `departDelay` | delay between intended and actual vehicle insertion | seconds | missing-trip/insertion component |
| person ride `waitingTime` | time spent waiting for a vehicle | seconds | not pedestrian signal wait |
| walk/ride `timeLoss` | time below maximum speed; ride inherits vehicle time loss | seconds | not a curb-arrival-to-crossing-start event by definition |
| E2 jam length | detector-reported jam length in vehicles/metres | count or metres | candidate side-street observation after detector validation |

## Assumption ledger

| Assumption | Exact locator | Used by | Project satisfies it? | Failure consequence |
|---|---|---|---|---|
| trip records are written on arrival by default | TripInfo, “Output for vehicles that have not arrived” | default denominator | no if used unchanged | congested arm drops unfinished trips and looks better |
| `--tripinfo-output.write-unfinished` changes inclusion | same section; output overview | censoring control | not yet specified | cross-arm denominator differs from intended cohort |
| person ride waiting is waiting for a vehicle | TripInfo person-stage field table | field interpretation | not relevant to crossing wait | semantic substitution |
| live docs match the executable release | not guaranteed | all implementation claims | unknown | field behavior can drift |

## Equation and definition ledger

| Item | Exact locator | Paper statement | Reconstruction | Checks | Status |
|---|---|---|---|---|---|
| arrived-only default | TripInfo “Output for vehicles that have not arrived” | unfinished vehicles generate no record unless option enabled | estimator denominator is outcome-dependent by default | congested-arm limit checked | verified |
| vehicle `waitingTime` | TripInfo generated-output table | speed threshold, vehicle-level | not crossing-service wait | units/agent checked | verified |
| person-stage `waitingTime` | TripInfo person-stage table | wait for a ride vehicle | not walk/crosswalk signal wait | stage type checked | verified |
| pedestrian crossing wait | absent as a direct TripInfo definition | must derive from frozen event timestamps/state transition | needs validation against hand-checked traces | event semantics missing | unresolved |
| physical side-street P95 | E2 fields plus project aggregation | detector output must be transformed over a declared population/sampling unit | detector coverage and percentile unit required | right-censor limit checked | inference-only |

## Theorem and proof ledger

Not applicable.

## Figure and table ledger

No figure is load-bearing. Official schema tables were read directly; no PDF
rendering was required.

## Algorithm and implementation reconstruction

- Required raw artifacts: per-person intended departure, route/mode, stage
  transitions, actual completion; per-crossing curb arrival and crossing entry;
  full-storage queue traces; unfinished/undeparted travelers; teleports.
- Estimator order: define the traveler/cohort and episode populations first,
  write raw events, then calculate the three frozen aggregates.
- Negative controls: a deliberately unfinished traveler must enter the chosen
  denominator; a synthetic stopped pedestrian waiting for a ride must not count
  as crossing wait; a queue extending beyond a short detector must trip the
  coverage check.
- Version contract: pin SUMO release/container and documentation/source commit
  before any claim-bearing implementation.
- Missing details: exact crossing-event state machine, detector configuration,
  percentile sampling unit, clear-down/hard-cap handling, and project version.

## Claim ledger

| Label | Claim | Exact evidence or derivation | Assumptions | Falsifier | Status |
|---|---|---|---|---|---|
| `[source]` | default TripInfo excludes unfinished vehicles | official TripInfo section | inspected live docs | version-pinned run differs | verified for snapshot |
| `[source]` | person ride `waitingTime` means waiting for a vehicle | official person-stage table | stage type | source schema differs | verified for snapshot |
| `[project-inference]` | crossing wait requires event-level derivation | no direct field plus target definition | event mapping must be validated | direct release-pinned field exists | inference-only |
| `[project-inference]` | E2 jam length can support the side-street metric | official E2 fields | full coverage and aggregation contract | trace/ground-truth mismatch | inference-only |
| `[conflict]` | built-in `waitingTime` alone closes both pedestrian and person delay | field definitions distinguish agents/stages | none | exact official equivalence | contradicted |

## Adversarial checks

- Semantic collision: three similarly named waiting/time-loss quantities refer
  to different agents and events.
- Censoring: the default arrived-only denominator rewards gridlock.
- Detector limit: a short E2 detector right-censors the queue exactly when the
  guardrail matters most.
- Version drift: the inspected live page cannot bind a future executable.

## Unresolved items and access limits

No SUMO version, commit, network, detector file, or hand-verified trace exists in
the example. The live documentation is adequate to expose the gap, not to close
release-specific implementation fidelity.

## Evidence-row disposition

- E2: `MISSING`; the three complete estimators and aggregation populations are
  not supplied by a single built-in field.
- E6: `MISSING`; no release/container or deterministic scenario manifest exists.
- E7: `INFERENCE_ONLY`; censoring controls are identified, but the statistical
  protocol is not frozen.
- E8: `INFERENCE_ONLY`; candidate raw surfaces exist, while event/detector
  validation does not.

This does not prevent a SUMO experiment. It prevents metric names from being
treated as an already-validated measurement bridge.

## Minimal quotation ledger

No verbatim quotation is needed; all specification statements above are
paraphrased.
