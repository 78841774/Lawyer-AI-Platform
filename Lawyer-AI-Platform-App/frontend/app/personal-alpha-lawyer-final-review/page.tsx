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
  PersonalAlphaLawyerFinalReviewActionList,
  PersonalAlphaLawyerFinalReviewActionRequest,
  PersonalAlphaLawyerFinalReviewActionResult,
  PersonalAlphaLawyerFinalReviewPacketDetail,
  PersonalAlphaLawyerFinalReviewStatus,
  PersonalAlphaLawyerFinalReviewSummary,
  getPersonalAlphaLawyerFinalReviewAction,
  getPersonalAlphaLawyerFinalReviewActions,
  getPersonalAlphaLawyerFinalReviewPacketDetail,
  getPersonalAlphaLawyerFinalReviewStatus,
  getPersonalAlphaLawyerFinalReviewSummary,
  submitPersonalAlphaLawyerFinalReviewAction
} from "@/services/api";

type SummaryResponse = {
  packet_id: string;
  workspace_run_id: string;
  summary: PersonalAlphaLawyerFinalReviewSummary;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

const DEFAULT_ACTION_FORM: PersonalAlphaLawyerFinalReviewActionRequest = {
  action: "approve_packet",
  reviewer_id: "local_demo_lawyer",
  reason: "Packet metadata is sufficient for controlled final lock readiness.",
  manual_review_confirmed: true,
  lawyer_review_confirmed: true,
  metadata_only_confirmation: true,
  no_final_legal_opinion_confirmation: true,
  no_final_report_generation_confirmation: true
};

export default function PersonalAlphaLawyerFinalReviewPage() {
  const router = useRouter();
  const [status, setStatus] = useState<PersonalAlphaLawyerFinalReviewStatus | null>(null);
  const [packetDetail, setPacketDetail] = useState<PersonalAlphaLawyerFinalReviewPacketDetail | null>(null);
  const [summary, setSummary] = useState<SummaryResponse | null>(null);
  const [actions, setActions] = useState<PersonalAlphaLawyerFinalReviewActionList | null>(null);
  const [actionResult, setActionResult] = useState<PersonalAlphaLawyerFinalReviewActionResult | null>(null);
  const [actionDetail, setActionDetail] = useState<Record<string, unknown> | null>(null);
  const [packetId, setPacketId] = useState("");
  const [actionId, setActionId] = useState("");
  const [actionForm, setActionForm] = useState(DEFAULT_ACTION_FORM);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadInitial() {
      try {
        setStatus(await getPersonalAlphaLawyerFinalReviewStatus());
        const queryValue = new URLSearchParams(window.location.search).get("packet_id") ?? "";
        if (queryValue) {
          setPacketId(queryValue);
          await loadPacket(queryValue);
        }
      } catch {
        setError("Personal Alpha Lawyer Final Review API 暂不可用，请确认后端服务已启动。");
      }
    }

    void loadInitial();
  }, []);

  async function loadPacket(id: string) {
    const trimmed = id.trim();
    if (!trimmed) {
      return;
    }
    setLoading(true);
    setError("");
    try {
      const [nextDetail, nextSummary, nextActions] = await Promise.all([
        getPersonalAlphaLawyerFinalReviewPacketDetail(trimmed),
        getPersonalAlphaLawyerFinalReviewSummary(trimmed),
        getPersonalAlphaLawyerFinalReviewActions(trimmed)
      ]);
      setPacketDetail(nextDetail);
      setSummary(nextSummary);
      setActions(nextActions);
    } catch {
      setError("Lawyer final review 加载失败，请确认 packet_id 已创建。");
    } finally {
      setLoading(false);
    }
  }

  async function submitPacket(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const id = packetId.trim();
    if (!id) {
      return;
    }
    router.replace(`/personal-alpha-lawyer-final-review?packet_id=${encodeURIComponent(id)}`);
    await loadPacket(id);
  }

  async function submitAction(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const id = packetId.trim();
    if (!id) {
      return;
    }
    setLoading(true);
    setError("");
    try {
      const result = await submitPersonalAlphaLawyerFinalReviewAction(id, actionForm);
      const [nextDetail, nextSummary, nextActions] = await Promise.all([
        getPersonalAlphaLawyerFinalReviewPacketDetail(id),
        getPersonalAlphaLawyerFinalReviewSummary(id),
        getPersonalAlphaLawyerFinalReviewActions(id)
      ]);
      setActionResult(result);
      setPacketDetail(nextDetail);
      setSummary(nextSummary);
      setActions(nextActions);
      if (result.action_id && result.status === "lawyer_final_review_action_recorded") {
        setActionId(result.action_id);
        setActionDetail(await getPersonalAlphaLawyerFinalReviewAction(result.action_id));
      }
    } catch {
      setError("Review action 提交失败，请确认 packet 存在、action 合法且所有 confirmation 均已勾选。");
    } finally {
      setLoading(false);
    }
  }

  async function submitActionDetail(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const id = actionId.trim();
    if (!id) {
      return;
    }
    setLoading(true);
    setError("");
    try {
      setActionDetail(await getPersonalAlphaLawyerFinalReviewAction(id));
    } catch {
      setError("Action detail 加载失败。");
    } finally {
      setLoading(false);
    }
  }

  const currentSummary = summary?.summary;

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Personal Alpha"
          title="Personal Alpha Controlled Lawyer Final Review"
          description="个人 Alpha 律师终审复核：基于 metadata-only final review packet 进行人工复核动作。该页面不生成正式法律意见，不生成最终报告正文，不调用真实服务。"
        />
        {packetId.trim() && currentSummary?.ready_for_controlled_final_lock ? (
          <Link href={`/personal-alpha-final-lock?packet_id=${encodeURIComponent(packetId.trim())}`} className="inline-flex rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
            View Controlled Final Lock
          </Link>
        ) : packetId.trim() ? (
          <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
            Controlled Final Lock requires the latest lawyer final review action to be approve_packet.
          </div>
        ) : null}
        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_personal_alpha_lawyer_final_review"} />
              <InfoRow label="local-only" value="true" />
              <InfoRow label="mock_first_enabled" value={String(status?.mock_first_enabled ?? true)} />
              <InfoRow label="controlled_first_enabled" value={String(status?.controlled_first_enabled ?? true)} />
              <InfoRow label="metadata_only" value={String(status?.metadata_only ?? true)} />
              <InfoRow label="advisory_only" value={String(status?.advisory_only ?? true)} />
              <InfoRow label="requires_final_packet" value={String(status?.requires_final_packet ?? true)} />
              <InfoRow label="requires_lawyer_review" value={String(status?.requires_lawyer_review ?? true)} />
              <InfoRow label="final_report_generation_enabled" value={String(status?.final_report_generation_enabled ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="runtime_storage_path" value={status?.runtime_storage_path ?? "storage/runtime/personal_alpha_lawyer_final_review/actions"} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Packet Input</h2>
            <form onSubmit={submitPacket} className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">
              <TextField label="packet_id" value={packetId} onChange={setPacketId} />
              <div className="flex items-end">
                <Button type="submit" disabled={loading}>{loading ? "加载中..." : "Load Lawyer Final Review"}</Button>
              </div>
            </form>
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-6">
          <SummaryTile label="actions" value={currentSummary?.action_count ?? 0} />
          <SummaryTile label="approved" value={currentSummary?.approved_packet_count ?? 0} />
          <SummaryTile label="revision" value={currentSummary?.revision_requested_count ?? 0} />
          <SummaryTile label="rejected" value={currentSummary?.rejected_packet_count ?? 0} />
          <BooleanTile label="ready for lock" value={currentSummary?.ready_for_controlled_final_lock ?? false} />
          <BooleanTile label="requires review" value={currentSummary?.requires_additional_lawyer_review ?? true} />
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Packet Review Summary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="packet_id" value={(packetDetail?.packet_id ?? packetId) || "-"} />
              <InfoRow label="workspace_run_id" value={packetDetail?.workspace_run_id ?? summary?.workspace_run_id ?? "-"} />
              <InfoRow label="packet_status" value={packetDetail?.packet_status ?? "not_loaded"} />
              <InfoRow label="review_status" value={currentSummary?.review_status ?? packetDetail?.review_status ?? "pending_lawyer_review"} />
              <InfoRow label="latest_action" value={currentSummary?.latest_action ?? "-"} />
              <InfoRow label="ready_for_controlled_final_lock" value={String(currentSummary?.ready_for_controlled_final_lock ?? false)} />
              <InfoRow label="requires_packet_revision" value={String(currentSummary?.requires_packet_revision ?? false)} />
              <InfoRow label="raw_content_included" value={String(packetDetail?.raw_content_included ?? false)} />
              <InfoRow label="final_legal_opinion_generated" value={String(packetDetail?.final_legal_opinion_generated ?? false)} />
              <InfoRow label="final_report_generated" value={String(packetDetail?.final_report_generated ?? false)} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Packet Metadata</h2>
            <JsonPanel title="packet_summary" value={packetDetail?.packet_summary ?? {}} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Lawyer Final Review Action Form</h2>
            <form onSubmit={submitAction} className="mt-4 grid gap-4 md:grid-cols-2">
              <label className="text-sm">
                <span className="text-muted">action</span>
                <select
                  value={actionForm.action}
                  onChange={(event) => setActionForm((current) => ({ ...current, action: event.target.value }))}
                  className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-ink"
                >
                  <option value="approve_packet">approve_packet</option>
                  <option value="request_packet_revision">request_packet_revision</option>
                  <option value="reject_packet">reject_packet</option>
                </select>
              </label>
              <TextField label="reviewer_id" value={actionForm.reviewer_id} onChange={(value) => setActionForm((current) => ({ ...current, reviewer_id: value }))} />
              <label className="text-sm md:col-span-2">
                <span className="text-muted">reason</span>
                <textarea
                  value={actionForm.reason}
                  onChange={(event) => setActionForm((current) => ({ ...current, reason: event.target.value }))}
                  className="mt-2 min-h-24 w-full rounded-md border border-line bg-white px-3 py-2 text-ink"
                />
              </label>
              <CheckField label="manual_review_confirmed" checked={actionForm.manual_review_confirmed} onChange={(checked) => setActionForm((current) => ({ ...current, manual_review_confirmed: checked }))} />
              <CheckField label="lawyer_review_confirmed" checked={actionForm.lawyer_review_confirmed} onChange={(checked) => setActionForm((current) => ({ ...current, lawyer_review_confirmed: checked }))} />
              <CheckField label="metadata_only_confirmation" checked={actionForm.metadata_only_confirmation} onChange={(checked) => setActionForm((current) => ({ ...current, metadata_only_confirmation: checked }))} />
              <CheckField label="no_final_legal_opinion_confirmation" checked={actionForm.no_final_legal_opinion_confirmation} onChange={(checked) => setActionForm((current) => ({ ...current, no_final_legal_opinion_confirmation: checked }))} />
              <CheckField label="no_final_report_generation_confirmation" checked={actionForm.no_final_report_generation_confirmation} onChange={(checked) => setActionForm((current) => ({ ...current, no_final_report_generation_confirmation: checked }))} />
              <div className="flex items-end">
                <Button type="submit" disabled={loading || !packetId.trim()}>{loading ? "提交中..." : "Submit Review Action"}</Button>
              </div>
            </form>
            {actionResult ? <JsonPanel title="latest_action_result" value={actionResult} /> : null}
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Review Action History</h2>
            <div className="mt-4 grid gap-3">
              {(actions?.actions ?? []).length ? actions?.actions.map((item) => (
                <div key={item.action_id} className="rounded-md border border-line bg-paper p-3">
                  <div className="grid gap-3 md:grid-cols-3">
                    <InfoRow label="action_id" value={item.action_id} />
                    <InfoRow label="action" value={item.action} />
                    <InfoRow label="ready_for_controlled_final_lock" value={String(item.ready_for_controlled_final_lock)} />
                    <InfoRow label="reviewer_id" value={item.reviewer_id} />
                    <InfoRow label="created_at" value={item.created_at} />
                    <InfoRow label="status" value={item.status} />
                  </div>
                  <JsonPanel title="warnings" value={item.warnings} />
                </div>
              )) : (
                <StatusMessage message="暂无 review actions。所有 action 都会写入 ignored runtime storage，且仅包含 metadata。" />
              )}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Action Detail</h2>
            <form onSubmit={submitActionDetail} className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">
              <TextField label="action_id" value={actionId} onChange={setActionId} />
              <div className="flex items-end">
                <Button type="submit" disabled={loading || !actionId.trim()}>{loading ? "加载中..." : "Load Action Detail"}</Button>
              </div>
            </form>
            <JsonPanel title="action_detail" value={actionDetail ?? {}} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">JSON Panels</h2>
            <JsonPanel title="packet_review_detail" value={packetDetail ?? {}} />
            <JsonPanel title="summary" value={summary ?? {}} />
            <JsonPanel title="actions" value={actions ?? {}} />
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

function BooleanTile({ label, value }: { label: string; value: boolean }) {
  return (
    <Card>
      <CardBody>
        <div className="text-xs uppercase tracking-wide text-muted">{label}</div>
        <div className="mt-2 text-xl font-semibold text-ink">{String(value)}</div>
      </CardBody>
    </Card>
  );
}

function TextField({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return (
    <label className="text-sm">
      <span className="text-muted">{label}</span>
      <input value={value} onChange={(event) => onChange(event.target.value)} className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-ink" />
    </label>
  );
}

function CheckField({ label, checked, onChange }: { label: string; checked: boolean; onChange: (checked: boolean) => void }) {
  return (
    <label className="flex items-center gap-2 rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
      <input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
      <span>{label}</span>
    </label>
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
