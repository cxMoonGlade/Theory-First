# Synthetic theory-fix walkthrough

This demonstration is fictional. Its method, measurements, and source labels do
not describe a real scientific result and must not be cited as evidence.

## Before

A team reports:

> Our new discretization is 12% more robust than the baseline. The result is
> clean across every seed, so use it in the next design decision.

The supporting table used “successful steps before divergence” as the metric.
Because the result is clean and already about to propagate, `$theory-fix` reopens
the load-bearing evidence and freezes the downstream design decision.

```yaml
reported_claim: new discretization is 12% more robust
reported_metric: successful steps before divergence
downstream_use: choose the production discretization
review_state: result_accepted_without_adversarial_check
```

## Stress test

The synthetic review applies multiple independent tripwires:

| Tripwire | Test | Outcome |
| --- | --- | --- |
| Formulation invariance | Re-express performance per simulated unit time | fired |
| Observable bridge | Check that step count represents physical horizon | fired |
| Independent ground truth | Compare against a solver with a different failure detector | pending |
| Negative control | Use the old update with the new step-size schedule | reproduces most of the gain |
| Propagation audit | Find decisions already relying on “12% more robust” | two dependants frozen |

Inspection reveals that the new method uses a smaller adaptive step. It survives
more steps but reaches nearly the same simulated time. Most of the apparent gain
also appears when only the schedule changes. That does not prove the method has
no benefit; it breaks the bridge from the measured rate to the stated robustness
claim.

## After

```yaml
decision: REPAIR
accepted_claim: the tested configuration completed 12% more solver steps before the recorded detector fired
rejected_upgrade: the discretization is 12% more robust
required_repairs:
  - preregister simulated-time-to-divergence and error-at-fixed-time
  - freeze the step-size schedule across the primary comparison
  - complete the independent failure-detector comparison
  - retain schedule-only and identity controls
propagation:
  production_choice: STOPPED
  dependent_summary: mark_as_under_review
```

The after-state is narrower and less exciting, but auditable. A later rerun may
support a robustness claim only under the repaired preregistration; the existing
result cannot be silently reinterpreted as that evidence.
