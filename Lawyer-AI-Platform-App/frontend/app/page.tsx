import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { getDashboardStats } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const { stats, error } = await loadDashboardStats();

  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">Dashboard</h1>
          <p className="mt-2 text-sm text-slate-600">
            Workspace overview backed by the v1.2 API.
          </p>
        </header>

        {error ? <StatusMessage message={error} /> : null}

        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          <StatCard label="Cases" value={formatCount(stats?.cases)} helper="Active workspace cases" />
          <StatCard label="Materials" value={formatCount(stats?.materials)} helper="Uploaded evidence files" />
          <StatCard label="Facts" value={formatCount(stats?.facts)} helper="Extracted fact records" />
          <StatCard label="Analyses" value={formatCount(stats?.analyses)} helper="Legal analysis runs" />
          <StatCard label="Reports" value={formatCount(stats?.reports)} helper="Generated reports" />
        </section>

        <section className="grid gap-4 md:grid-cols-2">
          <a className="rounded-md border border-line bg-white p-5 hover:border-accent" href="/cases">
            <div className="text-sm font-semibold text-ink">Cases</div>
            <p className="mt-2 text-sm text-slate-600">Review all persisted cases from the backend workspace.</p>
          </a>
          <a className="rounded-md border border-line bg-white p-5 hover:border-accent" href="/reports">
            <div className="text-sm font-semibold text-ink">Reports</div>
            <p className="mt-2 text-sm text-slate-600">Open generated preliminary reports and source references.</p>
          </a>
        </section>
      </div>
    </AppShell>
  );
}

async function loadDashboardStats() {
  try {
    return { stats: await getDashboardStats(), error: null };
  } catch {
    return { stats: null, error: "Backend API is unavailable. Start the backend on port 8001." };
  }
}

function formatCount(value: number | undefined) {
  return typeof value === "number" ? String(value) : "-";
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-slate-600">
      {message}
    </div>
  );
}
