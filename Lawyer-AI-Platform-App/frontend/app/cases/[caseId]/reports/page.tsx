import { AppShell } from "@/components/AppShell";

export default function ReportViewPage({ params }: { params: { caseId: string } }) {
  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">报告</h1>
          <p className="mt-2 text-sm text-slate-600">为 {params.caseId} 生成并查看报告。</p>
        </header>
        <section className="rounded-md border border-line bg-white p-5">
          <div className="text-sm font-semibold text-ink">法律分析报告</div>
          <p className="mt-2 text-sm text-slate-600">
            报告生成将使用案件事实、法律分析与报告运行结果。
          </p>
          <button className="mt-4 rounded-md bg-accent px-4 py-2 text-sm font-medium text-white">
            生成报告
          </button>
        </section>
      </div>
    </AppShell>
  );
}
