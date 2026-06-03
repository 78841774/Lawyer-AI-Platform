import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { SkillActionButton } from "@/components/SkillActionButton";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getSkillRegistry } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function SkillRegistryPage() {
  const { entries, error } = await loadRegistry();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 技能注册表"
          title="技能注册表"
          description="展示已发布或可发布的技能、领域、状态、版本与经验包信息。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <div className="grid gap-3 border-b border-line bg-slate-50 px-4 py-3 text-xs font-semibold text-muted md:grid-cols-8">
            <span>skill_id</span>
            <span>技能名称</span>
            <span>domain</span>
            <span>version</span>
            <span>status</span>
            <span>验证状态</span>
            <span>package</span>
            <span>操作</span>
          </div>
          {entries.length > 0 ? (
            entries.map((entry) => (
              <article key={entry.skill_id} className="grid gap-3 border-b border-line px-4 py-4 text-sm last:border-b-0 md:grid-cols-8">
                <span className="break-words font-medium text-ink">{entry.skill_id}</span>
                <span>
                  <Link href={`/skills/${entry.skill_id}`} className="font-medium text-ink hover:text-accent">
                    {entry.skill_name}
                  </Link>
                </span>
                <span className="text-muted">{entry.domain}</span>
                <span className="text-muted">{entry.version}</span>
                <span>
                  <Badge tone="gold">{entry.status}</Badge>
                </span>
                <span className="text-muted">{entry.validation_status || "暂无"}</span>
                <span className="break-words text-muted">
                  {entry.package_id ?? "暂无"} / {entry.package_status ?? "暂无"}
                </span>
                <span className="flex flex-wrap gap-2">
                  <SkillActionButton skillId={entry.skill_id} action="publish" variant="primary" />
                  <SkillActionButton skillId={entry.skill_id} action="deprecate" />
                </span>
                <span className="text-xs text-muted md:col-span-8">评估分数: {formatOptional(entry.evaluation_score)}</span>
              </article>
            ))
          ) : (
            <div className="p-5 text-sm text-muted">暂无技能注册表记录。</div>
          )}
        </Card>
      </div>
    </AppShell>
  );
}

async function loadRegistry() {
  try {
    return { entries: await getSkillRegistry(), error: null };
  } catch {
    return { entries: [], error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}

function formatOptional(value: number | string | null | undefined) {
  if (value === null || typeof value === "undefined" || value === "") {
    return "暂无";
  }
  return String(value);
}
