import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { ExperiencePackageRecord, getExperiencePackages } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function ExperiencePackagesPage() {
  const { packages, error } = await loadPackages();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 经验包"
          title="Experience Package Candidate"
          description="展示 mock training run 生成的 Candidate，以及历史 Experience Package。Candidate 需人工审核后才允许受控发布。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <div className="grid gap-3 border-b border-line bg-slate-50 px-4 py-3 text-xs font-semibold text-muted md:grid-cols-10">
            <span className="md:col-span-2">经验包 ID</span>
            <span className="md:col-span-2">来源训练运行</span>
            <span className="md:col-span-2">来源训练包</span>
            <span>案由</span>
            <span>状态</span>
            <span>审核状态</span>
            <span>操作</span>
          </div>
          {packages.length > 0 ? (
            packages.map((item) => <PackageRow key={packageId(item)} item={item} />)
          ) : (
            <div className="p-5 text-sm text-muted">暂无经验包。</div>
          )}
        </Card>
      </div>
    </AppShell>
  );
}

async function loadPackages() {
  try {
    return { packages: await getExperiencePackages(), error: null };
  } catch {
    return { packages: [], error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function PackageRow({ item }: { item: ExperiencePackageRecord }) {
  const id = packageId(item);
  return (
    <article className="grid gap-3 border-b border-line px-4 py-4 text-sm last:border-b-0 md:grid-cols-10">
      <Link href={`/experience-packages/${encodeURIComponent(id)}`} className="break-words font-medium text-ink hover:text-accent md:col-span-2">
        {id}
      </Link>
      <span className="break-words text-muted md:col-span-2">{item.source_run_id ?? item.skill_id ?? "暂无"}</span>
      <span className="break-words text-muted md:col-span-2">{item.source_package_id ?? item.package_path ?? "暂无"}</span>
      <span className="text-muted">{item.case_cause_code ?? item.domain ?? "暂无"}</span>
      <span>
        <Badge tone="gold">{item.status}</Badge>
      </span>
      <span className="text-muted">{item.review?.review_status ?? "暂无"}</span>
      <Link href={`/experience-packages/${encodeURIComponent(id)}`} className="font-medium text-accent">
        查看详情
      </Link>
      <span className="break-words text-xs text-muted md:col-span-10">
        可发布: {item.safety?.can_publish_to_skill_registry ? "是" : "否"} / Skill Registry 已发布: {item.skill_registry_published ? "是" : "否"}
      </span>
    </article>
  );
}

function packageId(item: ExperiencePackageRecord) {
  return item.experience_package_id ?? item.package_id ?? "unknown_experience_package";
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}
