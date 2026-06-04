"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  ControlledRevisionAuditLog,
  ControlledRevisionRecord,
  ControlledRevisionResult,
  ControlledRevisionStatus,
  getControlledRevision,
  getControlledRevisionAuditLogs,
  getControlledRevisionStatus,
  requestControlledRevision
} from "@/services/api";

export default function ControlledRevisionPage() {
  const [status, setStatus] = useState<ControlledRevisionStatus | null>(null);
  const [result, setResult] = useState<ControlledRevisionResult | null>(null);
  const [record, setRecord] = useState<ControlledRevisionRecord | null>(null);
  const [auditLogs, setAuditLogs] = useState<ControlledRevisionAuditLog[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState("");
  const [revisionId, setRevisionId] = useState("");
  const [form, setForm] = useState({
    case_id: "case_v48_demo_001",
    workspace_id: "workspace_demo_001",
    review_id: "review_demo_001",
    draft_id: "draft_demo_001",
    revision_reason: "需要补充争议焦点处的风险提示",
    revision_instructions: "请在 mock draft 的风险提示部分增加人工复核清单，不要生成正式法律意见。",
    requested_action: "revise_risk_warnings",
    explicit_revision_confirmation: true,
    manual_review_confirmed: true,
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
        getControlledRevisionStatus(),
        getControlledRevisionAuditLogs()
      ]);
      setStatus(nextStatus);
      setAuditLogs(nextAuditLogs);
    } catch {
      setError("Controlled Revision API 暂不可用，请确认后端服务已启动。");
    }
  }

  async function submitRevision(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("request");
    setError("");
    try {
      const nextResult = await requestControlledRevision(form);
      setResult(nextResult);
      setRevisionId(nextResult.revision_id);
      setAuditLogs(await getControlledRevisionAuditLogs());
    } catch {
      setError("Controlled revision request 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  async function loadRevision(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("load");
    setError("");
    try {
      setRecord(await getControlledRevision(revisionId));
      setAuditLogs(await getControlledRevisionAuditLogs());
    } catch {
      setError("Load revision 失败，请确认 revision_id 存在且后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="Controlled Revision"
          description="受控修改请求 workflow；仅生成 mock revision plan，不调用真实服务，不生成正式法律意见。"
        />
        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_controlled_revision"} />
              <InfoRow label="local-only" value="true" />
              <InfoRow label="mock_revision_enabled" value={String(status?.mock_revision_enabled ?? true)} />
              <InfoRow label="requires_review_id" value={String(status?.requires_review_id ?? true)} />
              <InfoRow label="requires_explicit_revision_confirmation" value={String(status?.requires_explicit_revision_confirmation ?? true)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
              <InfoRow label="runtime_storage_path" value={status?.runtime_storage_path ?? "storage/runtime/controlled_revisions"} />
            </div>
            <JsonPanel title="warnings" value={status?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Revision Request</h2>
            <form onSubmit={submitRevision} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="case_id" value={form.case_id} onChange={(value) => setForm({ ...form, case_id: value })} />
              <Field label="workspace_id" value={form.workspace_id} onChange={(value) => setForm({ ...form, workspace_id: value })} />
              <Field label="review_id" value={form.review_id} onChange={(value) => setForm({ ...form, review_id: value })} />
              <Field label="draft_id" value={form.draft_id} onChange={(value) => setForm({ ...form, draft_id: value })} />
              <Field label="revision_reason" value={form.revision_reason} onChange={(value) => setForm({ ...form, revision_reason: value })} />
              <Field label="revision_instructions" value={form.revision_instructions} onChange={(value) => setForm({ ...form, revision_instructions: value })} />
              <Field label="requested_action" value={form.requested_action} onChange={(value) => setForm({ ...form, requested_action: value })} />
              <Field label="llm_mode" value={form.llm_mode} onChange={(value) => setForm({ ...form, llm_mode: value })} />
              <Field label="provider_mode" value={form.provider_mode} onChange={(value) => setForm({ ...form, provider_mode: value })} />
              <CheckField label="explicit_revision_confirmation" checked={form.explicit_revision_confirmation} onChange={(checked) => setForm({ ...form, explicit_revision_confirmation: checked })} />
              <CheckField label="manual_review_confirmed" checked={form.manual_review_confirmed} onChange={(checked) => setForm({ ...form, manual_review_confirmed: checked })} />
              <CheckField label="preview_only" checked={form.preview_only} onChange={(checked) => setForm({ ...form, preview_only: checked })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "request"}>{loading === "request" ? "生成中..." : "Request Mock Revision"}</Button>
              </div>
            </form>
            {result ? <JsonPanel title="revision_result" value={result} /> : null}
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Load Revision</h2>
            <form onSubmit={loadRevision} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="revision_id" value={revisionId} onChange={setRevisionId} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "load"}>{loading === "load" ? "读取中..." : "Load Revision"}</Button>
              </div>
            </form>
            {record ? <JsonPanel title="revision_record" value={record} /> : null}
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

