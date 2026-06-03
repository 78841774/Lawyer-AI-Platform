import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getCases } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function CaseListPage() {
  const { cases, error } = await loadCases();

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
          <div className="grid gap-3 border-b border-line bg-slate-50 px-4 py-3 text-xs font-semibold uppercase tracking-wide text-muted md:grid-cols-8">
            <span>案件 ID</span>
            <span className="md:col-span-2">标题</span>
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
                className="grid gap-3 border-b border-line px-4 py-3 text-sm last:border-b-0 hover:bg-slate-50 md:grid-cols-8"
              >
                <span className="break-words font-medium text-ink">{item.case_id}</span>
                <span className="break-words text-ink md:col-span-2">{item.title}</span>
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

async function loadCases() {
  try {
    return { cases: await getCases(), error: null };
  } catch {
    return { cases: [], error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
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
