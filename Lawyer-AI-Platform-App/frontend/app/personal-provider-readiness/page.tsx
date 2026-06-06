"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DarkSafetyBadge,
  DiagnosticsPanel,
  InfoRows,
  Panel,
  RuntimeCard,
  SafeErrorNotice,
  StatusCard,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  createPersonalProviderReadinessLiveGateMock,
  getPersonalProviderReadinessAudit,
  getPersonalProviderReadinessHealthDryRun,
  getPersonalProviderReadinessLiveGate,
  getPersonalProviderReadinessSafety,
  getPersonalProviderReadinessSecretBoundary,
  getPersonalProviderReadinessStatus,
  getPersonalProviderReadinessUsagePolicy,
  listPersonalProviderReadinessCategories,
  listPersonalProviderReadinessLiveGates,
  listPersonalProviderReadinessProviders
} from "@/services/api";
import type { CategorySummary, ProviderMetadata } from "@/types";

const categoryLabels: Record<string, string> = {
  ai: "AI Provider",
  ocr: "OCR Provider",
  document: "Document Provider",
  legal: "Legal Search Provider",
  enterprise: "Enterprise Provider"
};

export default function PersonalProviderReadinessPage() {
  const [data, setData] = useState<Record<string, any>>({});
  const [selectedProviderId, setSelectedProviderId] = useState("openai");
  const [error, setError] = useState("");

  const providers = (data.providers?.providers ?? []) as ProviderMetadata[];
  const categories = (data.categories?.categories ?? []) as CategorySummary[];
  const selectedProvider = useMemo(
    () => providers.find((provider) => provider.provider_id === selectedProviderId) ?? providers[0],
    [providers, selectedProviderId]
  );
  const providerId = selectedProvider?.provider_id ?? selectedProviderId;

  async function loadReadiness(nextProviderId = selectedProviderId) {
    setError("");
    try {
      const [status, providersResponse, categoriesResponse, liveGates, audit, safety] = await Promise.all([
        getPersonalProviderReadinessStatus(),
        listPersonalProviderReadinessProviders(),
        listPersonalProviderReadinessCategories(),
        listPersonalProviderReadinessLiveGates(),
        getPersonalProviderReadinessAudit(),
        getPersonalProviderReadinessSafety()
      ]);
      const firstProviderId = nextProviderId || providersResponse.providers?.[0]?.provider_id || "openai";
      const [secretBoundary, liveGate, usagePolicy, healthDryRun] = await Promise.all([
        getPersonalProviderReadinessSecretBoundary(firstProviderId),
        getPersonalProviderReadinessLiveGate(firstProviderId),
        getPersonalProviderReadinessUsagePolicy(firstProviderId),
        getPersonalProviderReadinessHealthDryRun(firstProviderId)
      ]);
      setSelectedProviderId(firstProviderId);
      setData({ status, providers: providersResponse, categories: categoriesResponse, liveGates, audit, safety, secretBoundary, liveGate, usagePolicy, healthDryRun });
    } catch {
      setError("真实接口接入准备 API 暂不可用。页面保持安全 fallback，不读取密钥值，不调用真实 provider，不上传案件材料。");
    }
  }

  useEffect(() => {
    void loadReadiness();
  }, []);

  async function mockLiveGateCheck() {
    await createPersonalProviderReadinessLiveGateMock({
      provider_id: providerId,
      explicit_live_confirmation: false,
      owner_authorized: false,
      external_transfer_acknowledged: false,
      no_training_use_acknowledged: true,
      audit_acknowledged: true
    });
    await loadReadiness(providerId);
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}

        <section className="rounded-md border border-slate-800 bg-[#101820] p-8 text-white shadow-sm">
          <div className="text-sm font-medium text-cyan-200">v7.26 Provider Live Readiness & Secret Boundary</div>
          <h1 className="mt-3 text-4xl font-semibold">真实接口接入准备</h1>
          <p className="mt-4 max-w-4xl text-sm leading-6 text-slate-300">
            真实 OCR / AI / 法律 / 企业接口接入前检查。当前只显示配置与 gate metadata，不读取密钥值，不真实调用 provider，不上传案件材料。
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            {["只显示配置 metadata", "不读取密钥值", "不显示 masked key", "不真实调用 provider", "不上传案件材料", "live 默认关闭"].map((badge) => (
              <DarkSafetyBadge key={badge} label={badge} />
            ))}
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-3 xl:grid-cols-6">
          <StatusCard label="Provider Readiness" value={data.status?.provider_readiness_ready ?? true} detail="registry / gate / boundary" tone="safe" />
          <StatusCard label="Providers" value={data.status?.provider_count ?? data.providers?.provider_count ?? 13} detail="AI / OCR / Document / Legal / Enterprise" tone="info" />
          <StatusCard label="Key Loaded Count" value={data.status?.key_loaded_count ?? 0} detail="只显示 boolean count" tone="warning" />
          <StatusCard label="Live Default" value="disabled" detail="live_default_enabled=false" tone="safe" />
          <StatusCard label="Dry-run" value="true" detail="dry_run=true" tone="safe" />
          <StatusCard label="Live Calls" value="blocked" detail="live_call_executed=false" tone="safe" />
        </section>

        <Panel title="Provider Category Cards" eyebrow="分类总览">
          <div className="grid gap-4 md:grid-cols-5">
            {categories.map((category) => (
              <div key={category.category} className="rounded-md border border-line bg-stone-50 p-4">
                <div className="text-sm font-semibold text-ink">{categoryLabels[category.category] ?? category.category}</div>
                <div className="mt-4 grid gap-2 text-xs text-muted">
                  <span>provider count: {category.provider_count}</span>
                  <span>key loaded: {category.key_loaded_count}</span>
                  <span>dry-run ready: {category.dry_run_ready_count}</span>
                  <span>live disabled: {category.live_disabled_count}</span>
                  <span>blocked: {category.blocked_provider_count}</span>
                </div>
              </div>
            ))}
          </div>
        </Panel>

        <section className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
          <Panel title="Provider Registry Table" eyebrow="统一 provider registry">
            <div className="overflow-x-auto">
              <table className="min-w-full border-separate border-spacing-y-2 text-left text-sm">
                <thead className="text-xs text-muted">
                  <tr>
                    <th className="px-3 py-2">provider</th>
                    <th className="px-3 py-2">category</th>
                    <th className="px-3 py-2">live supported</th>
                    <th className="px-3 py-2">live default</th>
                    <th className="px-3 py-2">key loaded</th>
                    <th className="px-3 py-2">key exposed</th>
                    <th className="px-3 py-2">dry-run</th>
                    <th className="px-3 py-2">status</th>
                  </tr>
                </thead>
                <tbody>
                  {providers.map((provider) => (
                    <tr
                      key={provider.provider_id}
                      className={`cursor-pointer rounded-md ${providerId === provider.provider_id ? "bg-cyan-50" : "bg-white"}`}
                      onClick={() => void loadReadiness(provider.provider_id)}
                    >
                      <td className="rounded-l-md border-y border-l border-line px-3 py-3 font-medium text-ink">{provider.provider_name}</td>
                      <td className="border-y border-line px-3 py-3 text-muted">{provider.provider_category}</td>
                      <td className="border-y border-line px-3 py-3">{String(provider.live_supported)}</td>
                      <td className="border-y border-line px-3 py-3">{String(provider.live_default_enabled)}</td>
                      <td className="border-y border-line px-3 py-3">{String(provider.key_loaded)}</td>
                      <td className="border-y border-line px-3 py-3">{String(provider.key_value_exposed)}</td>
                      <td className="border-y border-line px-3 py-3">{String(provider.dry_run_supported)}</td>
                      <td className="rounded-r-md border-y border-r border-line px-3 py-3 text-xs text-muted">{provider.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Panel>

          <Panel title="Selected Provider" eyebrow="当前 provider">
            <InfoRows
              rows={[
                ["provider_id", selectedProvider?.provider_id],
                ["provider_name", selectedProvider?.provider_name],
                ["provider_category", selectedProvider?.provider_category],
                ["requires_api_key", selectedProvider?.requires_api_key],
                ["key_env_names", selectedProvider?.key_env_names?.join(" / ") || "not_required"],
                ["key_loaded", selectedProvider?.key_loaded],
                ["key_source", selectedProvider?.key_source],
                ["external_transfer_required", selectedProvider?.external_transfer_required],
                ["audit_required", selectedProvider?.audit_required]
              ]}
            />
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="Secret Boundary Panel">
            <InfoRows
              rows={[
                ["只检查 key 是否加载", true],
                ["key_env_names", data.secretBoundary?.key_env_names?.join(" / ") || "not_required"],
                ["key_loaded", data.secretBoundary?.key_loaded],
                ["key_source", data.secretBoundary?.key_source],
                ["key_value_exposed", data.secretBoundary?.key_value_exposed ?? false],
                ["key_prefix_returned", data.secretBoundary?.key_prefix_returned ?? false],
                ["key_suffix_returned", data.secretBoundary?.key_suffix_returned ?? false],
                ["masked_key_returned", data.secretBoundary?.masked_key_returned ?? false],
                ["frontend_key_input_enabled", data.secretBoundary?.frontend_key_input_enabled ?? false]
              ]}
            />
            <div className="mt-4 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
              前端只显示环境变量名和 key_loaded boolean，不显示 key 值、前缀、后缀或 masked key。
            </div>
          </Panel>

          <Panel title="Live Gate Panel">
            <InfoRows
              rows={[
                ["global_live_enabled", data.liveGate?.global_live_enabled ?? false],
                ["provider_live_enabled", data.liveGate?.provider_live_enabled ?? false],
                ["dry_run", data.liveGate?.dry_run ?? true],
                ["explicit_live_confirmation", data.liveGate?.explicit_live_confirmation ?? false],
                ["owner_authorized", data.liveGate?.owner_authorized ?? false],
                ["external_transfer_acknowledged", data.liveGate?.external_transfer_acknowledged ?? false],
                ["live_call_allowed", data.liveGate?.live_call_allowed ?? false],
                ["live_call_executed", data.liveGate?.live_call_executed ?? false],
                ["live_blocked_reason", data.liveGate?.live_blocked_reason]
              ]}
            />
            <button type="button" onClick={() => void mockLiveGateCheck()} className="mt-4 rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white">
              运行 live gate dry-run metadata
            </button>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Usage / Cost Metadata Panel">
            <InfoRows
              rows={[
                ["usage_meter_enabled", data.usagePolicy?.usage_meter_enabled ?? false],
                ["estimated_token_count", data.usagePolicy?.estimated_token_count ?? 0],
                ["estimated_page_count", data.usagePolicy?.estimated_page_count ?? 0],
                ["estimated_document_count", data.usagePolicy?.estimated_document_count ?? 0],
                ["estimated_call_count", data.usagePolicy?.estimated_call_count ?? 1],
                ["estimated_cost_available", data.usagePolicy?.estimated_cost_available ?? false],
                ["actual_cost_recorded", data.usagePolicy?.actual_cost_recorded ?? false],
                ["billable_call_executed", data.usagePolicy?.billable_call_executed ?? false]
              ]}
            />
          </Panel>

          <Panel title="Dry-run Health Panel">
            <RuntimeCard
              title={selectedProvider?.provider_name ?? "Provider"}
              category={selectedProvider?.provider_category ?? "provider"}
              status={data.healthDryRun?.live_gate_status ?? "blocked_by_default"}
              items={[
                ["config_detected", data.healthDryRun?.config_detected ?? true],
                ["key_loaded", data.healthDryRun?.key_loaded ?? false],
                ["adapter_registered", data.healthDryRun?.adapter_registered ?? false],
                ["dry_run_ready", data.healthDryRun?.dry_run_ready ?? true],
                ["network_call_executed", data.healthDryRun?.network_call_executed ?? false],
                ["next_required_confirmation", data.healthDryRun?.next_required_confirmation]
              ]}
            />
          </Panel>

          <Panel title="Live Gates Summary">
            <InfoRows
              rows={[
                ["live_gate_count", data.liveGates?.live_gate_count ?? 0],
                ["all_live_calls_allowed", false],
                ["all_live_calls_executed", false],
                ["dry_run", true],
                ["provider_gated", true]
              ]}
            />
          </Panel>
        </section>

        <TrustSafetyPanel
          title="Provider Readiness Trust / Safety Panel"
          items={data.safety?.safety_items ?? []}
          note="v7.26 仅用于真实接口接入前准备：不读取密钥值、不真实调用 provider、不上传案件材料、不生成最终法律意见或正式报告。"
        />

        <DiagnosticsPanel data={data} />
      </div>
    </AppShell>
  );
}

