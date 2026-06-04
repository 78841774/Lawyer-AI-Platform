"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  ControlledLegalCitationResolutionResult,
  ControlledLegalSearchAuditLog,
  ControlledLegalSearchPreviewResult,
  ControlledLegalSearchStatus,
  getControlledLegalSearchAuditLogs,
  getControlledLegalSearchStatus,
  resolveControlledLegalCitation,
  runControlledLegalSearchPreview
} from "@/services/api";

export default function ControlledLegalSearchPage() {
  const [status, setStatus] = useState<ControlledLegalSearchStatus | null>(null);
  const [previewResult, setPreviewResult] = useState<ControlledLegalSearchPreviewResult | null>(null);
  const [resolutionResult, setResolutionResult] = useState<ControlledLegalCitationResolutionResult | null>(null);
  const [auditLogs, setAuditLogs] = useState<ControlledLegalSearchAuditLog[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState("");
  const [previewForm, setPreviewForm] = useState({
    case_id: "case_v45_demo_001",
    workspace_id: "workspace_demo_001",
    query_text: "买卖合同货款纠纷，手机号13812345678，案号（2024）沪0101民初12345号",
    query_text_redacted: "",
    case_cause_code: "payment_dispute",
    jurisdiction: "CN",
    explicit_legal_search_confirmation: true,
    manual_review_confirmed: true,
    legal_search_mode: "mock",
    provider_mode: "controlled_local",
    preview_only: true
  });
  const [resolveForm, setResolveForm] = useState({
    citation_id: "mock_citation_001",
    search_preview_id: "search_preview_demo_001",
    manual_review_confirmed: true,
    legal_search_mode: "mock",
    provider_mode: "controlled_local"
  });

  useEffect(() => {
    void refresh();
  }, []);

  async function refresh() {
    try {
      const [nextStatus, nextAuditLogs] = await Promise.all([
        getControlledLegalSearchStatus(),
        getControlledLegalSearchAuditLogs()
      ]);
      setStatus(nextStatus);
      setAuditLogs(nextAuditLogs);
    } catch {
      setError("Controlled Legal Search API 暂不可用，请确认后端服务已启动。");
    }
  }

  async function submitPreview(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("preview");
    setError("");
    try {
      const nextResult = await runControlledLegalSearchPreview(previewForm);
      setPreviewResult(nextResult);
      setResolveForm({ ...resolveForm, search_preview_id: nextResult.search_preview_id });
      setAuditLogs(await getControlledLegalSearchAuditLogs());
    } catch {
      setError("Controlled legal search preview 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  async function submitResolve(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("resolve");
    setError("");
    try {
      setResolutionResult(await resolveControlledLegalCitation(resolveForm));
      setAuditLogs(await getControlledLegalSearchAuditLogs());
    } catch {
      setError("Citation resolve 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader eyebrow="Runtime Tools" title="Controlled Legal Search" description="受控法律检索引用预览；默认 mock，不调用真实法律数据库或 LLM。" />
        {error ? <StatusMessage message={error} /> : null}
        <Card><CardBody>
          <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <InfoRow label="mode" value={status?.mode ?? "local_only_controlled_legal_search"} />
            <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
            <InfoRow label="mock_legal_search_enabled" value={String(status?.mock_legal_search_enabled ?? true)} />
            <InfoRow label="requires_explicit_legal_search_confirmation" value={String(status?.requires_explicit_legal_search_confirmation ?? true)} />
            <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
            <InfoRow label="query_redaction_enabled" value={String(status?.query_redaction_enabled ?? true)} />
            <InfoRow label="citation_resolver_enabled" value={String(status?.citation_resolver_enabled ?? true)} />
            <InfoRow label="runtime_storage_path" value={status?.runtime_storage_path ?? "storage/runtime/controlled_legal_search_previews"} />
            <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
          </div>
          <JsonPanel title="warnings" value={status?.warnings ?? []} />
        </CardBody></Card>
        <Card><CardBody>
          <h2 className="text-base font-semibold text-ink">Legal Search Preview</h2>
          <form onSubmit={submitPreview} className="mt-4 grid gap-4 md:grid-cols-3">
            <Field label="case_id" value={previewForm.case_id} onChange={(value) => setPreviewForm({ ...previewForm, case_id: value })} />
            <Field label="workspace_id" value={previewForm.workspace_id} onChange={(value) => setPreviewForm({ ...previewForm, workspace_id: value })} />
            <Field label="query_text" value={previewForm.query_text} onChange={(value) => setPreviewForm({ ...previewForm, query_text: value })} />
            <Field label="query_text_redacted" value={previewForm.query_text_redacted} onChange={(value) => setPreviewForm({ ...previewForm, query_text_redacted: value })} />
            <Field label="case_cause_code" value={previewForm.case_cause_code} onChange={(value) => setPreviewForm({ ...previewForm, case_cause_code: value })} />
            <Field label="jurisdiction" value={previewForm.jurisdiction} onChange={(value) => setPreviewForm({ ...previewForm, jurisdiction: value })} />
            <Field label="legal_search_mode" value={previewForm.legal_search_mode} onChange={(value) => setPreviewForm({ ...previewForm, legal_search_mode: value })} />
            <Field label="provider_mode" value={previewForm.provider_mode} onChange={(value) => setPreviewForm({ ...previewForm, provider_mode: value })} />
            <CheckField label="explicit_legal_search_confirmation" checked={previewForm.explicit_legal_search_confirmation} onChange={(checked) => setPreviewForm({ ...previewForm, explicit_legal_search_confirmation: checked })} />
            <CheckField label="manual_review_confirmed" checked={previewForm.manual_review_confirmed} onChange={(checked) => setPreviewForm({ ...previewForm, manual_review_confirmed: checked })} />
            <CheckField label="preview_only" checked={previewForm.preview_only} onChange={(checked) => setPreviewForm({ ...previewForm, preview_only: checked })} />
            <div className="md:col-span-3"><Button type="submit" disabled={loading === "preview"}>{loading === "preview" ? "预览中..." : "Run Legal Search Preview"}</Button></div>
          </form>
          {previewResult ? <JsonPanel title="preview_result" value={previewResult} /> : null}
        </CardBody></Card>
        <Card><CardBody>
          <h2 className="text-base font-semibold text-ink">Resolve Citation</h2>
          <form onSubmit={submitResolve} className="mt-4 grid gap-4 md:grid-cols-3">
            <Field label="citation_id" value={resolveForm.citation_id} onChange={(value) => setResolveForm({ ...resolveForm, citation_id: value })} />
            <Field label="search_preview_id" value={resolveForm.search_preview_id} onChange={(value) => setResolveForm({ ...resolveForm, search_preview_id: value })} />
            <Field label="legal_search_mode" value={resolveForm.legal_search_mode} onChange={(value) => setResolveForm({ ...resolveForm, legal_search_mode: value })} />
            <Field label="provider_mode" value={resolveForm.provider_mode} onChange={(value) => setResolveForm({ ...resolveForm, provider_mode: value })} />
            <CheckField label="manual_review_confirmed" checked={resolveForm.manual_review_confirmed} onChange={(checked) => setResolveForm({ ...resolveForm, manual_review_confirmed: checked })} />
            <div className="md:col-span-3"><Button type="submit" disabled={loading === "resolve"}>{loading === "resolve" ? "解析中..." : "Resolve Mock Citation"}</Button></div>
          </form>
          {resolutionResult ? <JsonPanel title="resolution_result" value={resolutionResult} /> : null}
        </CardBody></Card>
        <Card><CardBody><h2 className="text-base font-semibold text-ink">Audit Logs</h2><JsonPanel title="audit_logs" value={auditLogs} /></CardBody></Card>
      </div>
    </AppShell>
  );
}

function Field({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return <label className="text-sm"><span className="text-muted">{label}</span><input value={value} onChange={(event) => onChange(event.target.value)} className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-ink" /></label>;
}
function CheckField({ label, checked, onChange }: { label: string; checked: boolean; onChange: (checked: boolean) => void }) {
  return <label className="flex items-center gap-2 text-sm text-muted md:col-span-3"><input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />{label}</label>;
}
function JsonPanel({ title, value }: { title: string; value: unknown }) {
  return <div className="mt-4"><div className="text-xs font-semibold uppercase tracking-wide text-muted">{title}</div><pre className="mt-2 max-h-96 overflow-auto rounded-md border border-line bg-paper p-3 text-xs text-slate-700">{JSON.stringify(value ?? {}, null, 2)}</pre></div>;
}
function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}
