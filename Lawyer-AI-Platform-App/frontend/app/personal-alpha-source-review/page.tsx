"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  PersonalAlphaSourceReviewRunDetail,
  PersonalAlphaSourceReviewStatus,
  getPersonalAlphaSourceReviewRunDetail,
  getPersonalAlphaSourceReviewStatus
} from "@/services/api";

export default function PersonalAlphaSourceReviewPage() {
  const router = useRouter();
  const [status, setStatus] = useState<PersonalAlphaSourceReviewStatus | null>(null);
  const [runDetail, setRunDetail] = useState<PersonalAlphaSourceReviewRunDetail | null>(null);
  const [workspaceRunId, setWorkspaceRunId] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function loadStatus() {
      try {
        setStatus(await getPersonalAlphaSourceReviewStatus());
        const queryValue = new URLSearchParams(window.location.search).get("workspace_run_id") ?? "";
        if (queryValue) {
          setWorkspaceRunId(queryValue);
          await loadRun(queryValue);
        }
      } catch {
        setError("Personal Alpha Source Review API 暂不可用，请确认后端服务已启动。");
      }
    }

    void loadStatus();
  }, []);

  async function loadRun(id: string) {
    setLoading(true);
    setError("");
    try {
      setRunDetail(await getPersonalAlphaSourceReviewRunDetail(id));
    } catch {
      setError("Source trace review 加载失败，请确认 workspace_run_id 存在且后端服务已启动。");
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
    router.replace(`/personal-alpha-source-review?workspace_run_id=${encodeURIComponent(id)}`);
    await loadRun(id);
  }

  const evidenceSummary = runDetail?.evidence_summary;
  const safetyChecklist = runDetail?.safety_checklist;

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Personal Alpha"
          title="Personal Alpha Source Review"
          description="个人 Alpha 证据链 / source refs 复核页面；仅展示 metadata，不显示原文，显示 blocked / ready / pending / mock 状态。"
        />
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
                <Button type="submit" disabled={loading}>{loading ? "加载中..." : "Load Source Review"}</Button>
              </div>
            </form>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_personal_alpha_source_review"} />
              <InfoRow label="local-only" value="true" />
              <InfoRow label="mock_first_enabled" value={String(status?.mock_first_enabled ?? true)} />
              <InfoRow label="controlled_first_enabled" value={String(status?.controlled_first_enabled ?? true)} />
              <InfoRow label="metadata_only" value={String(status?.metadata_only ?? true)} />
              <InfoRow label="redacted_only" value={String(status?.redacted_only ?? true)} />
              <InfoRow label="preview_only" value={String(status?.preview_only ?? true)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
              <InfoRow label="auto_skill_publish_enabled" value={String(status?.auto_skill_publish_enabled ?? false)} />
              <InfoRow label="auto_workspace_runtime_enabled" value={String(status?.auto_workspace_runtime_enabled ?? false)} />
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
              <InfoRow label="mock_or_redacted_only" value={String(runDetail?.mock_or_redacted_only ?? true)} />
              <InfoRow label="raw_content_included" value={String(runDetail?.raw_content_included ?? false)} />
            </div>
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-3 xl:grid-cols-5">
          <SummaryTile label="total sources" value={evidenceSummary?.total_sources ?? 0} />
          <SummaryTile label="evidence items" value={evidenceSummary?.total_evidence_items ?? 0} />
          <SummaryTile label="ready" value={evidenceSummary?.ready_sources ?? 0} />
          <SummaryTile label="pending" value={evidenceSummary?.pending_sources ?? 0} />
          <SummaryTile label="blocked" value={evidenceSummary?.blocked_sources ?? 0} />
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Checklist</h2>
            <JsonPanel title="safety_checklist" value={safetyChecklist ?? { metadata_only: true, raw_material_text_included: false }} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Source Trace Metadata</h2>
            <JsonPanel title="source_traces" value={runDetail?.source_traces ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Audit Timeline</h2>
            <JsonPanel title="audit_timeline" value={runDetail?.audit_timeline ?? []} />
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
