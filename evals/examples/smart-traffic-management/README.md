# Smart Traffic Management Worked Example

English | [简体中文](README.zh-CN.md)

This is a real, same-prompt run of the released Theory First suite against an
ordinary deep-research arm. The task asks whether a four-intersection SUMO study
can support a 10% person-delay benefit while protecting two 5% P95 guardrails.
No simulation was run and no local calibration data was invented.

## Result

| Arm | Illusion | Drift | Status |
|---|---|---|---|
| Theory First | `CONTROLLED` | `ANCHORED` | `CODE_BLOCKED` |
| Ordinary deep research | `CONTROLLED` | `ANCHORED` + one definition watch item | no live pilot; prepare study |

The ordinary answer was strong: neither arm leaked a load-bearing hallucination
into its advice. Theory First caught more source-level hazards and mechanically
stopped on open prerequisites. The ordinary arm selected a cyclic,
pedestrian-aware, finite-storage composite, but the prompt had not frozen
original vehicle-only Q-MP; final audit therefore treats that as a definition
watch item, not a proved drift event.

Read the [full comparison](COMPARISON.md) and per-arm
[scorecards](scorecards/) for event ledgers, practical cost, audit limitations,
and the limits of this one-example result.

## Reproduce the route

Install the pinned wheel and provision the complete suite:

```bash
python -m pip install https://github.com/cxMoonGlade/Theory-First/releases/download/v0.3.0/theory_first-0.3.0-py3-none-any.whl
theory-first install --agent codex
```

Open a new agent task, paste [`PROMPT.md`](PROMPT.md), and invoke:

```text
Use $theory-first to analyze this claim before any claim-bearing code.
```

Expected route: landscape map → literature closure → assigned close reads →
preregistration gate. With only the public prompt, the expected honest state is
`CODE_BLOCKED`, not a fabricated protocol. A future run may change status only
when it supplies the missing local packet and closes the recorded rows.

## Audit trail

- [Frozen prompt](PROMPT.md)
- [Primary illusion/drift axes](PRIMARY_AXES.md)
- [Original ten-safeguard rubric](RUBRIC.md)
- [Run/isolation log](RUN_LOG.md)
- [Run manifest and artifact hashes](RUN_MANIFEST.json)
- [Per-arm scorecards](scorecards/)
- [Ordinary deep-research answer](DEEP_RESEARCH_BASELINE.md)
- [Theory First landscape](THEORY_FIRST_LANDSCAPE.md)
- [Theory First closure packet](THEORY_FIRST_PACKET.md)
- [Preregistration gate](THEORY_FIRST_PREREGISTRATION_GATE.md)
- [Close-reading source audits](source-audits/)

The full-text papers used for private inspection are not distributed.
