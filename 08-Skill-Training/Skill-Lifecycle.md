# Skill Lifecycle

Skill Lifecycle 定义技能从训练到退役的生命周期状态。

## 一、生命周期总览

```text
Draft
  |
  v
Candidate
  |
  v
Validated
  |
  v
Published
  |
  v
Deprecated
```

## 二、Draft

Draft 是技能草稿状态。

进入条件：

- 已创建 skill_id
- 已确定 domain
- 已确定 jurisdiction
- 已收集初始 Case 样本

允许操作：

- 修改 Prompt
- 修改 Template
- 调整 Schema
- 补充测试样本
- 修改 metadata

禁止操作：

- 发布到 Workspace
- 标记为可生产使用
- 作为正式 Experience Package 分发

退出条件：

- Prompt 初稿完成
- Template 初稿完成
- tests 初稿完成
- skill.json 字段完整

## 三、Candidate

Candidate 是候选技能状态。

进入条件：

- Draft 完成结构校验
- Prompt、Template、tests 均存在
- evaluation_metrics 已定义

允许操作：

- 运行测试
- 进行自动评估
- 进行律师复核
- 小范围优化 Prompt 和 Template

禁止操作：

- 用于线上案件
- 对外发布
- 跳过评估直接构建正式包

退出条件：

- 完成 Evaluation Framework 评估
- 无严重法律错误
- 达到最低指标阈值

## 四、Validated

Validated 是已验证状态。

进入条件：

- Candidate 通过评估
- 律师复核通过
- evaluation_report.json 已生成
- evaluation_summary.md 已生成

v2.2 Runtime 初版中，Candidate 满足以下条件即可进入运行时 `validated` 状态：

- `POST /skills/{skill_id}/evaluate` 执行完成
- evaluation_score >= 0.75
- validation_status = validated
- evaluation_details 已写入 skills 表
- 本地 skill.json 已同步写入 evaluation_details

允许操作：

- 构建 Experience Package
- 准备发布说明
- 执行兼容性检查
- 标记版本关系

禁止操作：

- 在不重新评估的情况下修改核心 Prompt
- 在不重新评估的情况下修改模板结构
- 跳过发布审批

退出条件：

- 构建通过
- 版本检查通过
- 发布审批通过

## 五、Published

Published 是已发布状态。

进入条件：

- Experience Package 构建完成
- 版本号唯一
- metadata 完整
- 发布审批通过

允许操作：

- 被 Workspace System 加载
- 用于案件分析生产流程
- 收集运行反馈
- 用于新版本训练参考

禁止操作：

- 直接修改已发布文件
- 覆盖同版本包
- 删除历史评估记录

退出条件：

- 出现替代版本
- 存在重大质量问题
- 法律规则或业务场景变化导致不再适用

## 六、Deprecated

Deprecated 是废弃状态。

进入条件：

- 新版本已发布
- 原版本不再推荐使用
- 原版本存在已知限制
- 法律规则变化导致原版本不再适配

允许操作：

- 历史案件复现
- 审计追溯
- 迁移对比
- 作为训练参考样本

禁止操作：

- 用于新案件
- 作为默认技能加载
- 对外推荐

## 七、状态变更记录

每次状态变更必须记录：

- skill_id
- version
- from_status
- to_status
- changed_at
- changed_by
- reason
- approval_record

示例：

```json
{
  "skill_id": "contract-dispute-cn-v1",
  "version": "v1",
  "from_status": "Validated",
  "to_status": "Published",
  "changed_at": "2026-06-03",
  "changed_by": "Skill Factory",
  "reason": "Passed evaluation and package build checks.",
  "approval_record": "lawyer-review-2026-06-03"
}
```

## 八、生命周期原则

生命周期管理必须遵循：

- 未验证不发布
- 已发布不直接修改
- 废弃不删除
- 升级必须重新评估
- 状态变化必须可追溯

## 九、v2.2 Runtime 状态

v2.2 在 `status` 之外增加 `validation_status`。

两者分工：

- status：描述 Skill Candidate 的构建阶段，例如 candidate。
- validation_status：描述评估结果，例如 validated 或 needs_improvement。

示例：

```json
{
  "status": "candidate",
  "validation_status": "validated",
  "evaluation_score": 0.82
}
```

这表示该技能仍是候选技能包，但已经通过 v2.2 运行时评估。

正式发布仍需后续 Published 流程。

## 十、v2.4 Skill Registry 状态

v2.4 引入 Skill Registry 作为统一能力登记入口。

Registry 不新增独立状态表。

状态来源：

- skills 表保存 skill 的 status、validation_status 和 evaluation_score。
- experience_packages 表保存 package 的 status、package_id 和 package_path。

Registry 聚合二者，形成未来 Workspace 加载能力包所需的统一视图。

发布规则：

```text
validation_status = validated
package_status = built
```

满足以上条件时：

```text
skill.status -> published
package.status -> published
```

废弃规则：

```text
skill.status -> deprecated
package.status -> deprecated
```

已废弃的 skill 不允许再次 publish。

如需重新启用，应创建新版本并重新完成 Evaluation 和 Package Build。

## 十一、v2.5 Workspace Skill Loader 状态

v2.5 让 Workspace Runtime 加载已发布能力。

Workspace 只加载：

```text
skill.status = published
package.status = published
```

Workspace 不加载：

- candidate
- built
- deprecated
- needs_improvement
- validated 但未 published 的 skill

案件应用记录写入：

```text
case_skill_bindings
```

字段：

- binding_id
- case_id
- skill_id
- package_id
- status
- created_at

v2.5 暂不执行真实 AI 推理。

`POST /cases/{case_id}/skills/{skill_id}/apply` 仅表示该 case workspace 已绑定并准备使用该 Skill。
