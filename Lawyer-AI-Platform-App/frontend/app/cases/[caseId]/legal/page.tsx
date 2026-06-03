import { AppShell } from "@/components/AppShell";

const issues = [
  {
    issueId: "issue_demo_001",
    issue: "延迟交付是否构成合同违约",
    conclusion: "当前事实支持中等风险的违约分析。",
    riskLevel: "medium"
  }
];

export default function LegalAnalysisPage({ params }: { params: { caseId: string } }) {
  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">法律分析</h1>
          <p className="mt-2 text-sm text-slate-600">分析 {params.caseId} 的法律问题。</p>
        </header>
        <section className="rounded-md border border-line bg-white">
          {issues.map((item) => (
            <article key={item.issueId} className="border-b border-line p-4 last:border-b-0">
              <div className="text-sm font-semibold text-ink">{item.issue}</div>
              <p className="mt-2 text-sm text-slate-700">{item.conclusion}</p>
              <div className="mt-3 text-xs text-slate-500">
                {item.issueId} · 风险 {item.riskLevel}
              </div>
            </article>
          ))}
        </section>
      </div>
    </AppShell>
  );
}
