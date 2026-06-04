import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getSkillRegistry, SkillRegistryRecord } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function SkillRegistryPage() {
  const { entries, error } = await loadRegistry();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 技能注册表"
          title="Skill Registry"
          description="展示受控本地发布记录与历史技能注册表。受控发布不会自动启用 Workspace Runtime。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <div className="grid gap-3 border-b border-line bg-slate-50 px-4 py-3 text-xs font-semibold text-muted md:grid-cols-12">
            <span className="md:col-span-2">Skill ID</span>
            <span className="md:col-span-2">来源经验包</span>
            <span className="md:col-span-2">来源训练运行</span>
            <span>案由</span>
            <span>版本</span>
            <span>状态</span>
            <span>工作空间</span>
            <span>Runtime</span>
            <span>操作</span>
          </div>
          {entries.length > 0 ? (
            entries.map((entry) => <RegistryRow key={entry.skill_id} entry={entry} />)
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

function RegistryRow({ entry }: { entry: SkillRegistryRecord }) {
  return (
    <article className="grid gap-3 border-b border-line px-4 py-4 text-sm last:border-b-0 md:grid-cols-12">
      <Link href={`/skill-registry/${encodeURIComponent(entry.skill_id)}`} className="break-words font-medium text-ink hover:text-accent md:col-span-2">
        {entry.skill_id}
      </Link>
      <span className="break-words text-muted md:col-span-2">{entry.source_experience_package_id ?? entry.package_id ?? "暂无"}</span>
      <span className="break-words text-muted md:col-span-2">{entry.source_run_id ?? "暂无"}</span>
      <span className="text-muted">{entry.case_cause_code ?? entry.domain ?? "暂无"}</span>
      <span className="text-muted">{entry.version}</span>
      <span>
        <Badge tone="gold">{entry.status}</Badge>
      </span>
      <span className="text-muted">{entry.workspace_scope ?? "暂无"}</span>
      <span className="text-muted">{entry.runtime?.workspace_runtime_enabled ? "已启用" : "未启用"}</span>
      <Link href={`/skill-registry/${encodeURIComponent(entry.skill_id)}`} className="font-medium text-accent">
        查看详情
      </Link>
      <span className="break-words text-xs text-muted md:col-span-12">
        受控发布: {entry.safety?.controlled_publish ? "是" : "否"} / auto_publish_enabled: {entry.safety?.auto_publish_enabled ? "true" : "false"} / 发布时间: {entry.published_at ?? "暂无"}
      </span>
    </article>
  );
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}
