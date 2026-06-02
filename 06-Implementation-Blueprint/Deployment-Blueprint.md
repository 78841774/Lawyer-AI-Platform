# Deployment Blueprint

Deployment Blueprint 定义 Lawyer AI Platform 的本地开发、测试环境和生产环境部署方案。

部署方案应支持前端、后端、数据库、对象存储、AI Runtime、日志和备份的统一配置，并保证不同环境之间配置隔离。

## 本地开发环境

本地开发环境用于功能开发和调试。

建议组件：

* Frontend：本地开发服务器。
* Backend API：本地应用进程。
* Database：PostgreSQL 或兼容关系型数据库。
* Object Storage：本地目录或 MinIO。
* AI Runtime：连接开发用模型配置。
* Logs：本地日志文件。

建议能力：

* 使用 .env.local 管理环境变量。
* 使用 Docker Compose 启动数据库和对象存储。
* 使用本地 seed 数据初始化 Experience Package。
* 开发环境允许详细日志和调试输出。

## 测试环境

测试环境用于接口联调、流程验证和验收测试。

建议组件：

* 独立前端测试部署。
* 独立后端测试服务。
* 独立测试数据库。
* 独立对象存储 bucket。
* 独立 AI Runtime 配置和限流策略。
* 集中日志和错误追踪。

建议能力：

* 使用 .env.test 或环境变量管理平台配置。
* 启用数据库迁移和回滚脚本。
* 启用自动化测试、接口测试和基础性能测试。
* 每次发布记录版本号、提交哈希和配置版本。

## 生产环境

生产环境用于真实案件运行。

建议组件：

* Frontend：静态资源部署到 CDN 或 Web 服务。
* Backend API：容器化部署，支持水平扩展。
* Database：高可用 PostgreSQL 或托管数据库。
* Object Storage：启用加密、版本管理和访问控制的对象存储。
* AI Runtime：独立服务或后端内部模块，启用限流、重试和审计。
* Logs：集中日志、指标监控和告警。
* Backup：数据库和对象存储定期备份。

## 环境变量

建议环境变量：

```text
APP_ENV=production
APP_VERSION=0.3.0
DATABASE_URL=postgres://user:password@host:5432/lawyer_ai
OBJECT_STORAGE_ENDPOINT=https://storage.example.com
OBJECT_STORAGE_BUCKET=lawyer-ai-platform
OBJECT_STORAGE_ACCESS_KEY=change-me
OBJECT_STORAGE_SECRET_KEY=change-me
AI_MODEL_PROVIDER=provider-name
AI_MODEL_NAME=model-name
AI_REQUEST_TIMEOUT_SECONDS=180
EXPERIENCE_PACKAGE_ROOT=/app/experience-packages
LOG_LEVEL=info
AUDIT_LOG_ENABLED=true
```

## Docker 建议

建议拆分镜像：

* frontend：前端静态资源或前端服务。
* backend：后端 API 和业务服务。
* worker：AI 任务、报告生成和异步处理。

建议 Docker Compose 覆盖：

* backend
* frontend
* worker
* postgres
* minio
* redis

## 数据库

* 使用迁移工具管理表结构。
* 生产环境启用备份和恢复演练。
* 关键表使用 case_id、request_id 和 created_at 索引。
* 敏感数据访问应记录 audit_logs。

## 对象存储

* 按 case_id 隔离文件路径。
* 启用服务端加密。
* 生产环境启用版本管理。
* 下载链接使用短期签名。

## 日志

日志应覆盖：

* API 请求日志。
* AI Runtime 执行日志。
* Gate 检查日志。
* 文件上传和下载日志。
* 审计日志。

生产环境应将日志集中到可检索系统，并配置错误率、延迟、任务失败率和存储异常告警。

## 备份

备份范围：

* 数据库每日全量备份和必要的增量备份。
* 对象存储版本和归档备份。
* Experience Package manifest 和模板备份。
* 部署配置和环境变量版本记录。

恢复要求：

* 支持按 case_id 恢复案件数据。
* 支持恢复报告历史版本。
* 支持恢复 Experience Package 指定版本。
