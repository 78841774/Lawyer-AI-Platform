"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  MaterialInventoryResult,
  PersonalAlphaAuditLog,
  PersonalAlphaDryRunResult,
  PersonalAlphaStatus,
  PersonalCaseManifestPreview,
  getPersonalAlphaAuditLogs,
  getPersonalAlphaStatus,
  previewPersonalAlphaManifest,
  previewPersonalAlphaMaterialInventory,
  runPersonalAlphaDryRun
} from "@/services/api";

export default function PersonalAlphaPage() {
  const [status, setStatus] = useState<PersonalAlphaStatus | null>(null);
  const [manifestPreview, setManifestPreview] = useState<PersonalCaseManifestPreview | null>(null);
  const [materialInventory, setMaterialInventory] = useState<MaterialInventoryResult | null>(null);
  const [dryRunResult, setDryRunResult] = useState<PersonalAlphaDryRunResult | null>(null);
  const [auditLogs, setAuditLogs] = useState<PersonalAlphaAuditLog[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState("");
  const [manifestForm, setManifestForm] = useState({
    case_id: "case_personal_alpha_001",
    workspace_id: "workspace_demo_001",
    case_title_redacted: "合同纠纷测试样本",
    local_case_root: "~/Lawyer-AI-Local-Cases/demo_case",
    case_cause_code: "payment_dispute",
    jurisdiction: "CN",
    dry_run_only: true,
    manual_review_confirmed: true
  });
  const [inventoryForm, setInventoryForm] = useState({
    case_id: "case_personal_alpha_001",
    workspace_id: "workspace_demo_001",
    local_case_root: "~/Lawyer-AI-Local-Cases/demo_case",
    include_file_names: false,
    dry_run_only: true
  });
  const [dryRunForm, setDryRunForm] = useState({
    case_id: "case_personal_alpha_001",
    workspace_id: "workspace_demo_001",
    local_case_root: "~/Lawyer-AI-Local-Cases/demo_case",
    case_cause_code: "payment_dispute",
    jurisdiction: "CN",
    provider_mode: "mock",
    ocr_mode: "mock",
    legal_search_mode: "mock",
    llm_mode: "mock",
    dry_run_only: true,
    manual_review_confirmed: true
  });

  useEffect(() => {
    void refresh();
  }, []);

  async function refresh() {
    try {
      const [nextStatus, nextAuditLogs] = await Promise.all([getPersonalAlphaStatus(), getPersonalAlphaAuditLogs()]);
      setStatus(nextStatus);
      setAuditLogs(nextAuditLogs);
    } catch {
      setError("Personal Alpha API 暂不可用，请确认后端服务已启动。");
    }
  }

  async function submitManifest(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("manifest");
    setError("");
    try {
      setManifestPreview(await previewPersonalAlphaManifest(manifestForm));
    } catch {
      setError("Manifest preview 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  async function submitInventory(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("inventory");
    setError("");
    try {
      setMaterialInventory(await previewPersonalAlphaMaterialInventory(inventoryForm));
    } catch {
      setError("Material inventory preview 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  async function submitDryRun(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading("dry-run");
    setError("");
    try {
      setDryRunResult(await runPersonalAlphaDryRun(dryRunForm));
      setAuditLogs(await getPersonalAlphaAuditLogs());
    } catch {
      setError("Personal Alpha dry-run 失败，请确认后端服务已启动。");
    } finally {
      setLoading("");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="Personal Alpha"
          description="个人本地真实案件 Alpha dry-run 预览；只做 metadata-only、mock preview 和人工复核门。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "personal_local_alpha"} />
              <InfoRow label="production_enabled" value={String(status?.production_enabled ?? false)} />
              <InfoRow label="team_mode_enabled" value={String(status?.team_mode_enabled ?? false)} />
              <InfoRow label="real_case_processing_enabled" value={String(status?.real_case_processing_enabled ?? false)} />
              <InfoRow label="material_content_reading_enabled" value={String(status?.material_content_reading_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="local_only" value={String(status?.local_only ?? true)} />
              <InfoRow label="dry_run_only" value={String(status?.dry_run_only ?? true)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
            </div>
            <JsonPanel title="warnings" value={status?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Manifest Preview</h2>
            <form onSubmit={submitManifest} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="case_id" value={manifestForm.case_id} onChange={(value) => setManifestForm({ ...manifestForm, case_id: value })} />
              <Field label="workspace_id" value={manifestForm.workspace_id} onChange={(value) => setManifestForm({ ...manifestForm, workspace_id: value })} />
              <Field label="case_title_redacted" value={manifestForm.case_title_redacted} onChange={(value) => setManifestForm({ ...manifestForm, case_title_redacted: value })} />
              <Field label="local_case_root" value={manifestForm.local_case_root} onChange={(value) => setManifestForm({ ...manifestForm, local_case_root: value })} />
              <Field label="case_cause_code" value={manifestForm.case_cause_code} onChange={(value) => setManifestForm({ ...manifestForm, case_cause_code: value })} />
              <Field label="jurisdiction" value={manifestForm.jurisdiction} onChange={(value) => setManifestForm({ ...manifestForm, jurisdiction: value })} />
              <CheckField label="dry_run_only" checked={manifestForm.dry_run_only} onChange={(checked) => setManifestForm({ ...manifestForm, dry_run_only: checked })} />
              <CheckField label="manual_review_confirmed" checked={manifestForm.manual_review_confirmed} onChange={(checked) => setManifestForm({ ...manifestForm, manual_review_confirmed: checked })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "manifest"}>{loading === "manifest" ? "预览中..." : "生成 Manifest Preview"}</Button>
              </div>
            </form>
            {manifestPreview ? <JsonPanel title="manifest_preview" value={manifestPreview} /> : null}
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Material Inventory Preview</h2>
            <form onSubmit={submitInventory} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="case_id" value={inventoryForm.case_id} onChange={(value) => setInventoryForm({ ...inventoryForm, case_id: value })} />
              <Field label="workspace_id" value={inventoryForm.workspace_id} onChange={(value) => setInventoryForm({ ...inventoryForm, workspace_id: value })} />
              <Field label="local_case_root" value={inventoryForm.local_case_root} onChange={(value) => setInventoryForm({ ...inventoryForm, local_case_root: value })} />
              <CheckField label="include_file_names" checked={inventoryForm.include_file_names} onChange={(checked) => setInventoryForm({ ...inventoryForm, include_file_names: checked })} />
              <CheckField label="dry_run_only" checked={inventoryForm.dry_run_only} onChange={(checked) => setInventoryForm({ ...inventoryForm, dry_run_only: checked })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "inventory"}>{loading === "inventory" ? "预览中..." : "生成 Inventory Preview"}</Button>
              </div>
            </form>
            {materialInventory ? <JsonPanel title="material_inventory" value={materialInventory} /> : null}
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Personal Alpha Dry Run</h2>
            <form onSubmit={submitDryRun} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="case_id" value={dryRunForm.case_id} onChange={(value) => setDryRunForm({ ...dryRunForm, case_id: value })} />
              <Field label="workspace_id" value={dryRunForm.workspace_id} onChange={(value) => setDryRunForm({ ...dryRunForm, workspace_id: value })} />
              <Field label="local_case_root" value={dryRunForm.local_case_root} onChange={(value) => setDryRunForm({ ...dryRunForm, local_case_root: value })} />
              <Field label="case_cause_code" value={dryRunForm.case_cause_code} onChange={(value) => setDryRunForm({ ...dryRunForm, case_cause_code: value })} />
              <Field label="jurisdiction" value={dryRunForm.jurisdiction} onChange={(value) => setDryRunForm({ ...dryRunForm, jurisdiction: value })} />
              <Field label="provider_mode" value={dryRunForm.provider_mode} onChange={(value) => setDryRunForm({ ...dryRunForm, provider_mode: value })} />
              <Field label="ocr_mode" value={dryRunForm.ocr_mode} onChange={(value) => setDryRunForm({ ...dryRunForm, ocr_mode: value })} />
              <Field label="legal_search_mode" value={dryRunForm.legal_search_mode} onChange={(value) => setDryRunForm({ ...dryRunForm, legal_search_mode: value })} />
              <Field label="llm_mode" value={dryRunForm.llm_mode} onChange={(value) => setDryRunForm({ ...dryRunForm, llm_mode: value })} />
              <CheckField label="dry_run_only" checked={dryRunForm.dry_run_only} onChange={(checked) => setDryRunForm({ ...dryRunForm, dry_run_only: checked })} />
              <CheckField label="manual_review_confirmed" checked={dryRunForm.manual_review_confirmed} onChange={(checked) => setDryRunForm({ ...dryRunForm, manual_review_confirmed: checked })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading === "dry-run"}>{loading === "dry-run" ? "检查中..." : "运行 Personal Alpha Dry Run"}</Button>
              </div>
            </form>
            {dryRunResult ? <JsonPanel title="dry_run_result" value={dryRunResult} /> : null}
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
