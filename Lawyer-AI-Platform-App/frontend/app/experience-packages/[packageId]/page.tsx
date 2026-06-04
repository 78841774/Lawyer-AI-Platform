import Link from "next/link";
import { notFound } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { ApiError, ExperiencePackageRecord, getExperiencePackage } from "@/services/api";
import { ExperiencePackageActions } from "./ExperiencePackageActions";

export const dynamic = "force-dynamic";

export default async function ExperiencePackageDetailPage({ params }: { params: { packageId: string } }) {
  const packageId = decodeURIComponent(params.packageId);
  const { item, error } = await loadPackage(packageId);

  if (!item && !error) {
    notFound();
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <Link href="/experience-packages" className="text-sm font-medium text-accent">
            返回经验包
          </Link>
          <h1 className="mt-3 text-2xl font-semibold text-ink">{displayName(item) ?? "经验包详情"}</h1>
          <p className="mt-2 text-sm text-muted">{packageId}</p>
        </header>

        {error ? <StatusMessage message={error} /> : null}

        {item ? <ExperiencePackageDetail item={item} /> : null}
      </div>
    </AppShell>
  );
}

async function loadPackage(packageId: string) {
  try {
    return { item: await getExperiencePackage(packageId), error: null };
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return { item: null, error: null };
    }
    return { item: null, error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function ExperiencePackageDetail({ item }: { item: ExperiencePackageRecord }) {
  const id = item.experience_package_id ?? item.package_id ?? "暂无";
  return (
    <>
      <Card>
        <CardBody className="grid gap-4 md:grid-cols-2">
          <InfoRow label="experience_package_id" value={id} />
          <InfoRow label="source_run_id" value={item.source_run_id ?? "暂无"} />
          <InfoRow label="source_package_id" value={item.source_package_id ?? "暂无"} />
          <InfoRow label="case_cause_code" value={item.case_cause_code ?? item.domain ?? "暂无"} />
          <InfoRow label="status" value={item.status} />
          <InfoRow label="build_mode" value={item.build_mode ?? "暂无"} />
          <InfoRow label="llm_called" value={item.llm_called ? "是" : "否"} />
          <InfoRow label="real_case_material_used" value={item.real_case_material_used ? "是" : "否"} />
          <InfoRow label="skill_registry_published" value={item.skill_registry_published ? "是" : "否"} />
          <InfoRow label="published_skill_id" value={item.published_skill_id ?? "暂无"} />
          <InfoRow label="created_at" value={item.created_at ? formatDate(item.created_at) : "暂无"} />
        </CardBody>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">继承链与案由路径</h2>
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
            <h2 className="text-base font-semibold text-ink">Review / Safety</h2>
            <ul className="mt-3 space-y-2 text-sm text-muted">
              <li>requires_human_review: {item.review?.requires_human_review ? "true" : "false"}</li>
              <li>review_status: {item.review?.review_status ?? "暂无"}</li>
              <li>reviewed_by: {item.review?.reviewed_by ?? "暂无"}</li>
              <li>reviewed_at: {item.review?.reviewed_at ?? "暂无"}</li>
              <li>auto_publish_enabled: {item.safety?.auto_publish_enabled ? "true" : "false"}</li>
              <li>can_publish_to_skill_registry: {item.safety?.can_publish_to_skill_registry ? "true" : "false"}</li>
              <li>child_package_cannot_disable_safety_rules: {item.safety?.child_package_cannot_disable_safety_rules ? "true" : "false"}</li>
            </ul>
          </CardBody>
        </Card>
      </div>

      <Card>
        <CardBody>
          <h2 className="text-base font-semibold text-ink">Package Contents</h2>
          <pre className="mt-4 overflow-auto rounded-md border border-line bg-paper p-4 text-xs text-slate-700">
            {JSON.stringify(item.package_contents ?? item.manifest ?? {}, null, 2)}
          </pre>
        </CardBody>
      </Card>

      {item.experience_package_id ? (
        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Human Review Gate</h2>
            <div className="mt-4">
              <ExperiencePackageActions packageRecord={item} />
            </div>
          </CardBody>
        </Card>
      ) : null}
    </>
  );
}

function displayName(item: ExperiencePackageRecord | null) {
  return item?.experience_package_id ?? item?.name ?? item?.package_id;
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}
