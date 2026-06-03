import Link from "next/link";
import { notFound } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { SkillActionButton } from "@/components/SkillActionButton";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { getSkill, getSkillRegistryDetail, ApiError } from "@/services/api";
import type { SkillRegistryDetail } from "@/types";

export const dynamic = "force-dynamic";

export default async function SkillDetailPage({ params }: { params: { skillId: string } }) {
  const { skill, registry, error } = await loadSkill(params.skillId);

  if (!skill && !error) {
    notFound();
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <Link href="/skills" className="text-sm font-medium text-accent">
            返回技能
          </Link>
          <h1 className="mt-3 text-2xl font-semibold text-ink">{skill?.skill_name ?? "技能详情"}</h1>
          <p className="mt-2 text-sm text-muted">{params.skillId}</p>
        </header>

        {error ? <StatusMessage message={error} /> : null}

        {skill ? (
          <>
            <Card>
              <CardBody>
                <div className="grid gap-4 md:grid-cols-2">
                  <InfoRow label="skill_id" value={skill.skill_id} />
                  <InfoRow label="case_id" value={skill.case_id ?? "暂无"} />
                  <InfoRow label="skill_name" value={skill.skill_name} />
                  <InfoRow label="domain" value={skill.domain} />
                  <InfoRow label="version" value={skill.version} />
                  <InfoRow label="status" value={skill.status} />
                  <InfoRow label="evaluation_score" value={formatOptional(skill.evaluation_score)} />
                  <InfoRow label="validation_status" value={skill.validation_status ?? "暂无"} />
                  <InfoRow label="package_path" value={skill.package_path ?? "暂无"} />
                </div>
                <div className="mt-5 flex flex-wrap gap-2">
                  <SkillActionButton skillId={skill.skill_id} action="evaluate" />
                  <SkillActionButton skillId={skill.skill_id} action="build-package" />
                  <SkillActionButton skillId={skill.skill_id} action="publish" variant="primary" />
                </div>
              </CardBody>
            </Card>

            <Card>
              <CardBody>
                <div className="text-sm font-semibold text-ink">技能注册表状态</div>
                {registry ? (
                  <div className="mt-4 grid gap-4 md:grid-cols-2">
                    <InfoRow label="package_id" value={registry.package?.package_id ?? "暂无"} />
                    <InfoRow label="package_status" value={registry.lifecycle_status.package_status ?? "暂无"} />
                    <InfoRow label="skill_status" value={registry.lifecycle_status.skill_status} />
                    <InfoRow label="validation_status" value={registry.lifecycle_status.validation_status} />
                  </div>
                ) : (
                  <div className="mt-3 text-sm text-muted">暂无注册表记录。</div>
                )}
              </CardBody>
            </Card>
          </>
        ) : null}
      </div>
    </AppShell>
  );
}

async function loadSkill(skillId: string) {
  try {
    const skill = await getSkill(skillId);
    const registry = await getSkillRegistryDetail(skillId).catch(() => null as SkillRegistryDetail | null);
    return { skill, registry, error: null };
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return { skill: null, registry: null, error: null };
    }
    return { skill: null, registry: null, error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
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
