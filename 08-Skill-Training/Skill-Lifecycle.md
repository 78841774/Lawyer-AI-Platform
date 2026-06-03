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

