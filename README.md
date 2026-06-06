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

## v2.9 Production Readiness Foundation

新增生产化基础改造：后端支持 `APP_ENV`、环境变量驱动的 `DATABASE_URL`、本地 SQLite 默认模式、PostgreSQL Docker Compose 模式和 Alembic 基础结构。

当前阶段仍不包含用户登录和正式云部署，真实生产环境应使用 Alembic migration、外部密钥管理、日志监控和备份恢复流程。

## AIHome.law Personal Production Pilot

AIHome.law Personal Production Pilot 是一个面向律师个人版生产验证的 mock-first、controlled runtime 骨架。它把 AI 草稿、材料处理、法律与企业信息 mock 核验、Experience Package、受控案件生产工作流、交付包草案、Source Trace、Lawyer Review 和 Final Lock 组织成可演示、可截图、可回归验证的受控流程。

当前阶段是个人生产试点与公开演示准备：页面和文档仅展示 mock metadata，lawyer review required / 律师复核必需，source-trace-required / 来源可追踪，Final Lock 只代表受控 metadata 门禁。系统不生成最终法律意见，不生成最终报告，不生成真实 PDF/DOCX，不发送邮件，也不自动对外交付。

Team Workspace deferred / 团队版后置。External Client Delivery deferred / 外部交付后置。后续个人版路线会在安全边界继续收口后，按 provider-gated、lawyer-review-required 的方式连续推进 AI Provider Live Gateway、OCR / Document Provider Live Gateway、Legal / Enterprise API Live Gateway、Skill Training、Controlled Case Analysis、Personal Real AI Gated Pilot、Fact Preview & Correction Workbench，并在大阶段完成后统一做最终安全审计。

AIHome.law Personal Production Pilot is a mock-first, controlled-runtime workflow for validating personal legal production flows. It connects AI draft assistance, material processing, legal and enterprise mock intelligence, experience packages, controlled case production, delivery packet drafts, Source Trace, Lawyer Review, and Final Lock into a showcase-ready process. The current stage is metadata-only and does not generate final legal opinions, final reports, real final files, email sending, or automatic external delivery.

## Personal Local Pilot

v7.11 adds local pilot hardening for the continuous v7.10-v7.23 development stage. Use backend port `8001` and frontend port `3001`; keep live provider disabled by default.

```bash
bash scripts/dev/start_personal_local_pilot.sh
```

Suggested local path: `/` -> `/personal-production` -> `/personal-production-pilot` -> `/personal-case-workspace` -> `/personal-showcase-pack` -> `/personal-delivery-packet` -> `/personal-case-analysis` -> `/personal-case-production` -> `/personal-ai-gateway` -> `/personal-material-runtime` -> `/personal-intelligence` -> `/personal-skill-studio`.

## AI Provider Live Gateway

v7.12 adds the controlled AI Provider Live Gateway foundation. Live mode is disabled by default, dry-run is available, and any live attempt requires explicit confirmation, lawyer review acknowledgement, draft-only acknowledgement, and no-final-opinion acknowledgement. API keys are only checked by backend environment lookup and are never displayed in the frontend. AI output remains draft metadata only.

## OCR / Document Provider Live Gateway

v7.13 adds the controlled OCR / Document Provider Live Gateway foundation. OCR and document live modes are disabled by default, document dry-run and OCR dry-run are available, and any live attempt requires explicit confirmation, material owner acknowledgement, raw-content handling acknowledgement, no-AI-prompt-injection acknowledgement, lawyer review acknowledgement, and draft-only acknowledgement. Raw OCR text and raw document content are not displayed, not injected into AI prompts, and do not trigger fact extraction, legal analysis, final legal opinions, final reports, email sending, real final PDF/DOCX generation, or external delivery.

## Legal / Enterprise API Live Gateway

v7.14 adds the controlled Legal / Enterprise API Live Gateway foundation. Legal and enterprise live modes are disabled by default, legal dry-run and enterprise dry-run are available, and citation / enterprise results remain metadata candidates only. Raw legal results and raw enterprise results are not displayed, not injected into AI prompts, and do not become final citations, final legal opinions, final reports, or external delivery.

## Skill Training Runtime

v7.15 adds the controlled Skill Training Runtime foundation. Training samples remain desensitized metadata, manual confirmation and lawyer review are required, source trace is required, and Skill output stays draft-only. The runtime does not trigger AI prompts, real training, final Skill publish, final legal opinions, final reports, email sending, or external delivery.

## Controlled Case Analysis Runtime

v7.16 adds the controlled open-case analysis runtime. It references existing `case_fact_extraction_skill` and `case_legal_analysis_skill` metadata from v7.15, then creates fact analysis draft metadata and legal analysis draft metadata for unfinished cases. Training and execution are separated: v7.16 does not generate training data, write to training sets, update Skills, publish Skills, generate final legal opinions, generate final reports, send email, create real PDF/DOCX files, or trigger external delivery.

## Personal Production Pilot with Real AI Gated Mode

v7.17 connects the uncommitted v7.10-v7.23 Personal Live Intelligence & Controlled Case Analysis large stage. It connects AI Provider Live Gateway, OCR / Document Provider Live Gateway, Legal / Enterprise API Live Gateway, Skill Training metadata, Controlled Case Analysis metadata, Personal Delivery Packet metadata, and owner-only download metadata into one gated pilot route.

Live providers remain disabled by default. Any live-provider path requires explicit confirmation and returns gated / adapter-unavailable metadata if a provider adapter is incomplete. Owner-only download records support Markdown, JSON, PDF draft, and DOCX draft metadata for Skill final drafts, fact preview drafts, legal analysis drafts, case analysis drafts, source trace summaries, review summaries, and delivery packet drafts.

The pilot does not create public links, send email, upload to third-party systems, deliver to clients, generate final legal opinions, generate formal final reports, train on open cases, write open cases to training sets, update Skills, or publish Skills.

## Case Intake & Material Workspace Hardening

v7.18 adds `/personal-case-workspace` for owner-only case and material metadata handling inside the continuous personal-version large stage. It shows case metadata, material metadata, OCR status metadata, owner raw view gate metadata, fact input correction metadata, source trace summary, audit summary, and a Trust / Safety panel.

The workspace does not read real case materials, return raw content, show local paths, send raw OCR text to AI prompts, generate training data, update Skills, publish Skills, generate final legal opinions, generate final reports, send email, create public links, or trigger external delivery.

## Personal Production Pilot Dashboard Enhancement

v7.19 enhances `/personal-production-pilot` with dashboard status, metrics, quality score cards, gate status, optimization suggestions, review queue, source trace summary, export boundary, and unified safety presentation.

Quality scores and optimization suggestions are synthetic mock metadata for local pilot visibility only. They are not real case results, legal correctness guarantees, final legal opinions, formal lawyer reports, or external delivery artifacts.

## Fact Preview & Correction Workbench

v7.20 enhances `/personal-case-workspace` as the 事实预览与输入纠正工作台. It adds fact preview draft cards, owner correction metadata, fact version history, reference-only quality and gate metadata, source trace summary, owner-only download boundary, and legal analysis input readiness.

The fact workbench does not auto-trigger legal analysis, generate final fact findings, train on open cases, write to training sets, update Skills, publish Skills, generate final legal opinions, generate final reports, create real PDF/DOCX files, send email, create public links, or trigger external delivery.

## Legal Analysis Draft Workbench

v7.21 adds `/personal-case-analysis/legal-drafts` as the 法律分析草稿工作台. It creates legal analysis draft metadata from confirmed fact input metadata and presents legal analysis summary, dispute focus, claim basis, defense path, risk notes, next step checklist, version history, quality reference, gate reference, source trace, review queue, and owner-only download boundary.

Legal drafts remain metadata-only and draft-only. They are not final legal opinions, not final reports, not real PDF/DOCX files, and not external delivery artifacts.

## Skill Final Draft & Optimization Workbench

v7.22 adds `/personal-skill-studio/final-drafts` as the 两个 Skill 最终稿与优化工作台. It summarizes existing Skill baselines and supporting metadata into owner-only final draft metadata for `case_fact_extraction_skill` and `case_legal_analysis_skill`.

The v7.22 workbench does not re-invent the evaluation system, does not auto-publish Skills, does not train on open cases, does not write training sets, and does not trigger public links, email, final legal opinions, final reports, or external delivery.

## Owner-only Output Center

v7.23 adds `/personal-owner-output-center` as the 用户本人产出下载中心. It aggregates Skill final drafts, fact outputs, legal analysis drafts, and Pilot / Delivery drafts into one owner-only output registry.

All outputs are viewable and downloadable by the owner only. The center supports Markdown, JSON, PDF draft metadata, and DOCX draft metadata actions as mock metadata. It does not add a real export engine, does not create public links, does not send email, does not automatically deliver externally, does not mark output as final legal opinion, and does not mark output as a formal lawyer report.

Quality and gate metadata are only scoring and optimization references. They do not block owner-only downloads and do not trigger Skill publishing, training, final reports, final legal opinions, public links, email, or external delivery.

## Legal-Tech UI/UX Polish

v7.24 polishes the Personal Production page matrix with a mixed legal-tech workbench style. It standardizes shared badges, status cards, runtime cards, steppers, Trust / Safety panels, diagnostics, and info rows across the personal-version routes.

The five standard visible safety badges are: 受控运行、仅模拟结果、律师复核必需、来源可追踪、不自动对外交付. Diagnostics remain folded by default. Stepper final stages state that they will not trigger real export, final reports, or final legal opinions.

v7.24 does not add backend business logic, provider calls, real exports, final legal opinions, final reports, email, public links, Skill publishing, or external delivery.
