"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  PersonalAlphaCaseOSAuditTimeline,
  PersonalAlphaCaseOSCaseDetail,
  PersonalAlphaCaseOSNextAction,
  PersonalAlphaCaseOSStageState,
  getPersonalAlphaCaseOSAuditTimeline,
  getPersonalAlphaCaseOSCaseDetail,
  getPersonalAlphaCaseOSNextAction,
  getPersonalAlphaCaseOSSafetyChecklist
} from "@/services/api";

const STAGE_ORDER = [
  "workspace",
  "source_review",
  "source_review_decision",
  "final_readiness",
  "final_gate",
  "final_packet",
  "lawyer_final_review",
  "final_lock"
];

export default function PersonalAlphaCaseOSDetailPage() {
  const params = useParams<{ caseId: string }>();
  const caseId = decodeURIComponent(params.caseId);
  const [detail, setDetail] = useState<PersonalAlphaCaseOSCaseDetail | null>(null);
  const [timeline, setTimeline] = useState<PersonalAlphaCaseOSAuditTimeline | null>(null);
  const [nextAction, setNextAction] = useState<PersonalAlphaCaseOSNextAction | null>(null);
  const [safetyResponse, setSafetyResponse] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadDetail() {
    setLoading(true);
    setError("");
    try {
      const [nextDetail, nextTimeline, nextActionValue, nextSafety] = await Promise.all([
        getPersonalAlphaCaseOSCaseDetail(caseId),
        getPersonalAlphaCaseOSAuditTimeline(caseId),
        getPersonalAlphaCaseOSNextAction(caseId),
        getPersonalAlphaCaseOSSafetyChecklist(caseId)
      ]);
      setDetail(nextDetail);
      setTimeline(nextTimeline);
      setNextAction(nextActionValue);
      setSafetyResponse(nextSafety);
    } catch {
      setError("Case OS detail 加载失败。若 case_id 不存在，后端会返回 safe not_found，不暴露本地路径或原文。");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadDetail();
  }, [caseId]);

  const stageCards = useMemo(() => {
    const summary = detail?.stage_summary ?? {};
    return STAGE_ORDER.map((stageId) => ({
      stageId,
      stage: summary[stageId as keyof typeof summary] as PersonalAlphaCaseOSStageState | undefined
    }));
  }, [detail]);

  const actionHref = buildActionHref(nextAction?.target_route, nextAction?.target_id);

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Personal Alpha Case OS"
          title={detail?.title ?? "Case OS Detail"}
          description="案件级 Personal Alpha workflow 总览：仅聚合 metadata、redacted 状态和审计事件，不显示原始材料、OCR 原文、法律检索原文或最终法律意见。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <div className="flex flex-wrap gap-3">
          <Link href="/case-os">
            <Button type="button">Back to Case OS</Button>
          </Link>
          <Button type="button" onClick={() => void loadDetail()} disabled={loading}>
            {loading ? "刷新中..." : "Refresh Detail"}
          </Button>
          {actionHref ? (
            <Link href={actionHref}>
              <Button type="button">Open Next Action</Button>
            </Link>
          ) : null}
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Run Summary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="case_id" value={detail?.case_id ?? caseId} />
              <InfoRow label="workspace_id" value={detail?.workspace_id ?? "-"} />
              <InfoRow label="current_stage" value={detail?.current_stage ?? "-"} />
              <InfoRow label="next_action" value={detail?.next_action ?? nextAction?.next_action ?? "-"} />
              <InfoRow label="blocked" value={String(detail?.blocked ?? nextAction?.blocked ?? false)} />
              <InfoRow label="workspace_runs" value={String(detail?.workspace_runs?.length ?? 0)} />
              <InfoRow label="raw_content_included" value={String(detail?.raw_content_included ?? false)} />
              <InfoRow label="mock_or_redacted_only" value={String(detail?.mock_or_redacted_only ?? true)} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Next Action</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="action" value={nextAction?.next_action ?? "-"} />
              <InfoRow label="label" value={nextAction?.next_action_label ?? "-"} />
              <InfoRow label="target_route" value={nextAction?.target_route ?? "-"} />
              <InfoRow label="target_id" value={nextAction?.target_id ?? "-"} />
              <InfoRow label="blocked" value={String(nextAction?.blocked ?? false)} />
              <InfoRow label="raw_content_included" value={String(nextAction?.raw_content_included ?? false)} />
            </div>
            {nextAction?.blocked_reasons?.length ? (
              <div className="mt-4 rounded-md border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800">
                {nextAction.blocked_reasons.join(" / ")}
              </div>
            ) : null}
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {stageCards.map(({ stageId, stage }) => (
            <Card key={stageId}>
              <CardBody>
                <div className="text-xs uppercase tracking-wide text-muted">{stage?.stage_id ?? stageId}</div>
                <div className="mt-2 text-base font-semibold text-ink">{stage?.label ?? stageId}</div>
                <div className="mt-3 rounded-md border border-line bg-paper px-3 py-2 text-sm text-muted">
                  {stage?.status ?? "pending"}
                </div>
                <div className="mt-3 space-y-2 text-xs text-muted">
                  <div>next: {stage?.next_action ?? "-"}</div>
                  <div>raw: {String(stage?.raw_content_included ?? false)}</div>
                  <div>metadata: {String(stage?.mock_or_redacted_only ?? true)}</div>
                </div>
              </CardBody>
            </Card>
          ))}
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Checklist</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              {Object.entries(detail?.safety_checklist ?? {}).map(([key, value]) => (
                <InfoRow key={key} label={key} value={String(value)} />
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Audit Timeline</h2>
            <div className="mt-4 space-y-3">
              {(timeline?.timeline ?? detail?.audit_timeline ?? []).map((event) => (
                <div key={event.timeline_event_id} className="rounded-md border border-line bg-white p-4">
                  <div className="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
                    <div>
                      <div className="text-sm font-semibold text-ink">{event.stage_id}</div>
                      <div className="mt-1 text-xs text-muted">{event.timeline_event_id}</div>
                    </div>
                    <div className="text-xs text-muted">{event.created_at || "-"}</div>
                  </div>
                  <div className="mt-3 grid gap-2 text-xs text-muted md:grid-cols-4">
                    <span>event: {event.event_type}</span>
                    <span>result: {event.result}</span>
                    <span>metadata: {String(event.mock_or_redacted_only)}</span>
                    <span>raw: {String(event.raw_content_included)}</span>
                  </div>
                </div>
              ))}
              {!(timeline?.timeline ?? detail?.audit_timeline ?? []).length ? (
                <div className="rounded-md border border-dashed border-line p-5 text-sm text-muted">
                  暂无审计事件。Case OS 不会读取真实材料来补齐时间线。
                </div>
              ) : null}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Metadata JSON</h2>
            <pre className="mt-4 max-h-96 overflow-auto rounded-md bg-slate-950 p-4 text-xs leading-5 text-slate-100">
              {JSON.stringify({ detail, timeline, nextAction, safetyResponse }, null, 2)}
            </pre>
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}

function buildActionHref(targetRoute?: string, targetId?: string | null) {
  if (!targetRoute) {
    return "";
  }
  if (!targetId) {
    return targetRoute;
  }
  const encoded = encodeURIComponent(targetId);
  if (targetRoute.includes("final-lock") || targetRoute.includes("lawyer-final-review")) {
    return `${targetRoute}?packet_id=${encoded}`;
  }
  if (targetRoute.includes("workspace")) {
    return targetRoute;
  }
  return `${targetRoute}?workspace_run_id=${encoded}`;
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800">{message}</div>;
}
