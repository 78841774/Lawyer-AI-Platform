# 07-MVP-Architecture

07-MVP-Architecture 是 Lawyer AI Platform v0.4 的 MVP Architecture 目录。

本阶段在 v0.1 Documentation Foundation、v0.2 System Design 和 v0.3 Implementation Blueprint 的基础上，进一步收敛第一阶段 MVP 的功能边界、技术栈、服务架构、数据库结构、API 草案、Agent 调度和研发路线。

v0.4 的目标不是扩展全部理想能力，而是明确第一版可运行、可演示、可迭代的最小产品架构。

## 文档结构

* MVP-Scope.md：定义 MVP 第一阶段功能边界。
* Tech-Stack.md：确定前端、后端、数据库、存储、AI Runtime 和部署技术栈。
* Service-Architecture.md：定义 MVP 服务拆分和服务间协作方式。
* Database-Schema.md：输出 MVP 核心数据表设计。
* API-Specification.md：输出 MVP REST API 草案。
* Agent-Orchestration.md：设计 Agent 调度架构和任务执行链路。
* Development-Roadmap.md：拆分 Phase 1 MVP、Phase 2 Internal Beta、Phase 3 Production。

## MVP 原则

* 先完成案件闭环，再扩展专业深度。
* 先保证事实、法律分析和报告可追溯，再优化自动化程度。
* 先支持单一 Workspace 流程，再支持复杂协同和多角色权限。
* 先以 Experience Package 加载为架构边界，再逐步接入训练系统闭环。
