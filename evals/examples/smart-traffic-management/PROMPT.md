# Frozen comparison prompt — smart traffic management

- Frozen at: 2026-07-15
- Prompt ID: `STM-COMPARE-001-v1`

> You are advising a city traffic-research lab. Design a simulation study to
> decide whether the lab should pilot a queue-based max-pressure traffic-signal
> controller instead of a recalibrated fixed-time controller on a
> four-intersection urban corridor. The proposed claim is: in SUMO, under a
> recurrent peak-demand profile and one predeclared incident perturbation, the
> max-pressure controller reduces network-wide mean person delay by at least
> 10%, while increasing neither 95th-percentile pedestrian waiting time nor
> 95th-percentile side-street queue length by more than 5%. Provide literature
> grounding, metrics and baselines, an experimental protocol, and a go/no-go
> decision. Do not run the simulation or invent local calibration data.

Both comparison arms receive the text above unchanged. The ordinary-research
arm may use normal web and academic research but is not given the Theory First
status model, templates, or child-skill routing. The Theory First arm must use
the released seven-skill workflow and may stop at `CODE_BLOCKED` when its gates
require that result.
