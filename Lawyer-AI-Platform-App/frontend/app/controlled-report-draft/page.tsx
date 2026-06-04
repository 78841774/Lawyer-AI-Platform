"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  assembleControlledReportDraft,
  ControlledReportDraftAssembleResult,
  ControlledReportDraftAuditLog,
  ControlledReportDraftRecord,
  ControlledReportDraftStatus,
  getControlledReportDraft,
  getControlledReportDraftAuditLogs,
  getControlledReportDraftStatus
} from "@/services/api";

export default function ControlledReportDraftPage() {
  const [status, setStatus] = useState<ControlledReportDraftStatus | null>(null);
  const [assembleResult, setAssembleResult] = useState<ControlledReportDraftAssembleResult | null>(null);
  const [draftRecord, setDraftRecord] = useState<ControlledReportDraftRecord | null>(null);
  const [auditLogs, setAuditLogs] = useState<ControlledReportDraftAuditLog[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState("");
  const [draftId, setDraftId] = useState("");
  const [form, setForm] = useState({
    case_id: "case_v46_demo_001",
    workspace_id: "workspace_demo_001",
    material_preview_ids: "controlled_preview_demo_001",
    ocr_preview_ids: "ocr_preview_demo_001",
    legal_search_preview_ids: "legal_search_preview_demo_001",
    citation_ids: "mock_citation_001",
    explicit_assembly_confirmation: true,
    manual_review_confirmed: true,
    report_mode: "mock_draft",
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
        getControlledReportDraftStatus(),
        getControlledReportDraftAuditLogs()
      ]);
      setStatus(nextStatus);
      setAuditLogs(nextAuditLogs);
    } catch {
      setError("Controlled Report Draft API 暂不可用，请确认后端服务已启动。");
    }
  }

  async function submitAssemble(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("assemble");
    setError("");
    try {
      const nextResult = await assembleControlledReportDraft({
        case_id: form.case_id,
        workspace_id: form.workspace_id,
        material_preview_ids: splitIds(form.material_preview_ids),
        ocr_preview_ids: splitIds(form.ocr_preview_ids),
        legal_search_preview_ids: splitIds(form.legal_search_preview_ids),
        citation_ids: splitIds(form.citation_ids),
        explicit_assembly_confirmation: form.explicit_assembly_confirmation,
        manual_review_confirmed: form.manual_review_confirmed,
        report_mode: form.report_mode,
        llm_mode: form.llm_mode,
        provider_mode: form.provider_mode,
        preview_only: form.preview_only
      });
      setAssembleResult(nextResult);
      setDraftId(nextResult.draft_id);
      setAuditLogs(await getControlledReportDraftAuditLogs());
    } catch {
      setError("Controlled report draft assemble 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  async function submitLoadDraft(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("load");
    setError("");
    try {
      setDraftRecord(await getControlledReportDraft(draftId));
      setAuditLogs(await getControlledReportDraftAuditLogs());
    } catch {
      setError("Load draft 失败，请确认 draft_id 存在且后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="Controlled Report Draft"
          description="受控报告草稿装配；默认 mock，只合并预览 ID、source refs 与 citation placeholders，不生成正式法律意见。"
        />
        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_controlled_report_draft"} />
              <InfoRow label="local-only" value="true" />
              <InfoRow label="mock_report_assembly_enabled" value={String(status?.mock_report_assembly_enabled ?? true)} />
              <InfoRow label="requires_explicit_assembly_confirmation" value={String(status?.requires_explicit_assembly_confirmation ?? true)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
              <InfoRow label="runtime_storage_path" value={status?.runtime_storage_path ?? "storage/runtime/controlled_report_drafts"} />
              <InfoRow label="source_trace_enabled" value={String(status?.source_trace_enabled ?? true)} />
            </div>
            <JsonPanel title="warnings" value={status?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Assemble Report Draft</h2>
            <form onSubmit={submitAssemble} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="case_id" value={form.case_id} onChange={(value) => setForm({ ...form, case_id: value })} />
              <Field label="workspace_id" value={form.workspace_id} onChange={(value) => setForm({ ...form, workspace_id: value })} />
              <Field label="material_preview_ids" value={form.material_preview_ids} onChange={(value) => setForm({ ...form, material_preview_ids: value })} />
              <Field label="ocr_preview_ids" value={form.ocr_preview_ids} onChange={(value) => setForm({ ...form, ocr_preview_ids: value })} />
              <Field label="legal_search_preview_ids" value={form.legal_search_preview_ids} onChange={(value) => setForm({ ...form, legal_search_preview_ids: value })} />
              <Field label="citation_ids" value={form.citation_ids} onChange={(value) => setForm({ ...form, citation_ids: value })} />
              <Field label="report_mode" value={form.report_mode} onChange={(value) => setForm({ ...form, report_mode: value })} />
              <Field label="llm_mode" value={form.llm_mode} onChange={(value) => setForm({ ...form, llm_mode: value })} />
              <Field label="provider_mode" value={form.provider_mode} onChange={(value) => setForm({ ...form, provider_mode: value })} />
              <CheckField label="explicit_assembly_confirmation" checked={form.explicit_assembly_confirmation} onChange={(checked) => setForm({ ...form, explicit_assembly_confirmation: checked })} />
              <CheckField label="manual_review_confirmed" checked={form.manual_review_confirmed} onChange={(checked) => setForm({ ...form, manual_review_confirmed: checked })} />
              <CheckField label="preview_only" checked={form.preview_only} onChange={(checked) => setForm({ ...form, preview_only: checked })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "assemble"}>{loading === "assemble" ? "装配中..." : "Assemble Mock Report Draft"}</Button>
              </div>
            </form>
            {assembleResult ? <JsonPanel title="assemble_result" value={assembleResult} /> : null}
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Load Draft</h2>
            <form onSubmit={submitLoadDraft} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="draft_id" value={draftId} onChange={setDraftId} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "load"}>{loading === "load" ? "读取中..." : "Load Draft"}</Button>
              </div>
            </form>
            {draftRecord ? <JsonPanel title="draft_record" value={draftRecord} /> : null}
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

function splitIds(value: string) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
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

