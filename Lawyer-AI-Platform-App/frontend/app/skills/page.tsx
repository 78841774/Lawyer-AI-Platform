import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getWorkspaceSkills, WorkspaceSkillRecord } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function SkillsPage() {
  const { skills, error } = await loadSkills();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 技能"
          title="已发布技能"
          description="可在案件工作空间中复用的法律技能。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          {skills.length > 0 ? (
            skills.map((skill) => <SkillRow key={skill.skill_id} skill={skill} />)
          ) : (
            <div className="p-5 text-sm text-muted">
              暂无已发布技能。请先从 Skill Registry 发布已验证技能。
            </div>
          )}
        </Card>
      </div>
    </AppShell>
  );
}

async function loadSkills() {
  try {
    return { skills: await getWorkspaceSkills(), error: null };
  } catch {
    return { skills: [], error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function SkillRow({ skill }: { skill: WorkspaceSkillRecord }) {
  return (
    <article
      id={skill.skill_id}
      className="grid gap-3 border-b border-line px-4 py-4 text-sm last:border-b-0 hover:bg-slate-50 md:grid-cols-7"
    >
      <div className="md:col-span-2">
        <div className="text-xs text-muted">技能名称</div>
        <Link href={`/skills#${skill.skill_id}`} className="font-medium text-ink hover:text-accent">
          {skill.skill_name}
        </Link>
        <div className="mt-1 text-xs text-muted">技能 ID: {skill.skill_id}</div>
      </div>
      <Meta label="领域" value={skill.domain} />
      <Meta label="版本" value={`v${skill.version}`} />
      <Meta label="经验包 ID" value={skill.package_id} />
      <Meta label="评估分数" value="-" />
      <div>
        <div className="text-xs text-muted">状态</div>
        <div className="mt-1">
          <Badge tone="gold">{skill.status}</Badge>
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

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
