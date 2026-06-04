"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  PersonalAlphaFinalReadinessRunDetail,
  PersonalAlphaFinalReadinessStatus,
  PersonalAlphaFinalReadinessSummaryResponse,
  getPersonalAlphaFinalReadinessRunDetail,
  getPersonalAlphaFinalReadinessRunSummary,
  getPersonalAlphaFinalReadinessStatus
} from "@/services/api";

export default function PersonalAlphaFinalReadinessPage() {
  const router = useRouter();
  const [status, setStatus] = useState<PersonalAlphaFinalReadinessStatus | null>(null);
  const [runDetail, setRunDetail] = useState<PersonalAlphaFinalReadinessRunDetail | null>(null);
  const [runSummary, setRunSummary] = useState<PersonalAlphaFinalReadinessSummaryResponse | null>(null);
  const [workspaceRunId, setWorkspaceRunId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadStatus() {
      try {
        setStatus(await getPersonalAlphaFinalReadinessStatus());
        const queryValue = new URLSearchParams(window.location.search).get("workspace_run_id") ?? "";
        if (queryValue) {
          setWorkspaceRunId(queryValue);
          await loadRun(queryValue);
        }
      } catch {
        setError("Personal Alpha Final Readiness API 暂不可用，请确认后端服务已启动。");
      }
    }

    void loadStatus();
  }, []);

  async function loadRun(id: string) {
    setLoading(true);
    setError("");
    try {
      const [nextRunDetail, nextRunSummary] = await Promise.all([
        getPersonalAlphaFinalReadinessRunDetail(id),
        getPersonalAlphaFinalReadinessRunSummary(id)
      ]);
      setRunDetail(nextRunDetail);
      setRunSummary(nextRunSummary);
    } catch {
      setError("Final readiness 加载失败，请确认 workspace_run_id 存在且后端服务已启动。");
    } finally {
      setLoading(false);
    }
  }

  async function submitRun(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const id = workspaceRunId.trim();
    if (!id) {
      return;
    }
    router.replace(`/personal-alpha-final-readiness?workspace_run_id=${encodeURIComponent(id)}`);
    await loadRun(id);
  }

  const summary = runDetail?.summary ?? runSummary?.summary;
  const safetyChecklist = runDetail?.safety_checklist;

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Personal Alpha"
          title="Personal Alpha Final Review Readiness"
          description="个人 Alpha 最终复核准备度：聚合本地 controlled mock workflow 的阶段状态、source review decisions 和安全 gate，仅展示 metadata。"
        />
        {workspaceRunId.trim() ? (
          <div className="flex flex-wrap gap-2">
            <Link href={`/personal-alpha-final-gate?workspace_run_id=${encodeURIComponent(workspaceRunId.trim())}`} className="inline-flex rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
              View Controlled Final Gate
            </Link>
            <Link href={`/personal-alpha-final-packet?workspace_run_id=${encodeURIComponent(workspaceRunId.trim())}`} className="inline-flex rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
              View Final Review Packet
            </Link>
            <span className="rounded-md border border-line bg-white px-3 py-2 text-sm text-muted">
              Packet creation requires final gate approval.
            </span>
          </div>
        ) : null}
        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Load Workspace Run</h2>
            <form onSubmit={submitRun} className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">
              <label className="text-sm">
                <span className="text-muted">workspace_run_id</span>
                <input value={workspaceRunId} onChange={(event) => setWorkspaceRunId(event.target.value)} className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-ink" />
              </label>
              <div className="flex items-end">
                <Button type="submit" disabled={loading}>{loading ? "加载中..." : "Load Readiness"}</Button>
              </div>
            </form>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_personal_alpha_final_readiness"} />
              <InfoRow label="local-only" value="true" />
              <InfoRow label="mock_first_enabled" value={String(status?.mock_first_enabled ?? true)} />
              <InfoRow label="controlled_first_enabled" value={String(status?.controlled_first_enabled ?? true)} />
              <InfoRow label="metadata_only" value={String(status?.metadata_only ?? true)} />
              <InfoRow label="redacted_only" value={String(status?.redacted_only ?? true)} />
              <InfoRow label="preview_only" value={String(status?.preview_only ?? true)} />
              <InfoRow label="advisory_only" value={String(status?.advisory_only ?? true)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
              <InfoRow label="runtime_storage_path" value={status?.runtime_storage_path ?? "storage/runtime/personal_alpha_final_readiness"} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Run Summary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="workspace_run_id" value={(runDetail?.workspace_run_id ?? workspaceRunId) || "-"} />
              <InfoRow label="case_id" value={runDetail?.case_id ?? "-"} />
              <InfoRow label="workspace_id" value={runDetail?.workspace_id ?? "-"} />
              <InfoRow label="workflow_mode" value={runDetail?.workflow_mode ?? "-"} />
              <InfoRow label="status" value={runDetail?.status ?? "not_loaded"} />
              <InfoRow label="created_at" value={runDetail?.created_at ?? "-"} />
              <InfoRow label="advisory_only" value={String(runDetail?.advisory_only ?? true)} />
              <InfoRow label="final_legal_opinion_generated" value={String(runDetail?.final_legal_opinion_generated ?? false)} />
              <InfoRow label="raw_content_included" value={String(runDetail?.raw_content_included ?? false)} />
            </div>
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-3 xl:grid-cols-6">
          <SummaryTile label="stages" value={summary?.total_stages ?? 0} />
          <SummaryTile label="mandatory" value={summary?.mandatory_stage_count ?? 0} />
          <SummaryTile label="ready" value={summary?.ready_stage_count ?? 0} />
          <SummaryTile label="blocked" value={summary?.blocked_stage_count ?? 0} />
          <SummaryTile label="pending" value={summary?.pending_stage_count ?? 0} />
          <SummaryTile label="decisions" value={summary?.decision_count ?? 0} />
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Readiness Summary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="stage_ready" value={String(summary?.stage_ready ?? false)} />
              <InfoRow label="final_review_ready" value={String(summary?.final_review_ready ?? false)} />
              <InfoRow label="requires_additional_review" value={String(summary?.requires_additional_review ?? true)} />
              <InfoRow label="approved_decision_count" value={String(summary?.approved_decision_count ?? 0)} />
              <InfoRow label="rejected_decision_count" value={String(summary?.rejected_decision_count ?? 0)} />
              <InfoRow label="revision_requested_count" value={String(summary?.revision_requested_count ?? 0)} />
              <InfoRow label="unclear_decision_count" value={String(summary?.unclear_decision_count ?? 0)} />
              <InfoRow label="mock_or_redacted_only" value={String(summary?.mock_or_redacted_only ?? true)} />
            </div>
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {(runDetail?.stages ?? []).map((stage) => (
            <Card key={stage.stage_id}>
              <CardBody>
                <div className="text-xs uppercase tracking-wide text-muted">{stage.stage_id}</div>
                <div className="mt-2 text-base font-semibold text-ink">{stage.label}</div>
                <div className="mt-3 space-y-2 text-sm text-muted">
                  <div>{stage.workspace_stage_status}</div>
                  <div>decision: {stage.latest_decision}</div>
                  <div>stage_ready: {String(stage.stage_ready)}</div>
                  <div>blocked: {String(stage.blocked)}</div>
                  <div>{stage.notes}</div>
                </div>
              </CardBody>
            </Card>
          ))}
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Checklist</h2>
            <JsonPanel title="safety_checklist" value={safetyChecklist ?? { metadata_only: true, advisory_only: true }} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Warnings / Alerts</h2>
            <JsonPanel title="warnings" value={runDetail?.warnings ?? runSummary?.warnings ?? []} />
            <JsonPanel title="blocked_stages" value={runDetail?.blocked_stages ?? runSummary?.blocked_stages ?? []} />
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}

function SummaryTile({ label, value }: { label: string; value: number }) {
  return (
    <Card>
      <CardBody>
        <div className="text-xs uppercase tracking-wide text-muted">{label}</div>
        <div className="mt-2 text-2xl font-semibold text-ink">{value}</div>
      </CardBody>
    </Card>
  );
}

function JsonPanel({ title, value }: { title: string; value: unknown }) {
  return (
    <div className="mt-4">
      <div className="text-xs font-semibold uppercase tracking-wide text-muted">{title}</div>
      <pre className="mt-2 max-h-96 overflow-auto rounded-md border border-line bg-paper p-3 text-xs text-slate-700">{JSON.stringify(value ?? {}, null, 2)}</pre>
    </div>
  );
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}
