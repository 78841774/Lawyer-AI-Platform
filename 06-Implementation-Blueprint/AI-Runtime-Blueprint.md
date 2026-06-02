# AI Runtime Blueprint

AI Runtime Blueprint 定义 Lawyer AI Platform 中 AI 调用运行时的实施方案。

AI Runtime 负责模型调用、Prompt 装配、Experience Package 加载、缓存策略、上下文构造、日志记录和错误重试。AI Runtime 不训练能力，只在 Workspace Runtime 中加载经验包并执行案件任务。

## 核心能力

### 模型调用

AI Runtime 应提供统一模型调用接口。

要求：

* 支持按任务类型选择模型。
* 支持结构化输出约束。
* 支持超时、重试、取消和降级策略。
* 支持记录 token 用量、耗时、模型版本和 request_id。

### Prompt 装配

Prompt 装配应由 Experience Package、案件上下文和任务参数共同决定。

输入来源：

* Experience Package 中的 skill 和 template。
* Fact Schema、Legal Reasoning Schema 和 Gate 配置。
* 材料摘录、OCR 结果、用户问题和案件目标。
* 系统级安全约束和输出格式要求。

### Experience Package 加载

AI Runtime 通过 Experience Package Service 获取经验包配置。

加载内容：

* skills：事实抽取、法律分析、策略生成、报告生成能力。
* gates：质量门控规则。
* schemas：结构化输出格式。
* templates：报告模板和 Prompt 模板。
* knowledge_refs：法律、案例、内部经验和知识库引用。
* runtime_config：模型策略、超时、日志和必选 Gate。

### 缓存策略

缓存用于降低重复调用成本并提升响应速度。

建议缓存对象：

* 材料 OCR 和分片结果。
* Experience Package manifest。
* 知识库检索结果。
* 同一输入哈希下的中间分析结果。

缓存键建议包含：

* case_id
* package_id
* package_version
* task_type
* input_hash
* schema_version

### 上下文构造

上下文构造负责把案件材料、事实、法律规则和任务目标组合成模型可处理的输入。

要求：

* 优先使用已验证事实。
* 法律分析必须通过 related_facts 引用 Fact Schema。
* 控制上下文长度，支持材料分片、摘要和检索。
* 保留 source_materials、evidence_refs 和 citations。
* 避免把无来源事实直接注入法律结论。

### 日志记录

AI Runtime 应记录完整执行链路。

建议记录：

* request_id、job_id、case_id、actor_id。
* package_id、package_version、skill_id、template_id。
* task_type、model、model_version、token_usage、latency_ms。
* input_ref、output_ref、error_code、retry_count。
* created_at。

### 错误重试

错误重试应按错误类型处理。

建议策略：

* 网络错误、临时限流、超时：可重试。
* Schema 校验失败：可尝试修复输出或重新生成。
* 材料缺失、事实缺失、权限不足：不自动重试，返回明确错误。
* 多次失败后写入审计日志，并向前端展示可操作的错误说明。

## 运行流程

```text
Backend Service
  |
  v
AI Runtime
  |
  |-- Load Experience Package
  |-- Build Context
  |-- Assemble Prompt
  |-- Call Model
  |-- Validate Schema
  |-- Write Result
  |-- Write Logs
  v
Backend Service
```

## 结构化输出要求

* 事实提炼输出必须符合 Fact Schema。
* 法律分析输出必须符合 Legal Reasoning Schema。
* 报告生成应引用 fact_id、issue_id 和 citations。
* Gate 检查结果应写入 gate_results。
