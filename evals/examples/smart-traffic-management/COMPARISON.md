# Comparison result — Theory First vs ordinary deep research

[简体中文](COMPARISON.zh-CN.md)

- Snapshot: 2026-07-15
- Prompt: [`STM-COMPARE-001-v1`](PROMPT.md)
- Primary axes: [`PRIMARY_AXES.md`](PRIMARY_AXES.md)
- Method and isolation: [`RUN_LOG.md`](RUN_LOG.md)

## Headline

| Arm | Evidence illusion | Decision drift | Immediate status |
|---|---|---|---|
| Released Theory First workflow | **`CONTROLLED`** — 0 load-bearing illusion events survived; 9 hazards were caught | **`ANCHORED`** — 0 surviving drift events | **`CODE_BLOCKED`**: do not preregister or implement claim v1 yet |
| Ordinary deep-research answer | **`CONTROLLED`** — 0 load-bearing illusion events survived; 1 low-severity attribution error remained | **`ANCHORED`** — 0 proved drift events; 1 intervention-definition watch item | no live pilot; proceed toward a locked confirmatory study |

Neither axis produced a clean count win. The ordinary answer was unusually
careful and blocked many common evidence errors on its own. Theory First added a
more durable, inspectable mechanism for preventing those hazards from becoming
premises, exposed source-level conflicts that synthesis alone missed, and
stopped when the exact controller remained unresolved.

The drift result was corrected during final audit. The prompt did not freeze
“original vehicle-only Q-MP,” and the ordinary answer explicitly labeled its
composite controller and the alternative original treatment. Its choice is
therefore a material **watch item**, but not a proved drift event under the
literal prompt. The primary axes were also added after the Theory First
landscape was produced, so the comparison is retrospective rather than
preregistered.

This is one qualitative worked example, not a statistical benchmark of agents,
products, or “deep research” systems.

Per-arm event ledgers are in the [Theory First scorecard](scorecards/THEORY_FIRST_SCORECARD.md)
and [ordinary-research scorecard](scorecards/ORDINARY_RESEARCH_SCORECARD.md).

## Axis A — evidence illusion

### Theory First: `CONTROLLED`

The closure packet records nine hazards and stops every one before
preregistration:

1. stability/throughput theorem → 10% person-delay prediction;
2. average pedestrian delay → P95 crossing wait;
3. vehicle `timeLoss` or ride `waitingTime` → target person/crossing delay;
4. scenario/default fixed timing → locally recalibrated fixed timing;
5. original Q-MP → capacity-/pedestrian-aware composite;
6. live SUMO documentation → release-pinned implementation fidelity;
7. Liu manuscript `lambda=0.0006` → copied tuning value, despite the tested
   grid and Fig. 9 pointing to `0.006`;
8. a wrong `arXiv:2103.01115` search association → RESCO evidence, rejected
   after title/body inspection;
9. favorable source result → local city-pilot authority.

Exact evidence and dispositions are in the
[`Illusion and drift trip ledger`](THEORY_FIRST_PACKET.md#illusion-and-drift-trip-ledger).
No load-bearing event survived into `CODE_BLOCKED`.

Theory First did not make the agent infallible. An isolated pre-release audit
found two non-load-bearing errors in the Grégoire reading note: a same-run seed
statement had been misread as ten replications, and the note had omitted the
paper's internal “3-hour” versus “7–9 a.m.” duration conflict. They were
corrected and logged. Neither error entered the evidence matrix or gate result.

### Ordinary deep research: `CONTROLLED`

The baseline explicitly stopped the major illusion routes: it separated queue
stability from delay (lines 5 and 19), vehicles from people (lines 29 and
117–130), means from tails (lines 9–11 and 134–144), arbitrary timing from a
recalibrated comparator (lines 68–80), arrived-only output from the intended
cohort (lines 119–132), and simulation mobility evidence from field safety
(lines 240–264). Its proposed estimators and joint uncertainty rule are strong
and immediately useful. The exact caught-hazard ledger is in its
[scorecard](scorecards/ORDINARY_RESEARCH_SCORECARD.md).

One low-severity `source-identity` error remained in
[`DEEP_RESEARCH_BASELINE.md`, lines 33 and 279](DEEP_RESEARCH_BASELINE.md): the
MnDOT report is attributed to “Hao and Stern.” The [official
record](https://rosap.ntl.bts.gov/view/dot/79015) names Raphael Stern, Michael W.
Levin, and Amirhossein Kiani as authors; Ben Hao is the technical liaison. The
report still supports the attached hardware-in-the-loop and staged-deployment
statements, so the error is not load-bearing.

The baseline had no equation/page/figure reading notes, so its source
entailments are harder to re-audit. It also did not expose the Liu tuning-value
conflict or the wrong-arXiv discovery trap. Those are **latent hazards**, not
proof that its final recommendation is hallucinated.

### What the illusion result means

Both arms prevented unsupported empirical confidence from reaching the main
advice. Theory First's advantage in this example is therefore **containment and
traceability**:

- every premise has an evidence-row status;
- source claim and project inference remain separately labeled;
- a source conflict cannot be normalized away;
- an open row mechanically blocks preregistration;
- audit corrections remain visible instead of silently changing the decision.

The cost is substantially more work and a heavier artifact trail.

## Axis B — decision drift

### Theory First: `ANCHORED`

Theory First does **not** pretend that the prompt froze original vehicle-only
Q-MP. Evidence row E1 keeps the exact executable controller `inference-only`,
and the closure packet maps capacity-aware, pedestrian-aware, cyclic, and
occupancy-weighted variants without selecting one. Because intervention,
finite-storage, pedestrian-observability, and outcome bridges remain open, v1
stops. The comparator, person-delay endpoint, both P95 guardrails,
peak/incident regimes, 10%/5%/5% margins, and no-invented-data boundary all
remain fixed.

One watch item is explicit: several disconfirmation discussions specialize the
still-undefined incident to a capacity-reducing incident. No protocol was
emitted and the local incident remains a missing input, so this did not change
the answer; a future preregistration must freeze the incident type rather than
inherit that assumption.

### Ordinary deep research: `ANCHORED`, with a watch item

The baseline selects a “cyclic, pedestrian-queue-aware max-pressure controller
with finite-storage safeguards” (lines 15 and 60–64), tunes that composite in
the primary study (lines 193–194), and retains pure Q-MP as a diagnostic (line
234).

This is not hidden: the answer says the variants are different, labels the
composite, explains why it prefers it, and says to test original vehicle-only
Q-MP instead if that is what the lab intended (line 62). Because the prompt
never specified original vehicle-only Q-MP, the audit cannot prove that the
answer changed a frozen treatment. Under the published rule, this remains an
intervention-definition watch item rather than a drift event.

The watch item still matters: the answer resolves a consequential ambiguity
inside the research response instead of stopping until the lab chooses. A
future benchmark should freeze the exact controller before either arm runs. If
that prompt explicitly named original Q-MP, this same answer would warrant a
`WOBBLED` score.

## Secondary ten-safeguard rubric

| Safeguard | Theory First | Ordinary deep research |
|---|---|---|
| 1. frozen decision/scope/regime/kill condition | explicit | partial — treatment choice is resolved inside the answer |
| 2. source claims vs project predictions | explicit | explicit |
| 3. mechanism → person-observable bridge | explicit | explicit |
| 4. exact primary-source locators | explicit | partial — DOI/pages, but no equation/page/figure ledger |
| 5. rivals, limitations, disconfirmation | explicit | explicit |
| 6. metrics, baseline, numerical provenance | explicit | explicit |
| 7. pre-result predictions and decision rules | partial — gate stops before statistical design | explicit |
| 8. independent truth and corruption falsifiers | partial — specified but not instantiated | partial — engineering checks, no explicit corruption artifact |
| 9. bounded simplifications and gaps | explicit | explicit |
| 10. scoped status cannot mimic validation | explicit | explicit |
| **Total** | **8 explicit / 2 partial / 0 absent** | **7 explicit / 3 partial / 0 absent** |

## Practical cost

| Cost surface | Theory First | Ordinary deep research |
|---|---|---|
| search record | 22 ledger entries, including capability discovery | 5 declared query families and about 20 linked sources |
| close reading | 4 primary papers + 1 official SUMO technical-source set | not auditable from the output |
| artifacts before comparison | landscape, closure packet, gate, 5 reading notes | one 282-line advice document |
| time-to-advice | wall-clock not recorded; short gate is fast to read, full chain is heavy | bottom line is immediately readable |
| actionability now | precise smallest next packet; no fake protocol | detailed study blueprint, but several selections remain open |

Theory First is not the right tool for every question. Here it spends more time
to obtain a stronger property: the research state cannot advance merely because
the prose sounds complete.

## Bottom-line judgment

- **Illusion:** both arms controlled load-bearing hallucination in this run.
  Theory First recorded more source-level detections and explicit provenance and
  propagation barriers; ordinary research was shorter and still excellent.
- **Drift:** both arms are `ANCHORED` under the literal prompt. Theory First
  exposed the exact-controller ambiguity as an open evidence row and stopped;
  ordinary research made a visible, reasoned choice. Theory First exposed a more
  explicit containment mechanism in its artifacts, but this run does not
  establish a comparative drift-rate advantage.
- **Scientific action:** do not run claim-bearing code yet. Supply the local
  corridor/calibration packet, freeze the exact controller and incident, close
  the estimators and baseline, then preregister. The ordinary blueprint is a
  useful input **after** those gates pass.

The defensible claim from this example is narrow: **on this prompt, the released
Theory First workflow made illusion and drift containment more auditable and
turned unresolved prerequisites into a mechanical stop.** It does not establish
lower hallucination or drift rates without a preregistered, blinded evaluation
set.
