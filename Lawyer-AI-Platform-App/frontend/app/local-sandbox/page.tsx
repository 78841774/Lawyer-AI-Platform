"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  LocalSandboxAuditLog,
  LocalSandboxDryRunResult,
  LocalSandboxGuardStatus,
  LocalSandboxStatus,
  getLocalSandboxAuditLogs,
  getLocalSandboxGuards,
  getLocalSandboxStatus,
  runLocalSandboxDryRun
} from "@/services/api";

export default function LocalSandboxPage() {
  const [status, setStatus] = useState<LocalSandboxStatus | null>(null);
  const [guards, setGuards] = useState<LocalSandboxGuardStatus | null>(null);
  const [auditLogs, setAuditLogs] = useState<LocalSandboxAuditLog[]>([]);
  const [result, setResult] = useState<LocalSandboxDryRunResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    case_id: "case_demo_001",
    workspace_id: "workspace_demo_001",
    local_case_root: "~/Lawyer-AI-Local-Cases/demo_case",
    provider_mode: "mock",
    ocr_mode: "mock",
    legal_search_mode: "mock",
    dry_run_only: true
  });

  useEffect(() => {
    void refresh();
  }, []);

  async function refresh() {
    try {
      const [nextStatus, nextGuards, nextAuditLogs] = await Promise.all([
        getLocalSandboxStatus(),
        getLocalSandboxGuards(),
        getLocalSandboxAuditLogs()
      ]);
      setStatus(nextStatus);
      setGuards(nextGuards);
      setAuditLogs(nextAuditLogs);
    } catch {
      setError("Local Sandbox API 暂不可用，请确认后端服务已启动。");
    }
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const nextResult = await runLocalSandboxDryRun(form);
      setResult(nextResult);
      setAuditLogs(await getLocalSandboxAuditLogs());
      setGuards(await getLocalSandboxGuards());
    } catch {
      setError("Local Sandbox dry-run 失败，请确认后端服务已启动。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="Local Sandbox"
          description="仅做 local-only dry-run、安全边界和审计记录；不读取真实材料，不调用真实 OCR、法律数据库或 LLM。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Sandbox Status</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="enabled" value={String(status?.enabled ?? true)} />
              <InfoRow label="mode" value={status?.mode ?? "local_only"} />
              <InfoRow label="real_case_processing_enabled" value={String(status?.real_case_processing_enabled ?? false)} />
              <InfoRow label="live_provider_enabled" value={String(status?.live_provider_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="real_ocr_enabled" value={String(status?.real_ocr_enabled ?? false)} />
              <InfoRow label="real_legal_search_enabled" value={String(status?.real_legal_search_enabled ?? false)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="mock_only" value={String(status?.mock_only ?? true)} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Guard Status</h2>
            <div className="mt-4 grid gap-4 lg:grid-cols-3">
              <JsonPanel title="provider_mode_guard" value={guards?.provider_mode_guard} />
              <JsonPanel title="material_safety_guard" value={guards?.material_safety_guard} />
              <JsonPanel title="git_safety_guard" value={guards?.git_safety_guard} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Dry Run</h2>
            <form onSubmit={submit} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="case_id" value={form.case_id} onChange={(value) => setForm({ ...form, case_id: value })} />
              <Field label="workspace_id" value={form.workspace_id} onChange={(value) => setForm({ ...form, workspace_id: value })} />
              <Field label="local_case_root" value={form.local_case_root} onChange={(value) => setForm({ ...form, local_case_root: value })} />
              <Field label="provider_mode" value={form.provider_mode} onChange={(value) => setForm({ ...form, provider_mode: value })} />
              <Field label="ocr_mode" value={form.ocr_mode} onChange={(value) => setForm({ ...form, ocr_mode: value })} />
              <Field label="legal_search_mode" value={form.legal_search_mode} onChange={(value) => setForm({ ...form, legal_search_mode: value })} />
              <label className="flex items-center gap-2 text-sm text-muted md:col-span-3">
                <input
                  type="checkbox"
                  checked={form.dry_run_only}
                  onChange={(event) => setForm({ ...form, dry_run_only: event.target.checked })}
                />
                dry_run_only
              </label>
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading}>{loading ? "检查中..." : "运行 Dry Run"}</Button>
              </div>
            </form>

            {result ? (
              <div className="mt-5 grid gap-4 lg:grid-cols-2">
                <InfoRow label="dry_run_id" value={result.dry_run_id} />
                <InfoRow label="status" value={result.status} />
                <InfoRow label="allowed_to_continue" value={String(result.allowed_to_continue)} />
                <InfoRow label="audit_log_id" value={result.audit_log_id} />
                <InfoRow label="dry_run_only" value={String(result.dry_run_only)} />
                <InfoRow label="created_at" value={result.created_at} />
                <div className="lg:col-span-2">
                  <JsonPanel title="guard_results" value={result.guard_results} />
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

function JsonPanel({ title, value }: { title: string; value: unknown }) {
  return (
    <div>
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
