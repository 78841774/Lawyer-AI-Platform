type BadgeTone = "safe" | "info" | "warning" | "muted" | "blocked";

export const CORE_SAFETY_ITEMS = [
  "未调用真实 provider",
  "未读取 API key",
  "未读取真实案件材料",
  "未生成最终法律意见",
  "未生成最终报告",
  "未自动对外交付",
  "未发送邮件",
  "未生成真实 PDF/DOCX",
  "律师复核必需",
  "来源追踪必需",
  "最终锁定必需",
  "当前仅为展示与验证流程"
];

export function SafetyBadge({ label, tone = "safe" }: { label: string; tone?: BadgeTone }) {
  const tones: Record<BadgeTone, string> = {
    safe: "border-emerald-200 bg-emerald-50 text-emerald-800",
    info: "border-cyan-200 bg-cyan-50 text-cyan-800",
    warning: "border-amber-200 bg-amber-50 text-amber-800",
    muted: "border-slate-200 bg-slate-50 text-slate-700",
    blocked: "border-rose-200 bg-rose-50 text-rose-800"
  };
  return <span className={`inline-flex rounded-md border px-3 py-1 text-xs font-medium ${tones[tone]}`}>{label}</span>;
}

export function DarkSafetyBadge({ label }: { label: string }) {
  return <span className="inline-flex rounded-md border border-white/20 bg-white/10 px-3 py-1 text-xs font-medium text-slate-100">{label}</span>;
}

export function StatusPill({ label, tone = "info" }: { label: string; tone?: BadgeTone }) {
  return <SafetyBadge label={label} tone={tone} />;
}

export function Panel({ title, eyebrow, children }: { title: string; eyebrow?: string; children: React.ReactNode }) {
  return (
    <section className="rounded-md border border-line bg-white p-5 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          {eyebrow ? <div className="text-xs font-medium text-muted">{eyebrow}</div> : null}
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
    <div className="rounded-md border border-line bg-white p-4 shadow-sm">
      <div className="text-xs font-medium text-muted">{label}</div>
      <div className="mt-2 break-words text-xl font-semibold text-ink">{String(value)}</div>
      {detail ? <div className="mt-2 text-xs leading-5 text-muted">{detail}</div> : null}
      <div className="mt-3">
        <StatusPill label={tone === "blocked" ? "未就绪" : tone === "warning" ? "需复核" : "受控"} tone={tone} />
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
    <div className="rounded-md border border-line bg-slate-50 p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm font-semibold text-ink">{title}</div>
          <div className="mt-1 text-xs text-muted">{category}</div>
        </div>
        <StatusPill label={status} tone={status.includes("live") ? "warning" : "info"} />
      </div>
      <div className="mt-4 grid gap-2 text-xs text-muted">
        {items.map(([label, value]) => (
          <div key={label} className="flex items-center justify-between gap-3">
            <span>{label}</span>
            <span className="break-all text-right text-ink">{String(value ?? "pending")}</span>
          </div>
        ))}
        {targetRoute ? (
          <div className="flex items-center justify-between gap-3">
            <span>target_route</span>
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
      {steps.map((step, index) => (
        <div key={`${step.label}-${index}`} className="rounded-md border border-line bg-slate-50 p-4">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-slate-900 text-sm font-semibold text-white">{index + 1}</div>
          <div className="mt-3 text-sm font-semibold text-ink">{step.label}</div>
          {step.detail ? <div className="mt-2 text-xs leading-5 text-muted">{step.detail}</div> : null}
          {step.status ? <div className="mt-3"><StatusPill label={step.status} tone="info" /></div> : null}
        </div>
      ))}
    </div>
  );
}

export function TrustSafetyPanel({
  items = CORE_SAFETY_ITEMS,
  title = "Trust / Safety Panel",
  note = "仅展示受控 metadata，不暴露 raw content、本地路径或 secret。"
}: {
  items?: string[];
  title?: string;
  note?: string;
}) {
  const mergedItems = Array.from(new Set([...CORE_SAFETY_ITEMS, ...items]));
  return (
    <Panel title={title} eyebrow="安全边界">
      <div className="grid gap-2">
        {mergedItems.map((item) => (
          <div key={item} className="flex items-center justify-between gap-3 rounded-md border border-line bg-slate-50 px-3 py-2">
            <span className="text-sm text-ink">{item}</span>
            <StatusPill label="已启用" tone="safe" />
          </div>
        ))}
      </div>
      <div className="mt-4 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">{note}</div>
    </Panel>
  );
}

export function DiagnosticsPanel({ data, title = "Developer Diagnostics" }: { data: unknown; title?: string }) {
  return (
    <details className="rounded-md border border-line bg-slate-950 text-slate-100">
      <summary className="cursor-pointer px-4 py-3 text-sm font-medium text-slate-200">{title}</summary>
      <pre className="max-h-[420px] overflow-auto border-t border-slate-800 p-4 text-xs leading-5">
        {JSON.stringify(data, null, 2)}
      </pre>
    </details>
  );
}

export function InfoRows({ rows }: { rows: Array<[string, unknown]> }) {
  return (
    <div className="grid gap-2">
      {rows.map(([label, value]) => (
        <div key={label} className="grid gap-1 rounded-md border border-line bg-slate-50 px-3 py-2 text-sm md:grid-cols-[190px_1fr]">
          <span className="font-medium text-muted">{label}</span>
          <span className="break-words text-ink">{String(value ?? "pending")}</span>
        </div>
      ))}
    </div>
  );
}
