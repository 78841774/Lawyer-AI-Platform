# 05-System-Design

05-System-Design 是 Lawyer AI Platform v0.2 的系统设计阶段目录。

本阶段负责把 v0.1 的业务架构、训练系统、Experience Package 规范和 Workspace System 文档，转化为可研发的系统接口、数据结构和运行时设计。

系统设计阶段的目标是：

* 明确案件事实、法律推理、经验包的核心数据结构
* 明确 Workspace Runtime 的运行时组成和调度方式
* 明确模块 API 的版本、请求、错误、审计和幂等规范
* 为后续工程实现、接口联调和系统测试提供基础约束

## 核心文件

* Fact-Schema.md：定义案件事实数据结构，确保事实可追溯、可验证、可被 Legal Layer 引用。
* Legal-Reasoning-Schema.md：定义法律推理数据结构，确保法律分析基于事实、法条和推理链形成。
* Experience-Package-Format.md：定义经验包目录、元数据和运行时配置格式，连接 Training System 与 Workspace System。
* Runtime-Architecture.md：定义 Workspace Runtime 的运行时模块、职责边界和执行流程。
* API-Design.md：定义模块 API 设计原则和 v1 接口草案。
