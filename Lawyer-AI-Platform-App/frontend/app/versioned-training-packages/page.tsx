import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getVersionedTrainingPackages, VersionedSkillTrainingPackage } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function VersionedTrainingPackagesPage() {
  const { packages, error } = await loadPackages();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law Skill Factory"
          title="版本化训练包"
          description="展示 legacy assets 封装后的只读训练输入包。当前状态为 prepared_for_training，不自动训练、不自动发布。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <div className="grid gap-3 border-b border-line bg-slate-50 px-4 py-3 text-xs font-semibold text-muted md:grid-cols-8">
            <span className="md:col-span-2">training_package_id</span>
            <span>domain</span>
            <span>version</span>
            <span>status</span>
            <span>来源资产</span>
            <span>人工复核</span>
            <span>操作</span>
          </div>
          {packages.length > 0 ? (
            packages.map((item) => <PackageRow key={item.training_package_id} item={item} />)
          ) : (
            <div className="p-5 text-sm text-muted">暂无版本化训练包。</div>
          )}
        </Card>
      </div>
    </AppShell>
  );
}

async function loadPackages() {
  try {
    return { packages: await getVersionedTrainingPackages(), error: null };
  } catch {
    return { packages: [], error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function PackageRow({ item }: { item: VersionedSkillTrainingPackage }) {
  return (
    <article className="grid gap-3 border-b border-line px-4 py-4 text-sm last:border-b-0 md:grid-cols-8">
      <div className="md:col-span-2">
        <Link
          href={`/versioned-training-packages/${encodeURIComponent(item.training_package_id)}`}
          className="font-medium text-ink hover:text-accent"
        >
          {item.training_package_id}
        </Link>
        <div className="mt-1 text-xs text-muted">{item.display_name ?? "暂无"}</div>
      </div>
      <span className="text-muted">{item.domain ?? "暂无"}</span>
      <span className="text-muted">{item.version}</span>
      <span>
        <Badge tone="gold">{item.status}</Badge>
      </span>
      <span className="break-words text-muted">{item.legacy_skill_id ?? "组合包"}</span>
      <span className="text-muted">需要人工复核</span>
      <span>
        <Link
          href={`/versioned-training-packages/${encodeURIComponent(item.training_package_id)}`}
          className="rounded-md border border-line bg-white px-3 py-2 text-xs font-medium text-ink shadow-sm"
        >
          查看详情
        </Link>
      </span>
      <div className="text-xs text-muted md:col-span-8">
        不自动训练: 是 / 不自动发布: 是 / registry: {item.registry_status ?? "readonly"}
      </div>
    </article>
  );
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}
