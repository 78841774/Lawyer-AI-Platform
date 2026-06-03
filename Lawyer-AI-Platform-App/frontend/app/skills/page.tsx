import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { SkillActionButton } from "@/components/SkillActionButton";
import { getSkills, WorkspaceSkillRecord } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function SkillsPage() {
  const { skills, error } = await loadSkills();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 技能"
          title="技能"
          description="展示 Skill Training 主链路已生成的技能、评估状态与经验包路径。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          {skills.length > 0 ? (
            skills.map((skill) => <SkillRow key={skill.skill_id} skill={skill} />)
          ) : (
            <div className="p-5 text-sm text-muted">
              暂无技能记录。可先在案件详情页构建 Skill。
            </div>
          )}
        </Card>
      </div>
    </AppShell>
  );
}

async function loadSkills() {
  try {
    return { skills: await getSkills(), error: null };
  } catch {
    return { skills: [], error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function SkillRow({ skill }: { skill: WorkspaceSkillRecord }) {
  return (
    <article
      id={skill.skill_id}
      className="grid gap-3 border-b border-line px-4 py-4 text-sm last:border-b-0 hover:bg-slate-50 md:grid-cols-8"
    >
      <div className="md:col-span-2">
        <div className="text-xs text-muted">技能名称</div>
        <Link href={`/skills/${skill.skill_id}`} className="font-medium text-ink hover:text-accent">
          {skill.skill_name}
        </Link>
        <div className="mt-1 text-xs text-muted">技能 ID: {skill.skill_id}</div>
        <div className="mt-1 text-xs text-muted">case_id: {skill.case_id ?? "暂无"}</div>
      </div>
      <Meta label="领域" value={skill.domain} />
      <Meta label="版本" value={`v${skill.version}`} />
      <Meta label="评估分数" value={formatOptional(skill.evaluation_score)} />
      <Meta label="验证状态" value={skill.validation_status ?? "暂无"} />
      <Meta label="package_path" value={skill.package_path ?? "暂无"} />
      <div>
        <div className="text-xs text-muted">状态</div>
        <div className="mt-1">
          <Badge tone="gold">{skill.status}</Badge>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          <Link
            href={`/skills/${skill.skill_id}`}
            className="rounded-md border border-line bg-white px-3 py-2 text-xs font-medium text-ink shadow-sm"
          >
            查看详情
          </Link>
          <SkillActionButton skillId={skill.skill_id} action="evaluate" />
          <SkillActionButton skillId={skill.skill_id} action="build-package" />
          <SkillActionButton skillId={skill.skill_id} action="publish" />
        </div>
      </div>
    </article>
  );
}

function Meta({ label, value }: { label: string; value: string }) {
  return (
    <div className="text-muted">
      <div className="text-xs text-muted">{label}</div>
      <div>{value}</div>
    </div>
  );
}

function formatOptional(value: number | string | null | undefined) {
  if (value === null || typeof value === "undefined" || value === "") {
    return "暂无";
  }
  return String(value);
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
