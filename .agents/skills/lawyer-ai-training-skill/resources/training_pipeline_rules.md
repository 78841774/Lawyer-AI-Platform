# Training Pipeline Rules

This resource describes the controlled Lawyer-AI-Platform training chain for Codex development tasks.

## Pipeline

unredacted raw materials
-> controlled raw training material zone
-> OCR / document parsing
-> legal retrieval
-> parse quality gate
-> rule alignment
-> redacted experience package
-> training dataset
-> Codex training skill spec
-> dry-run/internal training
-> trained artifact
-> lawyer review
-> controlled runtime loading

## Rules

- Unredacted inputs may exist only in the controlled raw training material zone.
- OCR, document parsing, legal retrieval, rule alignment, and parse quality gate must finish before experience package output is treated as ready.
- Downstream outputs must be redacted, abstracted, metadata-only, audit-required, and source-trace-required.
- Open or unresolved cases must not automatically enter training.
- Training output must not automatically publish Skills or replace runtime packages.
