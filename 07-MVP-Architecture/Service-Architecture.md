# Service Architecture

Service Architecture 定义 Lawyer AI Platform v0.4 MVP 的服务拆分方式。

MVP 阶段建议采用模块化单体架构：部署为一个 Backend API 应用，但在代码层面按照服务模块拆分职责。这样可以降低早期部署复杂度，同时保留后续拆分为独立服务的可能性。

## 服务模块

### Case Service

负责案件生命周期。

职责：

* 创建案件。
* 查询案件列表和案件详情。
* 更新案件状态。
* 绑定 Experience Package。
* 汇总案件工作流进度。

### Material Service

负责案件材料处理。

职责：

* 上传和登记材料。
* 保存原始文件。
* 提取文本或 OCR。
* 管理材料解析状态。
* 为 Fact Service 提供材料上下文。

### Fact Service

负责事实提炼。

职责：

* 调用 AI Runtime 执行 Fact Extraction。
* 保存 facts。
* 维护事实状态和可信度。
* 支持人工确认、驳回和争议标记。
* 保证事实来源可追溯。

### Legal Service

负责法律分析。

职责：

* 基于 Fact Schema 调用 AI Runtime。
* 保存 legal_analyses。
* 管理法律争点、推理链、结论和风险等级。
* 支持重新生成和版本记录。

### Report Service

负责报告生成。

职责：

* 基于案件、事实和法律分析生成报告。
* 保存 reports。
* 管理报告状态、版本和文件路径。
* 支持预览、下载和重新生成。

### Experience Package Service

负责经验包管理。

职责：

* 注册和查询 Experience Package。
* 加载 package manifest。
* 向 AI Runtime 提供 skills、schemas、templates 和 runtime_config。
* 向 Case Service 提供可选经验包列表。

## MVP 服务调用链

```text
Frontend
  |
  v
Backend API
  |
  |-- Case Service
  |-- Material Service
  |-- Fact Service
  |     |
  |     v
  |   AI Runtime
  |
  |-- Legal Service
  |     |
  |     v
  |   AI Runtime
  |
  |-- Report Service
  |     |
  |     v
  |   AI Runtime
  |
  |-- Experience Package Service
  |
  |-- PostgreSQL
  |-- Object Storage
```

## 异步任务建议

以下任务建议异步执行：

* 材料 OCR 和文本解析。
* Fact Extraction。
* Legal Analysis。
* Report Generation。

异步任务应返回 job_id，并允许前端轮询任务状态。

## 架构边界

* Case Service 不直接调用模型。
* Legal Service 不直接读取原始文件，应通过 facts 和 material text references 获取上下文。
* Report Service 不生成无来源结论，应引用 facts 和 legal_analyses。
* Experience Package Service 不负责训练，只负责加载和提供包配置。
