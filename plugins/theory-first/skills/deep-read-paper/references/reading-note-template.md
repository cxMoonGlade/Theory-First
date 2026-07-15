# Auditable close-reading note

Use one note per inspected source version. Remove empty optional rows, but do
not remove unresolved-item or inference sections.

## Assignment

- Target evidence row:
- Claim or bridge under review:
- Consequence if wrong:
- Required fidelity:
- Acceptance condition:
- Failure condition:

## Source identity and provenance

| Field | Value |
|---|---|
| Title | |
| Authors | |
| Venue or repository | |
| DOI, arXiv ID, or stable identifier | |
| Version and date | |
| Supplement or correction | |
| Artifact SHA-256 | |
| Access date | |
| Evidence class | primary / secondary / project-authored |
| Implementation locator and commit | |

Do not record an absolute local path.

## Source map

| Section or artifact | Purpose | Relevance to assignment | Read depth |
|---|---|---|---|
| | | | mapped / close-read / visually verified |

## Notation ledger

| Symbol | Paper meaning | Type or shape | Units | Domain | First definition | Project mapping |
|---|---|---|---|---|---|---|
| | | | | | page/section/equation | |

## Assumption ledger

| Assumption | Exact locator | Used by | Project satisfies it? | Failure consequence |
|---|---|---|---|---|
| | | equation/theorem/algorithm | yes / no / unknown | |

## Equation and definition ledger

| Item | Exact locator | Paper statement | Reconstruction | Checks | Status |
|---|---|---|---|---|---|
| | page/equation | minimal expression or paraphrase | steps and bridge | units/limits/sign | verified / inference / unresolved |

Keep quoted or transcribed material to the minimum needed for audit.

## Theorem and proof ledger

| Result | Locator | Hypotheses and quantifiers | Conclusion | Dependency or proof route | Project applicability |
|---|---|---|---|---|---|
| | | | | | satisfied / violated / unknown |

## Figure and table ledger

| Item | Locator | Visual facts | Caption claim | Author inference | Project inference | Visual status |
|---|---|---|---|---|---|---|
| | page/figure/panel | axes, units, scale, uncertainty | | | | verified / visually-unverified |

## Algorithm and implementation reconstruction

- Inputs and outputs:
- State and update order:
- Preprocessing and data selection:
- Objective and estimator:
- Initialization and stopping rule:
- Discretization, tolerance, and numerical precision:
- Randomness and seeds:
- Negative controls and ablations:
- Paper-to-code differences:
- Missing implementation details:

## Claim ledger

| Label | Claim | Exact evidence or derivation | Assumptions | Falsifier | Status |
|---|---|---|---|---|---|
| `[source]` | | page/section/figure | | | |
| `[reconstructed]` | | derivation steps | | | |
| `[project-inference]` | | bridge | | | |
| `[unknown]` | | | | | |
| `[conflict]` | | conflicting locators | | | |

## Adversarial checks

- Dimensional or limiting-case check:
- Alternative interpretation of the observable:
- Failed theorem hypothesis or assumption:
- Implementation ambiguity:
- Result that would reverse the bridge:
- Version, supplement, or correction conflict:

## Unresolved items and access limits

List inaccessible supplements, illegible equations, visually unverified items,
undefined notation, missing code versions, and questions requiring another
source. Do not infer around an access failure.

## Evidence-row disposition

Choose one and justify it with locators:

- `CLOSED`
- `INFERENCE_ONLY`
- `MISSING`
- `AMBIGUOUS`
- `CONTRADICTED`

State precisely what this disposition does **not** establish.

## Minimal quotation ledger

| Quoted fragment | Why paraphrase was insufficient | Locator | Word count | License or access note |
|---|---|---|---:|---|
| | | | | |

Do not attach or redistribute the source or extracted full text.
