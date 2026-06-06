"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { DiagnosticsPanel, InfoRows, SafeErrorNotice, StatusCard, TrustSafetyPanel } from "@/components/personal-production/ProductionShowcaseUI";
import {
  LegalEnterpriseCategorySummaryList,
  LegalEnterpriseProviderList,
  LegalEnterpriseStatus,
  createPersonalEnterpriseLookupDryRun,
  createPersonalLegalSearchDryRun,
  getPersonalLegalEnterpriseAudit,
  getPersonalLegalEnterpriseHealthDryRun,
  getPersonalLegalEnterpriseLiveGate,
  getPersonalLegalEnterpriseReviewQueue,
  getPersonalLegalEnterpriseSafety,
  getPersonalLegalEnterpriseSecretBoundary,
  getPersonalLegalEnterpriseSourceTraces,
  getPersonalLegalEnterpriseStatus,
  getPersonalLegalEnterpriseUsagePolicy,
  listPersonalEnterpriseLookupRuns,
  listPersonalLegalEnterpriseCategories,
  listPersonalLegalEnterpriseLiveGates,
  listPersonalLegalEnterpriseProviders,
  listPersonalLegalSearchRuns
} from "@/services/api";

export default function PersonalLegalEnterprisePage() {
  const [status, setStatus] = useState<LegalEnterpriseStatus | null>(null);
  const [providers, setProviders] = useState<LegalEnterpriseProviderList | null>(null);
  const [categories, setCategories] = useState<LegalEnterpriseCategorySummaryList | null>(null);
  const [selectedProvider, setSelectedProvider] = useState("legal_search_placeholder");
  const [secret, setSecret] = useState<Record<string, any> | null>(null);
  const [gate, setGate] = useState<Record<string, any> | null>(null);
  const [usage, setUsage] = useState<Record<string, any> | null>(null);
  const [health, setHealth] = useState<Record<string, any> | null>(null);
  const [liveGates, setLiveGates] = useState<Record<string, any> | null>(null);
  const [legalRuns, setLegalRuns] = useState<Record<string, any> | null>(null);
  const [enterpriseRuns, setEnterpriseRuns] = useState<Record<string, any> | null>(null);
  const [reviewQueue, setReviewQueue] = useState<Record<string, any> | null>(null);
  const [sourceTraces, setSourceTraces] = useState<Record<string, any> | null>(null);
  const [audit, setAudit] = useState<Record<string, any> | null>(null);
  const [safety, setSafety] = useState<Record<string, any> | null>(null);
  const [lastResult, setLastResult] = useState<Record<string, any> | null>(null);
  const [error, setError] = useState("");

  async function load(providerId = selectedProvider) {
    setError("");
    try {
      const [nextStatus, nextProviders, nextCategories, nextSecret, nextGate, nextUsage, nextHealth, nextLiveGates, nextLegalRuns, nextEnterpriseRuns, nextQueue, nextTraces, nextAudit, nextSafety] =
        await Promise.all([
          getPersonalLegalEnterpriseStatus(),
          listPersonalLegalEnterpriseProviders(),
          listPersonalLegalEnterpriseCategories(),
          getPersonalLegalEnterpriseSecretBoundary(providerId),
          getPersonalLegalEnterpriseLiveGate(providerId),
          getPersonalLegalEnterpriseUsagePolicy(providerId),
          getPersonalLegalEnterpriseHealthDryRun(providerId),
          listPersonalLegalEnterpriseLiveGates(),
          listPersonalLegalSearchRuns(),
          listPersonalEnterpriseLookupRuns(),
          getPersonalLegalEnterpriseReviewQueue(),
          getPersonalLegalEnterpriseSourceTraces(),
          getPersonalLegalEnterpriseAudit(),
          getPersonalLegalEnterpriseSafety()
        ]);
      setStatus(nextStatus);
      setProviders(nextProviders);
      setCategories(nextCategories);
      setSecret(nextSecret);
      setGate(nextGate);
      setUsage(nextUsage);
      setHealth(nextHealth);
      setLiveGates(nextLiveGates);
      setLegalRuns(nextLegalRuns);
      setEnterpriseRuns(nextEnterpriseRuns);
      setReviewQueue(nextQueue);
      setSourceTraces(nextTraces);
      setAudit(nextAudit);
      setSafety(nextSafety);
    } catch {
      setError("法律与企业信息接口 API 暂不可用，请确认后端服务已启动。");
    }
  }

  useEffect(() => {
    void load();
  }, []);

  const legalProviders = useMemo(() => providers?.providers.filter((provider) => provider.provider_category === "legal") ?? [], [providers]);
  const enterpriseProviders = useMemo(() => providers?.providers.filter((provider) => provider.provider_category === "enterprise") ?? [], [providers]);

  async function legalDryRun() {
    const result = await createPersonalLegalSearchDryRun({
      provider_id: legalProviders[0]?.provider_id ?? "legal_search_placeholder",
      query_type: "claim_basis_search",
      query_text_metadata: "请求权基础检索 metadata",
      dry_run: true
    });
    setLastResult(result);
    await load(selectedProvider);
  }

  async function enterpriseDryRun() {
    const result = await createPersonalEnterpriseLookupDryRun({
      provider_id: enterpriseProviders[0]?.provider_id ?? "enterprise_registry_placeholder",
      lookup_type: "company_registry",
      company_query_metadata: "企业主体核验 metadata",
      dry_run: true
    });
    setLastResult(result);
    await load(selectedProvider);
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}

        <section className="rounded-md border border-slate-800 bg-[#101820] p-6 text-white">
          <div className="text-xs font-semibold uppercase tracking-wide text-cyan-200">{status?.version ?? "v7.29"} · legal / enterprise gateway</div>
          <h1 className="mt-3 text-3xl font-semibold md:text-5xl">法律与企业信息接口受控接入</h1>
          <p className="mt-4 max-w-3xl text-sm leading-7 text-slate-300">
            法律检索与企业信息接口接入前检查，只显示配置、gate、source trace 和 dry-run metadata。不读取密钥值，默认不真实调用 provider，检索与企业信息结果必须进入律师复核。
          </p>
          <div className="mt-6 grid gap-3 md:grid-cols-4">
            <StatusCard label="Legal Providers" value={status?.legal_provider_count ?? 0} detail="法律检索 provider" tone="info" />
            <StatusCard label="Enterprise Providers" value={status?.enterprise_provider_count ?? 0} detail="企业信息 provider" tone="info" />
            <StatusCard label="Live Calls" value={String(status?.live_call_executed ?? false)} detail="live_call_executed=false" tone="safe" />
            <StatusCard label="Final Opinion" value={String(status?.final_legal_opinion_generated ?? false)} detail="不生成最终法律意见" tone="safe" />
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-2">
          {(categories?.categories ?? []).map((category) => (
            <StatusCard key={category.category} label={category.category} value={category.provider_count} detail={`dry-run ready ${category.dry_run_ready_count}`} tone="safe" />
          ))}
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
          <Panel title="Provider Registry">
            <select
              value={selectedProvider}
              onChange={(event) => {
                setSelectedProvider(event.target.value);
                void load(event.target.value);
              }}
              className="mb-4 w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
            >
              {(providers?.providers ?? []).map((provider) => (
                <option key={provider.provider_id} value={provider.provider_id}>{provider.provider_name}</option>
              ))}
            </select>
            <div className="grid gap-3 md:grid-cols-2">
              {(providers?.providers ?? []).map((provider) => (
                <div key={provider.provider_id} className="rounded-md border border-line bg-white p-4">
                  <div className="text-sm font-semibold text-ink">{provider.provider_name}</div>
                  <div className="mt-1 text-xs text-muted">{provider.provider_category} · {provider.provider_subtype}</div>
                  <InfoRows rows={[
                    ["key_loaded", provider.key_loaded],
                    ["key_value_exposed", provider.key_value_exposed],
                    ["dry_run_supported", provider.dry_run_supported],
                    ["audit_required", provider.audit_required]
                  ]} />
                </div>
              ))}
            </div>
          </Panel>

          <Panel title="Secret / Gate / Health">
            <InfoRows rows={[
              ["key_loaded", secret?.key_loaded ?? false],
              ["key_value_exposed", secret?.key_value_exposed ?? false],
              ["masked_key_returned", secret?.masked_key_returned ?? false],
              ["global_live_enabled", gate?.global_live_enabled ?? false],
              ["provider_live_enabled", gate?.provider_live_enabled ?? false],
              ["network_call_executed", health?.network_call_executed ?? false],
              ["live_blocked_reason", gate?.live_blocked_reason ?? "global_live_disabled"]
            ]} />
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="Legal Search Dry-run">
            <button onClick={() => void legalDryRun()} className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white">生成法律检索 dry-run metadata</button>
            <InfoRows rows={[
              ["legal run count", legalRuns?.run_count ?? 0],
              ["final_citation_selected", lastResult?.final_citation_selected ?? false],
              ["review_required", lastResult?.review_required ?? true],
              ["source_trace_count", sourceTraces?.source_trace_count ?? 0]
            ]} />
          </Panel>
          <Panel title="Enterprise Lookup Dry-run">
            <button onClick={() => void enterpriseDryRun()} className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white">生成企业信息 dry-run metadata</button>
            <InfoRows rows={[
              ["enterprise run count", enterpriseRuns?.run_count ?? 0],
              ["final_fact_finding", lastResult?.final_fact_finding ?? false],
              ["verification_required", lastResult?.verification_required ?? true],
              ["review queue", reviewQueue?.item_count ?? 0]
            ]} />
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Usage / Cost">
            <InfoRows rows={[
              ["estimated_query_count", usage?.estimated_query_count ?? 1],
              ["estimated_result_count", usage?.estimated_result_count ?? 0],
              ["billable_call_executed", usage?.billable_call_executed ?? false],
              ["actual_cost_recorded", usage?.actual_cost_recorded ?? false]
            ]} />
          </Panel>
          <Panel title="Review / Source Trace">
            <InfoRows rows={[
              ["review_items", reviewQueue?.item_count ?? 0],
              ["pending_review", reviewQueue?.pending_review_count ?? 0],
              ["source_traces", sourceTraces?.source_trace_count ?? 0],
              ["live_gates", liveGates?.live_gate_count ?? 0]
            ]} />
          </Panel>
          <Panel title="Audit / Safety">
            <InfoRows rows={[
              ["audit_events", audit?.event_count ?? 0],
              ["safety_items", safety?.safety_item_count ?? 0],
              ["raw_provider_response_exposed", status?.raw_provider_response_exposed ?? false],
              ["external_delivery", status?.external_delivery_triggered ?? false]
            ]} />
          </Panel>
        </section>

        <TrustSafetyPanel items={safety?.safety_items ?? ["provider-gated", "live disabled by default", "律师复核必需", "来源可追踪"]} />
        <DiagnosticsPanel data={{ status, providers, categories, secret, gate, usage, health, legalRuns, enterpriseRuns, reviewQueue, sourceTraces, audit, safety }} />
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

