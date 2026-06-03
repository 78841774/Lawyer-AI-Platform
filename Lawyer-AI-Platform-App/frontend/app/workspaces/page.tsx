import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getWorkspaces } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function WorkspacesPage() {
  const { workspaces, error } = await loadWorkspaces();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 工作空间"
          title="工作空间"
          description="展示工作空间身份、所有权与后续成员管理预留位。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <div className="grid gap-3 border-b border-line bg-slate-50 px-4 py-3 text-xs font-semibold uppercase tracking-wide text-muted md:grid-cols-6">
            <span>工作空间 ID</span>
            <span>名称</span>
            <span>所有人 ID</span>
            <span>状态</span>
            <span>创建时间</span>
            <span>成员</span>
          </div>
          {workspaces.length > 0 ? (
            workspaces.map((workspace) => (
              <article key={workspace.workspace_id} className="grid gap-3 border-b border-line px-4 py-4 text-sm last:border-b-0 md:grid-cols-6">
                <span className="break-words font-medium text-ink">{workspace.workspace_id}</span>
                <span className="text-muted">{workspace.name}</span>
                <span className="break-words text-muted">{workspace.owner_user_id}</span>
                <span>
                  <Badge tone="gold">{workspace.status}</Badge>
                </span>
                <span className="text-muted">{formatDate(workspace.created_at)}</span>
                <span className="flex flex-wrap gap-1">
                  <Badge tone="muted">role</Badge>
                  <Badge tone="muted">邀请成员</Badge>
                </span>
              </article>
            ))
          ) : (
            <div className="p-5 text-sm text-muted">暂无工作空间。</div>
          )}
        </Card>
      </div>
    </AppShell>
  );
}

async function loadWorkspaces() {
  try {
    return { workspaces: await getWorkspaces(), error: null };
  } catch {
    return { workspaces: [], error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
