import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card, CardBody } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  getVersionedTrainingPackage,
  getVersionedTrainingPackageFiles,
  VersionedSkillTrainingPackageDetail,
  VersionedSkillTrainingPackageFile
} from "@/services/api";
import { CreateMockTrainingRunButton } from "./CreateMockTrainingRunButton";

export const dynamic = "force-dynamic";

type PageProps = {
  params: {
    packageId: string;
  };
};

export default async function VersionedTrainingPackageDetailPage({ params }: PageProps) {
  const packageId = decodeURIComponent(params.packageId);
  const { detail, files, error } = await loadPackage(packageId);

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="训练包详情"
          title={packageId}
          description="查看 metadata、README、文件列表与训练范围。该页面只读，不触发训练运行。"
          action={
            <Link href="/versioned-training-packages" className="rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
              返回列表
            </Link>
          }
        />

        {error ? <StatusMessage message={error} /> : null}
        {detail ? <DetailContent detail={detail} files={files} /> : null}
      </div>
    </AppShell>
  );
}

async function loadPackage(packageId: string) {
  try {
    const [detail, files] = await Promise.all([
      getVersionedTrainingPackage(packageId),
      getVersionedTrainingPackageFiles(packageId)
    ]);
    return { detail, files, error: null };
  } catch {
    return { detail: null, files: [], error: "训练包详情暂不可用，请确认后端服务已启动。" };
  }
}

function DetailContent({
  detail,
  files
}: {
  detail: VersionedSkillTrainingPackageDetail;
  files: VersionedSkillTrainingPackageFile[];
}) {
  const metadata = detail.metadata;
  return (
    <>
      <Card>
        <CardBody className="grid gap-4 text-sm md:grid-cols-4">
          <Meta label="display_name" value={metadata.display_name} />
          <Meta label="version" value={metadata.version} />
          <Meta label="status" value={metadata.status} badge />
          <Meta label="source" value={metadata.source ?? metadata.source_packages?.join(", ") ?? "暂无"} />
          <Meta label="案由路径" value={metadata.case_cause_display_path ?? "暂无"} />
          <Meta label="适用案由" value={metadata.case_cause_code ?? "暂无"} />
          <Meta label="需要人工复核" value={metadata.requires_human_review ? "是" : "否"} />
          <Meta label="不自动训练" value={metadata.auto_train_enabled ? "否" : "是"} />
          <Meta label="不自动发布" value={metadata.auto_publish_enabled ? "否" : "是"} />
          <Meta label="下一阶段训练运行" value={metadata.next_stage ?? "v3.6-E versioned skill training run"} />
        </CardBody>
      </Card>

      <Card>
        <CardBody>
          <h2 className="text-base font-semibold text-ink">Mock Training Run</h2>
          <div className="mt-3 text-sm text-muted">
            仅创建 mock run metadata，不调用真实 LLM，不使用真实案件材料，不发布 Skill Registry。
          </div>
          <div className="mt-4">
            <CreateMockTrainingRunButton packageId={metadata.training_package_id} />
          </div>
        </CardBody>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">训练范围</h2>
            <div className="mt-4 flex flex-wrap gap-2">
              {metadata.training_scope.map((scope) => (
                <Badge key={scope} tone="gold">
                  {scope}
                </Badge>
              ))}
            </div>
            <h2 className="mt-6 text-base font-semibold text-ink">来源资产</h2>
            <ul className="mt-3 space-y-2 text-sm text-muted">
              {(metadata.source_assets ?? metadata.source_packages ?? []).map((asset) => (
                <li key={asset} className="break-words">
                  {asset}
                </li>
              ))}
            </ul>
            <h2 className="mt-6 text-base font-semibold text-ink">父级训练包</h2>
            <ul className="mt-3 space-y-2 text-sm text-muted">
              {(metadata.parent_package_ids ?? []).map((item) => (
                <li key={item}>{item}</li>
              ))}
              {(metadata.parent_package_ids ?? []).length === 0 ? <li>暂无</li> : null}
            </ul>
            <h2 className="mt-6 text-base font-semibold text-ink">继承顺序</h2>
            <div className="mt-3 text-sm text-muted">
              {(metadata.inheritance_order ?? []).join(" → ") || "暂无"}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">风险提示</h2>
            <div className="mt-3 space-y-2 text-sm text-muted">
              <p>当前训练包只读，仅作为后续训练输入。</p>
              <p>不会自动训练，不会自动发布，不覆盖现有 published skill。</p>
              <p>训练前仍需人工复核、脱敏检查与 schema 校验。</p>
              <p>规则继承采用父级到子级加载，安全规则不可关闭。</p>
            </div>
            {metadata.rule_override_policy ? (
              <>
                <h2 className="mt-6 text-base font-semibold text-ink">规则继承</h2>
                <ul className="mt-3 space-y-2 text-sm text-muted">
                  <li>更具体案由覆盖通用规则: {metadata.rule_override_policy.more_specific_overrides_general ? "是" : "否"}</li>
                  <li>安全规则不可关闭: {metadata.rule_override_policy.safety_rules_cannot_be_disabled ? "是" : "否"}</li>
                  <li>需要人工复核: {metadata.rule_override_policy.human_review_required ? "是" : "否"}</li>
                </ul>
              </>
            ) : null}
            {metadata.a10_validation ? (
              <>
                <h2 className="mt-6 text-base font-semibold text-ink">A10 校验</h2>
                <div className="mt-3 text-sm text-muted">{metadata.a10_validation.required_title ?? "暂无"}</div>
                <ul className="mt-3 space-y-2 text-sm text-muted">
                  {(metadata.a10_validation.required_modules ?? []).map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </>
            ) : null}
          </CardBody>
        </Card>
      </div>

      <Card>
        <CardBody>
          <h2 className="text-base font-semibold text-ink">README</h2>
          <pre className="mt-4 max-h-96 overflow-auto whitespace-pre-wrap rounded-md border border-line bg-slate-50 p-4 text-xs leading-6 text-muted">
            {detail.readme || "暂无 README"}
          </pre>
        </CardBody>
      </Card>

      <Card>
        <CardBody>
          <h2 className="text-base font-semibold text-ink">文件列表</h2>
          <div className="mt-4 divide-y divide-line text-sm">
            {files.map((file) => (
              <div key={file.path} className="grid gap-2 py-2 md:grid-cols-5">
                <span className="break-words md:col-span-4">{file.path}</span>
                <span className="text-muted">{file.size} bytes</span>
              </div>
            ))}
          </div>
        </CardBody>
      </Card>
    </>
  );
}

function Meta({ label, value, badge = false }: { label: string; value: string; badge?: boolean }) {
  return (
    <div>
      <div className="text-xs text-muted">{label}</div>
      <div className="mt-1 break-words text-ink">{badge ? <Badge tone="gold">{value}</Badge> : value}</div>
    </div>
  );
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}
