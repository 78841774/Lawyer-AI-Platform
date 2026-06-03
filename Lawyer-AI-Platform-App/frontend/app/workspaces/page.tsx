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
          eyebrow="AIHome.law Workspace"
          title="Workspaces"
          description="Workspace identity, ownership, and future membership controls."
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <div className="grid gap-3 border-b border-line bg-slate-50 px-4 py-3 text-xs font-semibold uppercase tracking-wide text-muted md:grid-cols-6">
            <span>Workspace</span>
            <span>Name</span>
            <span>Owner</span>
            <span>Status</span>
            <span>Created</span>
            <span>Members</span>
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
                  <Badge tone="muted">invite soon</Badge>
                </span>
              </article>
            ))
          ) : (
            <div className="p-5 text-sm text-muted">No workspaces found.</div>
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
    return { workspaces: [], error: "Backend API is unavailable. Start the backend on port 8001." };
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
