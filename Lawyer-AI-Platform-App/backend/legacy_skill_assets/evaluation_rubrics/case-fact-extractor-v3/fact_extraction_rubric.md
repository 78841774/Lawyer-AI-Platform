# case-fact-extractor-v3 Fact Extraction Rubric

Source basis: `case-fact-extractor-v3/references/scoring.md`.

Status: readonly evaluation rubric candidate.

## Gate

Lawyer casework requires score >= 90, no unresolved P1, and completed core amount verification before full A-series analysis.

## Common Criteria

| item | score |
| --- | ---: |
| Independent files | 10 |
| Naming and source structure | 10 |
| Current date and versioning | 10 |
| Source references and original excerpts | 10 |
| Legal professional language | 10 |

## Fact Extraction Criteria

| item | score |
| --- | ---: |
| Material completeness | 10 |
| Per-file extraction depth | 10 |
| Fact classification logic | 10 |
| Cross-checking and contradiction handling | 10 |
| Amount audit and admission conclusion | 10 |

## One-Vote Rejection

* Search replaces folder traversal.
* Total amount is wrong.
* Party or legal relationship is materially wrong.
* Core OCR issue is ignored.
* Unresolved P1 is hidden.
