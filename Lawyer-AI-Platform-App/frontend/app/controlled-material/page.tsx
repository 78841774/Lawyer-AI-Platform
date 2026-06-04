"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  ControlledMaterialAuditLog,
  ControlledMaterialReadResult,
  ControlledMaterialStatus,
  ControlledReportDraftResult,
  generateControlledReportDraft,
  getControlledMaterialAuditLogs,
  getControlledMaterialStatus,
  runControlledMaterialReadConfirmed
} from "@/services/api";

export default function ControlledMaterialPage() {
  const [status, setStatus] = useState<ControlledMaterialStatus | null>(null);
  const [readResult, setReadResult] = useState<ControlledMaterialReadResult | null>(null);
  const [reportResult, setReportResult] = useState<ControlledReportDraftResult | null>(null);
  const [auditLogs, setAuditLogs] = useState<ControlledMaterialAuditLog[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState("");
  const [readForm, setReadForm] = useState({
    case_id: "case_v42_demo_001",
    workspace_id: "workspace_demo_001",
    local_case_root: "~/Lawyer-AI-Local-Cases/demo_case",
    material_id: "material_demo_001",
    filename_redacted: "<filename_redacted>.pdf",
    read_mode: "controlled_local",
    explicit_read_confirmation: true,
    manual_review_confirmed: true,
    provider_mode: "controlled_local",
    ocr_mode: "mock",
    llm_mode: "mock",
    legal_search_mode: "mock"
  });
  const [reportForm, setReportForm] = useState({
    case_id: "case_v42_demo_001",
    workspace_id: "workspace_demo_001",
    controlled_read_id: "controlled_read_demo_001",
    report_mode: "mock_draft",
    manual_review_confirmed: true,
    llm_mode: "mock"
  });

  useEffect(() => {
    void refresh();
  }, []);

  async function refresh() {
    try {
      const [nextStatus, nextAuditLogs] = await Promise.all([
        getControlledMaterialStatus(),
        getControlledMaterialAuditLogs()
      ]);
      setStatus(nextStatus);
      setAuditLogs(nextAuditLogs);
    } catch {
      setError("Controlled Material API 暂不可用，请确认后端服务已启动。");
    }
  }

  async function submitRead(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("read");
    setError("");
    try {
      const nextResult = await runControlledMaterialReadConfirmed(readForm);
      setReadResult(nextResult);
      setReportForm({ ...reportForm, controlled_read_id: nextResult.controlled_read_id });
      setAuditLogs(await getControlledMaterialAuditLogs());
    } catch {
      setError("Controlled read-confirmed 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  async function submitReport(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("report");
    setError("");
    try {
      setReportResult(await generateControlledReportDraft(reportForm));
      setAuditLogs(await getControlledMaterialAuditLogs());
    } catch {
      setError("Controlled report draft 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="Controlled Material"
          description="受控本地真实材料处理门禁；本阶段只建立 read gate 和 mock draft，不读取真实正文。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_controlled"} />
              <InfoRow label="production_enabled" value={String(status?.production_enabled ?? false)} />
              <InfoRow label="real_material_reading_enabled" value={String(status?.real_material_reading_enabled ?? false)} />
              <InfoRow label="requires_explicit_read_confirmation" value={String(status?.requires_explicit_read_confirmation ?? true)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="store_extracted_text_in_git" value={String(status?.store_extracted_text_in_git ?? false)} />
              <InfoRow label="store_material_content_in_git" value={String(status?.store_material_content_in_git ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
            </div>
            <JsonPanel title="warnings" value={status?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Read Confirmation Gate</h2>
            <form onSubmit={submitRead} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="case_id" value={readForm.case_id} onChange={(value) => setReadForm({ ...readForm, case_id: value })} />
              <Field label="workspace_id" value={readForm.workspace_id} onChange={(value) => setReadForm({ ...readForm, workspace_id: value })} />
              <Field label="local_case_root" value={readForm.local_case_root} onChange={(value) => setReadForm({ ...readForm, local_case_root: value })} />
              <Field label="material_id" value={readForm.material_id} onChange={(value) => setReadForm({ ...readForm, material_id: value })} />
              <Field label="filename_redacted" value={readForm.filename_redacted} onChange={(value) => setReadForm({ ...readForm, filename_redacted: value })} />
              <Field label="read_mode" value={readForm.read_mode} onChange={(value) => setReadForm({ ...readForm, read_mode: value })} />
              <Field label="provider_mode" value={readForm.provider_mode} onChange={(value) => setReadForm({ ...readForm, provider_mode: value })} />
              <Field label="ocr_mode" value={readForm.ocr_mode} onChange={(value) => setReadForm({ ...readForm, ocr_mode: value })} />
              <Field label="llm_mode" value={readForm.llm_mode} onChange={(value) => setReadForm({ ...readForm, llm_mode: value })} />
              <Field label="legal_search_mode" value={readForm.legal_search_mode} onChange={(value) => setReadForm({ ...readForm, legal_search_mode: value })} />
              <CheckField label="explicit_read_confirmation" checked={readForm.explicit_read_confirmation} onChange={(checked) => setReadForm({ ...readForm, explicit_read_confirmation: checked })} />
              <CheckField label="manual_review_confirmed" checked={readForm.manual_review_confirmed} onChange={(checked) => setReadForm({ ...readForm, manual_review_confirmed: checked })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "read"}>{loading === "read" ? "检查中..." : "运行 Read Gate"}</Button>
              </div>
            </form>
            {readResult ? (
              <div className="mt-5 grid gap-4 lg:grid-cols-2">
                <InfoRow label="controlled_read_id" value={readResult.controlled_read_id} />
                <InfoRow label="allowed_to_continue" value={String(readResult.allowed_to_continue)} />
                <InfoRow label="content_read" value={String(readResult.content_read)} />
                <InfoRow label="requires_next_stage_real_read" value={String(readResult.requires_next_stage_real_read)} />
                <InfoRow label="extracted_text_stored" value={String(readResult.extracted_text_stored)} />
                <InfoRow label="git_storage_allowed" value={String(readResult.git_storage_allowed)} />
                <div className="lg:col-span-2">
                  <JsonPanel title="guard_results" value={readResult.guard_results} />
                  <JsonPanel title="source_refs" value={readResult.source_refs} />
                  <JsonPanel title="read_result" value={readResult} />
                </div>
              </div>
            ) : null}
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Mock Report Draft</h2>
            <form onSubmit={submitReport} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="case_id" value={reportForm.case_id} onChange={(value) => setReportForm({ ...reportForm, case_id: value })} />
              <Field label="workspace_id" value={reportForm.workspace_id} onChange={(value) => setReportForm({ ...reportForm, workspace_id: value })} />
              <Field label="controlled_read_id" value={reportForm.controlled_read_id} onChange={(value) => setReportForm({ ...reportForm, controlled_read_id: value })} />
              <Field label="report_mode" value={reportForm.report_mode} onChange={(value) => setReportForm({ ...reportForm, report_mode: value })} />
              <Field label="llm_mode" value={reportForm.llm_mode} onChange={(value) => setReportForm({ ...reportForm, llm_mode: value })} />
              <CheckField label="manual_review_confirmed" checked={reportForm.manual_review_confirmed} onChange={(checked) => setReportForm({ ...reportForm, manual_review_confirmed: checked })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "report"}>{loading === "report" ? "生成中..." : "生成 Mock Report Draft"}</Button>
              </div>
            </form>
            {reportResult ? <JsonPanel title="report_draft_result" value={reportResult} /> : null}
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
