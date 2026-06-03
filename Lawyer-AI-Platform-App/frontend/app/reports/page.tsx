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
          eyebrow="AIHome.law Reports"
          title="Reports"
          description="Generated legal reports with source references and runtime metadata."
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
                    <Badge tone="muted">Export</Badge>
                  </div>
                </div>
                <p className="mt-3 line-clamp-2 text-sm text-muted">
                  {report.content.replaceAll("\n", " ").slice(0, 180)}
                </p>
                <div className="mt-3 grid gap-2 text-xs text-muted md:grid-cols-4">
                  <span>skill: {report.source_refs.skill_id ?? "-"}</span>
                  <span>package: {report.source_refs.package_id ?? "-"}</span>
                  <span>llm: {report.source_refs.llm_provider ?? "-"}</span>
                  <span>llm_status: {report.source_refs.llm_status ?? "-"}</span>
                </div>
              </Link>
            ))
          ) : (
            <div className="p-5 text-sm text-muted">No reports found.</div>
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
    return { reports: [], error: "Backend API is unavailable. Start the backend on port 8001." };
  }
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
