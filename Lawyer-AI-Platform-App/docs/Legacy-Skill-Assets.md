# Legacy Skill Assets

v3.6-C begins reshaping audited legacy Skill content into explicit, reviewable assets.

This is still analysis-only. These assets are not imported into Skill Registry, not used for automatic training, and not published as Experience Packages.

## Asset Registry

The local registry file is:

* `/Users/wazhen/Lawyer-AI-Platform/Lawyer-AI-Platform-App/backend/legacy_skill_assets/registry.json`

Current registered asset:

| asset_id | skill_family | asset_type | status |
| --- | --- | --- | --- |
| `case-analysis-pro-v3.legal_analysis_chain_rules` | `case-analysis-pro-v3` | runtime rules | source-aligned |

v3.6-D extends the registry with fact extraction, legal analysis, and combined contract dispute assets. These assets are readonly sources for versioned training packages.

v3.6-D also adds Case Cause Taxonomy metadata so experience package templates and training packages can be archived by legal case-cause tree rather than a flat domain.

## v3.6-D Versioned Training Packages

Legacy assets are now packaged into:

* `case-fact-extractor-v3@v1.0.0`
* `case-analysis-pro-v3@v1.0.0`
* `contract_dispute_combined@v1.0.0`

Each package has:

* `metadata.json`
* `README.md`
* copied readonly source assets by type
* status `prepared_for_training`
* `auto_train_enabled=false`
* `auto_publish_enabled=false`

These packages do not overwrite `skill_001` or `skill_002`.

## 案由树归档

The contract dispute experience package template now carries:

* `case_cause_code`
* `case_cause_path`
* `case_cause_display_path`
* `parent_package_ids`
* `inheritance_order`
* `applicable_case_causes`

Current applicable case causes:

* `contract_dispute`
* `sales_contract_dispute`
* `payment_dispute`

## case-analysis-pro-v3 Chain Correction

The `case-analysis-pro-v3` asset must follow the old Skill source exactly:

* Step0: `事实提炼报告.md`, `材料流转分析报告.md`
* E1: `接案评估卡.md`
* 00: `产出总览.md`
* A1: 案由分析
* A2: 法规清单
* A3: 类案检索
* A4: 请求权 / 抗辩权基础
* A5: 举证策略
* A6: 诉状 / 答辩状
* A7: 诉求量化 / 反请求
* A8: 证据清单
* A9: 质证意见
* A10: 争议焦点法律深化分析
* A11: 庭审提纲
* A12: 代理词
* A13: 结案报告 / 结案框架
* E: `执行评估.md`

Do not use the earlier simplified four-part mapping that collapsed the old A-series into intake, facts, legal relation, and drafting format.

## A10 Rule

A10 is `争议焦点法律深化分析` and must use the source template from `references/a10-structure-template.md`.

Required A10 skeleton:

1. 模块一：焦点 → 法律问题提炼
2. 模块二：实务观点 —— 裁判倾向规律
3. 模块三：理论观点
4. 模块四：实务与理论对比运用策略
5. 模块五：综合策略结论（含法官审查清单）
6. 焦点评分卡
7. 深度自评卡

Drafting outputs belong to:

* A6 `诉状 / 答辩状`
* A12 `代理词`
* A13 `结案报告 / 结案框架`

## Runtime Rule Asset

The reshaped rule file is:

* `/Users/wazhen/Lawyer-AI-Platform/Lawyer-AI-Platform-App/backend/legacy_skill_assets/runtime_rules/case-analysis-pro-v3/legal_analysis_chain_rules.md`

It preserves:

* E1, 00, A1-A13, E delivery boundaries.
* Full A-series file names and step responsibilities.
* A10 five-module skeleton.
* A10 focus scoring card.
* A10 depth self-assessment card.
* A6/A12/A13 placement for drafting outputs.

## Legacy Skill 清洗规则

1. 旧 Skill 原文优先。
2. `references` 模板优先。
3. 不得凭记忆或通用法律流程重写 A 系列。
4. A10 必须保留为 `争议焦点法律深化分析`。
5. 诉状、答辩状、代理词、结案报告等输出不得归入第十步。
6. 所有清洗必须记录在 v3.6 changelog。

## Non-Goals

v3.6-C does not:

* Execute old scripts.
* Call any LLM.
* Train a Skill.
* Import the asset registry into the product database.
* Publish an Experience Package.

v3.6-D also does not train, publish, or execute legacy scripts. It only prepares versioned readonly package inputs for a later training run.
