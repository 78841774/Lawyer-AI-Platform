type BadgeTone = "safe" | "info" | "warning" | "muted" | "blocked";

export const CORE_SAFETY_ITEMS = [
  "受控运行",
  "仅模拟结果",
  "律师复核必需",
  "来源可追踪",
  "不自动对外交付"
];

export function SafetyBadge({ label, tone = "safe" }: { label: string; tone?: BadgeTone }) {
  const tones: Record<BadgeTone, string> = {
    safe: "border-emerald-200 bg-emerald-50 text-emerald-800",
    info: "border-cyan-200 bg-cyan-50 text-cyan-800",
    warning: "border-amber-200 bg-amber-50 text-amber-800",
    muted: "border-stone-200 bg-stone-50 text-stone-700",
    blocked: "border-rose-200 bg-rose-50 text-rose-800"
  };
  return <span className={`inline-flex min-h-7 items-center rounded-md border px-3 py-1 text-xs font-semibold ${tones[tone]}`}>{label}</span>;
}

export function DarkSafetyBadge({ label }: { label: string }) {
  return <span className="inline-flex min-h-7 items-center rounded-md border border-cyan-200/30 bg-cyan-100/10 px-3 py-1 text-xs font-semibold text-cyan-50">{label}</span>;
}

export function StatusPill({ label, tone = "info" }: { label: string; tone?: BadgeTone }) {
  return <SafetyBadge label={label} tone={tone} />;
}

export function Panel({ title, eyebrow, children }: { title: string; eyebrow?: string; children: React.ReactNode }) {
  return (
    <section className="rounded-md border border-line bg-white p-5 shadow-sm ring-1 ring-transparent">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          {eyebrow ? <div className="text-xs font-semibold text-cyan-700">{eyebrow}</div> : null}
          <h2 className="text-lg font-semibold text-ink">{title}</h2>
        </div>
      </div>
      <div className="mt-4">{children}</div>
    </section>
  );
}

export function StatusCard({
  label,
  value,
  detail,
  tone = "info"
}: {
  label: string;
  value: string | number | boolean;
  detail?: string;
  tone?: BadgeTone;
}) {
  return (
    <div className="min-h-[138px] rounded-md border border-line bg-white p-4 shadow-sm">
      <div className="text-xs font-semibold text-cyan-700">{label}</div>
      <div className="mt-2 break-words text-xl font-semibold leading-snug text-ink">{String(value)}</div>
      {detail ? <div className="mt-2 text-xs leading-5 text-muted">{detail}</div> : null}
      <div className="mt-3">
        <StatusPill label={tone === "blocked" ? "未就绪" : tone === "warning" ? "需复核" : tone === "safe" ? "已受控" : "运行中"} tone={tone} />
      </div>
    </div>
  );
}

export function RuntimeCard({
  title,
  category,
  status,
  items,
  targetRoute
}: {
  title: string;
  category: string;
  status: string;
  items: Array<[string, unknown]>;
  targetRoute?: string;
}) {
  return (
    <div className="rounded-md border border-line bg-stone-50 p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm font-semibold text-ink">{title}</div>
          <div className="mt-1 text-xs text-muted">{category}</div>
        </div>
        <StatusPill label={status} tone={status.includes("live") ? "warning" : "info"} />
      </div>
      <div className="mt-4 grid gap-2 text-xs text-muted">
        {items.map(([label, value]) => (
          <div key={label} className="grid gap-1 rounded-md border border-white bg-white/80 px-3 py-2 md:grid-cols-[150px_1fr]">
            <span className="font-medium">{label}</span>
            <span className="break-all text-right text-ink">{String(value ?? "pending")}</span>
          </div>
        ))}
        {targetRoute ? (
          <div className="grid gap-1 rounded-md border border-white bg-white/80 px-3 py-2 md:grid-cols-[150px_1fr]">
            <span className="font-medium">target_route</span>
            <span className="break-all text-right text-ink">{targetRoute}</span>
          </div>
        ) : null}
      </div>
    </div>
  );
}

export function ShowcaseStepper({
  steps,
  columns = "lg:grid-cols-7"
}: {
  steps: Array<{ label: string; detail?: string; status?: string }>;
  columns?: string;
}) {
  return (
    <div className={`grid gap-3 ${columns}`}>
      {steps.map((step, index) => {
        const isFinalStep = index === steps.length - 1;
        return (
        <div key={`${step.label}-${index}`} className="min-h-[160px] rounded-md border border-line bg-white p-4 shadow-sm">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-cyan-900 text-sm font-semibold text-white">{index + 1}</div>
          <div className="mt-3 text-sm font-semibold text-ink">{step.label}</div>
          {step.detail ? <div className="mt-2 text-xs leading-5 text-muted">{step.detail}</div> : null}
          {step.status ? <div className="mt-3"><StatusPill label={step.status} tone="info" /></div> : null}
          {isFinalStep ? (
            <div className="mt-3 rounded-md border border-amber-200 bg-amber-50 px-2 py-1 text-xs leading-5 text-amber-900">
              不会触发真实导出/最终报告/最终法律意见
            </div>
          ) : null}
        </div>
      );})}
    </div>
  );
}

export function TrustSafetyPanel({
  items = CORE_SAFETY_ITEMS,
  title = "信任与安全面板",
  note = "仅展示受控元数据，不暴露原始内容、本地路径或密钥值。"
}: {
  items?: string[];
  title?: string;
  note?: string;
}) {
  const mergedItems = Array.from(new Set([...CORE_SAFETY_ITEMS, ...items]));
  return (
    <Panel title={title} eyebrow="安全边界">
      <div className="grid gap-2 md:grid-cols-2">
        {mergedItems.map((item) => (
          <div key={item} className="flex min-h-11 items-center justify-between gap-3 rounded-md border border-line bg-stone-50 px-3 py-2">
            <span className="text-sm text-ink">{item}</span>
            <StatusPill label="已启用" tone="safe" />
          </div>
        ))}
      </div>
      <div className="mt-4 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">{note}</div>
    </Panel>
  );
}

export function DiagnosticsPanel({ data, title = "开发诊断（默认折叠）" }: { data: unknown; title?: string }) {
  return (
    <details className="rounded-md border border-line bg-slate-950 text-slate-100">
      <summary className="cursor-pointer px-4 py-3 text-sm font-medium text-slate-200">{title}</summary>
      <pre className="max-h-[420px] overflow-auto border-t border-slate-800 p-4 text-xs leading-5">
        {JSON.stringify(data, null, 2)}
      </pre>
    </details>
  );
}

export function SafeErrorNotice({
  title = "本地 API 暂不可用",
  message = "页面已进入安全 fallback。请确认后端运行在 8001、前端运行在 3001；当前仍保持 mock-first、provider-gated、律师复核必需，不会调用真实 provider 或显示敏感信息。"
}: {
  title?: string;
  message?: string;
}) {
  return (
    <div className="rounded-md border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-900">
      <div className="font-semibold">{title}</div>
      <div className="mt-1 leading-6">{message}</div>
    </div>
  );
}

export function LocalPilotPath() {
  const steps = [
    ["/", "首页"],
    ["/personal-production", "个人生产总控台"],
    ["/personal-production-pilot", "个人生产实战 Pilot"],
    ["/personal-trial-readiness", "个人版实战试运行准备"],
    ["/personal-provider-readiness", "真实接口接入准备"],
    ["/personal-owner-output-center", "用户本人产出下载中心"],
    ["/personal-case-workspace", "个人案件与材料工作台"],
    ["/personal-showcase-pack", "公开演示入口"],
    ["/personal-delivery-packet", "交付包草案"],
    ["/personal-case-analysis", "受控案件分析 Runtime"],
    ["/personal-case-production", "受控案件生产工作流"],
    ["/personal-ai-gateway", "AI 草稿 Runtime"],
    ["/personal-material-runtime", "材料与 OCR Runtime"],
    ["/personal-intelligence", "法律/企业信息网关"],
    ["/personal-skill-studio", "经验包与技能工作室"],
    ["/personal-skill-studio/training-artifacts", "训练产物加载器"]
  ];
  return (
    <Panel title="本地 Pilot 操作路径" eyebrow="Local Pilot">
      <div className="grid gap-2 md:grid-cols-3">
        {steps.map(([route, label], index) => (
          <div key={route} className="rounded-md border border-line bg-slate-50 px-3 py-2">
            <div className="text-xs font-semibold text-muted">{index + 1}. {route}</div>
            <div className="mt-1 text-sm font-medium text-ink">{label}</div>
          </div>
        ))}
      </div>
      <div className="mt-4 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
        建议本地启动后端 8001、前端 3001，避免使用自动 reload。当前路径仅用于个人本地试点和模拟元数据展示，不生成最终法律意见、不自动对外交付。
      </div>
    </Panel>
  );
}

export function InfoRows({ rows }: { rows: Array<[string, unknown]> }) {
  return (
    <div className="grid gap-2">
      {rows.map(([label, value]) => (
        <div key={label} className="grid gap-1 rounded-md border border-line bg-stone-50 px-3 py-2 text-sm md:grid-cols-[190px_1fr]">
          <span className="font-medium text-muted">{label}</span>
          <span className="break-words text-ink">{String(value ?? "pending")}</span>
        </div>
      ))}
    </div>
  );
}
