"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  ControlledFinalReviewLockAuditLog,
  ControlledFinalReviewLockRecord,
  ControlledFinalReviewLockResult,
  ControlledFinalReviewLockStatus,
  getControlledFinalReviewAuditLogs,
  getControlledFinalReviewLock,
  getControlledFinalReviewStatus,
  lockControlledFinalReview
} from "@/services/api";

export default function ControlledFinalReviewPage() {
  const [status, setStatus] = useState<ControlledFinalReviewLockStatus | null>(null);
  const [result, setResult] = useState<ControlledFinalReviewLockResult | null>(null);
  const [record, setRecord] = useState<ControlledFinalReviewLockRecord | null>(null);
  const [auditLogs, setAuditLogs] = useState<ControlledFinalReviewLockAuditLog[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState("");
  const [finalLockId, setFinalLockId] = useState("");
  const [form, setForm] = useState({
    case_id: "case_v49_demo_001",
    workspace_id: "workspace_demo_001",
    draft_id: "draft_demo_001",
    review_id: "review_demo_001",
    revision_id: "revision_demo_001",
    final_review_notes: "律师已完成最终人工复核，本次仅锁定 mock final review candidate，不生成正式法律意见。",
    final_checklist_confirmed: true,
    explicit_final_lock_confirmation: true,
    manual_final_review_confirmed: true,
    lock_mode: "mock_final_review_candidate",
    llm_mode: "mock",
    provider_mode: "controlled_local",
    preview_only: true
  });

  useEffect(() => {
    void refresh();
  }, []);

  async function refresh() {
    try {
      const [nextStatus, nextAuditLogs] = await Promise.all([
        getControlledFinalReviewStatus(),
        getControlledFinalReviewAuditLogs()
      ]);
      setStatus(nextStatus);
      setAuditLogs(nextAuditLogs);
    } catch {
      setError("Controlled Final Review API 暂不可用，请确认后端服务已启动。");
    }
  }

  async function submitLock(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("lock");
    setError("");
    try {
      const nextResult = await lockControlledFinalReview(form);
      setResult(nextResult);
      setFinalLockId(nextResult.final_lock_id);
      setAuditLogs(await getControlledFinalReviewAuditLogs());
    } catch {
      setError("Controlled final review lock 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  async function loadLock(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("load");
    setError("");
    try {
      setRecord(await getControlledFinalReviewLock(finalLockId));
      setAuditLogs(await getControlledFinalReviewAuditLogs());
    } catch {
      setError("Load final review lock 失败，请确认 final_lock_id 存在且后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="Controlled Final Review"
          description="受控最终复核锁定 workflow；仅锁定 mock final review candidate，不调用真实服务，不生成正式法律意见。"
        />
        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_controlled_final_review_lock"} />
              <InfoRow label="local-only" value="true" />
              <InfoRow label="mock_final_lock_enabled" value={String(status?.mock_final_lock_enabled ?? true)} />
              <InfoRow label="requires_draft_id" value={String(status?.requires_draft_id ?? true)} />
              <InfoRow label="requires_review_id" value={String(status?.requires_review_id ?? true)} />
              <InfoRow label="requires_revision_id" value={String(status?.requires_revision_id ?? true)} />
              <InfoRow label="requires_explicit_final_lock_confirmation" value={String(status?.requires_explicit_final_lock_confirmation ?? true)} />
              <InfoRow label="requires_manual_final_confirmation" value={String(status?.requires_manual_final_confirmation ?? true)} />
              <InfoRow label="immutable_snapshot_enabled" value={String(status?.immutable_snapshot_enabled ?? true)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
              <InfoRow label="runtime_storage_path" value={status?.runtime_storage_path ?? "storage/runtime/controlled_final_review_locks"} />
            </div>
            <JsonPanel title="warnings" value={status?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Final Review Lock</h2>
            <form onSubmit={submitLock} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="case_id" value={form.case_id} onChange={(value) => setForm({ ...form, case_id: value })} />
              <Field label="workspace_id" value={form.workspace_id} onChange={(value) => setForm({ ...form, workspace_id: value })} />
              <Field label="draft_id" value={form.draft_id} onChange={(value) => setForm({ ...form, draft_id: value })} />
              <Field label="review_id" value={form.review_id} onChange={(value) => setForm({ ...form, review_id: value })} />
              <Field label="revision_id" value={form.revision_id} onChange={(value) => setForm({ ...form, revision_id: value })} />
              <Field label="final_review_notes" value={form.final_review_notes} onChange={(value) => setForm({ ...form, final_review_notes: value })} />
              <Field label="lock_mode" value={form.lock_mode} onChange={(value) => setForm({ ...form, lock_mode: value })} />
              <Field label="llm_mode" value={form.llm_mode} onChange={(value) => setForm({ ...form, llm_mode: value })} />
              <Field label="provider_mode" value={form.provider_mode} onChange={(value) => setForm({ ...form, provider_mode: value })} />
              <CheckField label="final_checklist_confirmed" checked={form.final_checklist_confirmed} onChange={(checked) => setForm({ ...form, final_checklist_confirmed: checked })} />
              <CheckField label="explicit_final_lock_confirmation" checked={form.explicit_final_lock_confirmation} onChange={(checked) => setForm({ ...form, explicit_final_lock_confirmation: checked })} />
              <CheckField label="manual_final_review_confirmed" checked={form.manual_final_review_confirmed} onChange={(checked) => setForm({ ...form, manual_final_review_confirmed: checked })} />
              <CheckField label="preview_only" checked={form.preview_only} onChange={(checked) => setForm({ ...form, preview_only: checked })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "lock"}>{loading === "lock" ? "锁定中..." : "Lock Mock Final Review"}</Button>
              </div>
            </form>
            {result ? <JsonPanel title="final_lock_result" value={result} /> : null}
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Load Final Lock</h2>
            <form onSubmit={loadLock} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="final_lock_id" value={finalLockId} onChange={setFinalLockId} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "load"}>{loading === "load" ? "读取中..." : "Load Final Lock"}</Button>
              </div>
            </form>
            {record ? <JsonPanel title="final_lock_record" value={record} /> : null}
          </CardBody>
        </Card>

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
