import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { getReports } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function ReportsPage() {
  const { reports, error } = await loadReports();

  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">Reports</h1>
          <p className="mt-2 text-sm text-slate-600">Generated reports from the Workspace API.</p>
        </header>

        {error ? <StatusMessage message={error} /> : null}

        <section className="rounded-md border border-line bg-white">
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
                    <div className="mt-1 text-xs text-slate-500">
                      {report.report_id} · {report.case_id} · version {report.version}
                    </div>
                  </div>
                  <span className="rounded-md border border-line px-2 py-1 text-xs text-slate-600">
                    {report.status}
                  </span>
                </div>
                <p className="mt-3 line-clamp-2 text-sm text-slate-600">
                  {report.content.replaceAll("\n", " ").slice(0, 180)}
                </p>
              </Link>
            ))
          ) : (
            <div className="p-5 text-sm text-slate-600">No reports found.</div>
          )}
        </section>
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
    <div className="rounded-md border border-line bg-white p-4 text-sm text-slate-600">
      {message}
    </div>
  );
}
