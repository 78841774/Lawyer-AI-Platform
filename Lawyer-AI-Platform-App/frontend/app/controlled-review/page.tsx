"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  approveControlledLawyerReview,
  ControlledLawyerReviewAuditLog,
  ControlledLawyerReviewRecord,
  ControlledLawyerReviewResult,
  ControlledLawyerReviewStatus,
  getControlledLawyerReview,
  getControlledLawyerReviewAuditLogs,
  getControlledLawyerReviewStatus,
  rejectControlledLawyerReview,
  requestRevisionControlledLawyerReview,
  submitControlledLawyerReview
} from "@/services/api";

export default function ControlledReviewPage() {
  const [status, setStatus] = useState<ControlledLawyerReviewStatus | null>(null);
  const [result, setResult] = useState<ControlledLawyerReviewResult | null>(null);
  const [record, setRecord] = useState<ControlledLawyerReviewRecord | null>(null);
  const [auditLogs, setAuditLogs] = useState<ControlledLawyerReviewAuditLog[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState("");
  const [reviewId, setReviewId] = useState("");
  const [submitForm, setSubmitForm] = useState({
    draft_id: "controlled_report_draft_demo_001",
    case_id: "case_v47_demo_001",
    workspace_id: "workspace_demo_001",
    submitted_by: "lawyer_demo",
    explicit_review_confirmation: true,
    explicit_assembly_confirmation: true,
    manual_review_confirmed: true,
    review_mode: "mock_review",
    draft_status: "mock_draft",
    llm_mode: "mock",
    provider_mode: "controlled_local",
    preview_only: true
  });
  const [actionForm, setActionForm] = useState({
    reviewer_id: "lawyer_reviewer_demo",
    review_notes: "mock review action; no final legal opinion",
    explicit_review_confirmation: true,
    manual_review_confirmed: true,
    llm_mode: "mock",
    provider_mode: "controlled_local"
  });

  useEffect(() => {
    void refresh();
  }, []);

  async function refresh() {
    try {
      const [nextStatus, nextAuditLogs] = await Promise.all([
        getControlledLawyerReviewStatus(),
        getControlledLawyerReviewAuditLogs()
      ]);
      setStatus(nextStatus);
      setAuditLogs(nextAuditLogs);
    } catch {
      setError("Controlled Review API 暂不可用，请确认后端服务已启动。");
    }
  }

  async function submitReview(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("submit");
    setError("");
    try {
      const nextResult = await submitControlledLawyerReview(submitForm);
      setResult(nextResult);
      setReviewId(nextResult.review_id);
      setAuditLogs(await getControlledLawyerReviewAuditLogs());
    } catch {
      setError("Submit controlled review 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  async function loadReview(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("load");
    setError("");
    try {
      setRecord(await getControlledLawyerReview(reviewId));
      setAuditLogs(await getControlledLawyerReviewAuditLogs());
    } catch {
      setError("Load review 失败，请确认 review_id 存在且后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  async function runAction(action: "approve" | "reject" | "request_revision") {
    setLoading(action);
    setError("");
    try {
      const nextResult =
        action === "approve"
          ? await approveControlledLawyerReview(reviewId, actionForm)
          : action === "reject"
            ? await rejectControlledLawyerReview(reviewId, actionForm)
            : await requestRevisionControlledLawyerReview(reviewId, actionForm);
      setResult(nextResult);
      setRecord(await getControlledLawyerReview(reviewId));
      setAuditLogs(await getControlledLawyerReviewAuditLogs());
    } catch {
      setError("Review action 失败，请确认 review_id 存在且后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="Controlled Review"
          description="受控律师人工复核 workflow；仅处理 v4.6 mock report draft，不生成正式法律意见。"
        />
        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_controlled_lawyer_review"} />
              <InfoRow label="local-only" value="true" />
              <InfoRow label="mock_review_enabled" value={String(status?.mock_review_enabled ?? true)} />
              <InfoRow label="requires_explicit_review_confirmation" value={String(status?.requires_explicit_review_confirmation ?? true)} />
              <InfoRow label="requires_explicit_assembly_confirmation" value={String(status?.requires_explicit_assembly_confirmation ?? true)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="skill_publish_enabled" value={String(status?.skill_publish_enabled ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
              <InfoRow label="runtime_storage_path" value={status?.runtime_storage_path ?? "storage/runtime/controlled_lawyer_reviews"} />
            </div>
            <JsonPanel title="warnings" value={status?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Submit Mock Draft For Review</h2>
            <form onSubmit={submitReview} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="draft_id" value={submitForm.draft_id} onChange={(value) => setSubmitForm({ ...submitForm, draft_id: value })} />
              <Field label="case_id" value={submitForm.case_id} onChange={(value) => setSubmitForm({ ...submitForm, case_id: value })} />
              <Field label="workspace_id" value={submitForm.workspace_id} onChange={(value) => setSubmitForm({ ...submitForm, workspace_id: value })} />
              <Field label="submitted_by" value={submitForm.submitted_by} onChange={(value) => setSubmitForm({ ...submitForm, submitted_by: value })} />
              <Field label="review_mode" value={submitForm.review_mode} onChange={(value) => setSubmitForm({ ...submitForm, review_mode: value })} />
              <Field label="draft_status" value={submitForm.draft_status} onChange={(value) => setSubmitForm({ ...submitForm, draft_status: value })} />
              <Field label="llm_mode" value={submitForm.llm_mode} onChange={(value) => setSubmitForm({ ...submitForm, llm_mode: value })} />
              <Field label="provider_mode" value={submitForm.provider_mode} onChange={(value) => setSubmitForm({ ...submitForm, provider_mode: value })} />
              <CheckField label="explicit_review_confirmation" checked={submitForm.explicit_review_confirmation} onChange={(checked) => setSubmitForm({ ...submitForm, explicit_review_confirmation: checked })} />
              <CheckField label="explicit_assembly_confirmation" checked={submitForm.explicit_assembly_confirmation} onChange={(checked) => setSubmitForm({ ...submitForm, explicit_assembly_confirmation: checked })} />
              <CheckField label="manual_review_confirmed" checked={submitForm.manual_review_confirmed} onChange={(checked) => setSubmitForm({ ...submitForm, manual_review_confirmed: checked })} />
              <CheckField label="preview_only" checked={submitForm.preview_only} onChange={(checked) => setSubmitForm({ ...submitForm, preview_only: checked })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "submit"}>{loading === "submit" ? "提交中..." : "Submit Controlled Review"}</Button>
              </div>
            </form>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Review Actions</h2>
            <form onSubmit={loadReview} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="review_id" value={reviewId} onChange={setReviewId} />
              <Field label="reviewer_id" value={actionForm.reviewer_id} onChange={(value) => setActionForm({ ...actionForm, reviewer_id: value })} />
              <Field label="review_notes" value={actionForm.review_notes} onChange={(value) => setActionForm({ ...actionForm, review_notes: value })} />
              <Field label="llm_mode" value={actionForm.llm_mode} onChange={(value) => setActionForm({ ...actionForm, llm_mode: value })} />
              <Field label="provider_mode" value={actionForm.provider_mode} onChange={(value) => setActionForm({ ...actionForm, provider_mode: value })} />
              <CheckField label="explicit_review_confirmation" checked={actionForm.explicit_review_confirmation} onChange={(checked) => setActionForm({ ...actionForm, explicit_review_confirmation: checked })} />
              <CheckField label="manual_review_confirmed" checked={actionForm.manual_review_confirmed} onChange={(checked) => setActionForm({ ...actionForm, manual_review_confirmed: checked })} />
              <div className="flex flex-wrap gap-3 md:col-span-3">
                <Button type="submit" disabled={loading === "load"}>{loading === "load" ? "读取中..." : "Load Review"}</Button>
                <Button type="button" disabled={loading === "approve"} onClick={() => void runAction("approve")}>Approve</Button>
                <Button type="button" disabled={loading === "reject"} onClick={() => void runAction("reject")}>Reject</Button>
                <Button type="button" disabled={loading === "request_revision"} onClick={() => void runAction("request_revision")}>Request Revision</Button>
              </div>
            </form>
            {record ? <JsonPanel title="review_record" value={record} /> : null}
          </CardBody>
        </Card>

        {result ? (
          <Card>
            <CardBody>
              <h2 className="text-base font-semibold text-ink">Result</h2>
              <JsonPanel title="review_result" value={result} />
            </CardBody>
          </Card>
        ) : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Audit Logs</h2>
            <JsonPanel title="audit_logs" value={auditLogs} />
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}

function Field({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return (
    <label className="text-sm">
      <span className="text-muted">{label}</span>
      <input value={value} onChange={(event) => onChange(event.target.value)} className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-ink" />
    </label>
  );
}

function CheckField({ label, checked, onChange }: { label: string; checked: boolean; onChange: (checked: boolean) => void }) {
  return (
    <label className="flex items-center gap-2 text-sm text-muted md:col-span-3">
      <input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
      {label}
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

