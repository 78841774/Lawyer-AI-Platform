# Skill Versioning

Skill Versioning 定义技能版本、兼容性和升级策略。

## 一、版本格式

Skill Factory 使用业务版本格式：

```text
v1
v1.1
v2
```

含义：

- v1：初始稳定版本
- v1.1：兼容性增强版本
- v2：重大升级版本

## 二、v1

v1 是技能的第一个稳定发布版本。

要求：

- 已通过 Evaluation Framework
- 可被 Workspace System 加载
- 包含完整 Prompt、Template 和 tests
- metadata 记录训练来源和评估结果

适用情形：

- 首次发布某一领域技能
- 覆盖最核心案件模式
- 不承诺覆盖复杂分支

示例：

```text
contract-dispute-cn-v1
```

## 三、v1.1

v1.1 是在 v1 基础上的兼容性增强。

允许变更：

- 增加新模板
- 增加测试样本
- 优化 Prompt 表述
- 增加新争议焦点识别
- 增加风险提示规则
- 修复不影响输出结构的问题

禁止变更：

- 删除 v1 已有字段
- 改变核心输出结构
- 改变法域
- 改变 domain
- 让 Workspace v1 加载逻辑失效

适用情形：

- v1 发布后吸收反馈
- 扩展同一案件类型中的常见分支
- 提升报告质量但不改变技能边界

示例：

```text
contract-dispute-cn-v1.1
```

## 四、v2

v2 是重大升级版本。

允许变更：

- 重构 Prompt
- 重构模板
- 调整输出结构
- 增加新的子技能
- 拆分或合并技能能力
- 改变评估指标权重
- 调整 Experience Package 结构

必须满足：

- 明确迁移说明
- 重新完成完整评估
- 标记与 v1 或 v1.1 的兼容关系
- 更新 lifecycle 状态
- 保留历史版本可追溯记录

适用情形：

- 技能能力边界发生变化
- 输出格式发生重大变化
- 新法律规则或实践标准要求重训
- Workspace 加载逻辑需要适配

示例：

```text
contract-dispute-cn-v2
```

## 五、兼容性策略

### 向后兼容

v1.1 必须向后兼容 v1。

含义：

- Workspace 可按 v1 方式加载 v1.1
- v1 模板字段仍然存在
- v1 测试样本仍然通过
- v1 输出结构不被破坏

### 非兼容升级

v2 可以不完全兼容 v1。

但必须提供：

- breaking_changes
- migration_notes
- deprecated_fields
- new_fields
- compatibility_matrix

示例：

```json
{
  "from": "v1.1",
  "to": "v2",
  "compatible": false,
  "breaking_changes": [
    "legal_analysis output split into issue_analysis and risk_assessment"
  ],
  "migration_notes": [
    "Workspace must read templates/client_report.md as final report template."
  ]
}
```

## 六、升级策略

升级流程：

```text
Published Version
  |
  v
Collect Feedback
  |
  v
Create Draft Version
  |
  v
Run Evaluation
  |
  v
Validate Compatibility
  |
  v
Publish New Version
  |
  v
Deprecate Old Version if Needed
```

## 七、版本保留

已发布版本必须保留。

不得删除历史版本。

Deprecated 版本不得用于新案件，但可用于：

- 历史案件复现
- 评估对比
- 迁移验证
- 审计追溯

## 八、版本命名规则

命名格式：

```text
{domain}-{jurisdiction}-{version}
```

示例：

```text
contract-dispute-cn-v1
contract-dispute-cn-v1.1
contract-dispute-cn-v2
```

## 九、v2.4 Registry 与版本策略

v2.4 Skill Registry 以 `domain + version + lifecycle status` 管理可用能力。

Registry 聚合：

- skill_id
- domain
- version
- status
- validation_status
- package_id
- package_status

同一 domain 可以存在多个版本。

推荐策略：

- 新版本完成 validated 和 built 后再进入 publish。
- 新版本 publish 前，旧版本可以继续保持 published。
- 新版本确认可替代旧版本后，将旧版本 deprecate。
- deprecated 版本保留用于审计、复现和迁移验证。

v2.4 不强制实现版本冲突检测。

后续 Package Registry 阶段应增加：

- 同 domain 默认版本选择
- published 版本唯一性策略
- 版本兼容矩阵
- Workspace 加载版本策略
