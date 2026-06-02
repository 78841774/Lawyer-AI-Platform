import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";

export default function DashboardPage() {
  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">Dashboard</h1>
          <p className="mt-2 text-sm text-slate-600">
            MVP workspace for case management, materials, facts, legal analysis, and reports.
          </p>
        </header>
        <section className="grid gap-4 md:grid-cols-4">
          <StatCard label="Cases" value="0" helper="Ready for MVP data" />
          <StatCard label="Materials" value="0" helper="Upload flow scaffolded" />
          <StatCard label="Facts" value="0" helper="Extraction runtime pending" />
          <StatCard label="Reports" value="0" helper="Generation flow scaffolded" />
        </section>
      </div>
    </AppShell>
  );
}
