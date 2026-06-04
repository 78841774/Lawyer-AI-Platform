# Skill Factory

Skill Factory is the future operating layer for turning reviewed casework data into reusable Skills, Experience Packages, and evaluation rubrics.

## Current Status

As of v3.6-C, Skill Factory remains in analysis and asset-reshape mode.

Current local audit results:

* Existing legacy Skill assets analyzed: 17.
* Existing SkillOpt dataset files analyzed: 19.
* Existing SkillOpt dataset items analyzed: 96.
* Existing SkillOpt output runs analyzed: 14.
* Legacy runtime rule assets reshaped: 1.
* Skill Training main chain unchanged.

No new Skill was created.

No Experience Package was imported.

No Skill Registry record was published.

## v3.6-C Asset Reshape

v3.6-C adds a source-aligned runtime rule asset for `case-analysis-pro-v3`.

The asset preserves the old Skill's E1, 00, A1-A13, E chain. The A-series must be interpreted as:

| step | meaning |
| --- | --- |
| E1 | 接案评估卡 |
| 00 | 产出总览 |
| A1 | 案由分析 |
| A2 | 法规清单 |
| A3 | 类案检索 |
| A4 | 请求权 / 抗辩权基础 |
| A5 | 举证策略 |
| A6 | 诉状 / 答辩状 |
| A7 | 诉求量化 / 反请求 |
| A8 | 证据清单 |
| A9 | 质证意见 |
| A10 | 争议焦点法律深化分析 |
| A11 | 庭审提纲 |
| A12 | 代理词 |
| A13 | 结案报告 / 结案框架 |
| E | 执行评估 |

A10 must use the five-module disputed-issue analysis skeleton from the legacy `references/a10-structure-template.md`:

* 模块一：焦点 → 法律问题提炼.
* 模块二：实务观点 —— 裁判倾向规律.
* 模块三：理论观点.
* 模块四：实务与理论对比运用策略.
* 模块五：综合策略结论（含法官审查清单）.
* 焦点评分卡.
* 深度自评卡.

Drafting outputs belong to A6, A12, and A13.

## Legacy Skill 清洗规则

1. 旧 Skill 原文优先。
2. `references` 模板优先。
3. 不得凭记忆或通用法律流程重写 A 系列。
4. A10 必须保留为 `争议焦点法律深化分析`。
5. 诉状、答辩状、代理词、结案报告等输出不得归入第十步。
6. 所有清洗必须记录在 v3.6 changelog。

## Factory Inputs

Future Skill Factory inputs should come from reviewed packages, not raw legacy folders.

Input package categories:

* Dataset packages.
* Runtime rule packages.
* Prompt template packages.
* Report template packages.
* Evaluation rubric packages.
* Read-only reference packages.

## Factory Gates

Before an input can be used for training or publication, it must pass:

* Privacy review.
* Human curation review.
* Schema validation.
* Evaluation rubric completeness check.
* Source reference check.
* Legal safety review.

## v3.6-C Boundary

v3.6-C only adds source-aligned legacy asset reshaping and documentation.

It intentionally avoids:

* Training.
* Registry import.
* Package publication.
* LLM calls.
* Legacy script execution.
* Frontend changes.
