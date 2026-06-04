# Skill Training Optimization Plan

v3.6-B confirms that training should not start from raw legacy Skill files.

The correct order is:

1. Find legacy data.
2. Reshape the data into a controlled package.
3. Review and validate the package.
4. Import only approved package metadata.
5. Optimize the Skill Training flow from the reviewed package shape.
6. Train in a later stage.

## Current Finding

The legacy SkillOpt workspace contains useful training data and optimized Skill artifacts:

* 19 dataset files.
* 96 dataset items.
* 14 SkillOpt output runs.
* 12 `best_skill.md` outputs.
* 3 initial Skill seeds.

These assets are valuable, but they are not ready for direct import.

## Target Package Shape

Each future data package should use a stable structure:

```json
{
  "package_id": "legacy_casework_dataset_v1",
  "source": "legacy-skillopt",
  "privacy_status": "desensitized",
  "review_status": "curated",
  "skills": [],
  "samples": [],
  "rubrics": [],
  "runtime_rules": [],
  "prompt_templates": [],
  "report_templates": [],
  "rejected_items": [],
  "source_refs": []
}
```

Sample records should preserve only structured, reviewed content:

```json
{
  "sample_id": "sample_001",
  "skill_target": "case-fact-extractor-v3",
  "task_type": "fact_extraction",
  "case_type": "contract_dispute",
  "party_position": "plaintiff",
  "privacy_level": "desensitized",
  "review_status": "curated",
  "input_materials": [],
  "expected_output": {},
  "evaluation_rubric": {},
  "source_refs": []
}
```

## Gating Rules

Data can enter the future training path only when all gates pass:

* Privacy gate: no raw-private or unknown privacy items.
* Review gate: sample has a clear reviewer status.
* Structure gate: sample matches the normalized schema.
* Source gate: references are traceable without copying real case files.
* Evaluation gate: expected output and rubric are present for trainable tasks.
* Safety gate: legal conclusions remain reviewable and are not treated as automatic legal advice.

## Migration Buckets

Legacy assets should be split into these buckets:

| bucket | source | destination |
| --- | --- | --- |
| Runtime rules | SKILL.md constraints, admission gates, rejection rules | Skill runtime policy layer |
| Prompt templates | Initial skills and stable best_skill sections | Prompt/template package |
| Evaluation rubrics | scoring rules, must_include, must_not_include | Evaluation package |
| Report templates | fact report and case analysis output structures | Report template package |
| Dataset examples | curated SkillOpt `items.json` records | Dataset package |
| Reference-only | scripts, OCR instructions, legal search handoff notes | Internal reference |

## Legacy Skill 清洗规则

1. 旧 Skill 原文优先。
2. `references` 模板优先。
3. 不得凭记忆或通用法律流程重写 A 系列。
4. A10 必须保留为 `争议焦点法律深化分析`。
5. 诉状、答辩状、代理词、结案报告等输出不得归入第十步。
6. 所有清洗必须记录在 v3.6 changelog。

For `case-analysis-pro-v3`, reshaped runtime rules must preserve the E1, 00, A1-A13, E chain from the old Skill source. Training-package builders must treat this source-aligned structure as the package boundary.

## Optimization Sequence

v3.6-C should create a data reshaping script and package manifest.

v3.6-D prepares readonly versioned packages without changing the Skill Training main chain.

Prepared packages:

* `case-fact-extractor-v3@v1.0.0`
* `case-analysis-pro-v3@v1.0.0`
* `contract_dispute_combined@v1.0.0`

v3.6-E can then start an explicit versioned training run after review.

Recommended sequence:

1. Add a read-only data-package builder.
2. Produce a local package manifest from legacy SkillOpt data.
3. Mark every item as `curated`, `inbox`, `rejected`, or `raw-private`.
4. Exclude `unknown` and `raw-private` from trainable splits.
5. Generate package-level rubrics and templates.
6. Validate counts and schema.
7. Only then decide whether to import package metadata into the app.

## v3.6-D Package Boundary

The package registry is:

* `/Users/wazhen/Lawyer-AI-Platform/Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/registry.json`

The API is readonly:

* `GET /versioned-skill-training-packages`
* `GET /versioned-skill-training-packages/{package_id}`
* `GET /versioned-skill-training-packages/{package_id}/files`

No package in v3.6-D can auto-train or auto-publish.

Existing `skill_001` and `skill_002` remain untouched.

## Non-Goals

This plan does not include:

* Running SkillOpt.
* Running LLM evaluation.
* Publishing new Skills.
* Importing legacy outputs directly into Skill Registry.
* Copying private case materials into the repository.
