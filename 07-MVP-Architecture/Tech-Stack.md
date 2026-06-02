# Tech Stack

Tech Stack 定义 Lawyer AI Platform v0.4 MVP 推荐技术栈。

MVP 技术选型以开发效率、可维护性、可部署性和后续扩展性为优先，不追求过早微服务化或复杂基础设施。

## Frontend

建议技术栈：

* React：构建 Workspace 前端。
* TypeScript：保证接口类型和前端状态结构清晰。
* Vite：提供本地开发和构建工具。
* React Router：管理案件列表、案件详情和功能页面路由。
* TanStack Query：管理 API 请求、缓存和刷新。
* Tailwind CSS 或轻量组件库：快速实现一致 UI。

MVP 前端页面：

* Case List
* Case Detail
* Material Upload
* Fact Extraction
* Legal Analysis
* Report Generation
* Experience Package Selector

## Backend

建议技术栈：

* Python FastAPI：实现 REST API 和异步任务入口。
* Pydantic：定义请求、响应和 schema 校验。
* SQLAlchemy 或 SQLModel：管理数据库模型。
* Alembic：管理数据库迁移。
* Celery、RQ 或轻量任务队列：处理材料解析、AI 调用和报告生成任务。

MVP 后端形态：

* 单体后端应用，按 service module 分层。
* 保留未来拆分为独立服务的边界。
* API 层、Service 层、Repository 层清晰分离。

## Database

建议技术栈：

* PostgreSQL：保存案件、材料、事实、法律分析、报告和审计日志。
* JSONB：保存 source_materials、evidence_refs、reasoning_chain、citations 等结构化扩展字段。
* Alembic migration：保证表结构可演进。

MVP 不建议引入复杂分布式数据库。

## Storage

建议技术栈：

* 本地开发：本地文件目录或 MinIO。
* 测试和生产：S3、OSS 或兼容 S3 的对象存储。

存储对象：

* 原始案件材料。
* OCR 和解析结果。
* AI 中间结果。
* 报告文件。

## AI Runtime

建议技术栈：

* 后端内置 AI Runtime module。
* 使用统一 Model Client 封装模型调用。
* 使用 Experience Package Loader 加载 skills、schemas、templates 和 gates。
* 使用结构化输出校验保证 Fact Schema 和 Legal Reasoning Schema 的稳定性。

MVP AI Runtime 重点：

* Prompt 装配。
* 上下文构造。
* 模型调用。
* Schema 校验。
* 错误重试。
* 执行日志。

## Deployment

建议技术栈：

* Docker：统一封装前端、后端和 worker。
* Docker Compose：支持本地开发和测试环境。
* PostgreSQL container：本地数据库。
* MinIO container：本地对象存储。
* 环境变量：管理数据库、存储、模型和日志配置。

MVP 部署目标：

* 本地一键启动。
* 测试环境可复现部署。
* 生产环境保留容器化迁移路径。
