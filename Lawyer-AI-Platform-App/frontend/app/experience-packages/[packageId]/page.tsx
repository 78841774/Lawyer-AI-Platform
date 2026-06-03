import Link from "next/link";
import { notFound } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { ApiError, getExperiencePackage, getExperiencePackageManifest } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function ExperiencePackageDetailPage({ params }: { params: { packageId: string } }) {
  const { item, manifest, error } = await loadPackage(params.packageId);

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
          <h1 className="mt-3 text-2xl font-semibold text-ink">{item?.name ?? "经验包详情"}</h1>
          <p className="mt-2 text-sm text-muted">{params.packageId}</p>
        </header>

        {error ? <StatusMessage message={error} /> : null}

        {item ? (
          <>
            <Card>
              <CardBody>
                <div className="grid gap-4 md:grid-cols-2">
                  <InfoRow label="package_id" value={item.package_id} />
                  <InfoRow label="skill_id" value={item.skill_id} />
                  <InfoRow label="name" value={item.name} />
                  <InfoRow label="domain" value={item.domain} />
                  <InfoRow label="version" value={item.version} />
                  <InfoRow label="status" value={item.status} />
                  <InfoRow label="package_path" value={item.package_path || "暂无"} />
                  <InfoRow label="created_at" value={formatDate(item.created_at)} />
                </div>
              </CardBody>
            </Card>

            <Card>
              <CardBody>
                <div className="text-sm font-semibold text-ink">manifest</div>
                <pre className="mt-3 overflow-auto rounded-md border border-line bg-paper p-4 text-xs text-slate-700">
                  {JSON.stringify(manifest ?? {}, null, 2)}
                </pre>
              </CardBody>
            </Card>
          </>
        ) : null}
      </div>
    </AppShell>
  );
}

async function loadPackage(packageId: string) {
  try {
    const [item, manifest] = await Promise.all([
      getExperiencePackage(packageId),
      getExperiencePackageManifest(packageId)
    ]);
    return { item, manifest, error: null };
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return { item: null, manifest: null, error: null };
    }
    return { item: null, manifest: null, error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}
