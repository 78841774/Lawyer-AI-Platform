import Link from "next/link";
import { notFound } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { ApiError, getSkillRegistryDetail, SkillRegistryDetail, SkillRegistryRecord } from "@/services/api";
import { SkillRegistryActions } from "./SkillRegistryActions";

export const dynamic = "force-dynamic";

export default async function SkillRegistryDetailPage({ params }: { params: { skillId: string } }) {
  const skillId = decodeURIComponent(params.skillId);
  const { detail, error } = await loadSkill(skillId);

  if (!detail && !error) {
    notFound();
  }

  const item = detail ? normalizeDetail(detail) : null;

  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <Link href="/skill-registry" className="text-sm font-medium text-accent">
            返回技能注册表
          </Link>
          <h1 className="mt-3 text-2xl font-semibold text-ink">{skillId}</h1>
          <p className="mt-2 text-sm text-muted">Controlled Skill Registry Publish</p>
        </header>

        {error ? <StatusMessage message={error} /> : null}
        {item ? <RegistryDetail item={item} /> : null}
      </div>
    </AppShell>
  );
}

async function loadSkill(skillId: string) {
  try {
    return { detail: await getSkillRegistryDetail(skillId), error: null };
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return { detail: null, error: null };
    }
    return { detail: null, error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function RegistryDetail({ item }: { item: SkillRegistryRecord }) {
  return (
    <>
      <Card>
        <CardBody className="grid gap-4 md:grid-cols-2">
          <InfoRow label="skill_id" value={item.skill_id} />
          <InfoRow label="source_experience_package_id" value={item.source_experience_package_id ?? "暂无"} />
          <InfoRow label="source_run_id" value={item.source_run_id ?? "暂无"} />
          <InfoRow label="source_package_id" value={item.source_package_id ?? "暂无"} />
          <InfoRow label="case_cause_code" value={item.case_cause_code ?? item.domain ?? "暂无"} />
          <InfoRow label="status" value={item.status} />
          <InfoRow label="version" value={item.version} />
          <InfoRow label="publish_mode" value={item.publish_mode ?? "暂无"} />
          <InfoRow label="workspace_scope" value={item.workspace_scope ?? "暂无"} />
          <InfoRow label="llm_called" value={item.llm_called ? "是" : "否"} />
          <InfoRow label="real_case_material_used" value={item.real_case_material_used ? "是" : "否"} />
          <InfoRow label="published_at" value={item.published_at ?? "暂无"} />
        </CardBody>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Review / Safety</h2>
            <ul className="mt-3 space-y-2 text-sm text-muted">
              <li>requires_human_review: {item.review?.requires_human_review ? "true" : "false"}</li>
              <li>review_status: {item.review?.review_status ?? "暂无"}</li>
              <li>reviewed_by: {item.review?.reviewed_by ?? "暂无"}</li>
              <li>controlled_publish: {item.safety?.controlled_publish ? "true" : "false"}</li>
              <li>auto_publish_enabled: {item.safety?.auto_publish_enabled ? "true" : "false"}</li>
              <li>rollback_supported: {item.safety?.rollback_supported ? "true" : "false"}</li>
              <li>deprecate_supported: {item.safety?.deprecate_supported ? "true" : "false"}</li>
            </ul>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Runtime Boundary</h2>
            <ul className="mt-3 space-y-2 text-sm text-muted">
              <li>workspace_runtime_enabled: {item.runtime?.workspace_runtime_enabled ? "true" : "false"}</li>
              <li>skill_aware_case_processing_enabled: {item.runtime?.skill_aware_case_processing_enabled ? "true" : "false"}</li>
              <li>requires_manual_enablement: {item.runtime?.requires_manual_enablement ? "true" : "false"}</li>
            </ul>
          </CardBody>
        </Card>
      </div>

      <Card>
        <CardBody>
          <h2 className="text-base font-semibold text-ink">Inheritance / Taxonomy</h2>
          <div className="mt-4 flex flex-wrap gap-2">
            {(item.inheritance_chain ?? []).map((entry) => (
              <Badge key={entry} tone="gold">{entry}</Badge>
            ))}
          </div>
          <div className="mt-4 text-sm text-muted">{(item.taxonomy_path ?? []).join(" → ") || "暂无"}</div>
        </CardBody>
      </Card>

      <Card>
        <CardBody>
          <h2 className="text-base font-semibold text-ink">Deprecate / Rollback</h2>
          <div className="mt-4">
            <SkillRegistryActions skillId={item.skill_id} />
          </div>
        </CardBody>
      </Card>

      <Card>
        <CardBody>
          <h2 className="text-base font-semibold text-ink">Events</h2>
          <pre className="mt-4 overflow-auto rounded-md border border-line bg-paper p-4 text-xs text-slate-700">
            {JSON.stringify(item.events ?? [], null, 2)}
          </pre>
        </CardBody>
      </Card>
    </>
  );
}

function normalizeDetail(detail: SkillRegistryDetail): SkillRegistryRecord {
  if ("skill" in detail && detail.skill) {
    return {
      skill_id: detail.skill.skill_id,
      skill_name: detail.skill.skill_name,
      domain: detail.skill.domain,
      version: detail.skill.version,
      status: detail.skill.status,
      validation_status: detail.skill.validation_status,
      evaluation_score: detail.skill.evaluation_score,
      package_id: detail.package?.package_id ?? null,
      package_status: detail.package?.status ?? null
    };
  }
  return detail as SkillRegistryRecord;
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}
