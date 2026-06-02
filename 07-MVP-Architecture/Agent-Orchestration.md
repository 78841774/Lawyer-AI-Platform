# Agent Orchestration

Agent Orchestration 定义 Lawyer AI Platform v0.4 MVP 的 Agent 调度架构。

MVP 阶段不追求复杂多 Agent 自主协作，而是采用可控的任务编排：由 Orchestrator 根据案件阶段、Experience Package 和用户动作，调度专门 Agent 完成材料解析、事实提炼、法律分析和报告生成。

## 调度组件

### Orchestrator

Orchestrator 是任务调度中心。

职责：

* 接收 Backend Service 发起的任务。
* 加载 Experience Package。
* 构造任务上下文。
* 选择对应 Agent。
* 管理 job_id、任务状态、错误重试和执行日志。

### Material Agent

负责材料解析。

职责：

* 读取材料文件。
* 执行文本抽取或 OCR。
* 生成材料分片。
* 输出可供 Fact Agent 使用的 material context。

### Fact Agent

负责事实提炼。

职责：

* 根据 Experience Package 的 fact extraction skill 构造 Prompt。
* 从材料上下文中抽取 Fact Schema。
* 输出可追溯 source_materials 和 evidence_refs。
* 将结果交给 Fact Service 保存。

### Legal Agent

负责法律分析。

职责：

* 读取已确认或已验证事实。
* 根据 Experience Package 的 legal analysis skill 构造 Prompt。
* 输出 Legal Reasoning Schema。
* 保证每个 issue 关联 related_facts。

### Report Agent

负责报告生成。

职责：

* 读取案件信息、facts 和 legal_analyses。
* 加载报告模板。
* 生成法律分析报告。
* 输出 report file 和 source_refs。

### Review Agent

MVP 阶段 Review Agent 可作为轻量质量检查模块。

职责：

* 检查事实是否缺少来源。
* 检查法律分析是否缺少 related_facts。
* 检查报告是否包含无来源结论。
* 输出 warnings，供前端展示和人工复核。

## 调度流程

```text
User Action
  |
  v
Backend Service
  |
  v
Orchestrator
  |
  |-- Load Experience Package
  |-- Build Task Context
  |-- Select Agent
  |-- Execute Agent
  |-- Validate Output
  |-- Persist Result
  |-- Write Audit Log
  v
Job Result
```

## 端到端任务链

### 材料到事实

```text
Material Upload
  -> Material Agent
  -> material context
  -> Fact Agent
  -> Fact Schema
  -> Fact Service
```

### 事实到法律分析

```text
Verified Facts
  -> Legal Agent
  -> Legal Reasoning Schema
  -> Legal Service
```

### 法律分析到报告

```text
Case + Facts + Legal Analyses
  -> Report Agent
  -> Report Markdown
  -> Review Agent
  -> Report Service
```

## 上下文约束

* Fact Agent 只能从 material context 中抽取事实。
* Legal Agent 必须基于 Fact Schema 生成结论。
* Report Agent 必须引用 facts 和 legal_analyses。
* Review Agent 的 warning 不自动覆盖业务结果，应交由人工复核。

## 错误处理

* 模型调用失败：允许按 retry policy 重试。
* Schema 校验失败：允许重新生成或尝试结构修复。
* 缺少材料：任务失败并返回 MATERIAL_NOT_FOUND。
* 缺少已验证事实：法律分析任务返回 FACTS_REQUIRED。
* 报告缺少来源引用：Review Agent 输出 warning。

## MVP 调度原则

* 任务必须可观测，所有任务保存 job_id。
* 输出必须可校验，核心结果符合 schema。
* 失败必须可恢复，支持重新触发任务。
* 结论必须可追溯，避免无来源生成。
