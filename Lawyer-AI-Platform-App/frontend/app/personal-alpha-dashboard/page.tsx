"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  PersonalAlphaDashboardAuditTimeline,
  PersonalAlphaDashboardSourceTraceSummary,
  PersonalAlphaDashboardStageHealth,
  PersonalAlphaDashboardStatus,
  PersonalAlphaDashboardSummary,
  getPersonalAlphaDashboardAuditTimeline,
  getPersonalAlphaDashboardSourceTraceSummary,
  getPersonalAlphaDashboardStageHealth,
  getPersonalAlphaDashboardStatus,
  getPersonalAlphaDashboardSummary
} from "@/services/api";

export default function PersonalAlphaDashboardPage() {
  const router = useRouter();
  const [status, setStatus] = useState<PersonalAlphaDashboardStatus | null>(null);
  const [summary, setSummary] = useState<PersonalAlphaDashboardSummary | null>(null);
  const [stageHealth, setStageHealth] = useState<PersonalAlphaDashboardStageHealth[]>([]);
  const [auditTimeline, setAuditTimeline] = useState<PersonalAlphaDashboardAuditTimeline | null>(null);
  const [sourceTraceSummary, setSourceTraceSummary] = useState<PersonalAlphaDashboardSourceTraceSummary | null>(null);
  const [workspaceRunId, setWorkspaceRunId] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [nextStatus, nextSummary, nextStageHealth, nextAuditTimeline, nextSourceTraceSummary] = await Promise.all([
          getPersonalAlphaDashboardStatus(),
          getPersonalAlphaDashboardSummary(),
          getPersonalAlphaDashboardStageHealth(),
          getPersonalAlphaDashboardAuditTimeline(),
          getPersonalAlphaDashboardSourceTraceSummary()
        ]);
        setStatus(nextStatus);
        setSummary(nextSummary);
        setStageHealth(nextStageHealth);
        setAuditTimeline(nextAuditTimeline);
        setSourceTraceSummary(nextSourceTraceSummary);
      } catch {
        setError("Personal Alpha Dashboard API 暂不可用，请确认后端服务已启动。");
      }
    }

    void loadDashboard();
  }, []);

  function openRunDetail(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const id = workspaceRunId.trim();
    if (id) {
      router.push(`/personal-alpha-dashboard/runs/${encodeURIComponent(id)}`);
    }
  }

  const latestWorkspaceRunId = findWorkspaceRunId(auditTimeline?.timeline ?? []);

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Personal Alpha"
          title="个人 Alpha 案件总控台"
          description="个人 Alpha 案件总控台：集中查看本地 controlled mock workflow 的阶段健康度、审计时间线和 source trace 摘要。"
        />
        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_personal_alpha_dashboard"} />
              <InfoRow label="local-only" value="true" />
              <InfoRow label="mock_first_enabled" value={String(status?.mock_first_enabled ?? true)} />
              <InfoRow label="controlled_first_enabled" value={String(status?.controlled_first_enabled ?? true)} />
              <InfoRow label="metadata_only" value={String(status?.metadata_only ?? true)} />
              <InfoRow label="redacted_only" value={String(status?.redacted_only ?? true)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
              <InfoRow label="auto_skill_publish_enabled" value={String(status?.auto_skill_publish_enabled ?? false)} />
              <InfoRow label="auto_workspace_runtime_enabled" value={String(status?.auto_workspace_runtime_enabled ?? false)} />
              <InfoRow label="source_runtime_path" value={status?.source_runtime_path ?? "storage/runtime/personal_alpha_workspace"} />
            </div>
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-3 xl:grid-cols-6">
          <SummaryTile label="workspace runs" value={summary?.total_workspace_runs ?? 0} />
          <SummaryTile label="ready stages" value={summary?.ready_stage_count ?? 0} />
          <SummaryTile label="pending stages" value={summary?.pending_stage_count ?? 0} />
          <SummaryTile label="blocked stages" value={summary?.blocked_stage_count ?? 0} />
          <SummaryTile label="audit events" value={summary?.audit_event_count ?? 0} />
          <SummaryTile label="source refs" value={summary?.source_trace_count ?? 0} />
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Run Detail</h2>
            <form onSubmit={openRunDetail} className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">
              <label className="text-sm">
                <span className="text-muted">workspace_run_id</span>
                <input value={workspaceRunId} onChange={(event) => setWorkspaceRunId(event.target.value)} className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-ink" />
              </label>
              <div className="flex items-end">
                <Button type="submit">Load Run Detail</Button>
              </div>
            </form>
            {latestWorkspaceRunId ? (
              <Link href={`/personal-alpha-dashboard/runs/${encodeURIComponent(latestWorkspaceRunId)}`} className="mt-4 inline-flex rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
                View Run Detail
              </Link>
            ) : null}
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {stageHealth.map((stage) => (
            <Card key={stage.stage_id}>
              <CardBody>
                <div className="text-xs uppercase tracking-wide text-muted">{stage.stage_id}</div>
                <div className="mt-2 text-base font-semibold text-ink">{stage.label}</div>
                <div className="mt-3 grid gap-2 text-sm text-muted">
                  <span>{stage.status}</span>
                  <span>{stage.mock_only ? "mock-only" : "not mock-only"}</span>
                </div>
              </CardBody>
            </Card>
          ))}
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Audit Timeline</h2>
            <JsonPanel title="audit_timeline" value={auditTimeline ?? { timeline: [] }} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Source Trace Summary</h2>
            <JsonPanel title="source_trace_summary" value={sourceTraceSummary ?? { source_refs: [] }} />
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

function findWorkspaceRunId(timeline: Record<string, unknown>[]) {
  for (const event of timeline) {
    const value = event.workspace_run_id;
    if (typeof value === "string" && value.trim()) {
      return value;
    }
  }
  return "";
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
