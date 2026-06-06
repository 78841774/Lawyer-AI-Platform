# Personal Version Polish & Public Demo Readiness v7.10

## 定位

v7.10 继续打磨 AIHome.law Personal Production Pilot 的个人版展示体验。它不是新的业务 runtime，不接入真实 provider，不新增团队版，也不新增外部客户交付。

本版本重点让首次访问者更快理解当前产品状态：个人版生产验证、mock-first、controlled runtime、mock metadata、律师复核必需、来源可追踪、Final Lock 仅为受控 metadata 门禁。

## Product Design 审计摘要

审计覆盖首页、README 展示段落、个人生产总控台、Showcase Pack、Delivery Packet、受控案件生产工作流、Skill Studio、Intelligence Gateway、Material Runtime 和 AI Gateway。

主要结论：

- 首页需要更明确地指向个人版生产验证，而不是泛化工作空间。
- README 需要在首屏说明 Personal Production Pilot、mock-first、controlled runtime 和安全边界。
- `/personal-production` 应作为个人版总控台，展示当前阶段、已完成能力链路、后续个人版路线，以及 Team Workspace deferred / External Client Delivery deferred。
- `/personal-showcase-pack` 应作为公开演示入口，突出 3-5 分钟演示路线、synthetic mock metadata、Trust / Safety Panel。
- `/personal-delivery-packet` 必须强调交付包草案不是最终交付文件，Final Lock 不触发真实导出。
- Developer Diagnostics 应保持默认折叠，只展示安全 metadata，不展示 raw content、本地路径或 secret。

## 本轮落地

- README 增强中英双语 Personal Production Pilot 展示段落。
- 首页 Hero 改为个人版生产验证和公开演示准备入口。
- AppShell 文案改为个人版生产验证，个人生产分组保持不变。
- `/personal-production` 增强个人生产验证、后续个人版路线、Team Workspace deferred 和 External Client Delivery deferred。
- `/personal-showcase-pack` 增强公开演示入口、3-5 分钟演示路线和 synthetic mock metadata 边界。
- `/personal-delivery-packet` 增强 Delivery Packet draft 和 Final Lock 安全边界。
- 新增 public demo readiness regression，覆盖 README、页面文案、后续路线、安全边界和敏感字符串检查。

## 当前安全边界

- mock-first。
- controlled-first。
- provider-gated。
- metadata-only。
- draft-only。
- lawyer-review-required / 律师复核必需。
- source-trace-required / 来源可追踪。
- final-lock-required / 最终锁定必需。
- 未调用真实 provider。
- 未读取 API key。
- 未读取真实案件材料。
- 不生成最终法律意见。
- 不生成最终报告。
- 不生成真实 PDF/DOCX。
- 不发送邮件。
- 不自动对外交付。

## 后续个人版路线

- v7.11 Personal Production Stability & Local Pilot Hardening。
- v7.12 AI Provider Live Gateway 后续受控接入。
- v7.13 OCR / Document Provider Live Gateway 后续受控接入。
- v7.14 Legal / Enterprise API Live Gateway 后续受控接入。
- v7.15 Skill Training 后续受控训练。
- v7.16 Controlled Case Analysis 后续草稿分析。
- v7.17 Personal Production Pilot with Real AI Gated Mode。
- Final Security Audit for Personal Live Intelligence & Controlled Case Analysis。
- Team Workspace deferred / 团队版后置。
- External Client Delivery deferred / 外部交付后置。

## 后续大阶段节奏

v7.11-v7.17 作为 Personal Live Intelligence & Controlled Case Analysis 连续大阶段推进。每个子阶段运行必要的 compile、build、API smoke、full Personal Alpha regression、敏感路径检查、provider live boundary smoke check 和禁止文案检查。

中途不为每个小功能生成完整 Codex Security audit ledger。等 v7.17 完成并通过基础验收后，再统一执行 Final Security Audit，覆盖本大阶段所有新增模块、接口、前端、脚本、文档和 Project Context。

## Product Design 闭环规则

从 v7.10 开始，所有 UI polish、Showcase、产品宣传页面、Demo page、Landing page、README visual alignment、前端页面样式、截图和录屏体验相关任务，都必须形成 Product Design 闭环。

### 设计输入

- 使用 Product Design get-context / ideation / prototype brief；如果当前 Codex 环境没有暴露可调用 Product Design 工具，需要明确说明。
- 输出 2-3 个设计方向。
- 明确推荐方向。

### 设计选择

- 明确采用哪个方向。
- 说明为什么适合当前阶段。
- 说明不采用其他方向的原因。

### 代码落地

- 将选定设计转化为 React / TypeScript / Tailwind 代码。
- 优先落地为共享组件，而不是只改单页。
- 如已有组件，应复用或升级 SafetyBadge、StatusCard、RuntimeCard、ShowcaseStepper、TrustSafetyPanel、DiagnosticsPanel 和 AppShell navigation。

### 可见变化要求

必须至少有一类页面可见变化：

- Hero 区域视觉增强。
- 卡片布局明显优化。
- Stepper 结构更新。
- Trust / Safety Panel 位置或视觉增强。
- AppShell 导航更清楚。
- 中文文案更产品化。
- 页面截图 / 录屏路线更顺。
- 旧调试感降低。

如果代码改动后网页视觉没有明显变化，不得声称 Product Design 已完成落地。

### 浏览器验收

完成前端改动后，应在环境允许时：

- 启动后端。
- 启动前端。
- 用 Browser / Computer Use 打开目标页面。
- 检查页面是否真实加载。
- 检查设计变化是否可见。
- 检查 Diagnostics 是否默认折叠。
- 检查没有 raw content、API key、本地路径。
- 检查截图 / 录屏友好度。

### 设计落地报告

最终报告必须包含：

- Product Design 是否实际调用。
- 采用的设计方向。
- 哪些组件被新增或修改。
- 哪些页面发生了可见 UI 变化。
- 变化前的问题。
- 变化后的效果。
- 浏览器查看结果。
- 仍未解决的 UI 问题。

禁止用“已使用 Product Design”“已完成 ideation”“已输出 prototype brief”“建议后续落地”作为完成依据，除非同时完成代码落地、页面打开、可见变化确认和浏览器验收。

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
- 团队协作已上线。
- 外部客户交付已上线。
- 正式生产上线。
- 已接入真实 AI 自动分析。
- 自动案件分析。
- 自动训练成专家。

## 验收建议

- `check_personal_public_demo_readiness.sh`
- `check_personal_demo_pack_docs.sh`
- `check_personal_ui_polish.sh`
- full Personal Alpha regression suite
- frontend build if frontend pages changed
- local security review for public-facing copy

后续 UI 版本还应增加或更新 regression，检查目标页面存在、统一组件被引用、DiagnosticsPanel 默认折叠、TrustSafetyPanel 出现、禁止夸大文案不存在、页面文案包含 mock-first / 律师复核 / 不自动对外交付，以及 AppShell 导航包含对应入口。
