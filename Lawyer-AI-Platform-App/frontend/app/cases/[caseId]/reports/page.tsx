import { AppShell } from "@/components/AppShell";

export default function ReportViewPage({ params }: { params: { caseId: string } }) {
  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">Report View</h1>
          <p className="mt-2 text-sm text-slate-600">Generate and review reports for {params.caseId}.</p>
        </header>
        <section className="rounded-md border border-line bg-white p-5">
          <div className="text-sm font-semibold text-ink">Legal Analysis Report</div>
          <p className="mt-2 text-sm text-slate-600">
            Report generation will use case facts, legal analyses, and report runtime output.
          </p>
          <button className="mt-4 rounded-md bg-accent px-4 py-2 text-sm font-medium text-white">
            Generate Report
          </button>
        </section>
      </div>
    </AppShell>
  );
}
