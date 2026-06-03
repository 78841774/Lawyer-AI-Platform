import { AppShell } from "@/components/AppShell";
import { AuthStatusCard } from "@/components/dashboard/AuthStatusCard";
import { BrandHero } from "@/components/dashboard/BrandHero";
import { QuickActions } from "@/components/dashboard/QuickActions";
import { RecentCases } from "@/components/dashboard/RecentCases";
import { RuntimeStatusCard } from "@/components/dashboard/RuntimeStatusCard";
import { StatsGrid } from "@/components/dashboard/StatsGrid";
import { WorkspaceSummaryCard } from "@/components/dashboard/WorkspaceSummaryCard";
import { Card, CardBody } from "@/components/ui/Card";
import { getCases, getCurrentUser, getDashboardStats, getLLMStatus, getWorkspace, getWorkspaces } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const { stats, user, workspace, llmStatus, activeCases, cases, error } = await loadDashboard();

  return (
    <AppShell>
      <div className="space-y-6">
        <BrandHero />
        {error ? <StatusMessage message={error} /> : null}

        <section className="grid gap-4 lg:grid-cols-3">
          <AuthStatusCard />
          <WorkspaceSummaryCard workspace={workspace} activeCases={activeCases} />
          <RuntimeStatusCard runtime={llmStatus} />
        </section>

        <StatsGrid stats={stats} />

        <section className="grid gap-4 lg:grid-cols-2">
          <RecentCases cases={cases} />
          <QuickActions />
        </section>

        <Card>
          <CardBody>
            <div className="text-xs uppercase tracking-wide text-muted">当前用户</div>
            <div className="mt-2 text-sm font-semibold text-ink">{user?.display_name ?? "-"}</div>
            <div className="mt-1 text-xs text-muted">
              {user ? `${user.email} · ${user.role} · ${user.status}` : "-"}
            </div>
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}

async function loadDashboard() {
  try {
    const [stats, user, workspaces, llmStatus, cases] = await Promise.all([
      getDashboardStats(),
      getCurrentUser(),
      getWorkspaces(),
      getLLMStatus(),
      getCases()
    ]);
    const workspaceSummary = workspaces[0] ?? null;
    const workspace = workspaceSummary ? await getWorkspace(workspaceSummary.workspace_id) : null;
    const activeCases = workspace
      ? cases.filter((item) => item.workspace_id === workspace.workspace_id).length
      : cases.length;
    return { stats, user, workspace, llmStatus, activeCases, cases, error: null };
  } catch {
    return {
      stats: null,
      user: null,
      workspace: null,
      llmStatus: null,
      activeCases: 0,
      cases: [],
      error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。"
    };
  }
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
