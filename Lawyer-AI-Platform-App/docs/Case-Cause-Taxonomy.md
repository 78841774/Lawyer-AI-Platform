# Case Cause Taxonomy

v3.6-D introduces a multi-level case cause taxonomy for Versioned Skill Training Packages.

Legal case causes are hierarchical. Training packages, experience package templates, and future Skill Registry records should not rely on a single flat `domain` field.

## 案由层级模型

Standard fields:

* `case_cause_level_1`
* `case_cause_level_2`
* `case_cause_level_3`
* `case_cause_level_4`
* `case_cause_path`
* `case_cause_code`
* `parent_case_cause_code`
* `display_name`
* `aliases`
* `jurisdiction`
* `status`

Example:

```json
{
  "case_cause_level_1": "civil",
  "case_cause_level_2": "contract_dispute",
  "case_cause_level_3": "sales_contract_dispute",
  "case_cause_level_4": "payment_dispute",
  "case_cause_path": [
    "civil",
    "contract_dispute",
    "sales_contract_dispute",
    "payment_dispute"
  ],
  "display_path": "民事 > 合同纠纷 > 买卖合同纠纷 > 货款支付争议"
}
```

## Current Registry

The taxonomy registry is:

* `/Users/wazhen/Lawyer-AI-Platform/Lawyer-AI-Platform-App/backend/case_cause_taxonomy/registry.json`

Current minimal chain:

| level | code | display |
| ---: | --- | --- |
| 1 | `civil` | 民事 |
| 2 | `contract_dispute` | 合同纠纷 |
| 3 | `sales_contract_dispute` | 买卖合同纠纷 |
| 4 | `payment_dispute` | 货款支付争议 |

## 训练包继承规则

Loading order:

1. `civil_base`
2. `contract_dispute_base`
3. `sales_contract_dispute`
4. `payment_dispute`
5. case-specific runtime context

Rules:

* Parent packages provide general foundations.
* Child packages override or supplement parent rules.
* Child packages must not silently delete parent safety rules.
* When rules with the same name conflict, the more specific case cause rule wins.
* `human_review` and `legal_review_safety` rules cannot be disabled by child packages.

## v3.6-D Package Mapping

| package | case cause | inheritance |
| --- | --- | --- |
| `civil_base@v1.0.0` | `civil` | `civil_base@v1.0.0` |
| `contract_dispute_combined@v1.0.0` | `contract_dispute` | `civil_base@v1.0.0` → `contract_dispute_combined@v1.0.0` |
| `sales_contract_dispute@v1.0.0` | `sales_contract_dispute` | `civil_base@v1.0.0` → `contract_dispute_combined@v1.0.0` → `sales_contract_dispute@v1.0.0` |
| `sales_contract_payment_dispute@v1.0.0` | `payment_dispute` | `civil_base@v1.0.0` → `contract_dispute_combined@v1.0.0` → `sales_contract_dispute@v1.0.0` → `sales_contract_payment_dispute@v1.0.0` |

## Readonly API

```bash
GET /case-cause-taxonomy
GET /case-cause-taxonomy/{case_cause_code}
GET /case-cause-taxonomy/{case_cause_code}/ancestors
GET /case-cause-taxonomy/{case_cause_code}/children
GET /versioned-skill-training-packages/by-case-cause/{case_cause_code}
```

The API is readonly and does not affect `/cases`, Skill Training, Experience Packages, or Skill Registry state.
