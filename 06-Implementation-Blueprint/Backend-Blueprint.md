# Backend Blueprint

Backend Blueprint 定义 Lawyer AI Platform 后端服务模块和职责边界。

后端服务负责承接 Workspace 前端请求，协调数据库、文件存储、AI Runtime、Experience Package 和审计日志，确保案件执行过程可追溯、可复核、可恢复。

## 服务模块

### Case Service

负责案件生命周期管理。

核心职责：

* 创建、查询、更新案件。
* 管理案件类型、案件状态、当事人、负责人和案件目标。
* 绑定 Experience Package。
* 汇总案件材料、事实、法律分析、Gate 和报告状态。

### Material Service

负责案件材料管理。

核心职责：

* 接收材料上传和材料登记请求。
* 管理材料元数据、证据编号、证明目的、文件路径和解析状态。
* 调用 OCR、文本抽取、分片和索引流程。
* 为 Fact Service 提供可追溯的材料来源定位。

### Fact Service

负责案件事实抽取、存储和复核。

核心职责：

* 调用 AI Runtime 执行事实提炼。
* 生成和更新 Fact Schema。
* 管理事实状态、可信度、来源材料和证据引用。
* 支持人工确认、争议标记、驳回和补充事实。

### Legal Service

负责法律分析和法律推理管理。

核心职责：

* 基于 Fact Schema 调用 AI Runtime 执行法律分析。
* 生成和更新 Legal Reasoning Schema。
* 管理法律争点、事实引用、法律规则、推理链、结论和风险等级。
* 支持法律分析版本管理和人工复核。

### Gate Service

负责质量门控检查。

核心职责：

* 加载 Experience Package 中的 Gate 配置。
* 检查事实完整性、证据引用、法律依据、推理链和报告质量。
* 生成 gate_results。
* 支持重新检查、人工复核和问题定位。

### Report Service

负责报告和法律文书生成。

核心职责：

* 调用 AI Runtime 和模板系统生成报告。
* 管理报告类型、模板、版本、生成状态、文件路径和导出状态。
* 关联 Gate 结果和审计日志。
* 支持报告预览、下载、归档和再生成。

### Experience Package Service

负责经验包注册、查询和加载协调。

核心职责：

* 管理 Experience Package 元数据。
* 校验 package_id、version、case_type、schemas、skills、gates、templates。
* 为 AI Runtime 和 Gate Service 提供经验包配置。
* 记录案件绑定、切换和加载历史。

## 服务依赖关系

```text
Frontend
  |
  v
Backend API
  |
  |-- Case Service
  |-- Material Service
  |-- Fact Service --------> AI Runtime
  |-- Legal Service -------> AI Runtime
  |-- Gate Service --------> Experience Package Service
  |-- Report Service ------> AI Runtime
  |-- Experience Package Service
  |
  |-- Database
  |-- File Storage
  |-- Audit Logs
```

## 实施原则

* 服务之间通过 case_id、request_id 和资源 ID 关联。
* 所有写操作记录 audit_logs。
* AI 类任务优先采用异步 job 机制。
* 每个服务输出的数据结构应与 v0.2 System Design 保持一致。
