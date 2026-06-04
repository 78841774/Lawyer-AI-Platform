# case-fact-extractor-v3 Material Context Rules

Source basis: `/Users/wazhen/.codex/skills/case-fact-extractor-v3/SKILL.md`

Status: readonly legacy asset prepared for versioned training packages.

## Scope

The fact extractor must read case materials as a structured evidence folder, not as isolated search hits.

Required intake context:

* Full folder tree.
* File name.
* Relative path.
* File type.
* Source side inferred from directory context when available.
* Duplicate status.
* Read status.
* OCR or visual verification status.
* Material reliability and admissibility notes.

## Mandatory Outputs

The extractor must produce two independent files:

* `事实提炼报告.md`
* `材料流转分析报告.md`

The first file extracts facts. The second file tracks material movement, source reliability, duplicates, versions, original status, electronic evidence preservation, timestamp, notarization, screen recording, and pre-hearing correction tasks.

## Prohibited Shortcut

Do not use full-text search results as a substitute for folder traversal.

Every non-duplicate core file must be read and represented in the material list.
