# Personal Production Stability & Local Pilot Hardening v7.11

## 定位

v7.11 属于 v7.10-v7.17 Personal Live Intelligence & Controlled Case Analysis 连续大阶段。本阶段不接真实 AI、不调用真实 OCR、不调用真实法律检索或企业信息 API，不新增团队版和外部客户交付。

v7.11 的目标是加固个人版本地运行稳定性，为后续 AI Provider Live Gateway、OCR / Document Provider Live Gateway、Legal / Enterprise API Live Gateway、Skill Training Runtime、Controlled Case Analysis Runtime 和 Real AI Gated Pilot 做地基。

## 本地运行约定

- 后端端口：8001。
- 前端端口：3001。
- 本地启动脚本：`scripts/dev/start_personal_local_pilot.sh`。
- 后端启动不使用 reload，避免重复进程影响本地 pilot。
- 启动前检查端口占用。
- 后端启动后先检查 `/health`。
- 前端通过 `NEXT_PUBLIC_API_BASE_URL` 指向本地后端。

## 页面稳定性

v7.11 统一了个人生产页面矩阵的安全 fallback：

- `/personal-production`
- `/personal-showcase-pack`
- `/personal-delivery-packet`
- `/personal-case-production`
- `/personal-skill-studio`
- `/personal-intelligence`
- `/personal-material-runtime`
- `/personal-ai-gateway`

当 API 加载失败时，页面显示中文安全 fallback，不显示后端 stack、本地路径、API key 或 raw content。Trust / Safety Panel 保持可见，Developer Diagnostics 继续默认折叠。

## API Client 稳定性

前端 API client 继续使用 `NEXT_PUBLIC_API_BASE_URL` 或本地默认 `http://127.0.0.1:8001`。错误消息不再原样展示后端 detail，避免把 stack trace、本地路径或 provider 细节透出到 UI。

当前展示口径：

- live provider disabled。
- AI Provider Live Gateway 后续受控接入。
- OCR / Document Provider Live Gateway 后续受控接入。
- Legal / Enterprise API Live Gateway 后续受控接入。
- Skill Training 后续受控训练。
- Controlled Case Analysis 后续草稿分析。
- 不生成最终法律意见。
- 不自动对外交付。

## 本地 Pilot 路径

建议按以下顺序进行本地试点：

1. `/` 首页。
2. `/personal-production` 个人生产总控台。
3. `/personal-showcase-pack` 公开演示入口。
4. `/personal-delivery-packet` 交付包草案。
5. `/personal-case-production` 受控案件生产工作流。
6. `/personal-ai-gateway` AI 草稿 Runtime。
7. `/personal-material-runtime` 材料与 OCR Runtime。
8. `/personal-intelligence` 法律与企业信息网关。
9. `/personal-skill-studio` 经验包与技能工作室。

该路径仅用于个人本地试点和 mock metadata 展示，不生成最终法律意见、不生成最终报告、不自动对外交付。

## 轻量验收

v7.11 子阶段只运行轻量检查：

- `git diff --check`
- `find . -name "*.md" -size 0`
- `bash scripts/regression/check_personal_public_demo_readiness.sh`
- `bash scripts/regression/check_personal_local_pilot_stability.sh`
- frontend build if frontend files changed

不要求 full Personal Alpha regression，不做 Codex Security full audit，不 commit/tag/release。

## 后续

下一步进入 v7.12 AI Provider Live Gateway。Team Workspace 后置，External Client Delivery 后置。完整 regression、final security audit、commit、tag 和 release 将在 v7.17 完成后统一执行。
