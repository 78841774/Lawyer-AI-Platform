# case-fact-extractor-v3 Fact Extraction Prompt Template

Source basis: `case-fact-extractor-v3/SKILL.md`.

Status: readonly prompt template candidate.

## Instruction Skeleton

You are preparing a lawyer-grade fact extraction working paper.

Read the full material folder before extracting facts. Preserve file path, source side, material type, read status, OCR status, and duplicate status.

Produce two independent outputs:

1. `事实提炼报告.md`
2. `材料流转分析报告.md`

The fact report must include:

* case overview,
* full material list,
* party facts,
* contract and legal relationship facts,
* performance timeline,
* dispute timeline,
* amount audit,
* evidence-fact matrix,
* admissions and unfavorable facts,
* contradictions and P1/P2/P3 gaps,
* legal element mapping,
* court-usable excerpts,
* admission conclusion for full A-series analysis.

Do not produce final legal conclusions. Do not skip uncertain facts. Do not treat OCR-only amount data as final.
