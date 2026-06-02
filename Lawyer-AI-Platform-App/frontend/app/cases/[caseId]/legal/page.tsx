import { AppShell } from "@/components/AppShell";

const issues = [
  {
    issueId: "issue_demo_001",
    issue: "Whether delayed delivery constitutes breach of contract",
    conclusion: "The current facts support a medium-risk breach analysis.",
    riskLevel: "medium"
  }
];

export default function LegalAnalysisPage({ params }: { params: { caseId: string } }) {
  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">Legal Analysis View</h1>
          <p className="mt-2 text-sm text-slate-600">Analyze legal issues for {params.caseId}.</p>
        </header>
        <section className="rounded-md border border-line bg-white">
          {issues.map((item) => (
            <article key={item.issueId} className="border-b border-line p-4 last:border-b-0">
              <div className="text-sm font-semibold text-ink">{item.issue}</div>
              <p className="mt-2 text-sm text-slate-700">{item.conclusion}</p>
              <div className="mt-3 text-xs text-slate-500">
                {item.issueId} · risk {item.riskLevel}
              </div>
            </article>
          ))}
        </section>
      </div>
    </AppShell>
  );
}
