# Theory-fix packet

## Frozen record

```text
claim_id_and_version:
exact_claim:
registered_statement_type:
intended_claim_confidence_class:
code_identifier:
configuration_identifier:
data_identifier:
environment_identifier:
result_artifact_identifiers:
preregistration_id:
freeze_timestamp:
```

Do not replace missing identifiers with reconstructed certainty. Record them as missing provenance.

## Propagation ledger

| Consumer | How it depends on the claim | Current status | Required action if STOP/REPAIR | Owner or artifact |
|---|---|---|---|---|

Set current status to `PROPAGATION_PAUSED` while the review is open.

## Evidence delta

| Evidence row | Previous status | Current status | Added/removed/changed source | Effect on claim |
|---|---|---|---|---|

## Trip-wire ledger

| Trip wire | Test performed | Independent reference | Outcome | Artifact locator | Consequence |
|---|---|---|---|---|---|

Use `survives`, `fires`, `pending`, or `not applicable`, matching `stress-test-claim`. Map a recoverable pending item to `REOPEN_EVIDENCE`. Map irrecoverable claim-bearing provenance loss to a fired provenance wire and then to `STOP`, unless every fired defect meets the parent's bounded `REPAIR` contract. Neither pending nor unjustified `not applicable` permits acceptance.

## Decision record

```text
status: STOP | REPAIR | ACCEPT_WITH_CLASS | REOPEN_EVIDENCE
decisive_reasons:
statement_type_if_accepted:
claim_confidence_class_if_accepted:
exact_validity_scope:
residual_risks:
forbidden_extrapolations:
repair_contract_or_next_evidence_action:
downstream_actions:
review_snapshot_date:
```

For `REPAIR`, preserve the original acceptance test and define a fresh artifact version. For `ACCEPT_WITH_CLASS`, state the recorded attack surface; do not imply universal truth.
