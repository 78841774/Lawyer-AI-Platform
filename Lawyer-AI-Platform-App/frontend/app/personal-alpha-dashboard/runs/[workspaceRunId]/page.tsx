"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  PersonalAlphaRunDetail,
  getPersonalAlphaDashboardRunDetail
} from "@/services/api";

export default function PersonalAlphaRunDetailPage({ params }: { params: { workspaceRunId: string } }) {
  const workspaceRunId = decodeURIComponent(params.workspaceRunId);
  const [detail, setDetail] = useState<PersonalAlphaRunDetail | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDetail() {
      try {
        setDetail(await getPersonalAlphaDashboardRunDetail(workspaceRunId));
      } catch {
        setError("Personal Alpha Run Detail API 暂不可用，请确认后端服务已启动。");
      }
    }

    void loadDetail();
  }, [workspaceRunId]);

  const safetyChecklist = detail?.safety_checklist ?? null;

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Personal Alpha"
          title="Personal Alpha Run Detail"
          description="个人 Alpha 单次运行详情：查看某次本地 controlled mock workspace run 的阶段详情、审计时间线、source trace 和安全检查。"
        />
        <Link href="/personal-alpha-dashboard" className="inline-flex rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
          Back to Dashboard
        </Link>
        <Link href={`/personal-alpha-source-review?workspace_run_id=${encodeURIComponent(workspaceRunId)}`} className="ml-3 inline-flex rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
          View Source Trace Review
        </Link>
        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Run Summary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="workspace_run_id" value={detail?.workspace_run_id ?? workspaceRunId} />
              <InfoRow label="case_id" value={detail?.case_id ?? "-"} />
              <InfoRow label="workspace_id" value={detail?.workspace_id ?? "-"} />
              <InfoRow label="workflow_mode" value={detail?.workflow_mode ?? "-"} />
              <InfoRow label="status" value={detail?.status ?? "loading"} />
              <InfoRow label="created_at" value={detail?.created_at ?? "-"} />
              <InfoRow label="mock_or_redacted_only" value={String(detail?.mock_or_redacted_only ?? true)} />
              <InfoRow label="raw_content_included" value={String(detail?.raw_content_included ?? false)} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Checklist</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              {safetyChecklist ? (
                Object.entries(safetyChecklist).map(([key, value]) => <InfoRow key={key} label={key} value={String(value)} />)
              ) : (
                <InfoRow label="metadata_only" value="true" />
              )}
            </div>
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {(detail?.stage_details ?? []).map((stage) => (
            <Card key={stage.stage_id}>
              <CardBody>
                <div className="text-xs uppercase tracking-wide text-muted">{stage.stage_id}</div>
                <div className="mt-2 text-base font-semibold text-ink">{stage.label}</div>
                <div className="mt-3 space-y-2 text-sm text-muted">
                  <div>{stage.status}</div>
                  <div>{stage.mock_only ? "mock-only" : "not mock-only"}</div>
                  <div>{stage.notes}</div>
                </div>
              </CardBody>
            </Card>
          ))}
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Guard Summary / Warnings</h2>
            <JsonPanel title="guard_summary" value={detail?.guard_summary ?? { guard_count: 0, warnings: [] }} />
            <JsonPanel title="warnings" value={detail?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Audit Timeline</h2>
            <JsonPanel title="audit_timeline" value={detail?.audit_timeline ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Source Refs</h2>
            <JsonPanel title="source_refs" value={detail?.source_refs ?? []} />
          </CardBody>
        </Card>
      </div>
    </AppShell>
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
