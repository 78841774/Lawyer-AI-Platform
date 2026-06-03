import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getCases, getCurrentUser, getWorkspace, getWorkspaces } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function CaseListPage({
  searchParams
}: {
  searchParams?: { workspace_id?: string };
}) {
  const selectedWorkspaceId = searchParams?.workspace_id;
  const { cases, user, workspace, error } = await loadCases(selectedWorkspaceId);

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 案件"
          title="案件工作台"
          description="展示案件记录、工作空间归属与法律 AI 工作流状态。"
          action={
            <Link
              href="/cases/new"
              className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white shadow-sm"
            >
              创建案件
            </Link>
          }
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <div className="grid gap-4 md:grid-cols-3">
              <InfoRow label="当前用户" value={user ? `${user.display_name} / ${user.user_id}` : "-"} />
              <InfoRow label="当前工作空间" value={workspace ? `${workspace.name} / ${workspace.workspace_id}` : "-"} />
              <InfoRow label="当前列表案件数" value={String(cases.length)} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <div className="grid gap-3 border-b border-line bg-slate-50 px-4 py-3 text-xs font-semibold uppercase tracking-wide text-muted md:grid-cols-10">
            <span>案件 ID</span>
            <span className="md:col-span-2">标题</span>
            <span className="md:col-span-2">Intake 信息</span>
            <span>状态</span>
            <span>工作空间 ID</span>
            <span>所属用户 ID</span>
            <span>创建时间</span>
            <span>查看详情</span>
          </div>
          {cases.length > 0 ? (
            cases.map((item) => (
              <Link
                key={item.case_id}
                href={`/cases/${item.case_id}`}
                className="grid gap-3 border-b border-line px-4 py-3 text-sm last:border-b-0 hover:bg-slate-50 md:grid-cols-10"
              >
                <span className="break-words font-medium text-ink">{item.case_id}</span>
                <span className="break-words text-ink md:col-span-2">
                  <span className="font-medium">{item.title}</span>
                  <span className="mt-1 block text-xs text-muted">
                    客户：{displayValue(item.client_name)} / 对方：{displayValue(item.counterparty_name)}
                  </span>
                </span>
                <span className="break-words text-xs text-muted md:col-span-2">
                  <span className="block">案件类型：{displayValue(item.case_type)}</span>
                  <span className="block">合同类型：{displayValue(item.contract_type)}</span>
                  <span className="block">争议金额：{displayValue(item.dispute_amount)}</span>
                </span>
                <span className="text-muted">{item.status}</span>
                <span className="break-words text-muted">{item.workspace_id}</span>
                <span className="break-words text-muted">{item.owner_user_id}</span>
                <span className="text-muted">{formatDate(item.created_at)}</span>
                <span className="flex flex-wrap items-center gap-1">
                  <span className="font-medium text-accent">查看详情</span>
                  <Badge tone="muted">priority</Badge>
                  <Badge tone="muted">stage</Badge>
                </span>
              </Link>
            ))
          ) : (
            <div className="p-5 text-sm text-muted">暂无案件。</div>
          )}
        </Card>
      </div>
    </AppShell>
  );
}

async function loadCases(selectedWorkspaceId?: string) {
  try {
    const [allCases, user, workspaces] = await Promise.all([
      getCases(),
      getCurrentUser(),
      getWorkspaces()
    ]);
    const workspaceId = selectedWorkspaceId ?? workspaces[0]?.workspace_id;
    const workspace = workspaceId ? await getWorkspace(workspaceId) : null;
    const cases = workspaceId
      ? allCases.filter((item) => item.workspace_id === workspaceId)
      : allCases;
    return { cases, user, workspace, error: null };
  } catch {
    return { cases: [], user: null, workspace: null, error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

function displayValue(value?: string | null) {
  return value && value.trim() ? value : "暂无";
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
