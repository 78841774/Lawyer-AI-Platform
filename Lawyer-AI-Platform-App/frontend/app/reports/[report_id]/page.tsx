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
            Back to reports
          </Link>
          <h1 className="mt-3 text-2xl font-semibold text-ink">
            {report?.title ?? "Report Detail"}
          </h1>
          <p className="mt-2 text-sm text-slate-600">
            {report ? `${report.report_id} · ${report.case_id}` : params.report_id}
          </p>
        </header>

        {error ? <StatusMessage message={error} /> : null}

        {report ? (
          <>
            <section className="grid gap-4 md:grid-cols-4">
              <MetaCard label="Status" value={report.status} />
              <MetaCard label="Version" value={String(report.version)} />
              <MetaCard label="Type" value={report.report_type} />
              <MetaCard label="Created" value={formatDate(report.created_at)} />
            </section>

            <section className="rounded-md border border-line bg-white p-5">
              <div className="text-sm font-semibold text-ink">Source References</div>
              <div className="mt-2 text-sm text-slate-600">
                Analysis: {report.source_refs.analysis_id ?? "n/a"}
              </div>
              <div className="mt-1 text-sm text-slate-600">
                Facts: {(report.source_refs.fact_ids ?? []).join(", ") || "n/a"}
              </div>
              <div className="mt-1 text-sm text-slate-600">File: {report.storage_path}</div>
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
    return { report: null, error: "Backend API is unavailable. Start the backend on port 8001." };
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
