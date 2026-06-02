# Development Roadmap

Development Roadmap 定义 Lawyer AI Platform 从 v0.4 MVP Architecture 到生产可用版本的研发路线。

路线分为 Phase 1 MVP、Phase 2 Internal Beta 和 Phase 3 Production。

## Phase 1 MVP

目标：完成第一版可运行案件闭环。

范围：

* 案件管理：创建案件、案件列表、案件详情。
* 材料上传：上传材料、保存文件、解析文本。
* Fact Extraction：生成 Fact Schema，支持人工确认和驳回。
* Legal Analysis：基于 facts 生成 Legal Reasoning Schema。
* Report Generation：生成基础法律分析报告。
* Experience Package：支持加载一个合同纠纷 MVP 经验包。
* AI Runtime：支持 Prompt 装配、模型调用、结构化输出校验。
* 部署：支持本地 Docker Compose 启动。

交付标准：

* 样例案件可以端到端跑通。
* 所有核心输出可追溯到材料或事实。
* 前端可完成主要操作。
* 后端 API 有基础错误处理和日志。

## Phase 2 Internal Beta

目标：支持内部律师试用和真实样例案件验证。

范围：

* 增强材料解析：提升 OCR、分片和材料预览质量。
* 增强事实复核：支持事实编辑、争议处理和版本记录。
* 增强法律分析：支持多争点、风险等级和引用管理。
* 增强报告能力：支持更多模板和 Markdown 到 DOCX 导出。
* Gate 检查：引入事实完整性、法律依据和报告质量检查。
* 审计日志：完善 request_id、actor_id、job_id 的链路记录。
* 权限：支持基础用户和案件访问控制。
* 测试环境：建立可复现部署和测试数据集。

交付标准：

* 内部用户可以处理多起样例案件。
* 关键任务失败可以定位和重试。
* 报告可作为律师复核底稿。
* 数据库和对象存储具备备份方案。

## Phase 3 Production

目标：进入生产可用和持续迭代阶段。

范围：

* 多案件类型 Experience Package。
* 生产级权限、审计和安全策略。
* 稳定对象存储、数据库备份和恢复演练。
* 任务队列和 worker 水平扩展。
* 模型调用成本、延迟和错误率监控。
* 法律知识库和案例检索接入。
* 报告和文书模板体系完善。
* Training System 与 Workspace System 的反馈闭环。

交付标准：

* 生产环境可稳定部署。
* 核心指标可监控并配置告警。
* 关键数据可恢复。
* Experience Package 可以版本化发布和回滚。

## 里程碑建议

```text
Week 1-2: Backend skeleton, database schema, case and material APIs
Week 3-4: Frontend workspace, material upload, file storage
Week 5-6: AI Runtime, Fact Extraction, Legal Analysis
Week 7: Report Generation, job status, audit logs
Week 8: MVP integration test and demo
```
