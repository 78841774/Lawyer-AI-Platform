"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  PersonalAlphaFinalGateDecisionList,
  PersonalAlphaFinalGateDecisionResult,
  PersonalAlphaFinalGateRunDetail,
  PersonalAlphaFinalGateStatus,
  PersonalAlphaFinalGateSummaryResponse,
  getPersonalAlphaFinalGateDecisions,
  getPersonalAlphaFinalGateRunDetail,
  getPersonalAlphaFinalGateStatus,
  getPersonalAlphaFinalGateSummary,
  submitPersonalAlphaFinalGateDecision
} from "@/services/api";

const DEFAULT_GATE_FORM = {
  decision: "approve_gate",
  reviewer_id: "local_demo_reviewer",
  reason: "Final readiness metadata is sufficient for controlled final review gate.",
  manual_review_confirmed: true,
  metadata_only_confirmation: true,
  no_final_legal_opinion_confirmation: true
};

export default function PersonalAlphaFinalGatePage() {
  const router = useRouter();
  const [status, setStatus] = useState<PersonalAlphaFinalGateStatus | null>(null);
  const [runDetail, setRunDetail] = useState<PersonalAlphaFinalGateRunDetail | null>(null);
  const [summary, setSummary] = useState<PersonalAlphaFinalGateSummaryResponse | null>(null);
  const [decisionList, setDecisionList] = useState<PersonalAlphaFinalGateDecisionList | null>(null);
  const [decisionResult, setDecisionResult] = useState<PersonalAlphaFinalGateDecisionResult | null>(null);
  const [gateForm, setGateForm] = useState(DEFAULT_GATE_FORM);
  const [workspaceRunId, setWorkspaceRunId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadStatus() {
      try {
        setStatus(await getPersonalAlphaFinalGateStatus());
        const queryValue = new URLSearchParams(window.location.search).get("workspace_run_id") ?? "";
        if (queryValue) {
          setWorkspaceRunId(queryValue);
          await loadRun(queryValue);
        }
      } catch {
        setError("Personal Alpha Final Gate API 暂不可用，请确认后端服务已启动。");
      }
    }

    void loadStatus();
  }, []);

  async function loadRun(id: string) {
    setLoading(true);
    setError("");
    try {
      const [nextRunDetail, nextSummary, nextDecisionList] = await Promise.all([
        getPersonalAlphaFinalGateRunDetail(id),
        getPersonalAlphaFinalGateSummary(id),
        getPersonalAlphaFinalGateDecisions(id)
      ]);
      setRunDetail(nextRunDetail);
      setSummary(nextSummary);
      setDecisionList(nextDecisionList);
    } catch {
      setError("Final gate 加载失败，请确认 workspace_run_id 存在且后端服务已启动。");
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
    router.replace(`/personal-alpha-final-gate?workspace_run_id=${encodeURIComponent(id)}`);
    await loadRun(id);
  }

  async function submitDecision(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const id = workspaceRunId.trim();
    if (!id) {
      return;
    }
    setLoading(true);
    setError("");
    try {
      const result = await submitPersonalAlphaFinalGateDecision(id, gateForm);
      const [nextRunDetail, nextSummary, nextDecisionList] = await Promise.all([
        getPersonalAlphaFinalGateRunDetail(id),
        getPersonalAlphaFinalGateSummary(id),
        getPersonalAlphaFinalGateDecisions(id)
      ]);
      setDecisionResult(result);
      setRunDetail(nextRunDetail);
      setSummary(nextSummary);
      setDecisionList(nextDecisionList);
    } catch {
      setError("Gate decision 提交失败，请确认 readiness、manual review 和 metadata-only gate 均已通过。");
    } finally {
      setLoading(false);
    }
  }

  const gateSummary = runDetail?.gate_summary ?? summary?.summary;
  const gateRequirements = runDetail?.gate_requirements;

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Personal Alpha"
          title="Personal Alpha Controlled Final Review Gate"
          description="个人 Alpha 终审门禁：根据 Final Readiness metadata 和人工 gate decision，判断是否可进入 controlled final review step。该页面不生成正式法律意见，不调用真实服务。"
        />
        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_personal_alpha_final_gate"} />
              <InfoRow label="local-only" value="true" />
              <InfoRow label="mock_first_enabled" value={String(status?.mock_first_enabled ?? true)} />
              <InfoRow label="controlled_first_enabled" value={String(status?.controlled_first_enabled ?? true)} />
              <InfoRow label="metadata_only" value={String(status?.metadata_only ?? true)} />
              <InfoRow label="advisory_only" value={String(status?.advisory_only ?? true)} />
              <InfoRow label="requires_final_readiness" value={String(status?.requires_final_readiness ?? true)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="final_report_generation_enabled" value={String(status?.final_report_generation_enabled ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="auto_skill_publish_enabled" value={String(status?.auto_skill_publish_enabled ?? false)} />
              <InfoRow label="auto_workspace_runtime_enabled" value={String(status?.auto_workspace_runtime_enabled ?? false)} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Workspace Run Input</h2>
            <form onSubmit={submitRun} className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">
              <label className="text-sm">
                <span className="text-muted">workspace_run_id</span>
                <input value={workspaceRunId} onChange={(event) => setWorkspaceRunId(event.target.value)} className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-ink" />
              </label>
              <div className="flex items-end">
                <Button type="submit" disabled={loading}>{loading ? "加载中..." : "Load Final Gate"}</Button>
              </div>
            </form>
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-6">
          <BooleanTile label="gate open" value={gateSummary?.gate_open ?? false} />
          <BooleanTile label="final ready" value={gateSummary?.final_review_ready ?? false} />
          <BooleanTile label="requires review" value={gateSummary?.requires_additional_review ?? true} />
          <BooleanTile label="can proceed" value={gateSummary?.can_proceed_to_controlled_final_review ?? false} />
          <SummaryTile label="decisions" value={gateSummary?.gate_decision_count ?? 0} />
          <SummaryTile label="approved" value={gateSummary?.approved_gate_count ?? 0} />
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Gate Summary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="workspace_run_id" value={(runDetail?.workspace_run_id ?? workspaceRunId) || "-"} />
              <InfoRow label="status" value={runDetail?.status ?? "not_loaded"} />
              <InfoRow label="gate_open" value={String(gateSummary?.gate_open ?? false)} />
              <InfoRow label="final_review_ready" value={String(gateSummary?.final_review_ready ?? false)} />
              <InfoRow label="requires_additional_review" value={String(gateSummary?.requires_additional_review ?? true)} />
              <InfoRow label="latest_gate_decision" value={gateSummary?.latest_gate_decision ?? "-"} />
              <InfoRow label="gate_decision_count" value={String(gateSummary?.gate_decision_count ?? 0)} />
              <InfoRow label="can_proceed_to_controlled_final_review" value={String(gateSummary?.can_proceed_to_controlled_final_review ?? false)} />
              <InfoRow label="final_legal_opinion_generated" value={String(runDetail?.final_legal_opinion_generated ?? false)} />
              <InfoRow label="final_report_generated" value={String(runDetail?.final_report_generated ?? false)} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Gate Requirements</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              {gateRequirements ? (
                Object.entries(gateRequirements).map(([key, value]) => <InfoRow key={key} label={key} value={String(value)} />)
              ) : (
                <InfoRow label="requires_final_review_ready" value="true" />
              )}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Gate Decision Form</h2>
            <form onSubmit={submitDecision} className="mt-4 grid gap-4 md:grid-cols-2">
              <label className="text-sm">
                <span className="text-muted">decision</span>
                <select
                  value={gateForm.decision}
                  onChange={(event) => setGateForm((current) => ({ ...current, decision: event.target.value }))}
                  className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-ink"
                >
                  <option value="approve_gate">approve_gate</option>
                  <option value="block_gate">block_gate</option>
                  <option value="request_more_review">request_more_review</option>
                </select>
              </label>
              <TextField label="reviewer_id" value={gateForm.reviewer_id} onChange={(value) => setGateForm((current) => ({ ...current, reviewer_id: value }))} />
              <label className="text-sm md:col-span-2">
                <span className="text-muted">reason</span>
                <textarea
                  value={gateForm.reason}
                  onChange={(event) => setGateForm((current) => ({ ...current, reason: event.target.value }))}
                  className="mt-2 min-h-24 w-full rounded-md border border-line bg-white px-3 py-2 text-ink"
                />
              </label>
              <CheckField label="manual_review_confirmed" checked={gateForm.manual_review_confirmed} onChange={(checked) => setGateForm((current) => ({ ...current, manual_review_confirmed: checked }))} />
              <CheckField label="metadata_only_confirmation" checked={gateForm.metadata_only_confirmation} onChange={(checked) => setGateForm((current) => ({ ...current, metadata_only_confirmation: checked }))} />
              <CheckField label="no_final_legal_opinion_confirmation" checked={gateForm.no_final_legal_opinion_confirmation} onChange={(checked) => setGateForm((current) => ({ ...current, no_final_legal_opinion_confirmation: checked }))} />
              <div className="flex items-end">
                <Button type="submit" disabled={loading || !workspaceRunId.trim()}>{loading ? "提交中..." : "Submit Gate Decision"}</Button>
              </div>
            </form>
            {decisionResult ? <JsonPanel title="latest_gate_decision_result" value={decisionResult} /> : null}
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Gate Decision History</h2>
            <JsonPanel title="gate_decisions" value={decisionList?.decisions ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">JSON Panels</h2>
            <JsonPanel title="run_detail" value={runDetail ?? {}} />
            <JsonPanel title="summary" value={summary ?? {}} />
            <JsonPanel title="decisions" value={decisionList ?? { decisions: [] }} />
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
    <label className="flex items-center gap-3 rounded-md border border-line bg-paper px-3 py-2 text-sm text-ink">
      <input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
      <span>{label}</span>
    </label>
  );
}
