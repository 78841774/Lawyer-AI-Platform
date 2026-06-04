# Skill Factory Foundation v3.6

v3.6 establishes the local Skill Factory foundation for AIHome.law.

The goal is to prove the controlled local loop from reviewed, versioned assets to a local Skill Registry record without production training, without real case material, and without automatic runtime enablement.

## Closed Loop

The v3.6 foundation is:

```text
Versioned Training Package
-> Mock Training Run
-> Experience Package Candidate
-> Human Review
-> Controlled Skill Registry Publish
```

The loop is local, mock, and controlled. It is not a production training system.

## Case Cause Taxonomy

The current case cause taxonomy is:

```text
civil
-> contract_dispute
-> sales_contract_dispute
-> payment_dispute
```

For `payment_dispute`, the versioned package inheritance chain is:

```text
civil_base@v1.0.0
-> contract_dispute_combined@v1.0.0
-> sales_contract_dispute@v1.0.0
-> sales_contract_payment_dispute@v1.0.0
```

Child packages may specialize rules, but they cannot disable human review or legal safety rules.

## Versioned Training Packages

Versioned Training Packages remain readonly inputs.

They can describe:

* source legacy Skill assets
* case cause metadata
* inheritance order
* training scope
* A10 validation requirements
* safety and review requirements

They cannot:

* call LLM providers
* read real case materials
* publish Skill Registry records
* overwrite `skill_001` or `skill_002`

## Mock Training Run Structure

A mock training run records:

* `run_id`
* `package_id`
* `case_cause_code`
* `status=completed_mock`
* `llm_provider=mock`
* `llm_called=false`
* `started_at`
* `completed_at`
* `inheritance_chain`
* `taxonomy_path`
* `inputs.real_case_material_used=false`
* `outputs.experience_package_created=false`
* `outputs.skill_registry_published=false`
* `safety.requires_human_review=true`

Mock training run creation does not call DeepSeek or any live provider.

## Experience Package Candidate Structure

An Experience Package Candidate is built from a `completed_mock` run.

The candidate records:

* `experience_package_id`
* `source_run_id`
* `source_package_id`
* `case_cause_code`
* `status=candidate`
* `build_mode=mock_candidate_build`
* `llm_called=false`
* `real_case_material_used=false`
* `skill_registry_published=false`
* `published_skill_id=null`
* `package_contents`
* `review`
* `safety`

Candidates are not formal production Experience Packages. They are reviewable local package candidates.

## Human Review Gate

Human review is mandatory.

Allowed review states are:

* `pending`
* `approved`
* `rejected`
* `needs_revision`

Only `approved` candidates can be passed to controlled Skill Registry publish. Approval does not automatically publish anything.

## Controlled Skill Registry Publish

Controlled publish requires an approved candidate with:

* `review.requires_human_review=true`
* `review.review_status=approved`
* `safety.can_publish_to_skill_registry=true`
* `safety.auto_publish_enabled=false`
* `skill_registry_published=false`
* `llm_called=false`
* `real_case_material_used=false`

The resulting local Skill Registry record keeps:

* `status=published_local`
* `publish_mode=controlled_local_publish`
* `llm_called=false`
* `real_case_material_used=false`
* `safety.controlled_publish=true`
* `safety.auto_publish_enabled=false`
* `runtime.workspace_runtime_enabled=false`
* `runtime.skill_aware_case_processing_enabled=false`
* `runtime.requires_manual_enablement=true`

Deprecate and rollback append events or change local status. They do not delete history.

## Why Runtime Is Not Automatically Enabled

Publishing a controlled local Skill Registry record is not the same as enabling that Skill in Workspace Runtime.

Runtime enablement remains manual because:

* this stage is mock/local only
* no real training has occurred
* no production evaluation has occurred
* no real case material has been used
* legal outputs still require human review
* Skill-aware case processing must be explicitly approved later

## Safety Boundary

v3.6 does not:

* call a real LLM
* call DeepSeek live provider
* use real case materials
* read real case materials
* commit real case materials
* overwrite `skill_001`
* overwrite `skill_002`
* bypass human review
* automatically publish
* automatically enable Workspace Runtime
* automatically enter real case processing
* modify legacy Skill source assets

A10 remains:

```text
争议焦点法律深化分析
```

A10 must not be reclassified as a complaint, answer,代理词, closing report, drafting task, or document structure.

## API Surface

Training runs:

```bash
GET /versioned-skill-training-runs
GET /versioned-skill-training-runs/{run_id}
POST /versioned-skill-training-runs/mock
```

Experience Package Candidates:

```bash
GET /experience-packages
GET /experience-packages/{experience_package_id}
POST /experience-packages/create
POST /experience-packages/{experience_package_id}/review
```

Controlled Skill Registry:

```bash
GET /skill-registry
GET /skill-registry/{skill_id}
POST /skill-registry/publish
POST /skill-registry/{skill_id}/deprecate
POST /skill-registry/{skill_id}/rollback
```

## Frontend Surface

The local Skill Factory loop is visible through:

* `/versioned-training-packages`
* `/versioned-training-packages/{packageId}`
* `/versioned-training-runs`
* `/versioned-training-runs/{runId}`
* `/experience-packages`
* `/experience-packages/{experiencePackageId}`
* `/skill-registry`
* `/skill-registry/{skillId}`

## v3.7 / v4.0 Direction

After v3.6, the recommended next stage is v3.7 OCR / Legal Search API preparation:

1. OCR adapter reservation.
2. Legal Search API adapter reservation.
3. Material citation and source reference normalization.
4. Report source trace enhancement.
5. Local-only preparation for real case processing.

v4.0 should remain Internal Alpha deployment, not automatic production rollout.
