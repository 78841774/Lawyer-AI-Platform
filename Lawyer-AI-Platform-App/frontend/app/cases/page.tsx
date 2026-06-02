import Link from "next/link";
import { AppShell } from "@/components/AppShell";

const cases = [
  {
    caseId: "demo-case",
    title: "Software Development Contract Dispute",
    caseType: "contract_dispute",
    status: "draft",
    updatedAt: "2026-06-03"
  }
];

export default function CaseListPage() {
  return (
    <AppShell>
      <div className="space-y-6">
        <header className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-ink">Case List</h1>
            <p className="mt-2 text-sm text-slate-600">Manage MVP cases and workflow progress.</p>
          </div>
          <button className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white">
            New Case
          </button>
        </header>
        <section className="rounded-md border border-line bg-white">
          {cases.map((item) => (
            <Link
              key={item.caseId}
              href={`/cases/${item.caseId}`}
              className="grid gap-3 border-b border-line px-4 py-3 text-sm last:border-b-0 md:grid-cols-4"
            >
              <span className="font-medium text-ink">{item.title}</span>
              <span className="text-slate-600">{item.caseType}</span>
              <span className="text-slate-600">{item.status}</span>
              <span className="text-slate-500">{item.updatedAt}</span>
            </Link>
          ))}
        </section>
      </div>
    </AppShell>
  );
}
