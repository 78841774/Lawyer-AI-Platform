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

Team Workspace deferred / 团队版后置。External Client Delivery deferred / 外部交付后置。当前个人版连续大阶段已经包含 v7.25-v7.37：实战试运行准备、真实接口接入准备、OCR / 文档接口受控接入、个人生产统一受控接口接入总控台、法律检索与企业信息 API 受控接入、Codex 训练方案与多层级案由训练产物加载器、已结案件 Codex 训练执行、真实已结案件训练材料导入与脱敏管线、受控经验候选管线、Skill Experience Pool 与 Codex Skill 草案生成器、Skill Package 版本化封装与系统校验、Internal Training / Experience Package Builder、Practice Runtime Load Review Gate、Practice Runtime Controlled Loading & Monitoring、Practice Runtime Output Observation & Lawyer Feedback Loop、Practice Feedback Candidate Pack、Next Experience Package Rebuild、Experience Lifecycle Consolidation、Case Analysis Skill Output Schema Driven Workbench、Case Analysis Output Feedback to Experience Improvement Candidate、Training Dataset Builder & Training Gate、Codex Skill Training Dry Run、Codex Skill Internal Training Run。v7.34-v7.37 已在 `v7.37` 标签目标提交完成，v7.35/v7.36/v7.37 标签指向该连续阶段提交。

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

## Personal Practical Case Trial Readiness

v7.25 adds `/personal-trial-readiness` as the 个人版实战试运行准备 workbench. It records trial session metadata, trial checklist status, stage observations, issue logs, reference-only quality review, safety confirmation, optimization backlog, audit, and safety metadata before moving into practical case trial use.

The v7.25 workbench is owner-only, metadata-only, draft-only, and reference-only. It does not read real case raw content, call real providers, read API keys, train on open cases, write training sets, publish Skills, create final legal opinions, create final reports, generate real PDF/DOCX files, create public links, send email, or trigger external delivery. Issue logs and quality review are optimization input only and do not block the next stage.

## Provider Live Readiness & Secret Boundary

v7.26 adds `/personal-provider-readiness` as the 真实接口接入准备 page. It creates a unified provider readiness layer before any real OCR / AI / legal search / enterprise provider connection.

The runtime only returns provider registry metadata, key-loaded booleans, secret boundary status, live gate status, usage / cost dry-run metadata, provider dry-run health, audit, and safety metadata. It does not read or expose key values, does not call providers, does not upload case materials, does not train, does not run practical case analysis, and does not generate final legal opinions, formal reports, real files, email, public links, or external delivery.

## OCR / Document Provider Live Connection

v7.27 adds OCR / 文档接口受控接入 under `personal_material_runtime.live_gateway` and `/personal-material-runtime/live/*`. It provides OCR / Document provider registry metadata, secret boundary, live gate, dry-run health, review queue, source trace, audit, and safety metadata. It does not add an independent OCR route; the live connection layer intentionally extends the existing material runtime.

## Unified Personal Live Connection Dashboard

v7.28 adds `/personal-live-connection` as the 个人生产统一受控接口接入总控台. It uses `personal_live_connection` to summarize AI / OCR / Document / Legal / Enterprise provider readiness, secret boundary, live gate, usage / cost, health, audit, and safety metadata. It is not a standalone AI Provider Live Connection; AI Provider is one category in the unified dashboard.

## Legal / Enterprise API Live Connection

v7.29 adds `/personal-legal-enterprise` as 法律检索与企业信息 API 受控接入. It uses `personal_legal_enterprise_gateway` for legal search / enterprise lookup dry-runs, live gate, secret boundary, review queue, source trace, audit, and safety metadata. Legal search results only enter source trace and lawyer review metadata, and enterprise lookup results do not automatically become final fact findings.

## Codex Training Scheme & Multi-Level Case-Cause Artifact Loader

v7.30 adds `/personal-skill-studio/training-artifacts` as Codex 训练方案、多层级案由经验包与训练产物加载器. Codex training here means metadata artifact generation and loading, not model fine-tuning. It defines synthetic multi-level case-cause taxonomy, experience package manifests, two core Skill manifests, evaluation / gate / test case manifests, loading manifest, fallback matching, Skill Context dry-run, and regression checks.

v7.30 does not execute real training, does not read real case material or raw OCR, does not read API keys, does not use open cases for training, does not update or publish Skills, and does not generate final legal opinions, final reports, real files, public links, email, or external delivery.

## Codex Training on Closed Case Samples

v7.31 adds `/personal-skill-studio/training-artifacts/training-runs` as 已结案件 Codex 训练执行. It uses synthetic closed-case samples with `source_case_mode=synthetic_closed_case` when no real redacted closed-case sample set is read. It generates training run manifest metadata, experience package metadata, generated Skill manifests for `case_fact_extraction_skill` and `case_legal_analysis_skill`, evaluation / gate / test case manifests, loading manifest metadata, and v7.30 loader dry-run validation metadata.

v7.31 does not fine-tune model parameters, does not read real case material or raw OCR, does not read API keys, does not use open or unresolved cases for training, does not write training sets, does not update or publish Skills, and does not generate final legal opinions, final reports, real files, public links, email, or external delivery.

## Real Closed-Case Training Intake & Redaction

v7.31a adds `/personal-skill-studio/training-artifacts/real-closed-case-*` as 真实已结案件训练材料导入与脱敏管线. It prepares authorized closed-case training material metadata through intake, redaction, multi-level case-cause classification, training sample segmentation, review queue, source trace, audit, and safety checks.

v7.31a only prepares training material and does not execute Codex training. It does not use unresolved/open cases, does not return raw content or raw OCR, does not read API keys, does not write training sets, does not update or publish Skills, and does not create final legal opinions, final reports, public links, email, or external delivery. Redaction preserves legally necessary metadata such as jurisdiction context, age/capacity context, subject type, contract type, object type, timeline markers, and evidence type.

## Controlled Experience Pipeline

v7.31b adds `/personal-skill-studio/training-artifacts/raw-work-product-boundary/status`, `/ocr-jobs`, `/legal-retrieval-jobs`, and `/experience-candidates/*` as the controlled lawyer work-product experience extraction pipeline. It produces redacted, source-traced, audited, manually reviewed experience candidate metadata only.

## Skill Experience Pool & Draft Builder

v7.31c adds `/personal-skill-studio/training-artifacts/skill-experience-pool/*`, `/skill-experience-bindings/*`, and `/codex-skill-drafts/*`. It imports only v7.31b `approved_for_skill_experience` candidates, creates non-publishable Codex Skill draft metadata, and keeps all draft confirmation manual.

## Skill Package Versioning & System Validation Gate

v7.31d adds `/personal-skill-studio/training-artifacts/skill-packages/*`. It packages confirmed v7.31c Skill Draft metadata into versioned Skill Package metadata, generates manifest/source trace/audit bundles, and runs a system validation gate. Training-output manual review is not applicable in v7.31d and practice runtime load review is deferred to v7.31f.

## Internal Training / Experience Package Builder

v7.31e adds `/personal-skill-studio/training-artifacts/training-tasks/*` and `/personal-skill-studio/training-artifacts/training-packages/*`. It builds internal training task metadata and experience package metadata only from v7.31d system-validated Skill Packages. Experience packages move to `pending_practice_load_review` for v7.31f.

## Practice Runtime Load Review Gate

v7.31f adds `/personal-skill-studio/training-artifacts/practice-load-review/*`. It preserves generated experience packages as read-only metadata, lets lawyers edit experience cards, saves lawyer-approved package metadata, reruns system revalidation, and approves or rejects future practice runtime loading candidates. Actual controlled loading is deferred to v7.31g.

## Practice Runtime Controlled Loading & Monitoring

v7.31g adds controlled practice runtime loading for v7.31f lawyer-approved package metadata. It records runtime registry state, policy evaluation, usage monitoring, risk events, audit, source trace, disable, and rollback metadata. It does not read source content, call providers, update Skills, trigger real training, generate final legal opinions, generate final reports, or trigger external delivery.

## Practice Runtime Output Observation & Lawyer Feedback Loop

v7.31h records redacted output observation metadata, lawyer feedback metadata, risk event metadata, rule-based classification, audit, source trace, and feedback summaries. Feedback may become later iteration input, but it does not automatically mutate loaded packages, disable, rollback, update Skills, trigger training, or trigger external delivery.

## Practice Feedback Candidate Pack

v7.31i builds next-iteration candidate pack metadata from triaged v7.31h feedback/risk/observation metadata. Candidate packs are preparation metadata only and do not modify loaded packages, lawyer-approved packages, runtime policy, Skills, training artifacts, or delivery state.

## Next Experience Package Rebuild

v7.31j rebuilds next experience package draft metadata from ready v7.31i candidate packs. A draft may enter `pending_practice_load_review`, but it is not loaded into practice runtime and still requires a later review boundary before any controlled runtime use.

## Experience Lifecycle Consolidation

v7.32 adds experience lifecycle state, graph, audit timeline, source trace view, integrity check, and safety summary across v7.31b-v7.31j. Recompute is view-level only and does not mutate package content, runtime state, Skills, training artifacts, or delivery state.

## Case Analysis Skill Output Schema Workbench

v7.33 adds the Case Analysis Skill Output Schema Driven Workbench inside `/personal-skill-studio/training-artifacts`. Backend `CaseAnalysisSkillOutputSchema` defines fact extraction and legal analysis output groups, and the frontend renders backend `output_groups` only. The workbench supports output filtering, detail view, mark-reviewed, lawyer feedback, risk events, audit, and source trace metadata.

v7.33 does not process unredacted lawyer work product, does not expose raw case material or OCR text, does not call providers, does not read API keys, does not hardcode frontend output definitions, does not update Skills, does not trigger training, and does not generate final legal opinions, formal reports, real files, public links, email, or external delivery.

## Case Analysis Improvement Candidate

v7.34 adds the Case Analysis Output Feedback to Experience Improvement Candidate layer inside `/personal-skill-studio/training-artifacts`. It maps v7.33 output feedback, risk event, audit, and source trace metadata into improvement candidates, output-to-experience traces, diff summaries, and readiness reports for later v7.35 Training Dataset Builder & Training Gate use.

v7.34 does not modify loaded packages, lawyer-approved packages, or output schema metadata; does not trigger training, replace runtime packages, publish Skills, call providers, read key values, generate final legal opinions, generate formal reports, create real files, public links, email, or external delivery.

## Training Dataset Builder & Gate

v7.35 adds Training Dataset Manifest, abstracted Training Examples, Training Task Plan, and reference-only Training Gate Report metadata inside `/personal-skill-studio/training-artifacts`. It uses only v7.34 improvement candidates marked `ready_for_training_dataset_build` and preserves candidate, package, Skill output schema, output-to-experience trace, audit, and source trace lineage.

v7.35 does not execute real training, call providers, read key values, use open cases automatically, mutate loaded packages, update Skills, publish Skills, generate final legal opinions, generate formal reports, create files, public links, email, or external delivery.

## Codex Skill Training Dry Run

v7.36 adds Codex Skill Training Dry Run status, logs, and gate report metadata. It reuses the v7.35 dataset and gate artifacts and performs an internal simulation only.

Dry-run logs remain owner-only, metadata-only, redacted / abstracted, audited, and source-traced. v7.36 does not call providers, read key values, access external training services, replace runtime packages, update Skills, publish Skills, or trigger external delivery.

## Codex Skill Internal Training Run

v7.37 adds Codex Skill Internal Training Run status, metrics, logs, dry-run comparison, and gate report metadata. The training run is an internal workspace metadata flow and does not replace runtime packages or publish Skills.

v7.37 does not call external providers, read key values, expose raw case material or raw OCR text, expose local paths, mutate loaded packages, generate final legal opinions, generate formal reports, create PDF/DOCX files, public links, email, or external delivery.

## Next Step

The implementation is complete through v7.37 in the local worktree. The next recommended step is user-confirmed release handling or an explicitly scoped next personal-version sub-stage. Codex training remains metadata artifact generation/loading, not automatic public Skill publishing or external model training.
