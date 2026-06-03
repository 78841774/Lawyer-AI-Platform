# Lawyer-AI-Platform
律师AI能力平台  基于 Experience Package 的律师经验数字化体系  包含： - Codex训练系统 - Experience Package标准 - 案件分析生产系统 Workspace

## v0.2 System Design

新增 05-System-Design 目录，作为 Lawyer AI Platform v0.2 系统设计阶段目录。

该目录负责把 v0.1 的业务架构文档转化为可研发的系统接口、数据结构和运行时设计，覆盖案件事实结构、法律推理结构、经验包格式、Workspace Runtime 架构和 API 设计。

## v0.3 Implementation Blueprint

新增 06-Implementation-Blueprint 目录，作为 Lawyer AI Platform v0.3 实施蓝图阶段目录。

该目录负责把 v0.1 架构和 v0.2 系统设计转化为研发落地方案，覆盖 Workspace 前端、后端服务、数据库、文件存储、AI Runtime 和部署方案。

## v0.4 MVP Architecture

新增 07-MVP-Architecture 目录，作为 Lawyer AI Platform v0.4 MVP 架构阶段目录。

该目录负责将 v0.1 Documentation Foundation、v0.2 System Design 和 v0.3 Implementation Blueprint 收敛为第一阶段可运行 MVP 的功能边界、技术栈、服务架构、数据库结构、API 草案、Agent 调度和研发路线。

## v0.6 Case Service

新增并集成 v0.6 Case Service 到 MVP backend，提供基于 FastAPI 的案件创建与查询接口。

当前接口：

* POST /cases：创建案件，MVP 阶段暂用内存 dict 存储。
* GET /cases/{case_id}：查询指定案件。

## v2.0 Skill Training Specification

新增 08-Skill-Training 目录，作为 Lawyer AI Platform v2.0 Skill Factory 架构规范。

该目录负责定义如何从真实案件中沉淀律师经验，并生成可复用、可评估、可发布的 Experience Package。

核心内容：

* Skill Schema：定义 skill_id、skill_name、domain、jurisdiction、version、prompts、templates、evaluation_metrics 和 metadata。
* Training Pipeline：定义从 Case 到 Experience Package 的技能训练流水线。
* Evaluation Framework：定义 accuracy、consistency、completeness、legal_relevance 和 report_quality 评分机制。
* Package Build System：定义 skill.json、Prompt 文件、templates 和 tests 的输出格式。
* Skill Versioning：定义 v1、v1.1、v2 的兼容性与升级策略。
* Skill Lifecycle：定义 Draft、Candidate、Validated、Published、Deprecated 生命周期。
* Example Contract Dispute Skill：以合同纠纷技能说明 Skill Factory 的落地方式。
