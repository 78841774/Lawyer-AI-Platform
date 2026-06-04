# case-analysis-pro-v3 Legal Analysis Chain Rules

Asset status: v3.6-C cleaned runtime rule candidate.

Source basis:

* Legacy Skill: `/Users/wazhen/.codex/skills/case-analysis-pro-v3/SKILL.md`
* A10 template: `/Users/wazhen/.codex/skills/case-analysis-pro-v3/references/a10-structure-template.md`
* Lawyer output standards: `/Users/wazhen/.codex/skills/case-analysis-pro-v3/references/lawyer-output-standards.md`
* Depth standards: `/Users/wazhen/.codex/skills/case-analysis-pro-v3/references/depth-standards.md`
* Admission gates: `/Users/wazhen/.codex/skills/case-analysis-pro-v3/references/admission-gates.md`
* Scoring rules: `/Users/wazhen/.codex/skills/case-analysis-pro-v3/references/scoring.md`

This asset is a read-only reshaping of old Skill text. It is not a new Skill, not a training run, and not a Skill Registry publication.

## Source Priority

1. Old `SKILL.md` controls the E1, 00, A1-A13, E chain.
2. `references/a10-structure-template.md` controls the A10 skeleton.
3. `references/lawyer-output-standards.md`, `references/depth-standards.md`, `references/admission-gates.md`, and `references/scoring.md` control quality gates.
4. Do not rewrite the A-series from memory, shorthand, or a generic legal workflow.

## Core Rule

The workflow must follow the old E1, 00, A1-A13, E deep analysis chain.

Each file is independent, deepened step by step, and controlled by its own scoring gate. Do not merge fact extraction, statute lists, case retrieval, pleadings, advocacy, and closing materials into one combined report.

## Precondition Gate

Full A-series output can start only after Step0 fact extraction passes the old Skill gate:

* `事实提炼报告.md` exists.
* `材料流转分析报告.md` exists.
* Fact extraction score is at least 90.
* No unresolved P1 item remains.
* Core amounts have completed three-round verification.
* Case parties and agency position are clear.
* OCR and judgment-document risks that affect claims, liability, amount, jurisdiction, res judicata, or enforcement have been reviewed.

If the gate fails, output only preliminary legal judgment, evidence supplementation tasks, and legal search tasks. Do not produce A6, A7, A12, or the full A-series package.

## Full Delivery Package

| step | file | boundary |
| --- | --- | --- |
| Step0 | `事实提炼报告.md` | Fact extraction only; no final legal conclusion |
| Step0 | `材料流转分析报告.md` | Material flow and source reliability only |
| E1 | `接案评估卡.md` | Intake evaluation, risk ranking, engagement recommendation |
| 00 | `产出总览.md` | Output index, process overview, conclusion preview |
| A1 | `案由分析.md` | Cause of action, jurisdiction, subject qualification, initial claim direction |
| A2 | `法规清单.md` | Current legal basis and application notes |
| A3 | `类案检索.md` | Case retrieval, case numbers, relevance, favorable and unfavorable patterns |
| A4 | `请求权 / 抗辩权基础.md` | Claim or defense basis, legal elements, fact mapping, burden of proof |
| A5 | `举证策略.md` | Evidence grouping, proof route, gap list, court presentation strategy |
| A6 | `诉状 / 答辩状.md` | Court-ready complaint, arbitration application, answer, or defense document |
| A7 | `诉求量化 / 反请求.md` | Claim amount, formulas, counterclaim feasibility, settlement leverage |
| A8 | `证据清单.md` | Formal evidence list with number, name, source, purpose, page reference |
| A9 | `质证意见.md` | Cross-examination opinions on opposing evidence |
| A10 | `争议焦点法律深化分析.md` | Disputed-issue legal deep analysis using the mandatory skeleton below |
| A11 | `庭审提纲.md` | Hearing outline, attack-defense pairs, questions, evidence presentation |
| A12 | `代理词.md` | Court-facing advocacy brief by disputed issue |
| A13 | `结案报告 / 结案框架.md` | Client-facing closing report or closing framework |
| E | `执行评估.md` | Enforcement feasibility, preservation, settlement, recovery cost |

## A-Series Boundaries

* A1 defines cause of action, jurisdiction, parties, and initial risk.
* A2 lists statutes and application notes; it does not become an advocacy brief.
* A3 records case retrieval and裁判规律; it does not replace disputed-issue analysis.
* A4 maps legal elements to facts and evidence; it does not draft pleadings.
* A5 designs proof strategy; it does not become a formal evidence list.
* A6 carries complaint, arbitration application, answer, and defense drafting.
* A7 handles quantified claims, formulas, support probability, reduction risk, and settlement floor.
* A8 is a formal evidence list and should follow A5 grouping.
* A9 addresses opposing evidence only.
* A10 carries disputed-issue legal deep analysis.
* A11 converts focus issues into hearing operations.
* A12 carries the advocacy brief.
* A13 carries the closing report or closing framework.
* E1 and E are internal strategy materials when appropriate.

## A10 Mandatory Rule

A10 correct name:

`A10 争议焦点法律深化分析`

This step is responsible for deep legal analysis of disputed issues.

It does not produce complaints, answers, advocacy briefs, closing reports, or their drafting formats.

Those output categories belong to A6, A12, and A13.

A10 may provide the legal-analysis foundation for later A11, A12, and A13 outputs.

It must cite or inherit:

* A3 case retrieval results.
* A4 claim or defense basis.
* A5 proof strategy when evidence strategy affects the disputed issue.
* A7 amount analysis when a disputed issue affects claim amount.

It must not repeat A3 case retrieval as a raw case list. It must convert A3 results into裁判倾向规律 and litigation strategy.

## A10 Five-Module Skeleton

A10 must use the five-module skeleton from `references/a10-structure-template.md`.

### 模块一：焦点 → 法律问题提炼

For each disputed focus `F{n}`, include:

* Focus title.
* Relevant facts, clauses, evidence, or prior-step conclusion.
* Conversion from case focus to legal questions.
* Applicable legal basis.
* Core jurisprudential conflict.
* Three-layer claim or defense route:
  * 主位请求 / 抗辩.
  * 备位请求 / 抗辩.
  * 兜底方案.

Required table:

| 序号 | 法律问题 | 法律依据 | 核心法理矛盾 |
| --- | --- | --- | --- |
| Q{n}-1 | To be filled per case | To be filled per case | To be filled per case |

Required route table:

| 防线层级 | 策略 | 法律依据 | 风险等级 |
| --- | --- | --- | --- |
| 主位 | To be filled per case | To be filled per case | 高/中/低 |
| 备位 | To be filled per case | To be filled per case | 高/中/低 |
| 兜底 | To be filled per case | To be filled per case | 高/中/低 |

### 模块二：实务观点 —— 裁判倾向规律

For each focus, synthesize practical judicial tendencies from A3.

Required table:

| 案例 | 案号 | 裁判要点 | 关联焦点 | 关联度 | 对我方 |
| --- | --- | --- | --- | --- | --- |
| To be filled per case | To be filled per case | To be filled per case | F{n} | 高/中/低 | 有利/不利 |

### 模块三：理论观点

For each focus, identify the relevant legal theory or doctrinal dispute.

Required table:

| 维度 | 通说观点 | 争议观点 |
| --- | --- | --- |
| To be filled per case | To be filled per case | To be filled per case |

### 模块四：实务与理论对比运用策略

Compare court practice and theory, then convert the comparison into litigation strategy.

Required table:

| 对比维度 | 实务倾向 | 理论通说 | 差异分析 | 我方策略 |
| --- | --- | --- | --- | --- |
| To be filled per case | To be filled per case | To be filled per case | To be filled per case | To be filled per case |

### 模块五：综合策略结论（含法官审查清单）

End with a strategy conclusion and judge-oriented review checklist.

Required conclusion table:

| 焦点 | 裁判预测 | 风险等级 | 最优策略 |
| --- | --- | --- | --- |
| F1 | To be filled per case | 高/中/低 | To be filled per case |

Required judge review checklist:

| 审查项 | 法官可能关注的问题 | 我方回应要点 | 证据支撑 | 风险 |
| --- | --- | --- | --- | --- |
| To be filled per case | To be filled per case | To be filled per case | To be filled per case | 高/中/低 |

Required overall assessment:

* 第一层防线: core route and probability.
* 第二层防线: fallback route and probability.
* 第三层防线: worst-case route, amount cap, or settlement floor.

## A10 Focus Scoring Card

| 焦点 | 得分 | 论证强度 | 证据支撑 | 法律依据 | 主要扣分项 |
| --- | ---: | --- | --- | --- | --- |
| F1 | /25 | To be filled | To be filled | To be filled | To be filled |
| F2 | /25 | To be filled | To be filled | To be filled | To be filled |
| F3 | /25 | To be filled | To be filled | To be filled | To be filled |
| F4 | /25 | To be filled | To be filled | To be filled | To be filled |
| 合计 | /100 | To be filled | To be filled | To be filled | To be filled |

## A10 Depth Self-Assessment Card

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 5模块结构完整 | 是/否 | To be filled |
| 每焦点三层防线 | 是/否 | To be filled |
| 类案联动不少于5件 | 是/否 | To be filled |
| 实务观点与理论观点均已覆盖 | 是/否 | To be filled |
| 实务与理论对比形成策略 | 是/否 | To be filled |
| 法官审查清单完整 | 是/否 | To be filled |
| 焦点评分卡完整 | 是/否 | To be filled |
| 未错误归类第十步 | 是/否 | To be filled |

## Drafting Output Placement Rule

Drafting outputs are placed only in:

* A6 `诉状 / 答辩状.md`.
* A12 `代理词.md`.
* A13 `结案报告 / 结案框架.md`.

The disputed-issue analysis step may support later drafting outputs, but it does not replace them.

## Prohibited Simplification

The prohibited shortcut is the generic four-part mapping that turns the old A-series into intake, facts, legal relation, and drafting format.

The correct structure is always the old E1, 00, A1-A13, E delivery chain defined above.
