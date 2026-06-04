"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  PersonalAlphaWorkspaceAuditLog,
  PersonalAlphaWorkspaceRunRecord,
  PersonalAlphaWorkspaceRunResult,
  PersonalAlphaWorkspaceStatus,
  getPersonalAlphaWorkspaceAuditLogs,
  getPersonalAlphaWorkspaceRun,
  getPersonalAlphaWorkspaceStatus,
  runPersonalAlphaWorkspace
} from "@/services/api";

export default function PersonalAlphaWorkspacePage() {
  const [status, setStatus] = useState<PersonalAlphaWorkspaceStatus | null>(null);
  const [result, setResult] = useState<PersonalAlphaWorkspaceRunResult | null>(null);
  const [record, setRecord] = useState<PersonalAlphaWorkspaceRunRecord | null>(null);
  const [auditLogs, setAuditLogs] = useState<PersonalAlphaWorkspaceAuditLog[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState("");
  const [workspaceRunId, setWorkspaceRunId] = useState("");
  const [form, setForm] = useState({
    case_id: "case_v50_demo_001",
    workspace_id: "workspace_demo_001",
    workflow_mode: "end_to_end_mock",
    material_preview_id: "controlled_preview_demo_001",
    ocr_preview_id: "ocr_preview_demo_001",
    legal_search_preview_id: "legal_search_preview_demo_001",
    draft_id: "draft_demo_001",
    review_id: "review_demo_001",
    revision_id: "revision_demo_001",
    final_lock_id: "final_lock_demo_001",
    explicit_workspace_confirmation: true,
    manual_review_confirmed: true,
    provider_mode: "controlled_local",
    llm_mode: "mock",
    preview_only: true
  });

  useEffect(() => {
    void refresh();
  }, []);

  async function refresh() {
    try {
      const [nextStatus, nextAuditLogs] = await Promise.all([
        getPersonalAlphaWorkspaceStatus(),
        getPersonalAlphaWorkspaceAuditLogs()
      ]);
      setStatus(nextStatus);
      setAuditLogs(nextAuditLogs);
    } catch {
      setError("Personal Alpha Workspace API 暂不可用，请确认后端服务已启动。");
    }
  }

  async function submitRun(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("run");
    setError("");
    try {
      const nextResult = await runPersonalAlphaWorkspace(form);
      setResult(nextResult);
      setWorkspaceRunId(nextResult.workspace_run_id);
      setAuditLogs(await getPersonalAlphaWorkspaceAuditLogs());
    } catch {
      setError("Personal alpha workspace run 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  async function loadRun(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("load");
    setError("");
    try {
      setRecord(await getPersonalAlphaWorkspaceRun(workspaceRunId));
      setAuditLogs(await getPersonalAlphaWorkspaceAuditLogs());
    } catch {
      setError("Load workspace run 失败，请确认 workspace_run_id 存在且后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  const stages = result?.stage_statuses ?? record?.stage_statuses ?? [];

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="Personal Alpha Workspace"
          description="个人本地端到端案件工作区；仅聚合 controlled mock workflow，不调用真实服务，不生成正式法律意见。"
        />
        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_personal_alpha_workspace"} />
              <InfoRow label="local-only" value="true" />
              <InfoRow label="mock_first_enabled" value={String(status?.mock_first_enabled ?? true)} />
              <InfoRow label="end_to_end_workflow_enabled" value={String(status?.end_to_end_workflow_enabled ?? true)} />
              <InfoRow label="requires_explicit_workspace_confirmation" value={String(status?.requires_explicit_workspace_confirmation ?? true)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
              <InfoRow label="auto_skill_publish_enabled" value={String(status?.auto_skill_publish_enabled ?? false)} />
              <InfoRow label="auto_workspace_runtime_enabled" value={String(status?.auto_workspace_runtime_enabled ?? false)} />
              <InfoRow label="runtime_storage_path" value={status?.runtime_storage_path ?? "storage/runtime/personal_alpha_workspace"} />
            </div>
            <JsonPanel title="warnings" value={status?.warnings ?? []} />
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {stageCards.map((stage) => (
            <Card key={stage.id}>
              <CardBody>
                <div className="text-xs uppercase tracking-wide text-muted">{stage.id}</div>
                <div className="mt-2 text-base font-semibold text-ink">{stage.label}</div>
                <div className="mt-3 text-sm text-muted">mock-only</div>
              </CardBody>
            </Card>
          ))}
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Workspace Run</h2>
            <form onSubmit={submitRun} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="case_id" value={form.case_id} onChange={(value) => setForm({ ...form, case_id: value })} />
              <Field label="workspace_id" value={form.workspace_id} onChange={(value) => setForm({ ...form, workspace_id: value })} />
              <Field label="workflow_mode" value={form.workflow_mode} onChange={(value) => setForm({ ...form, workflow_mode: value })} />
              <Field label="material_preview_id" value={form.material_preview_id} onChange={(value) => setForm({ ...form, material_preview_id: value })} />
              <Field label="ocr_preview_id" value={form.ocr_preview_id} onChange={(value) => setForm({ ...form, ocr_preview_id: value })} />
              <Field label="legal_search_preview_id" value={form.legal_search_preview_id} onChange={(value) => setForm({ ...form, legal_search_preview_id: value })} />
              <Field label="draft_id" value={form.draft_id} onChange={(value) => setForm({ ...form, draft_id: value })} />
              <Field label="review_id" value={form.review_id} onChange={(value) => setForm({ ...form, review_id: value })} />
              <Field label="revision_id" value={form.revision_id} onChange={(value) => setForm({ ...form, revision_id: value })} />
              <Field label="final_lock_id" value={form.final_lock_id} onChange={(value) => setForm({ ...form, final_lock_id: value })} />
              <Field label="provider_mode" value={form.provider_mode} onChange={(value) => setForm({ ...form, provider_mode: value })} />
              <Field label="llm_mode" value={form.llm_mode} onChange={(value) => setForm({ ...form, llm_mode: value })} />
              <CheckField label="explicit_workspace_confirmation" checked={form.explicit_workspace_confirmation} onChange={(checked) => setForm({ ...form, explicit_workspace_confirmation: checked })} />
              <CheckField label="manual_review_confirmed" checked={form.manual_review_confirmed} onChange={(checked) => setForm({ ...form, manual_review_confirmed: checked })} />
              <CheckField label="preview_only" checked={form.preview_only} onChange={(checked) => setForm({ ...form, preview_only: checked })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "run"}>{loading === "run" ? "运行中..." : "Run Mock Workspace"}</Button>
              </div>
            </form>
            {result ? <JsonPanel title="workspace_run_result" value={result} /> : null}
          </CardBody>
        </Card>

        {stages.length ? (
          <Card>
            <CardBody>
              <h2 className="text-base font-semibold text-ink">Unified Stage Status</h2>
              <JsonPanel title="stage_statuses" value={stages} />
            </CardBody>
          </Card>
        ) : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Load Workspace Run</h2>
            <form onSubmit={loadRun} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="workspace_run_id" value={workspaceRunId} onChange={setWorkspaceRunId} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "load"}>{loading === "load" ? "读取中..." : "Load Workspace Run"}</Button>
              </div>
            </form>
            {record ? <JsonPanel title="workspace_run_record" value={record} /> : null}
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

const stageCards = [
  { id: "material", label: "Material Preview" },
  { id: "ocr", label: "OCR Preview" },
  { id: "legal_search", label: "Legal Search Preview" },
  { id: "draft", label: "Report Draft" },
  { id: "review", label: "Lawyer Review" },
  { id: "revision", label: "Revision" },
  { id: "final_lock", label: "Final Review Lock" }
];

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
