import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getExperiencePackages } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function ExperiencePackagesPage() {
  const { packages, error } = await loadPackages();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 经验包"
          title="经验包"
          description="展示已构建的 Experience Package 与 manifest 查看入口。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <div className="grid gap-3 border-b border-line bg-slate-50 px-4 py-3 text-xs font-semibold text-muted md:grid-cols-8">
            <span>package_id</span>
            <span>skill_id</span>
            <span>名称</span>
            <span>领域</span>
            <span>版本</span>
            <span>状态</span>
            <span>创建时间</span>
            <span>manifest</span>
          </div>
          {packages.length > 0 ? (
            packages.map((item) => (
              <article key={item.package_id} className="grid gap-3 border-b border-line px-4 py-4 text-sm last:border-b-0 md:grid-cols-8">
                <span className="break-words font-medium text-ink">{item.package_id}</span>
                <span className="break-words text-muted">{item.skill_id}</span>
                <span className="text-muted">{item.name}</span>
                <span className="text-muted">{item.domain}</span>
                <span className="text-muted">{item.version}</span>
                <span>
                  <Badge tone="gold">{item.status}</Badge>
                </span>
                <span className="text-muted">{formatDate(item.created_at)}</span>
                <span>
                  <Link href={`/experience-packages/${item.package_id}`} className="font-medium text-accent">
                    查看 manifest
                  </Link>
                </span>
                <span className="break-words text-xs text-muted md:col-span-8">package_path: {item.package_path || "暂无"}</span>
              </article>
            ))
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

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}
