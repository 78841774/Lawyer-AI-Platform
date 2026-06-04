# Versioned Skill Training Runs

v3.6-E adds the foundation for versioned Skill Training Runs.

This layer is intentionally mock-only. It verifies that a versioned training package can be selected, linked to a case cause taxonomy path, expanded through its package inheritance chain, and evaluated with placeholder scores without calling a real LLM or publishing any Skill.

## Purpose

Versioned Skill Training Runs sit after versioned training packages and before any future candidate Skill.

The run layer records:

* which `training_package_id` was selected
* which `case_cause_code` applies
* which parent packages are inherited
* whether an LLM was called
* whether real case material was used
* whether any Skill, Experience Package, or Skill Registry record was produced
* the safety flags required before any future real training stage

## Relationship To Training Packages

The mock runner reads:

* `backend/versioned_skill_training_packages/registry.json`
* `backend/case_cause_taxonomy/registry.json`

It does not modify:

* legacy Skill assets
* versioned training package assets
* `skill_001`
* `skill_002`
* Skill Registry records
* Experience Package records

## Relationship To Case Cause Taxonomy

Every run keeps both:

* `case_cause_code`
* `taxonomy_path`

For `payment_dispute`, the current taxonomy path is:

`civil` -> `contract_dispute` -> `sales_contract_dispute` -> `payment_dispute`

The package inheritance chain is:

`civil_base@v1.0.0` -> `contract_dispute_combined@v1.0.0` -> `sales_contract_dispute@v1.0.0` -> `sales_contract_payment_dispute@v1.0.0`

## Mock Training Boundary

v3.6-E mock runs are not real training.

They always keep:

* `llm_provider=mock`
* `llm_called=false`
* `real_case_material_used=false`
* `legacy_asset_modified=false`
* `skill_candidate_created=false`
* `experience_package_created=false`
* `skill_registry_published=false`
* `requires_human_review=true`
* `auto_train_enabled=false`
* `auto_publish_enabled=false`
* `child_package_cannot_disable_safety_rules=true`

Mock evaluation scores are placeholders set to `0.0`.

## Data Structure

The registry lives at:

* `/Users/wazhen/Lawyer-AI-Platform/Lawyer-AI-Platform-App/backend/versioned_skill_training_runs/registry.json`

Each run includes:

```json
{
  "run_id": "training_run_payment_dispute_mock_001",
  "package_id": "sales_contract_payment_dispute@v1.0.0",
  "case_cause_code": "payment_dispute",
  "status": "completed_mock",
  "runner": "mock_training_runner",
  "llm_provider": "mock",
  "llm_called": false,
  "inheritance_chain": [],
  "taxonomy_path": [],
  "inputs": {},
  "outputs": {},
  "mock_evaluation": {},
  "safety": {}
}
```

## API

v3.6-E adds:

```bash
GET /versioned-skill-training-runs
GET /versioned-skill-training-runs/{run_id}
POST /versioned-skill-training-runs/mock
```

The POST payload is:

```json
{
  "package_id": "sales_contract_payment_dispute@v1.0.0"
}
```

The POST endpoint returns deterministic mock metadata. It does not call an LLM, does not train, and does not publish.

## Frontend

v3.6-E adds:

* `/versioned-training-runs`
* `/versioned-training-runs/{runId}`

The versioned training package detail page also includes a `Create Mock Training Run` action. This action creates mock metadata only.

## A10 Guard

The run foundation does not alter the A-series legal analysis assets.

`case-analysis-pro-v3` A10 remains:

`A10 争议焦点法律深化分析`

The required five modules, scoring card, and depth self-assessment card remain part of the versioned training package asset boundary.
