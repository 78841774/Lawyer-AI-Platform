"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  DatabaseReadinessStatus,
  InternalAlphaAuditLog,
  InternalAlphaDryRunResult,
  InternalAlphaReadinessChecklist,
  InternalAlphaStatus,
  SecretManagementChecklist,
  getInternalAlphaAuditLogs,
  getInternalAlphaDatabase,
  getInternalAlphaReadiness,
  getInternalAlphaSecrets,
  getInternalAlphaStatus,
  runInternalAlphaDryRun
} from "@/services/api";

export default function InternalAlphaPage() {
  const [status, setStatus] = useState<InternalAlphaStatus | null>(null);
  const [readiness, setReadiness] = useState<InternalAlphaReadinessChecklist | null>(null);
  const [secrets, setSecrets] = useState<SecretManagementChecklist | null>(null);
  const [database, setDatabase] = useState<DatabaseReadinessStatus | null>(null);
  const [auditLogs, setAuditLogs] = useState<InternalAlphaAuditLog[]>([]);
  const [result, setResult] = useState<InternalAlphaDryRunResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    case_id: "case_demo_alpha_001",
    workspace_id: "workspace_demo_001",
    local_case_root: "~/Lawyer-AI-Local-Cases/demo_case",
    provider_mode: "mock",
    ocr_mode: "mock",
    legal_search_mode: "mock",
    dry_run_only: true,
    manual_review_confirmed: true
  });

  useEffect(() => {
    void refresh();
  }, []);

  async function refresh() {
    try {
      const [nextStatus, nextReadiness, nextSecrets, nextDatabase, nextAuditLogs] = await Promise.all([
        getInternalAlphaStatus(),
        getInternalAlphaReadiness(),
        getInternalAlphaSecrets(),
        getInternalAlphaDatabase(),
        getInternalAlphaAuditLogs()
      ]);
      setStatus(nextStatus);
      setReadiness(nextReadiness);
      setSecrets(nextSecrets);
      setDatabase(nextDatabase);
      setAuditLogs(nextAuditLogs);
    } catch {
      setError("Internal Alpha API 暂不可用，请确认后端服务已启动。");
    }
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      setResult(await runInternalAlphaDryRun(form));
      setAuditLogs(await getInternalAlphaAuditLogs());
      setReadiness(await getInternalAlphaReadiness());
    } catch {
      setError("Internal Alpha dry-run 失败，请确认后端服务已启动。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="Internal Alpha"
          description="本地 Internal Alpha readiness、guard、dry-run 和审计汇总；不读取真实材料，不调用真实 provider。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_internal_alpha"} />
              <InfoRow label="production_enabled" value={String(status?.production_enabled ?? false)} />
              <InfoRow label="team_mode_enabled" value={String(status?.team_mode_enabled ?? false)} />
              <InfoRow label="real_case_processing_enabled" value={String(status?.real_case_processing_enabled ?? false)} />
              <InfoRow label="workspace_runtime_auto_enable" value={String(status?.workspace_runtime_auto_enable ?? false)} />
              <InfoRow label="skill_aware_case_processing_auto_enable" value={String(status?.skill_aware_case_processing_auto_enable ?? false)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="local_only" value={String(status?.local_only ?? true)} />
            </div>
            <JsonPanel title="warnings" value={status?.warnings ?? []} />
          </CardBody>
        </Card>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardBody>
              <h2 className="text-base font-semibold text-ink">Deployment Readiness</h2>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <InfoRow label="required_passed" value={String(readiness?.required_passed ?? false)} />
                <InfoRow label="manual_verification_required" value={String(readiness?.manual_verification_required ?? true)} />
              </div>
              <JsonPanel title="items" value={readiness?.items ?? []} />
            </CardBody>
          </Card>

          <Card>
            <CardBody>
              <h2 className="text-base font-semibold text-ink">Secrets / Database</h2>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <InfoRow label="env_file_not_committed" value={String(secrets?.env_file_not_committed ?? true)} />
                <InfoRow label="api_key_not_committed" value={String(secrets?.api_key_not_committed ?? true)} />
                <InfoRow label="deepseek_key_not_committed" value={String(secrets?.deepseek_key_not_committed ?? true)} />
                <InfoRow label="sqlite_local_ready" value={String(database?.sqlite_local_ready ?? true)} />
                <InfoRow label="local_db_ignored" value={String(database?.local_db_ignored ?? true)} />
                <InfoRow label="production_migration_out_of_scope" value={String(database?.production_migration_out_of_scope ?? true)} />
              </div>
              <JsonPanel title="secret_notes" value={secrets?.notes ?? []} />
              <JsonPanel title="database_notes" value={database?.notes ?? []} />
            </CardBody>
          </Card>
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Subsystem Status</h2>
            <JsonPanel title="subsystems" value={status?.subsystems ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Internal Alpha Dry Run</h2>
            <form onSubmit={submit} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="case_id" value={form.case_id} onChange={(value) => setForm({ ...form, case_id: value })} />
              <Field label="workspace_id" value={form.workspace_id} onChange={(value) => setForm({ ...form, workspace_id: value })} />
              <Field label="local_case_root" value={form.local_case_root} onChange={(value) => setForm({ ...form, local_case_root: value })} />
              <Field label="provider_mode" value={form.provider_mode} onChange={(value) => setForm({ ...form, provider_mode: value })} />
              <Field label="ocr_mode" value={form.ocr_mode} onChange={(value) => setForm({ ...form, ocr_mode: value })} />
              <Field label="legal_search_mode" value={form.legal_search_mode} onChange={(value) => setForm({ ...form, legal_search_mode: value })} />
              <CheckField label="dry_run_only" checked={form.dry_run_only} onChange={(checked) => setForm({ ...form, dry_run_only: checked })} />
              <CheckField label="manual_review_confirmed" checked={form.manual_review_confirmed} onChange={(checked) => setForm({ ...form, manual_review_confirmed: checked })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading}>{loading ? "检查中..." : "运行 Internal Alpha Dry Run"}</Button>
              </div>
            </form>

            {result ? (
              <div className="mt-5 grid gap-4 lg:grid-cols-2">
                <InfoRow label="alpha_dry_run_id" value={result.alpha_dry_run_id} />
                <InfoRow label="allowed_to_continue" value={String(result.allowed_to_continue)} />
                <InfoRow label="manual_review_required" value={String(result.manual_review_required)} />
                <InfoRow label="audit_log_id" value={result.audit_log_id} />
                <InfoRow label="created_at" value={result.created_at} />
                <div className="lg:col-span-2">
                  <JsonPanel title="dry_run_result" value={result} />
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
