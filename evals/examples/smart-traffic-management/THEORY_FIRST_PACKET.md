# Theory First closure packet — smart traffic management

## Header

```text
charter_id: STM-COMPARE-001
claim_version: v1
frozen_claim: in SUMO, under a recurrent peak-demand profile and one
  predeclared incident perturbation, queue-based max-pressure reduces
  network-wide mean person delay by at least 10%, while increasing neither
  P95 pedestrian waiting time nor P95 side-street queue length by more than 5%
decision_supported: whether a four-intersection corridor comparison is ready
  for preregistration and claim-bearing implementation, and what a later pass
  could support
project_profile_version: none; generic public-release defaults only
evidence_snapshot_date: 2026-07-15
search_languages: English
access_constraints: public sources only; no local city data; live SUMO docs
  not release-pinned; no authenticated literature database
closure_status: OPEN
```

Top-level workflow status: **`CODE_BLOCKED`**.

This is a completed outcome of the literature-closure stage, not a failed
attempt to produce a favorable answer. The published Theory First workflow
requires every load-bearing row to close before preregistration or experiment
code. Rows E1–E9 do not close for claim v1.

## Frozen charter

- Decision: decide whether claim v1 is specific and grounded enough to
  preregister a SUMO comparison; do not decide the empirical outcome.
- Consequence of a false go: simulation code could faithfully measure a
  substituted controller or metric and still answer the wrong question.
- Kill condition: any open intervention, target-estimator, local-calibration,
  validity-regime, or theorem-to-outcome bridge row.
- Invariants: four controlled intersections; queue-based MP; a genuinely
  recalibrated fixed-time comparator; person rather than vehicle delay; both
  P95 guardrails; recurrent peak and one predeclared incident; 10%/5%/5%; no
  invented calibration and no inspected results.
- Explicitly out of scope: running SUMO, choosing local geometry/demand,
  declaring a pilot safe, or silently replacing Q-MP with another MP variant.

## Evidence matrix

| Row ID | Function | Proposition that must be supported | Evidence locator | Evidence kind | Regime | Status | Conflict or next action |
|---|---|---|---|---|---|---|---|
| E1 | mechanism | one exact executable controller is the frozen “queue-based MP” intervention | Varaiya p. 184, eqs. (21)–(23); [close read](source-audits/varaiya-2013.md) | source claim + project inference | infinite point queues, period-level admissible stage | inference-only | source core is reconstructed; phase order, timing, full-link behavior, sensing, and tie rules remain unset |
| E2 | observable | equations and populations define mean person delay, P95 crossing wait, and P95 side-street queue | SUMO TripInfo field tables; Liu p. 19 and Fig. 9; [SUMO note](source-audits/sumo-output-docs-2026-07-15.md); [Liu note](source-audits/liu-gayah-levin-2024.md) | source claims + project inference | live SUMO docs; unrelated 5×5 source grid | missing | similarly named built-ins do not close traveler, crossing-event, detector, or aggregation semantics |
| E3 | metric/baseline | the fixed-time arm has a declared calibration-only surface, objective, cycle/splits/offsets, and frozen plan | Grégoire p. 7 §V-A item 3; Ault & Sharon p. 6 §3.4; [Grégoire note](source-audits/gregoire-et-al-2015.md); [Ault & Sharon note](source-audits/ault-sharon-2021.md) | source claim | non-optimized or scenario-defined source baselines | missing | neither source instantiates a recalibrated local comparator; local data are forbidden/absent |
| E4 | validity regime | the mechanism bridge covers finite storage, recurrent peak, and capacity-reducing incident | Varaiya pp. 194–195 §6; Grégoire p. 4 Theorem 1 and Figs. 4–6 | source claim | physical bounded links versus point queues | contradicted | ordinary back-pressure is not generally work-conserving with bounded queues; choose and version a remedy or narrow the regime |
| E5 | mechanism → outcome bridge | cited evidence entails the 10% person-delay benefit and both 5% P95 non-inferiority claims | Varaiya p. 184 Theorem 2 and p. 195 §6; Liu pp. 19–21 Fig. 9 | source claim | source queue stability; average delays for a different controller/grid | contradicted | stability is not finite-horizon delay; average pedestrian delay is not P95; no universal magnitude is supplied |
| E6 | implementation fidelity | a pinned SUMO version, scenario bundle, legal signal surface, censoring policy, and deterministic manifest exist | SUMO TripInfo unfinished-output section; live docs snapshot | source specification + project fact | no executable project artifact | missing | pin release/commit and supply network, demand, controller, detector, and incident artifacts |
| E7 | statistical validity | independent unit, paired inputs, run-count rule, uncertainty construction, and joint decision are frozen | no project preregistration; prompt supplies margins only | project design | future local study | missing | design after estimands and calibration surface exist; results may not be inspected first |
| E8 | disconfirmation/measurement | full-link and pedestrian observations are validated against independent traces and deliberate corruption | Grégoire p. 4; Liu p. 23 Fig. 11; SUMO E2/TripInfo docs | source claim + project inference | source models/live docs | inference-only | specify hand-labeled crossing traces, queue-coverage checks, full-link case, detector-noise/dropout controls |
| E9 | external validity | a minimum local calibration/validation packet exists for even a limited city-pilot inference | prompt explicitly withholds local calibration; no project profile | project fact | four-intersection local corridor | missing | obtain geometry, timing, demand/routes, occupancies, pedestrian arrivals, storage, saturation, incident, and independent validation data |

No row is `CLOSED` at the complete project-claim level. The sources do close
narrower propositions—classical MP's equation and theorem, bounded-storage
failure, PQ-MP's distinct theorem, and selected SUMO field semantics—but those
facts do not close the bridges required by claim v1.

## Numerical provenance

| Value ID | Value and units | Role | Source kind | Exact locator | Transformation chain | Regime compatibility | Status |
|---|---|---|---|---|---|---|---|
| N1 | four intersections | study boundary | project-design | frozen prompt, lines 7–9 | none | corridor geometry absent | declared, not instantiated |
| N2 | 10% mean-person-delay reduction | benefit margin | project-design | frozen prompt, lines 11–12 | intended ratio `D_MP/D_FT <= 0.90` | valid as a decision threshold, not a prediction fact | declared |
| N3 | 5% increase in P95 pedestrian wait | harm margin | project-design | frozen prompt, lines 12–13 | intended ratio `W_MP/W_FT <= 1.05` | denominator/episode population absent | declared, estimator missing |
| N4 | 5% increase in P95 side-street queue | harm margin | project-design | frozen prompt, line 13 | intended ratio `Q_MP/Q_FT <= 1.05` | unit and approach/time aggregation absent | declared, estimator missing |
| N5 | one recurrent peak + one incident | required regimes | project-design | frozen prompt, lines 9–10 | none | profile and perturbation unset | missing inputs |
| N6 | 1.3 persons/vehicle | source person-delay weighting | source-design | Liu p. 19, §4.3.2 | vehicle delay × 1.3 plus pedestrian delay | source grid only | **not imported** |
| N7 | `lambda=0.0006` or `0.006` | source PQ-MP tuning | source-design / internal conflict | Liu p. 19 prose versus Fig. 9 label | none accepted | different controller and grid | **ambiguous; not imported** |
| N8 | 7.5 m per stored vehicle | source capacity estimate | convenience | Grégoire p. 7, §V-A | 5 m vehicle + 2.5 m gap | source default fleet only | **not imported** |
| N9 | 15 s slot including 4 s yellow | source controller timing | source-design | Grégoire p. 7, §V-A | none | local signal contract absent | **not imported** |

The 10%/5%/5% values are legitimate project decision margins because the prompt
defines them. They are not represented as literature-derived expected effects or
universal operational standards.

## Illusion and drift trip ledger

| Trip ID | Tempting promotion or substitution | Detection artifact | Disposition |
|---|---|---|---|
| I1 | queue-stability theorem → 10% person-delay prediction | Varaiya theorem/§6 close read | blocked; E5 contradicted |
| I2 | average pedestrian delay → P95 crossing wait | Liu Fig. 9 and observable audit | blocked; E2/E5 missing |
| I3 | vehicle `timeLoss` or ride `waitingTime` → target person/crossing delay | official field definitions | blocked; derived estimator required |
| I4 | source benchmark fixed time → recalibrated local fixed time | Grégoire/Ault baseline reconstruction | blocked; E3 missing |
| I5 | unqualified Q-MP → capacity-/pedestrian-aware composite | controller-identity ledger | blocked; requires claim v2 |
| I6 | live SUMO docs → version-pinned implementation fidelity | version/provenance audit | blocked; E6 missing |
| I7 | `lambda=0.0006` → copied tuning fact | text/grid/Fig. 9 inconsistency | blocked; source conflict retained |
| I8 | wrong `arXiv:2103.01115` → RESCO evidence | title/body identity check | rejected before matrix entry |
| I9 | favorable source effect → local pilot advice | local calibration gate | blocked; E9 missing |

Surviving load-bearing illusion events in the Theory First recommendation: **0**.
Caught hazards: **9**. These counts describe this recorded run only.

Drift status: **`ANCHORED`**. Alternative MP variants are mapped as separate
claim versions; none silently replaces v1. The original claim is stopped.

## Search ledger

The exact query-by-query ledger is preserved in
[`THEORY_FIRST_LANDSCAPE.md`, §9](THEORY_FIRST_LANDSCAPE.md#9-exact-search-ledger-and-access-limits).
The closure stage additionally performed these identity and fidelity checks:

| Date | Corpus or database | Query family | Filters and language | Results screened | Relevant leads | Access limits |
|---|---|---|---|---:|---:|---|
| 2026-07-15 | repository-local files | traffic/MP/SUMO literature and project profile | tracked and ignored local example files; English | 1 template surface | 0 domain evidence artifacts | standalone release has no domain corpus or local city data |
| 2026-07-15 | AnySearch academic | MP foundation, finite capacity, pedestrians, metrics, incident | engineering/relevance or date; English | bounded result pages | Varaiya, Grégoire, Liu, corridor leads | snippets used only for routing; one search endpoint temporarily failed |
| 2026-07-15 | public web/primary hosts | exact titles, DOI, official FHWA/SUMO pages | primary/official preferred; English | bounded search pages | four close-read sources and SUMO specs | publisher access uneven; live docs unpinned |
| 2026-07-15 | acquired full texts | equation/theorem/figure/implementation fidelity | identified versions only | 4 papers | Varaiya; Grégoire; Liu; Ault & Sharon | no redistribution; journal correction/code not exhaustively checked |

One discovery result mapped the RESCO title to `arXiv:2103.01115`. Safe local
inspection showed that identifier contained an unrelated economics paper. It
was excluded and the official NeurIPS proceedings paper was used instead.

## Source inventory

| Source | Version | Assigned rows | Deep-read note | Correction/retraction status | Redistribution |
|---|---|---|---|---|---|
| Varaiya, “Max pressure control…” | publication PDF, 2013; DOI 10.1016/j.trc.2013.08.014 | E1, E4, E5 | [note](source-audits/varaiya-2013.md) | no correction checked; none observed | citation/notes only |
| Grégoire et al., “Capacity-Aware…” | arXiv v3, 2014; journal 2015 | E4, E5, E8 | [note](source-audits/gregoire-et-al-2015.md) | no correction checked; none observed | citation/notes only |
| Liu, Gayah, Levin, “Considering Pedestrian Queues” | arXiv v1, 2024; later journal DOI | E2, E3, E5, E8 | [note](source-audits/liu-gayah-levin-2024.md) | journal differences unresolved; manuscript has a tuning-value conflict | citation/notes only |
| Ault & Sharon, “RL Benchmarks…” | NeurIPS proceedings, 2021 | E2, E3, E6 | [note](source-audits/ault-sharon-2021.md) | no correction checked | citation/notes only |
| SUMO official output documentation | live snapshot, 2026-07-15 | E2, E6, E7, E8 | [note](source-audits/sumo-output-docs-2026-07-15.md) | live/version drift unresolved | links and paraphrase only |

## Closure decision and smallest next action

`closure_status=OPEN`; therefore the workflow returns **`CODE_BLOCKED`** and
does not create a preregistration or experiment code.

The smallest state-changing next step is not “search for one more favorable
paper.” It is to provide a versioned local input packet and choose one treatment:

1. keep original Q-MP and narrow the claim if pedestrian/finite-storage bridges
   cannot close; or create an explicitly new claim version for a declared
   capacity-/pedestrian-aware controller;
2. supply corridor geometry, legal phase programs, storage/saturation data,
   recurrent demand/routes, occupancies, pedestrian arrivals, and the exact
   incident;
3. specify and freeze the fixed-time recalibration surface;
4. bind release-pinned SUMO raw events to all three estimators and validate them
   with hand-checked traces/corruptions;
5. then rerun closure and, only if all rows close, preregister predictions,
   sample-size/stopping rules, and falsifiers before code or results.

That action preserves claim v1's failure rather than rewriting it into an easier
question.
