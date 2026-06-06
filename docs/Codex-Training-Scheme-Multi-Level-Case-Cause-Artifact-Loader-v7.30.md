# v7.30 Codex Training Scheme & Multi-Level Case-Cause Artifact Loader

## 中文定位

Codex 训练方案、多层级案由经验包与训练产物加载器。

## 实现内容

- 新增 `/personal-skill-studio/training-artifacts` API。
- 新增 Codex training scheme metadata。
- 新增 multi-level case-cause taxonomy metadata。
- 新增 synthetic experience package manifests。
- 新增 `case_fact_extraction_skill` 和 `case_legal_analysis_skill` Skill manifests。
- 新增 evaluation / gate / test case / loading manifests。
- 新增案由 exact match、ancestor fallback、common fallback、evidence overlay merge dry-run。
- 新增 Skill Context dry-run。
- 新增前端 `/personal-skill-studio/training-artifacts` 页面。

## 边界

Codex training 在本项目中不是 fine-tune 模型参数。v7.30 只定义和加载训练产物 metadata，不执行真实训练，不读取真实案件材料，不使用未结案件训练，不调用 provider，不读取 API key，不自动发布 Skill，不生成最终法律意见、正式报告、真实文件、邮件、公开链接或外部交付。

## 多层级案由

最低支持：

- `case_domain`
- `case_cause_level_1`
- `case_cause_level_2`
- `case_cause_level_3`
- `case_cause_name`
- `case_cause_code`
- `case_cause_path`

支持民事 / 合同纠纷 / 买卖合同纠纷、借款合同纠纷，民事 / 侵权责任纠纷 / 机动车交通事故责任纠纷、医疗损害责任纠纷，民事 / 婚姻家庭继承纠纷 / 离婚纠纷、继承纠纷等 synthetic taxonomy metadata。

## API

- `GET /personal-skill-studio/training-artifacts/status`
- `GET /personal-skill-studio/training-artifacts/scheme`
- `GET /personal-skill-studio/training-artifacts/case-cause-taxonomy`
- `GET /personal-skill-studio/training-artifacts/case-cause-taxonomy/{case_cause_id}`
- `GET /personal-skill-studio/training-artifacts/packages`
- `GET /personal-skill-studio/training-artifacts/packages/{package_id}`
- `GET /personal-skill-studio/training-artifacts/skills`
- `GET /personal-skill-studio/training-artifacts/skills/{skill_id}`
- `GET /personal-skill-studio/training-artifacts/evaluations`
- `GET /personal-skill-studio/training-artifacts/gates`
- `GET /personal-skill-studio/training-artifacts/test-cases`
- `GET /personal-skill-studio/training-artifacts/loading-manifests`
- `POST /personal-skill-studio/training-artifacts/case-cause-match/mock`
- `POST /personal-skill-studio/training-artifacts/load-dry-run/mock`
- `GET /personal-skill-studio/training-artifacts/load-dry-runs`
- `GET /personal-skill-studio/training-artifacts/load-dry-runs/{run_id}`
- `GET /personal-skill-studio/training-artifacts/skill-contexts`
- `GET /personal-skill-studio/training-artifacts/skill-contexts/{skill_context_id}`
- `GET /personal-skill-studio/training-artifacts/audit`
- `GET /personal-skill-studio/training-artifacts/safety`

## Regression

`scripts/regression/check_personal_training_artifact_loader_apis.sh` checks the v7.30 API surface, safety booleans, dry-run boundaries, and forbidden sensitive patterns.

