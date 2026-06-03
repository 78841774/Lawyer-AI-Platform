import Link from "next/link";
import { notFound } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { ApiError, getReport } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function ReportDetailPage({
  params
}: {
  params: { report_id: string };
}) {
  const { report, error } = await loadReport(params.report_id);

  if (!report && !error) {
    notFound();
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <Link href="/reports" className="text-sm text-accent">
            返回报告
          </Link>
          <h1 className="mt-3 text-2xl font-semibold text-ink">
            {report?.title ?? "报告详情"}
          </h1>
          <p className="mt-2 text-sm text-slate-600">
            {report ? `${report.report_id} · ${report.case_id}` : params.report_id}
          </p>
        </header>

        {error ? <StatusMessage message={error} /> : null}

        {report ? (
          <>
            <section className="grid gap-4 md:grid-cols-4">
              <MetaCard label="状态" value={report.status} />
              <MetaCard label="版本" value={String(report.version)} />
              <MetaCard label="报告类型" value={report.report_type} />
              <MetaCard label="创建时间" value={formatDate(report.created_at)} />
            </section>

            <section className="rounded-md border border-line bg-white p-5">
              <div className="text-sm font-semibold text-ink">引用来源 source_refs</div>
              <div className="mt-3 grid gap-3 md:grid-cols-2">
                <RuntimeRow label="fact_ids" value={(report.source_refs.fact_ids ?? []).join(", ") || "暂无"} />
                <RuntimeRow label="analysis_id" value={report.source_refs.analysis_id ?? "暂无"} />
                <RuntimeRow label="llm_provider" value={report.source_refs.llm_provider ?? "暂无"} />
                <RuntimeRow label="llm_status" value={report.source_refs.llm_status ?? "暂无"} />
                <RuntimeRow label="skill_id" value={report.source_refs.skill_id ?? "暂无"} />
                <RuntimeRow label="package_id" value={report.source_refs.package_id ?? "暂无"} />
              </div>
              <div className="mt-3 text-sm text-slate-600">storage_path: {report.storage_path || "暂无"}</div>
            </section>

            {report.source_refs.skill_id || report.source_refs.package_id ? (
              <section className="rounded-md border border-line bg-white p-5">
                <div className="text-sm font-semibold text-ink">使用技能</div>
                <div className="mt-2 text-sm text-slate-600">
                  skill_id: {report.source_refs.skill_id ?? "n/a"}
                </div>
                <div className="mt-1 text-sm text-slate-600">
                  package_id: {report.source_refs.package_id ?? "n/a"}
                </div>
              </section>
            ) : null}

            <section className="rounded-md border border-line bg-white p-5">
              <div className="text-sm font-semibold text-ink">报告运行信息</div>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <RuntimeRow label="report_id" value={report.report_id} />
                <RuntimeRow label="case_id" value={report.case_id} />
                <RuntimeRow label="report_type" value={report.report_type} />
                <RuntimeRow label="llm_provider" value={report.llm_provider ?? report.source_refs.llm_provider ?? "暂无"} />
                <RuntimeRow label="llm_status" value={report.llm_status ?? report.source_refs.llm_status ?? "暂无"} />
                <RuntimeRow label="skill_used" value={report.skill_used ?? report.source_refs.skill_id ?? "暂无"} />
                <RuntimeRow label="package_used" value={report.package_used ?? report.source_refs.package_id ?? "暂无"} />
                <RuntimeRow label="created_at" value={formatDate(report.created_at)} />
                <RuntimeRow label="updated_at" value={report.updated_at ? formatDate(report.updated_at) : "暂无"} />
              </div>
              <div className="mt-5">
                <div className="text-xs font-semibold uppercase tracking-wide text-muted">引用来源 source_refs</div>
                <div className="mt-2 rounded-md border border-line bg-paper p-3 text-sm text-slate-600">
                  <SourceRefsView value={report.source_refs} />
                </div>
              </div>
            </section>

            <article className="whitespace-pre-wrap rounded-md border border-line bg-white p-5 text-sm leading-6 text-slate-700">
              {report.content}
            </article>
          </>
        ) : null}
      </div>
    </AppShell>
  );
}

async function loadReport(reportId: string) {
  try {
    return { report: await getReport(reportId), error: null };
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return { report: null, error: null };
    }
    return { report: null, error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function MetaCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="mt-2 text-sm font-semibold text-ink">{value}</div>
    </div>
  );
}

function RuntimeRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line p-3">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="mt-1 break-words text-sm font-medium text-ink">{value || "暂无"}</div>
    </div>
  );
}

function SourceRefsView({ value }: { value: unknown }) {
  if (!value) {
    return <span>暂无引用来源</span>;
  }
  if (typeof value === "string") {
    return <span>{value || "暂无引用来源"}</span>;
  }
  if (Array.isArray(value)) {
    return value.length > 0 ? (
      <ul className="list-inside list-disc space-y-1">
        {value.map((item, index) => (
          <li key={index}>{String(item)}</li>
        ))}
      </ul>
    ) : (
      <span>暂无引用来源</span>
    );
  }
  if (typeof value === "object") {
    const entries = Object.entries(value as Record<string, unknown>);
    return entries.length > 0 ? (
      <dl className="space-y-2">
        {entries.map(([key, entryValue]) => (
          <div key={key} className="grid gap-1 md:grid-cols-[160px_1fr]">
            <dt className="font-medium text-ink">{key}</dt>
            <dd className="break-words">
              {Array.isArray(entryValue) ? entryValue.join(", ") || "暂无" : String(entryValue ?? "暂无")}
            </dd>
          </div>
        ))}
      </dl>
    ) : (
      <span>暂无引用来源</span>
    );
  }
  return <span>{String(value)}</span>;
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-slate-600">
      {message}
    </div>
  );
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}
