import { AppShell } from "@/components/AppShell";
import { AuthStatusCard } from "@/components/dashboard/AuthStatusCard";
import { BrandHero } from "@/components/dashboard/BrandHero";
import { QuickActions } from "@/components/dashboard/QuickActions";
import { RecentCases } from "@/components/dashboard/RecentCases";
import { RuntimeStatusCard } from "@/components/dashboard/RuntimeStatusCard";
import { StatsGrid } from "@/components/dashboard/StatsGrid";
import { WorkspaceSummaryCard } from "@/components/dashboard/WorkspaceSummaryCard";
import { Card, CardBody } from "@/components/ui/Card";
import Link from "next/link";
import type { Case } from "@/types";
import { getCases, getCurrentUser, getDashboardStats, getLLMStatus, getWorkspace, getWorkspaces } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const { stats, user, workspace, llmStatus, activeCases, cases, workspaceCases, error } = await loadDashboard();

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

        <CurrentWorkspaceCasesCard cases={workspaceCases} workspaceId={workspace?.workspace_id ?? null} />

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
    const workspaceCases = workspace
      ? cases.filter((item) => item.workspace_id === workspace.workspace_id)
      : cases;
    const activeCases = workspaceCases.length;
    return { stats, user, workspace, llmStatus, activeCases, cases, workspaceCases, error: null };
  } catch {
    return {
      stats: null,
      user: null,
      workspace: null,
      llmStatus: null,
      activeCases: 0,
      cases: [],
      workspaceCases: [],
      error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。"
    };
  }
}

function CurrentWorkspaceCasesCard({
  cases,
  workspaceId
}: {
  cases: Case[];
  workspaceId: string | null;
}) {
  return (
    <Card>
      <CardBody>
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <div className="text-xs uppercase tracking-wide text-muted">当前工作空间案件</div>
            <h2 className="mt-2 text-lg font-semibold text-ink">{workspaceId ?? "workspace_local_001"}</h2>
          </div>
          <Link
            href={workspaceId ? `/cases?workspace_id=${workspaceId}` : "/cases"}
            className="rounded-md border border-line px-3 py-2 text-xs font-medium text-ink hover:border-accent"
          >
            查看案件
          </Link>
        </div>
        <div className="mt-4 grid gap-3 md:grid-cols-2">
          {cases.slice(0, 6).map((item) => (
            <Link
              key={item.case_id}
              href={`/cases/${item.case_id}`}
              className="rounded-md border border-line p-3 hover:bg-slate-50"
            >
              <div className="text-sm font-medium text-ink">{item.title}</div>
              <div className="mt-1 text-xs text-muted">
                {item.case_id} · {item.workspace_id} · {item.owner_user_id}
              </div>
            </Link>
          ))}
          {cases.length === 0 ? <div className="text-sm text-muted">当前工作空间暂无案件。</div> : null}
        </div>
      </CardBody>
    </Card>
  );
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
