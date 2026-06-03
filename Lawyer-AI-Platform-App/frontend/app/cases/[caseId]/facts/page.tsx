import { AppShell } from "@/components/AppShell";

const facts = [
  {
    factId: "fact_demo_001",
    factType: "contract",
    description: "双方签署了软件开发服务合同。",
    confidence: 0.92,
    status: "draft"
  }
];

export default function FactViewPage({ params }: { params: { caseId: string } }) {
  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">事实</h1>
          <p className="mt-2 text-sm text-slate-600">查看 {params.caseId} 已抽取事实。</p>
        </header>
        <section className="rounded-md border border-line bg-white">
          {facts.map((fact) => (
            <article key={fact.factId} className="border-b border-line p-4 last:border-b-0">
              <div className="text-sm font-semibold text-ink">{fact.factType}</div>
              <p className="mt-2 text-sm text-slate-700">{fact.description}</p>
              <div className="mt-3 text-xs text-slate-500">
                {fact.factId} · 置信度 {fact.confidence} · {fact.status}
              </div>
            </article>
          ))}
        </section>
      </div>
    </AppShell>
  );
}
