"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  ControlledOCRAuditLog,
  ControlledOCRPreviewResult,
  ControlledOCRStatus,
  getControlledOCRAuditLogs,
  getControlledOCRStatus,
  runControlledOCRPreview
} from "@/services/api";

export default function ControlledOCRPage() {
  const [status, setStatus] = useState<ControlledOCRStatus | null>(null);
  const [previewResult, setPreviewResult] = useState<ControlledOCRPreviewResult | null>(null);
  const [auditLogs, setAuditLogs] = useState<ControlledOCRAuditLog[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState("");
  const [previewForm, setPreviewForm] = useState({
    case_id: "case_v44_demo_001",
    workspace_id: "workspace_demo_001",
    local_file_path: "~/Lawyer-AI-Local-Cases/demo_case/ocr_seed.txt",
    filename_redacted: "<filename_redacted>.txt",
    material_id: "material_ocr_demo_001",
    explicit_ocr_confirmation: true,
    manual_review_confirmed: true,
    ocr_mode: "mock",
    provider_mode: "controlled_local",
    preview_only: true
  });

  useEffect(() => {
    void refresh();
  }, []);

  async function refresh() {
    try {
      const [nextStatus, nextAuditLogs] = await Promise.all([
        getControlledOCRStatus(),
        getControlledOCRAuditLogs()
      ]);
      setStatus(nextStatus);
      setAuditLogs(nextAuditLogs);
    } catch {
      setError("Controlled OCR API 暂不可用，请确认后端服务已启动。");
    }
  }

  async function submitPreview(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("preview");
    setError("");
    try {
      setPreviewResult(await runControlledOCRPreview(previewForm));
      setAuditLogs(await getControlledOCRAuditLogs());
    } catch {
      setError("Controlled OCR preview 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="Controlled OCR"
          description="受控本地 OCR 预览；默认 mock OCR，不调用真实 OCR，不读取 PDF / image binary 内容。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_controlled_ocr"} />
              <InfoRow label="production_enabled" value={String(status?.production_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="ocr_live_default" value={String(status?.ocr_live_default ?? false)} />
              <InfoRow label="mock_ocr_enabled" value={String(status?.mock_ocr_enabled ?? true)} />
              <InfoRow label="requires_explicit_ocr_confirmation" value={String(status?.requires_explicit_ocr_confirmation ?? true)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="allowed_file_extensions" value={(status?.allowed_file_extensions ?? [".pdf", ".png", ".jpg", ".jpeg", ".txt"]).join(" / ")} />
              <InfoRow label="max_file_size_bytes" value={String(status?.max_file_size_bytes ?? 5000000)} />
              <InfoRow label="read_pdf_binary_enabled" value={String(status?.read_pdf_binary_enabled ?? false)} />
              <InfoRow label="read_image_binary_enabled" value={String(status?.read_image_binary_enabled ?? false)} />
              <InfoRow label="extract_real_ocr_text_enabled" value={String(status?.extract_real_ocr_text_enabled ?? false)} />
              <InfoRow label="store_raw_ocr_text_in_git" value={String(status?.store_raw_ocr_text_in_git ?? false)} />
              <InfoRow label="store_redacted_ocr_preview_in_git" value={String(status?.store_redacted_ocr_preview_in_git ?? false)} />
              <InfoRow label="runtime_storage_enabled" value={String(status?.runtime_storage_enabled ?? true)} />
              <InfoRow label="runtime_storage_path" value={status?.runtime_storage_path ?? "storage/runtime/controlled_ocr_previews"} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
            </div>
            <JsonPanel title="warnings" value={status?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">OCR Preview</h2>
            <div className="mt-3 grid gap-3 md:grid-cols-2">
              <InfoRow label="default" value="mock OCR only" />
              <InfoRow label="blocked" value="real OCR / LLM / Legal Search / DeepSeek live" />
              <InfoRow label="binary" value="PDF and image binary content not read" />
              <InfoRow label="storage" value="redacted OCR preview in ignored runtime only" />
            </div>
            <form onSubmit={submitPreview} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="case_id" value={previewForm.case_id} onChange={(value) => setPreviewForm({ ...previewForm, case_id: value })} />
              <Field label="workspace_id" value={previewForm.workspace_id} onChange={(value) => setPreviewForm({ ...previewForm, workspace_id: value })} />
              <Field label="local_file_path" value={previewForm.local_file_path} onChange={(value) => setPreviewForm({ ...previewForm, local_file_path: value })} />
              <Field label="filename_redacted" value={previewForm.filename_redacted} onChange={(value) => setPreviewForm({ ...previewForm, filename_redacted: value })} />
              <Field label="material_id" value={previewForm.material_id} onChange={(value) => setPreviewForm({ ...previewForm, material_id: value })} />
              <Field label="ocr_mode" value={previewForm.ocr_mode} onChange={(value) => setPreviewForm({ ...previewForm, ocr_mode: value })} />
              <Field label="provider_mode" value={previewForm.provider_mode} onChange={(value) => setPreviewForm({ ...previewForm, provider_mode: value })} />
              <CheckField label="explicit_ocr_confirmation" checked={previewForm.explicit_ocr_confirmation} onChange={(checked) => setPreviewForm({ ...previewForm, explicit_ocr_confirmation: checked })} />
              <CheckField label="manual_review_confirmed" checked={previewForm.manual_review_confirmed} onChange={(checked) => setPreviewForm({ ...previewForm, manual_review_confirmed: checked })} />
              <CheckField label="preview_only" checked={previewForm.preview_only} onChange={(checked) => setPreviewForm({ ...previewForm, preview_only: checked })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "preview"}>{loading === "preview" ? "预览中..." : "Run Controlled OCR Preview"}</Button>
              </div>
            </form>
            {previewResult ? (
              <div className="mt-5 grid gap-4 lg:grid-cols-2">
                <InfoRow label="ocr_preview_id" value={previewResult.ocr_preview_id} />
                <InfoRow label="allowed_to_continue" value={String(previewResult.allowed_to_continue)} />
                <InfoRow label="ocr_called" value={String(previewResult.ocr_called)} />
                <InfoRow label="real_ocr_called" value={String(previewResult.real_ocr_called)} />
                <InfoRow label="mock_ocr_used" value={String(previewResult.mock_ocr_used)} />
                <InfoRow label="raw_ocr_text_stored" value={String(previewResult.raw_ocr_text_stored)} />
                <InfoRow label="redacted_ocr_preview_created" value={String(previewResult.redacted_ocr_preview_created)} />
                <InfoRow label="redacted_ocr_preview_storage_path" value={previewResult.redacted_ocr_preview_storage_path} />
                <div className="lg:col-span-2">
                  <JsonPanel title="guard_results" value={previewResult.guard_results} />
                  <JsonPanel title="redacted_ocr_preview" value={previewResult.redacted_ocr_preview} />
                  <JsonPanel title="source_refs" value={previewResult.source_refs} />
                  <JsonPanel title="ocr_preview_result" value={previewResult} />
                </div>
              </div>
            ) : null}
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
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-ink"
      />
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
      <pre className="mt-2 max-h-96 overflow-auto rounded-md border border-line bg-paper p-3 text-xs text-slate-700">
        {JSON.stringify(value ?? {}, null, 2)}
      </pre>
    </div>
  );
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}
