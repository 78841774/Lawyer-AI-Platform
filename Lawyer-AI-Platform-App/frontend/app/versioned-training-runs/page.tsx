import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getVersionedTrainingRuns, VersionedSkillTrainingRun } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function VersionedTrainingRunsPage() {
  const { runs, error } = await loadRuns();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law Skill Factory"
          title="版本化训练运行"
          description="展示基于版本化训练包的 mock training run。当前不调用真实 LLM、不读取真实案件材料、不发布 Skill。"
          action={
            <Link href="/versioned-training-packages" className="rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
              查看训练包
            </Link>
          }
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <div className="grid gap-3 border-b border-line bg-slate-50 px-4 py-3 text-xs font-semibold text-muted md:grid-cols-12">
            <span className="md:col-span-2">Run ID</span>
            <span className="md:col-span-2">Package ID</span>
            <span>Case Cause</span>
            <span>Status</span>
            <span>LLM Called</span>
            <span>Real Case Material Used</span>
            <span>Experience Package</span>
            <span>Skill Published</span>
            <span>Requires Human Review</span>
            <span>操作</span>
          </div>
          {runs.length > 0 ? (
            runs.map((run) => <RunRow key={run.run_id} run={run} />)
          ) : (
            <div className="p-5 text-sm text-muted">暂无 mock training run。</div>
          )}
        </Card>
      </div>
    </AppShell>
  );
}

async function loadRuns() {
  try {
    return { runs: await getVersionedTrainingRuns(), error: null };
  } catch {
    return { runs: [], error: "训练运行 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function RunRow({ run }: { run: VersionedSkillTrainingRun }) {
  return (
    <article className="grid gap-3 border-b border-line px-4 py-4 text-sm last:border-b-0 md:grid-cols-12">
      <Link
        href={`/versioned-training-runs/${encodeURIComponent(run.run_id)}`}
        className="break-words font-medium text-ink hover:text-accent md:col-span-2"
      >
        {run.run_id}
      </Link>
      <span className="break-words text-muted md:col-span-2">{run.package_id}</span>
      <span className="text-muted">{run.case_cause_code}</span>
      <span>
        <Badge tone="gold">{run.status}</Badge>
      </span>
      <Bool value={run.llm_called} />
      <Bool value={run.inputs.real_case_material_used} />
      <Bool value={run.outputs.experience_package_created} />
      <Bool value={run.outputs.skill_registry_published} />
      <Bool value={run.safety.requires_human_review} />
      <span>
        <Link
          href={`/versioned-training-runs/${encodeURIComponent(run.run_id)}`}
          className="rounded-md border border-line bg-white px-3 py-2 text-xs font-medium text-ink shadow-sm"
        >
          查看详情
        </Link>
      </span>
    </article>
  );
}

function Bool({ value }: { value: boolean }) {
  return <span className={value ? "text-accent" : "text-muted"}>{value ? "是" : "否"}</span>;
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}
