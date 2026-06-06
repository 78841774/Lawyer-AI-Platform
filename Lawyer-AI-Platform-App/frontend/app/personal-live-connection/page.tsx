"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DiagnosticsPanel,
  InfoRows,
  SafeErrorNotice,
  StatusCard,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  LiveConnectionAuditTimeline,
  LiveConnectionHealthDryRun,
  LiveConnectionLiveGate,
  LiveConnectionProviderList,
  LiveConnectionRunList,
  LiveConnectionRunRecord,
  LiveConnectionRuntimeList,
  LiveConnectionSafetyStatus,
  LiveConnectionSecretBoundary,
  LiveConnectionStatus,
  LiveConnectionUsagePolicy,
  createPersonalLiveConnectionDryRun,
  getPersonalLiveConnectionAudit,
  getPersonalLiveConnectionHealthDryRun,
  getPersonalLiveConnectionLiveGate,
  getPersonalLiveConnectionSafety,
  getPersonalLiveConnectionSecretBoundary,
  getPersonalLiveConnectionStatus,
  getPersonalLiveConnectionUsagePolicy,
  listPersonalLiveConnectionProviders,
  listPersonalLiveConnectionRuns,
  listPersonalLiveConnectionRuntimes
} from "@/services/api";

export default function PersonalLiveConnectionPage() {
  const [status, setStatus] = useState<LiveConnectionStatus | null>(null);
  const [runtimes, setRuntimes] = useState<LiveConnectionRuntimeList | null>(null);
  const [providers, setProviders] = useState<LiveConnectionProviderList | null>(null);
  const [secret, setSecret] = useState<LiveConnectionSecretBoundary | null>(null);
  const [gate, setGate] = useState<LiveConnectionLiveGate | null>(null);
  const [usage, setUsage] = useState<LiveConnectionUsagePolicy | null>(null);
  const [health, setHealth] = useState<LiveConnectionHealthDryRun | null>(null);
  const [runs, setRuns] = useState<LiveConnectionRunList | null>(null);
  const [audit, setAudit] = useState<LiveConnectionAuditTimeline | null>(null);
  const [safety, setSafety] = useState<LiveConnectionSafetyStatus | null>(null);
  const [selectedProvider, setSelectedProvider] = useState("openai");
  const [runResult, setRunResult] = useState<LiveConnectionRunRecord | null>(null);
  const [error, setError] = useState("");

  async function load(providerId = selectedProvider) {
    setError("");
    try {
      const [nextStatus, nextRuntimes, nextProviders, nextSecret, nextGate, nextUsage, nextHealth, nextRuns, nextAudit, nextSafety] =
        await Promise.all([
          getPersonalLiveConnectionStatus(),
          listPersonalLiveConnectionRuntimes(),
          listPersonalLiveConnectionProviders(),
          getPersonalLiveConnectionSecretBoundary(providerId),
          getPersonalLiveConnectionLiveGate(providerId),
          getPersonalLiveConnectionUsagePolicy(providerId),
          getPersonalLiveConnectionHealthDryRun(providerId),
          listPersonalLiveConnectionRuns(),
          getPersonalLiveConnectionAudit(),
          getPersonalLiveConnectionSafety()
        ]);
      setStatus(nextStatus);
      setRuntimes(nextRuntimes);
      setProviders(nextProviders);
      setSecret(nextSecret);
      setGate(nextGate);
      setUsage(nextUsage);
      setHealth(nextHealth);
      setRuns(nextRuns);
      setAudit(nextAudit);
      setSafety(nextSafety);
    } catch {
      setError("受控接口接入 API 暂不可用，请确认后端服务已启动。");
    }
  }

  useEffect(() => {
    void load();
  }, []);

  const grouped = useMemo(() => {
    const groups: Record<string, number> = {};
    (providers?.providers ?? []).forEach((provider) => {
      groups[provider.provider_category] = (groups[provider.provider_category] ?? 0) + 1;
    });
    return groups;
  }, [providers]);

  async function createDryRun() {
    setError("");
    try {
      const result = await createPersonalLiveConnectionDryRun({
        provider_id: selectedProvider,
        run_type: "controlled_provider_readiness",
        case_id: "case_v55_approve_all",
        material_id: "material_demo_001",
        query_purpose: "personal_live_connection_dashboard",
        dry_run: true,
        manual_confirmation: false,
        owner_confirmation: false,
        lawyer_gate_acknowledged: false,
        source_trace_acknowledged: true,
        raw_content_boundary_acknowledged: true,
        draft_only_acknowledged: true
      });
      setRunResult(result);
      await load(selectedProvider);
    } catch {
      setError("Dry-run metadata 创建失败。");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}

        <section className="rounded-md border border-slate-800 bg-[#111827] p-6 text-white shadow-sm">
          <div className="max-w-3xl">
            <div className="text-xs font-semibold uppercase tracking-wide text-cyan-200">{status?.version ?? "v7.28"} · provider-gated · dry-run</div>
            <h1 className="mt-3 text-3xl font-semibold md:text-5xl">个人生产受控接口接入</h1>
            <p className="mt-4 text-sm leading-7 text-slate-300">
              统一展示 AI / OCR / Document / Legal / Enterprise Provider 的 readiness、secret boundary、live gate、usage/cost、health、audit 与安全边界。默认 live 关闭，所有输出仅为 metadata 草稿，不生成最终法律意见、报告或真实文件。
            </p>
          </div>
          <div className="mt-6 grid gap-3 md:grid-cols-4">
            <StatusCard label="Providers" value={status?.provider_count ?? 0} detail="AI / OCR / Legal / Enterprise" tone="info" />
            <StatusCard label="Dry-run Ready" value={status?.dry_run_ready_count ?? 0} detail="不调用真实服务" tone="safe" />
            <StatusCard label="Live Disabled" value={status?.live_disabled_count ?? 0} detail="live 默认关闭" tone="safe" />
            <StatusCard label="Network Call" value={String(status?.network_call_executed ?? false)} detail="network_call_executed=false" tone="safe" />
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-5">
          {Object.entries(grouped).map(([category, count]) => (
            <StatusCard key={category} label={category} value={count} detail="provider category" tone="info" />
          ))}
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
          <Panel title="Provider Cards">
            <div className="mb-4">
              <select
                value={selectedProvider}
                onChange={(event) => {
                  setSelectedProvider(event.target.value);
                  void load(event.target.value);
                }}
                className="w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
              >
                {(providers?.providers ?? []).map((provider) => (
                  <option key={provider.provider_id} value={provider.provider_id}>
                    {provider.display_name}
                  </option>
                ))}
              </select>
            </div>
            <div className="grid gap-3 md:grid-cols-2">
              {(providers?.providers ?? []).map((provider) => (
                <div key={provider.provider_id} className="rounded-md border border-line bg-white p-4">
                  <div className="text-sm font-semibold text-ink">{provider.display_name}</div>
                  <div className="mt-1 text-xs text-muted">{provider.provider_category} · {provider.provider_type}</div>
                  <InfoRows
                    rows={[
                      ["key_loaded", String(provider.key_loaded)],
                      ["dry_run_ready", String(provider.dry_run_ready)],
                      ["live_allowed", String(provider.live_call_allowed)],
                      ["adapter", String(provider.adapter_registered)]
                    ]}
                  />
                </div>
              ))}
            </div>
          </Panel>

          <Panel title="Secret Boundary / Live Gate">
            <InfoRows
              rows={[
                ["key_loaded", String(secret?.key_loaded ?? false)],
                ["key_value_exposed", String(secret?.key_value_exposed ?? false)],
                ["masked_key_returned", String(secret?.masked_key_returned ?? false)],
                ["live_gate_status", gate?.live_gate_status ?? "blocked_by_default"],
                ["live_blocked_reason", gate?.live_blocked_reason ?? "global_live_disabled"],
                ["live_call_allowed", String(gate?.live_call_allowed ?? false)]
              ]}
            />
            <button onClick={() => void createDryRun()} className="mt-4 rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white">
              创建 dry-run metadata
            </button>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Usage / Cost Metadata">
            <InfoRows
              rows={[
                ["estimated_token_count", String(usage?.estimated_token_count ?? 0)],
                ["estimated_page_count", String(usage?.estimated_page_count ?? 0)],
                ["estimated_query_count", String(usage?.estimated_query_count ?? 0)],
                ["billable_call_executed", String(usage?.billable_call_executed ?? false)]
              ]}
            />
          </Panel>
          <Panel title="Health Check / Dry-run">
            <InfoRows
              rows={[
                ["dry_run_ready", String(health?.dry_run_ready ?? true)],
                ["network_call_executed", String(health?.network_call_executed ?? false)],
                ["upload_executed", String(health?.upload_executed ?? false)],
                ["health_status", health?.health_status ?? "dry_run_ready_live_blocked"]
              ]}
            />
          </Panel>
          <Panel title="Run Result / Audit">
            <InfoRows
              rows={[
                ["last_run_status", runResult?.status ?? runs?.runs[0]?.status ?? "no_run"],
                ["run_count", String(runs?.run_count ?? 0)],
                ["audit_event_count", String(audit?.event_count ?? 0)],
                ["quality_reference_only", String(runResult?.quality_reference_only ?? true)]
              ]}
            />
          </Panel>
        </section>

        <TrustSafetyPanel
          title="Trust / Safety"
          items={(safety?.safety_items ?? [
            "provider-gated",
            "live disabled by default",
            "metadata-only",
            "draft-only",
            "不自动对外交付"
          ])}
        />

        <DiagnosticsPanel
          title="Developer Diagnostics"
          data={{ status, runtimes, providers, secret, gate, usage, health, runs, audit, safety }}
        />
      </div>
    </AppShell>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="rounded-md border border-line bg-white p-5 shadow-sm">
      <h2 className="text-base font-semibold text-ink">{title}</h2>
      <div className="mt-4">{children}</div>
    </section>
  );
}
