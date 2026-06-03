import { AppShell } from "@/components/AppShell";
import { AuthLoginPanel } from "@/components/AuthLoginPanel";
import { StatCard } from "@/components/StatCard";
import { getAuthStatus, getCurrentUser, getDashboardStats, getWorkspaces } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const { stats, user, workspace, authStatus, error } = await loadDashboard();

  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">Dashboard</h1>
          <p className="mt-2 text-sm text-slate-600">
            Workspace overview backed by the v3.0 Internal Alpha API.
          </p>
        </header>

        {error ? <StatusMessage message={error} /> : null}

        <section className="grid gap-4 md:grid-cols-3">
          <IdentityCard
            label="Auth Status"
            title={authStatus?.authenticated ? "Authenticated" : "-"}
            meta={authStatus ? `${authStatus.user_id} · ${authStatus.auth_mode}` : "-"}
          />
          <IdentityCard
            label="Current User"
            title={user?.display_name ?? "-"}
            meta={user && authStatus ? `${user.email} · ${authStatus.auth_mode}` : "-"}
          />
          <IdentityCard
            label="Current Workspace"
            title={workspace?.name ?? "-"}
            meta={workspace ? `${workspace.workspace_id} · ${workspace.status}` : "-"}
          />
        </section>

        <AuthLoginPanel />

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

async function loadDashboard() {
  try {
    const [stats, user, workspaces] = await Promise.all([
      getDashboardStats(),
      getCurrentUser(),
      getWorkspaces()
    ]);
    const authStatus = await getAuthStatus();
    return { stats, user, workspace: workspaces[0] ?? null, authStatus, error: null };
  } catch {
    return {
      stats: null,
      user: null,
      workspace: null,
      authStatus: null,
      error: "Backend API is unavailable. Start the backend on port 8001."
    };
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

function IdentityCard({
  label,
  title,
  meta
}: {
  label: string;
  title: string;
  meta: string;
}) {
  return (
    <div className="rounded-md border border-line bg-white p-4">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="mt-2 text-sm font-semibold text-ink">{title}</div>
      <div className="mt-1 break-words text-xs text-slate-500">{meta}</div>
    </div>
  );
}
