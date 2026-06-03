import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getReports } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function ReportsPage() {
  const { reports, error } = await loadReports();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 报告"
          title="报告"
          description="展示已生成法律报告、source_refs 与运行元数据。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          {reports.length > 0 ? (
            reports.map((report) => (
              <Link
                key={report.report_id}
                href={`/reports/${report.report_id}`}
                className="block border-b border-line p-4 last:border-b-0 hover:bg-slate-50"
              >
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold text-ink">{report.title}</div>
                    <div className="mt-1 text-xs text-muted">
                      {report.report_id} · {report.case_id} · version {report.version}
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Badge tone="blue">{report.status}</Badge>
                    <Badge tone="muted">导出</Badge>
                    <Badge tone="muted">查看报告</Badge>
                  </div>
                </div>
                <p className="mt-3 line-clamp-2 text-sm text-muted">
                  {report.content.replaceAll("\n", " ").slice(0, 180)}
                </p>
                <div className="mt-3 grid gap-2 text-xs text-muted md:grid-cols-4">
                  <span>报告 ID: {report.report_id}</span>
                  <span>报告类型: {report.report_type}</span>
                  <span>使用技能: {report.source_refs.skill_id ?? "-"}</span>
                  <span>模型提供方: {report.source_refs.llm_provider ?? "-"}</span>
                  <span>package_id: {report.source_refs.package_id ?? "-"}</span>
                  <span>模型状态: {report.source_refs.llm_status ?? "-"}</span>
                </div>
              </Link>
            ))
          ) : (
            <div className="p-5 text-sm text-muted">暂无报告。</div>
          )}
        </Card>
      </div>
    </AppShell>
  );
}

async function loadReports() {
  try {
    return { reports: await getReports(), error: null };
  } catch {
    return { reports: [], error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
