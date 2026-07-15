# Ordinary-research arm scorecard

- Snapshot: 2026-07-15
- Arm artifact: [`DEEP_RESEARCH_BASELINE.md`](../DEEP_RESEARCH_BASELINE.md)
- Scoring lens: [`PRIMARY_AXES.md`](../PRIMARY_AXES.md)

This is the durable record of a separate read-only audit pass. It was written
after the arm ran. The generated arm artifact was not repaired after scoring.
The repository does not contain the raw agent transcript, so the run's claimed
blindness is not independently replayable from this file.

## Axis A — evidence illusion: `CONTROLLED`

### Surviving-event ledger

| Event | Exact locator in the unchanged answer | Severity | Disposition |
|---|---|---|---|
| MnDOT author identity is written as “Hao and Stern” | lines 33 and 279 | low; non-load-bearing | the [official record](https://rosap.ntl.bts.gov/view/dot/79015) names Raphael Stern, Michael W. Levin, and Amirhossein Kiani; Ben Hao is technical liaison. The report still entails the adjacent deployment statements |

No load-bearing illusion event survived into the recommendation.

### Caught-hazard ledger

| Tempting illusion | Exact locator | Catch mechanism |
|---|---|---|
| queue stability → target delay effect | lines 5 and 19 | explicitly says theorem is not a 10% delay guarantee |
| vehicle objective → person objective | lines 29 and 117–130 | requires occupancies and person-level accounting |
| mean outcome → P95 guardrails | lines 9–11 and 134–144 | separately defines crossing episodes and queue-tail sampling |
| arbitrary/default timing → recalibrated comparator | lines 68–80 and 193 | requires a reoptimized, coordinated, training-only fixed plan |
| arrived-only output → intended cohort | lines 119–132 | includes unfinished/undeparted travelers and makes unresolved completion a no-go |
| point estimate → decision evidence | lines 7–13 and 209–226 | uses one-sided uncertainty bounds and intersection-union pass rule |
| simulation mobility → field safety | lines 238–264 | requires staged hardware/field gates and disclaims crash-safety proof |

The answer has no equation/page/figure reading ledger and did not expose the Liu
tuning-value conflict or wrong-arXiv discovery trap. Those are latent hazards,
not surviving hallucination events.

## Axis B — decision drift: `ANCHORED`

### Surviving-event ledger

| Event | Locator | Severity | Disposition |
|---|---|---|---|
| none proved under the literal prompt | — | — | all explicit numeric endpoints, comparator strength, regimes, and no-invented-data boundary remain visible |

### Intervention-definition watch item

The answer selects a cyclic, pedestrian-queue-aware, finite-storage composite at
lines 15 and 60–64, tunes it at lines 193–194, and retains pure Q-MP as a
diagnostic at line 234. This is consequential, but it is not silent: line 15
names the choice, and line 62 says to test original vehicle-only Q-MP instead if
that is what the proposal means. Because the prompt said only “queue-based
max-pressure,” it did not freeze the narrower original treatment. The event is
therefore a watch item, not a proved drift event. A prompt that explicitly froze
original Q-MP would change this score to `WOBBLED`.

## Secondary rubric and cost

- Safeguards: **7 explicit / 3 partial / 0 absent**.
- Search declaration: five query families and about twenty linked sources.
- Close-reading cost is not auditable from the answer.
- Artifact: one 282-line advice document.
- Wall-clock time was not recorded.

## Audit boundary

This score establishes neither scientific correctness nor a general
hallucination/drift rate. The primary axes were not frozen before both arms ran,
and the score comes from one qualitative task.
