# Personal Production Demo Script & Screenshot Pack v7.9

## 定位

v7.9 将 AIHome.law Personal Production Pilot 的展示材料整理为可复用的演示脚本、截图路线、录屏路线、产品说明、PPT 大纲、README 展示段落和宣传视觉 brief。

本版本不是业务功能版本，不新增后端 runtime，不新增真实 provider live mode，不生成真实交付文件。所有内容仅用于 mock metadata 展示、个人生产验证和受控演示准备。

## 演示边界

- 当前是 Personal Production Alpha / Pilot 骨架。
- mock-first。
- provider-gated。
- metadata-only。
- draft-only。
- 律师复核必需。
- 来源可追踪。
- final-lock-required。
- 不生成最终法律意见。
- 不生成最终报告。
- 不自动对外交付。
- 不发送邮件。
- 不生成真实 PDF/DOCX。
- 不使用真实客户、真实案件、真实材料、真实判决或真实企业信息。
- 不承担律师判断，不承诺案件结果。

## 3-5 分钟中文演示脚本

### 0:00-0:25 开场

大家好，这里展示的是 AIHome.law Personal Production Pilot。它面向律师个人生产验证，目标是辅助组织受控流程，而不是承担律师判断。当前演示把材料处理、草稿生成、来源追踪、律师复核和交付包准备串联起来，只使用 mock metadata，不读取真实案件材料，也不调用真实 provider。

### 0:25-1:05 `/personal-production`

首先进入个人生产总控台。这里可以看到 readiness、runtime registry 和各阶段能力状态。这个页面的价值是让律师在一个入口上确认：哪些模块已经就绪，哪些仍保持受控、草案和 metadata-only 状态。注意这里的真实 provider 调用、外部交付和团队工作区都没有启用。

### 1:05-1:55 `/personal-showcase-pack`

接着进入个人生产试点与展示包。这个页面按 Story Flow 展示从案件录入、材料处理、AI 草稿、法律与企业信息核验、技能沉淀、交付包到最终锁定的路径。Pilot Sample Cards 只代表演示样本，不是正式案例结果。Trust / Safety Panel 明确提示未调用真实 provider、未读取 API key、未读取真实案件材料，也不会生成最终法律意见或最终报告。

### 1:55-2:45 `/personal-delivery-packet`

然后看个人生产交付包。这里展示交付包草案、交付项清单、来源追踪包、导出准备度和 Final Lock 队列。Final Lock 在这里只表示 metadata 层面的受控锁定，不触发真实导出，不发送邮件，不生成最终法律意见，也不生成真实 PDF/DOCX。

### 2:45-3:30 `/personal-case-production`

再进入受控案件生产工作流。这个页面把材料处理、草稿分析、信息核验和律师复核门禁串联起来。Review Gate 和 Final Gate 的意义是把 AI 辅助过程放在律师复核之后，而不是把草稿直接作为最终结论。

### 3:30-4:10 Safety / Trust Panel

最后回到任一页面的 Trust / Safety Panel。演示结束前需要再次强调：当前所有页面仅为 mock metadata 展示；系统不生成最终法律意见，不生成最终报告，不自动对外交付，也不读取真实案件材料。律师复核、来源追踪和最终锁定是整个流程的基本边界。

### 4:10-4:30 收束

v7.9 的重点是把 v7.0-v7.8 已完成的受控能力整理成可讲述、可截图、可录屏的展示包。下一步继续打磨个人版公开展示、README、演示入口和安全边界；Team Workspace 后置，External Client Delivery 后置。

## 截图清单

| # | 页面路径 | 截图标题 | 截图目的 | 必须可见的安全文案 | 不应出现的内容 |
|---|---|---|---|---|---|
| 1 | `/personal-production` | 个人生产总控台 | 展示总览、readiness 和 runtime registry | 律师复核必需、来源可追踪 | API key、本地路径、真实材料 |
| 2 | `/personal-production` | Runtime 能力矩阵 | 展示各 runtime 处于受控状态 | 受控运行、不自动对外交付 | live provider enabled |
| 3 | `/personal-showcase-pack` | Story Flow 演示线 | 展示 v7.3-v7.6 能力串联 | mock metadata、律师复核必需 | 真实客户名、真实案号 |
| 4 | `/personal-showcase-pack` | Pilot Sample Cards | 展示演示样本结构 | 当前仅为展示与验证流程 | 真实案件事实、真实判决内容 |
| 5 | `/personal-showcase-pack` | Trust / Safety Panel | 展示安全边界 | 未调用真实 provider、未读取 API key | secret、local path |
| 6 | `/personal-delivery-packet` | 交付包草案 | 展示交付包 metadata 骨架 | 不生成最终法律意见 | 最终法律意见正文 |
| 7 | `/personal-delivery-packet` | 来源追踪与导出准备度 | 展示 source trace 与 export readiness | 来源可追踪、不自动对外交付 | 真实 PDF/DOCX 文件 |
| 8 | `/personal-delivery-packet` | Final Lock 队列 | 展示最终锁定门禁 | final lock 不触发真实导出 | 邮件发送、真实导出按钮 |
| 9 | `/personal-case-production` | 受控案件生产流程 | 展示 workflow stage 和 review gate | metadata-only、律师复核必需 | 真实案件材料原文 |
| 10 | `/personal-skill-studio` | 经验包与技能候选草案 | 展示草案和未发布边界 | 未自动发布、律师复核必需 | 正式 Skill 发布承诺 |
| 11 | `/personal-intelligence` | 来源追踪候选 | 展示 mock 法律/企业信息核验 | 仅模拟结果、来源可追踪 | 真实查询结果 |
| 12 | `/personal-ai-gateway` | 草稿 Runtime | 展示 prompt preview 不是最终意见 | draft-only、不生成最终法律意见 | 最终法律意见标题 |

## 录屏路线

| 顺序 | 页面 | 建议停留 | 解说重点 | 安全边界提示 |
|---|---|---:|---|---|
| 1 | `/personal-production` | 45 秒 | 总控台、readiness、runtime registry | 未启用真实 provider 和外部交付 |
| 2 | `/personal-showcase-pack` | 70 秒 | Story Flow、Pilot Sample、Trust / Safety | 演示样本是 mock metadata |
| 3 | `/personal-delivery-packet` | 65 秒 | 交付包草案、来源追踪、Final Lock | 不生成真实 PDF/DOCX，不发送邮件 |
| 4 | `/personal-case-production` | 50 秒 | 受控工作流、review gate、final gate | 草稿必须经过律师复核 |
| 5 | 任一 Trust / Safety Panel | 30 秒 | 收束安全边界 | 不生成最终法律意见，不自动对外交付 |

### 录屏前检查项

- 页面使用 mock sample。
- 浏览器地址不显示本地绝对路径截图。
- Developer Diagnostics 保持折叠，除非仅展示 metadata JSON。
- 不展示 API key、secret、raw content 或真实案件材料。
- 不把 Pilot Sample 口播为真实案例。

## 一页式产品说明

### 产品定位

AIHome.law Personal Production Pilot 是面向律师个人生产验证的受控工作流展示骨架，用于组织案件生产中的 metadata、来源追踪、律师复核、交付包准备和最终锁定。

### 适用场景

- 律师个人工作流验证。
- 内部产品演示。
- 受控 AI 辅助草稿流程说明。
- 来源追踪和复核门禁展示。
- 非真实案件的培训与试点演示。

### 核心能力

- Personal Production 总控台。
- AI Gateway 草稿 Runtime。
- Material Runtime 与 OCR preview。
- Legal & Enterprise Intelligence mock gateway。
- Experience Package Skill Studio。
- Controlled Case Production Workflow。
- Personal Delivery Packet。
- Showcase Pack Story Flow。

### 安全边界

- mock-first。
- provider-gated。
- metadata-only。
- draft-only。
- 律师复核必需。
- 来源可追踪。
- final-lock-required。
- 不生成最终法律意见。
- 不自动对外交付。

### 当前阶段

当前为 Personal Production Alpha / Pilot 展示阶段，适合说明架构、流程和安全边界，不作为外部客户交付版本。

### 下一步路线

- v7.10 Personal Version Polish & Public Demo Readiness，继续打磨个人版公开展示文案。
- v7.11 Personal Production Stability & Local Pilot Hardening。
- AI Provider Live Gateway、OCR / Document Provider Live Gateway、Legal / Enterprise API Live Gateway、Skill Training、Controlled Case Analysis 后续受控推进。
- v7.11-v7.17 作为连续大阶段推进，最后统一做完整安全审计。
- Team Workspace 后置。
- External Client Delivery 后置。

## PPT 大纲

1. 问题背景：律师 AI 工具需要可控、可复核、可追踪。
2. AIHome.law 定位：律师工作流辅助，而非最终结论替代。
3. Personal Production 工作流：从材料到草稿、核验、复核、交付包。
4. Story Flow 演示：v7.3-v7.6 能力如何串联。
5. Source Trace / Lawyer Review：来源可追踪，律师复核必需。
6. Delivery Packet / Final Lock：交付包草案与受控锁定。
7. Safety Boundary：不生成最终法律意见，不自动对外交付。
8. 技术架构：mock-first、provider-gated、metadata-only runtime。
9. 当前进展：v7.0-v7.8 已完成能力矩阵。
10. 下一步路线：v7.10 个人版公开展示 polish 与 v7.11 本地试点稳定性加固。

## README 展示段落

### 中文

AIHome.law Personal Production Pilot 是一个 mock-first、controlled runtime 的律师个人生产验证骨架。它把 AI 草稿、材料处理、法律与企业信息 mock 核验、Experience Package、受控案件生产、交付包草案、Source Trace、Lawyer Review 和 Final Lock 组织成可演示流程。当前阶段仅展示 metadata，不生成最终法律意见，不生成最终报告，也不自动对外交付。

### English

AIHome.law Personal Production Pilot is a mock-first, controlled-runtime workflow for validating personal legal production flows. It connects AI draft assistance, material processing, legal and enterprise mock intelligence, experience packages, controlled case production, delivery packet drafts, Source Trace, Lawyer Review, and Final Lock into a showcase-ready process. The current stage is metadata-only and does not generate final legal opinions, final reports, or automatic external delivery.

## 宣传视觉 Brief

### Hero visual 方向

以律师工作台、流程面板、来源追踪节点和复核门禁为主视觉。画面应表现“受控、清晰、专业”，不要表现系统自动裁判或承担律师判断。

### 社媒图方向

使用 3-4 个简洁模块：Story Flow、Source Trace、Lawyer Review、Final Lock。每张图都保留 mock metadata 或 controlled runtime 的边界提示。

### 展示图方向

适合官网或路演使用的横向构图：左侧是 Personal Production flow，右侧是 Trust / Safety Panel。建议用抽象 UI mock，不使用真实客户或真实案件截图。

### 色彩 / 氛围建议

低饱和蓝绿、墨色、白色与轻微金色点缀；整体气质应接近法律行业的专业工具，而不是夸张营销海报。

### 禁止视觉元素

- 夸张法槌胜诉暗示。
- 金钱赔付保证。
- 自动判案机器人。
- 真实客户照片。
- 真实案件材料截图。
- 任何暗示不需要律师的视觉符号。

## 禁用表达清单

以下表达仅作为安全审查负面清单存在，不应用于宣传正文、按钮、标题或截图标题：

- 自动胜诉。
- 替代律师。
- 保证准确。
- 自动出具最终法律意见。
- 自动完成客户交付。
- 一键交付。
- 全自动办案。
- 自动发送客户。
- 智能判案。
- 包赢。
- 无需律师。

## 安全审查清单

- 是否暗示系统可以承担律师判断。
- 是否暗示可以自动输出最终法律意见。
- 是否暗示可以自动完成外部交付。
- 是否包含真实材料、真实客户、真实案件、真实判决或真实企业信息。
- 是否包含 API key、secret、token 或本地路径。
- 是否把 mock sample 说成真实案例。
- 是否误导为已进入外部客户交付版本。
- 是否把 Developer Diagnostics 中的 metadata 当作业务结论展示。
