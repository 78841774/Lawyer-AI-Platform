# A1–A13 Legacy Skill Structure Audit Report

- Generated at: 2026-06-04 12:51:28
- Project: `/Users/wazhen/Lawyer-AI-Platform`
- Scope: docs / changelogs / backend / frontend / training samples / templates

## 1. Expected A-Series Structure

| Code | Expected Meaning |
|---|---|
| A1 | 案由分析 |
| A2 | 法规清单 |
| A3 | 类案检索 |
| A4 | 请求权 / 抗辩权 |
| A5 | 举证策略 |
| A6 | 诉状 / 答辩状 |
| A7 | 诉求量化 / 反请求 |
| A8 | 证据清单 |
| A9 | 质证意见 |
| A10 | 争议焦点法律深化分析 |
| A11 | 庭审提纲 |
| A12 | 代理词 |
| A13 | 结案报告 / 结案框架 |

## 2. Presence Check

| Code | Expected Terms | Status | Hit Count | Sample Locations |
|---|---|---|---:|---|
| A1 | 案由分析 | OK | 8 | `09-Change-Logs/v3.6.md:199` * A1: 案由分析<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:12` * A1: 案由分析<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:51` \| A1 \| `案由分析.md` \| Cause of action, jurisdiction, subject qualification, initial claim direction \|<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/report_templates/legal_analysis_report_template.md:12` * A1: 案由分析<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:51` \| A1 \| `案由分析.md` \| Cause of action, jurisdiction, subject qualification, initial claim direction \| |
| A2 | 法规清单 | OK | 14 | `09-Change-Logs/v3.6.md:200` * A2: 法规清单<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:13` * A2: 法规清单<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:52` \| A2 \| `法规清单.md` \| Current legal basis and application notes \|<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/report_templates/legal_analysis_report_template.md:13` * A2: 法规清单<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:52` \| A2 \| `法规清单.md` \| Current legal basis and application notes \| |
| A3 | 类案检索 | OK | 15 | `09-Change-Logs/v3.6.md:201` * A3: 类案检索<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:14` * A3: 类案检索<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:53` \| A3 \| `类案检索.md` \| Case retrieval, case numbers, relevance, favorable and unfavorable patterns \|<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/report_templates/legal_analysis_report_template.md:14` * A3: 类案检索<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:53` \| A3 \| `类案检索.md` \| Case retrieval, case numbers, relevance, favorable and unfavorable patterns \| |
| A4 | 请求权 / 抗辩权 | OK | 23 | `09-Change-Logs/v3.6.md:202` * A4: 请求权 / 抗辩权基础<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:15` * A4: 请求权 / 抗辩权基础<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:54` \| A4 \| `请求权 / 抗辩权基础.md` \| Claim or defense basis, legal elements, fact mapping, burden of proof \|<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/claim_defense_rules.md:9` A4 is `请求权 / 抗辩权基础`.<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/report_templates/legal_analysis_report_template.md:15` * A4: 请求权 / 抗辩权基础 |
| A5 | 举证策略 | OK | 9 | `09-Change-Logs/v3.6.md:203` * A5: 举证策略<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:16` * A5: 举证策略<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:55` \| A5 \| `举证策略.md` \| Evidence grouping, proof route, gap list, court presentation strategy \|<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/report_templates/legal_analysis_report_template.md:16` * A5: 举证策略<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:55` \| A5 \| `举证策略.md` \| Evidence grouping, proof route, gap list, court presentation strategy \| |
| A6 | 诉状 / 答辩状 | OK | 70 | `09-Change-Logs/v3.6.md:204` * A6: 诉状 / 答辩状<br>`09-Change-Logs/v3.6.md:224` Drafting outputs belong to A6 `诉状 / 答辩状`, A12 `代理词`, and A13 `结案报告 / 结案框架`.<br>`09-Change-Logs/v3.6.md:232` 5. 诉状、答辩状、代理词、结案报告等输出不得归入第十步。<br>`08-Skill-Training/Example-Contract-Dispute-Skill.md:42` - 起诉状或答辩状<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:17` * A6: 诉状 / 答辩状 |
| A7 | 诉求量化 / 反请求 | OK | 16 | `09-Change-Logs/v3.6.md:205` * A7: 诉求量化 / 反请求<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:18` * A7: 诉求量化 / 反请求<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:57` \| A7 \| `诉求量化 / 反请求.md` \| Claim amount, formulas, counterclaim feasibility, settlement leverage \|<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/report_templates/legal_analysis_report_template.md:18` * A7: 诉求量化 / 反请求<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:57` \| A7 \| `诉求量化 / 反请求.md` \| Claim amount, formulas, counterclaim feasibility, settlement leverage \| |
| A8 | 证据清单 | OK | 9 | `09-Change-Logs/v3.6.md:206` * A8: 证据清单<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:19` * A8: 证据清单<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:58` \| A8 \| `证据清单.md` \| Formal evidence list with number, name, source, purpose, page reference \|<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/report_templates/legal_analysis_report_template.md:19` * A8: 证据清单<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:58` \| A8 \| `证据清单.md` \| Formal evidence list with number, name, source, purpose, page reference \| |
| A9 | 质证意见 | OK | 8 | `09-Change-Logs/v3.6.md:207` * A9: 质证意见<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:20` * A9: 质证意见<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:59` \| A9 \| `质证意见.md` \| Cross-examination opinions on opposing evidence \|<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/report_templates/legal_analysis_report_template.md:20` * A9: 质证意见<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:59` \| A9 \| `质证意见.md` \| Cross-examination opinions on opposing evidence \| |
| A10 | 争议焦点法律深化分析 | OK | 23 | `09-Change-Logs/v3.6.md:52` * A10 remains `争议焦点法律深化分析`.<br>`09-Change-Logs/v3.6.md:96` The run foundation does not modify legacy assets or versioned package assets. A10 remains `争议焦点法律深化分析` with the five-mod<br>`09-Change-Logs/v3.6.md:162` `case-analysis-pro-v3@v1.0.0` keeps A10 as `争议焦点法律深化分析`.<br>`09-Change-Logs/v3.6.md:208` * A10: 争议焦点法律深化分析<br>`09-Change-Logs/v3.6.md:214` A10 is `争议焦点法律深化分析` and must include: |
| A11 | 庭审提纲 | OK | 9 | `09-Change-Logs/v3.6.md:209` * A11: 庭审提纲<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:22` * A11: 庭审提纲<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:61` \| A11 \| `庭审提纲.md` \| Hearing outline, attack-defense pairs, questions, evidence presentation \|<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/report_templates/legal_analysis_report_template.md:22` * A11: 庭审提纲<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:61` \| A11 \| `庭审提纲.md` \| Hearing outline, attack-defense pairs, questions, evidence presentation \| |
| A12 | 代理词 | OK | 20 | `09-Change-Logs/v3.6.md:210` * A12: 代理词<br>`09-Change-Logs/v3.6.md:224` Drafting outputs belong to A6 `诉状 / 答辩状`, A12 `代理词`, and A13 `结案报告 / 结案框架`.<br>`09-Change-Logs/v3.6.md:232` 5. 诉状、答辩状、代理词、结案报告等输出不得归入第十步。<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:23` * A12: 代理词<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:62` \| A12 \| `代理词.md` \| Court-facing advocacy brief by disputed issue \| |
| A13 | 结案报告 / 结案框架 | OK | 27 | `09-Change-Logs/v3.6.md:211` * A13: 结案报告 / 结案框架<br>`09-Change-Logs/v3.6.md:224` Drafting outputs belong to A6 `诉状 / 答辩状`, A12 `代理词`, and A13 `结案报告 / 结案框架`.<br>`09-Change-Logs/v3.6.md:232` 5. 诉状、答辩状、代理词、结案报告等输出不得归入第十步。<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:24` * A13: 结案报告 / 结案框架<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:63` \| A13 \| `结案报告 / 结案框架.md` \| Client-facing closing report or closing framework \| |

## 3. Forbidden A10 Misclassification Check

A10 must remain: `争议焦点法律深化分析`.

| Pattern | Status | Hit Count | Sample Locations |
|---|---|---:|---|
| `A10.*诉状` | OK | 0 |  |
| `A10.*答辩状` | OK | 0 |  |
| `A10.*代理词` | REVIEW_REQUIRED | 1 | `Lawyer-AI-Platform-App/backend/scripts/analyze_legacy_skills.py:527` if any(keyword in text for keyword in ["报告模板", "A10", "代理词", "事实提炼报告"]): |
| `A10.*结案报告` | OK | 0 |  |
| `A10.*文书起草` | OK | 0 |  |
| `A10.*文书结构` | OK | 0 |  |
| `第十步.*诉状` | OK | 0 |  |
| `第十步.*答辩状` | OK | 0 |  |
| `第十步.*代理词` | OK | 0 |  |
| `第十步.*结案报告` | OK | 0 |  |
| `第十步.*文书起草` | OK | 0 |  |
| `第十步.*文书结构` | OK | 0 |  |

## 4. Suspicious Cross-Classification Check

| Pattern | Status | Hit Count | Sample Locations |
|---|---|---:|---|
| `A1.*诉状` | OK | 0 |  |
| `A1.*代理词` | REVIEW_REQUIRED | 14 | `09-Change-Logs/v3.6.md:210` * A12: 代理词<br>`09-Change-Logs/v3.6.md:224` Drafting outputs belong to A6 `诉状 / 答辩状`, A12 `代理词`, and A13 `结案报告 / 结案框架`.<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/report_templates/legal_analysis_report_template.md:23` * A12: 代理词<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:62` \| A12 \| `代理词.md` \| Court-facing advocacy brief by disputed issue \|<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:218` * A12 `代理词.md`.<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/report_templates/legal_analysis_report_template.md:23` * A12: 代理词<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:62` \| A12 \| `代理词.md` \| Court-facing advocacy brief by disputed issue \|<br>`Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/runtime_rules/legal_analysis_chain_rules.md:218` * A12 `代理词.md`.<br>`Lawyer-AI-Platform-App/backend/scripts/analyze_legacy_skills.py:527` if any(keyword in text for keyword in ["报告模板", "A10", "代理词", "事实提炼报告"]):<br>`Lawyer-AI-Platform-App/backend/legacy_skill_assets/registry.json:126` "A12": "代理词", |
| `A2.*诉状` | OK | 0 |  |
| `A2.*代理词` | OK | 0 |  |
| `A3.*诉状` | OK | 0 |  |
| `A3.*代理词` | OK | 0 |  |
| `A4.*诉状` | OK | 0 |  |
| `A4.*代理词` | OK | 0 |  |
| `A5.*诉状` | OK | 0 |  |
| `A5.*代理词` | OK | 0 |  |
| `A6.*争议焦点法律深化分析` | OK | 0 |  |
| `A7.*争议焦点法律深化分析` | OK | 0 |  |
| `A8.*争议焦点法律深化分析` | OK | 0 |  |
| `A9.*争议焦点法律深化分析` | OK | 0 |  |
| `A11.*争议焦点法律深化分析` | OK | 0 |  |
| `A12.*争议焦点法律深化分析` | OK | 0 |  |
| `A13.*争议焦点法律深化分析` | OK | 0 |  |

## 5. JSON Parse Check

| JSON File | Status | Error |
|---|---|---|
| `Lawyer-AI-Platform-App/backend/controlled_skill_registry_publish/registry.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/versioned_skill_training_runs/registry.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/case_cause_taxonomy/registry.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/registry.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-fact-extractor-v3/v1.0.0/metadata.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/sales_contract_payment_dispute/v1.0.0/metadata.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/case-analysis-pro-v3/v1.0.0/metadata.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/civil_base/v1.0.0/metadata.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/sales_contract_dispute/v1.0.0/metadata.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/metadata.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/contract_dispute_combined/v1.0.0/experience_package_templates/experience_package_template.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/legacy_skill_assets/registry.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/legacy_skill_assets/experience_package_templates/contract_dispute_v1/experience_package_template.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/experience_package_build/registry.json` | OK |  |
| `Lawyer-AI-Platform-App/backend/reports/legacy_skill_analysis.json` | OK |  |
| `Lawyer-AI-Platform-App/frontend/package-lock.json` | OK |  |
| `Lawyer-AI-Platform-App/frontend/package.json` | OK |  |
| `Lawyer-AI-Platform-App/frontend/tsconfig.json` | OK |  |

## 6. Key Registry / Package Files

| Path | Exists | Notes |
|---|---|---|
| `Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/registry.json` | YES |  |
| `Lawyer-AI-Platform-App/backend/versioned_skill_training_runs/registry.json` | YES |  |
| `Lawyer-AI-Platform-App/backend/experience_package_build/registry.json` | YES |  |
| `Lawyer-AI-Platform-App/backend/controlled_skill_registry_publish/registry.json` | YES |  |
| `Lawyer-AI-Platform-App/backend/case_cause_taxonomy/registry.json` | YES |  |
| `docs/Skill-Factory-Foundation-v3.6.md` | NO |  |
| `09-Change-Logs/v3.6.md` | YES |  |

## 7. Summary

- Overall: **REVIEW_REQUIRED**
- Missing A-series items: `None`
- Forbidden A10 misclassification hits: `1`
- Suspicious cross-classification hits: `14`
- JSON parse errors: `0`

## 8. Required Manual Interpretation

- Some hits may appear in historical changelog text explaining old mistakes. Those are acceptable if they clearly describe past cleanup and not current runtime rules.
- Any current rule, runtime package, registry, prompt, or frontend label that maps A10 to pleadings / agency statement / closing report must be corrected.
- A6 may contain `诉状 / 答辩状`, A12 may contain `代理词`, and A13 may contain `结案报告 / 结案框架`; those are expected.
- A10 must remain `争议焦点法律深化分析`.
