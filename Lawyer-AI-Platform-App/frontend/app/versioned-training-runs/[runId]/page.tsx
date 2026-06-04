import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card, CardBody } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getVersionedTrainingRun, VersionedSkillTrainingRun } from "@/services/api";
import { CreateExperiencePackageCandidateButton } from "./CreateExperiencePackageCandidateButton";

export const dynamic = "force-dynamic";

type PageProps = {
  params: {
    runId: string;
  };
};

export default async function VersionedTrainingRunDetailPage({ params }: PageProps) {
  const runId = decodeURIComponent(params.runId);
  const { run, error } = await loadRun(runId);

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Mock Training Run"
          title={runId}
          description="查看 mock training run 的继承链、案由路径、mock evaluation 与安全边界。"
          action={
            <Link href="/versioned-training-runs" className="rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
              返回运行列表
            </Link>
          }
        />

        {error ? <StatusMessage message={error} /> : null}
        {run ? <RunDetail run={run} /> : null}
      </div>
    </AppShell>
  );
}

async function loadRun(runId: string) {
  try {
    return { run: await getVersionedTrainingRun(runId), error: null };
  } catch {
    return { run: null, error: "训练运行详情暂不可用，请确认后端服务已启动。" };
  }
}

function RunDetail({ run }: { run: VersionedSkillTrainingRun }) {
  return (
    <>
      <Card>
        <CardBody className="grid gap-4 text-sm md:grid-cols-4">
          <Meta label="Package ID" value={run.package_id} />
          <Meta label="Case Cause" value={run.case_cause_code} />
          <Meta label="Status" value={run.status} badge />
          <Meta label="Runner" value={run.runner} />
          <Meta label="LLM Provider" value={run.llm_provider} />
          <Meta label="LLM Called" value={run.llm_called ? "是" : "否"} />
          <Meta label="真实案件材料" value={run.inputs.real_case_material_used ? "已使用" : "未使用"} />
          <Meta label="Skill Registry 发布" value={run.outputs.skill_registry_published ? "已发布" : "未发布"} />
        </CardBody>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Package Inheritance</h2>
            <div className="mt-4 flex flex-wrap gap-2">
              {run.inheritance_chain.map((item) => (
                <Badge key={item} tone="gold">
                  {item}
                </Badge>
              ))}
            </div>
            <h2 className="mt-6 text-base font-semibold text-ink">Taxonomy Path</h2>
            <div className="mt-3 text-sm text-muted">{run.taxonomy_path.join(" → ") || "暂无"}</div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety</h2>
            <ul className="mt-3 space-y-2 text-sm text-muted">
              <li>需要人工复核: {run.safety.requires_human_review ? "是" : "否"}</li>
              <li>自动训练: {run.safety.auto_train_enabled ? "是" : "否"}</li>
              <li>自动发布: {run.safety.auto_publish_enabled ? "是" : "否"}</li>
              <li>子级训练包不可关闭安全规则: {run.safety.child_package_cannot_disable_safety_rules ? "是" : "否"}</li>
              <li>legacy asset 修改: {run.inputs.legacy_asset_modified ? "是" : "否"}</li>
              <li>正式经验包生成: {run.outputs.experience_package_created ? "是" : "否"}</li>
              <li>Skill candidate 生成: {run.outputs.skill_candidate_created ? "是" : "否"}</li>
            </ul>
          </CardBody>
        </Card>
      </div>

      <Card>
        <CardBody>
          <h2 className="text-base font-semibold text-ink">Experience Package Candidate</h2>
          <div className="mt-4">
            <CreateExperiencePackageCandidateButton runId={run.run_id} />
          </div>
        </CardBody>
      </Card>

      <Card>
        <CardBody>
          <h2 className="text-base font-semibold text-ink">Mock Evaluation</h2>
          <div className="mt-4 grid gap-3 text-sm md:grid-cols-5">
            <Meta label="accuracy" value={String(run.mock_evaluation.accuracy)} />
            <Meta label="consistency" value={String(run.mock_evaluation.consistency)} />
            <Meta label="completeness" value={String(run.mock_evaluation.completeness)} />
            <Meta label="legal_relevance" value={String(run.mock_evaluation.legal_relevance)} />
            <Meta label="report_quality" value={String(run.mock_evaluation.report_quality)} />
          </div>
          <div className="mt-4 rounded-md border border-line bg-slate-50 p-4 text-sm text-muted">
            {run.mock_evaluation.notes}
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
