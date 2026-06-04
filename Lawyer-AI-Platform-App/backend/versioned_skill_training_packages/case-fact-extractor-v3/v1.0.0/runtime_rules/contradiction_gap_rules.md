# case-fact-extractor-v3 Contradiction and Gap Rules

Source basis: `case-fact-extractor-v3/SKILL.md`.

Status: readonly legacy asset prepared for versioned training packages.

## Contradiction Detection

The extractor must compare different materials describing the same fact.

Contradictions must be marked by severity:

* Severe contradiction.
* Minor difference.
* Unclear or pending verification.

## Gap Level

Each gap must be classified as P1, P2, or P3.

P1 means the gap may affect claim basis, defense validity, amount calculation, subject qualification, jurisdiction, or core evidence authenticity.

Any unresolved P1 blocks full A-series analysis even when the fact extraction score reaches 90.

## Required Output

The report must state:

* What is missing.
* Why it matters.
* How to obtain it.
* What happens if it is not supplemented.
