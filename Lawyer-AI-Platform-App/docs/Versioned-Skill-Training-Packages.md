# Versioned Skill Training Packages

v3.6-D packages readonly legacy Skill assets into versioned training inputs.

This stage does not train, publish, or overwrite any existing Skill.

## Current Packages

| training_package_id | source | status | next stage |
| --- | --- | --- | --- |
| `civil_base@v1.0.0` | case cause taxonomy | `prepared_for_training` | v3.6-E training run |
| `case-fact-extractor-v3@v1.0.0` | `case-fact-extractor-v3` legacy assets | `prepared_for_training` | v3.6-E training run |
| `case-analysis-pro-v3@v1.0.0` | `case-analysis-pro-v3` legacy assets | `prepared_for_training` | v3.6-E training run |
| `contract_dispute_combined@v1.0.0` | fact extractor + legal analysis packages | `prepared_for_training` | v3.6-E training run |
| `sales_contract_dispute@v1.0.0` | case cause taxonomy | `prepared_for_training` | v3.6-E training run |
| `sales_contract_payment_dispute@v1.0.0` | case cause taxonomy | `prepared_for_training` | v3.6-E training run |

## Location

Training packages live under:

* `/Users/wazhen/Lawyer-AI-Platform/Lawyer-AI-Platform-App/backend/versioned_skill_training_packages`

The registry file is:

* `/Users/wazhen/Lawyer-AI-Platform/Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/registry.json`

## Readonly API

v3.6-D adds readonly endpoints:

```bash
GET /versioned-skill-training-packages
GET /versioned-skill-training-packages/{package_id}
GET /versioned-skill-training-packages/{package_id}/files
```

These endpoints only read package metadata, README content, and relative file lists.

They do not:

* Execute package files.
* Execute old scripts.
* Call LLM providers.
* Start training.
* Publish Skills.
* Modify the existing Skill Registry.
* Expose local absolute package paths.

v3.6-E adds a separate mock run foundation:

```bash
GET /versioned-skill-training-runs
GET /versioned-skill-training-runs/{run_id}
POST /versioned-skill-training-runs/mock
```

The mock run layer reads package metadata and taxonomy metadata, but it does not call LLM providers, train, publish, or create formal Experience Packages.

## Frontend

The frontend page is:

* `/versioned-training-packages`

The detail page is:

* `/versioned-training-packages/{packageId}`

The page displays:

* training package ID
* display name
* domain
* version
* status
* source assets or source packages
* training scope
* human review requirement
* no-auto-training and no-auto-publish status
* README content
* package file list
* case cause path
* parent packages
* inheritance order
* applicable case cause
* safety rule override policy

## Case Cause Taxonomy

v3.6-D adds multi-level case cause metadata to every package:

* `case_cause_level_1`
* `case_cause_level_2`
* `case_cause_level_3`
* `case_cause_level_4`
* `case_cause_code`
* `case_cause_path`
* `case_cause_display_path`
* `parent_package_ids`
* `inheritance_order`
* `rule_override_policy`

The current minimal taxonomy chain is:

`civil` → `contract_dispute` → `sales_contract_dispute` → `payment_dispute`

For `payment_dispute`, the complete package inheritance chain is:

`civil_base@v1.0.0` → `contract_dispute_combined@v1.0.0` → `sales_contract_dispute@v1.0.0` → `sales_contract_payment_dispute@v1.0.0`

Safety rules cannot be disabled by child packages.

## A10 Gate

`case-analysis-pro-v3@v1.0.0` preserves A10 as:

`A10 争议焦点法律深化分析`

The package must contain:

* 模块一：焦点 → 法律问题提炼
* 模块二：实务观点 —— 裁判倾向规律
* 模块三：理论观点
* 模块四：实务与理论对比运用策略
* 模块五：综合策略结论（含法官审查清单）
* 评分卡
* 深度自评卡

Drafting outputs remain in A6, A12, and A13.

## Safety Boundary

v3.6-D does not overwrite:

* `skill_001`
* `skill_002`

Future v3.6-E training output should create a new candidate Skill, such as `skill_003`, after human review and training-run approval.

v3.6-E currently creates mock training run metadata only. It does not create candidate Skills.
