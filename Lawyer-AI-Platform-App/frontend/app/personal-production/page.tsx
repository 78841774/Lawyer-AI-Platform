"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  PersonalProductionConsoleSummary,
  PersonalProductionMode,
  PersonalProductionProviderCapabilities,
  PersonalProductionReadiness,
  PersonalProductionRuntimeRegistry,
  PersonalProductionSafety,
  PersonalProductionShowcase,
  PersonalProductionStatus,
  getPersonalProductionConsoleSummary,
  getPersonalProductionMode,
  getPersonalProductionProviderCapabilities,
  getPersonalProductionReadiness,
  getPersonalProductionRuntimeRegistry,
  getPersonalProductionSafety,
  getPersonalProductionShowcase,
  getPersonalProductionStatus
} from "@/services/api";

const workflowSteps = [
  "Intake",
  "Materials",
  "OCR",
  "Fact Extraction",
  "法律检索与企业信息核验",
  "Draft Analysis",
  "Lawyer Review",
  "个人生产交付包",
  "个人生产试点与展示包"
];

const safetyMessages = [
  "AI 辅助草稿",
  "律师复核必需",
  "来源可追踪",
  "受控运行",
  "交付前锁定",
  "不自动对外发送"
];

export default function PersonalProductionPage() {
  const [status, setStatus] = useState<PersonalProductionStatus | null>(null);
  const [mode, setMode] = useState<PersonalProductionMode | null>(null);
  const [showcase, setShowcase] = useState<PersonalProductionShowcase | null>(null);
  const [runtimeRegistry, setRuntimeRegistry] = useState<PersonalProductionRuntimeRegistry | null>(null);
  const [providerCapabilities, setProviderCapabilities] = useState<PersonalProductionProviderCapabilities | null>(null);
  const [readiness, setReadiness] = useState<PersonalProductionReadiness | null>(null);
  const [safety, setSafety] = useState<PersonalProductionSafety | null>(null);
  const [consoleSummary, setConsoleSummary] = useState<PersonalProductionConsoleSummary | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadConsole() {
    setLoading(true);
    setError("");
    try {
      const [
        nextStatus,
        nextMode,
        nextShowcase,
        nextRuntimeRegistry,
        nextProviderCapabilities,
        nextReadiness,
        nextSafety,
        nextConsoleSummary
      ] = await Promise.all([
        getPersonalProductionStatus(),
        getPersonalProductionMode(),
        getPersonalProductionShowcase(),
        getPersonalProductionRuntimeRegistry(),
        getPersonalProductionProviderCapabilities(),
        getPersonalProductionReadiness(),
        getPersonalProductionSafety(),
        getPersonalProductionConsoleSummary()
      ]);
      setStatus(nextStatus);
      setMode(nextMode);
      setShowcase(nextShowcase);
      setRuntimeRegistry(nextRuntimeRegistry);
      setProviderCapabilities(nextProviderCapabilities);
      setReadiness(nextReadiness);
      setSafety(nextSafety);
      setConsoleSummary(nextConsoleSummary);
    } catch {
      setError("Personal Production API 暂不可用，请确认后端服务已启动。");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadConsole();
  }, []);

  const readinessCards = useMemo(
    () => [
      { label: "Case OS RC", value: Boolean(readiness?.readiness.case_os_release_candidate_ready) },
      { label: "Regression Suite", value: Boolean(readiness?.readiness.regression_suite_passed) },
      { label: "Hardening", value: Boolean(readiness?.readiness.hardening_layer_enabled) },
      { label: "Personal Production Mode", value: Boolean(readiness?.readiness.personal_production_mode_defined) },
      { label: "AI Gateway", value: Boolean(readiness?.readiness.ai_gateway_registered) },
      { label: "Material Runtime", value: Boolean(readiness?.readiness.material_runtime_gateway_registered) },
      { label: "PaddleOCR-ready", value: Boolean(readiness?.readiness.ocr_runtime_gateway_registered) },
      { label: "法律与企业信息网关", value: Boolean(readiness?.readiness.legal_intelligence_gateway_registered && readiness?.readiness.enterprise_intelligence_gateway_registered) },
      { label: "经验包与技能工作室", value: Boolean(readiness?.readiness.skill_studio_gateway_registered) },
      { label: "真实案件生产工作流", value: Boolean(readiness?.readiness.case_production_gateway_registered) },
      {
        label: "个人生产交付包",
        value: Boolean(
          readiness?.readiness.delivery_packet_gateway_registered &&
            readiness?.readiness.packet_item_gateway_registered &&
            readiness?.readiness.source_bundle_gateway_registered &&
            readiness?.readiness.export_readiness_gateway_registered &&
            readiness?.readiness.final_lock_gateway_registered
        )
      },
      {
        label: "个人生产试点与展示包",
        value: Boolean(
          readiness?.readiness.showcase_pack_gateway_registered &&
            readiness?.readiness.pilot_sample_gateway_registered &&
            readiness?.readiness.story_flow_gateway_registered &&
            readiness?.readiness.showcase_metrics_gateway_registered &&
            readiness?.readiness.trust_panel_gateway_registered
        )
      }
    ],
    [readiness]
  );

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <div className="rounded-md border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800">{error}</div> : null}

        <section className="overflow-hidden rounded-md border border-slate-800 bg-[#111827] text-white shadow-sm">
          <div className="grid gap-6 p-6 md:grid-cols-[1.4fr_0.8fr] md:p-8">
            <div>
              <div className="inline-flex items-center rounded-md border border-cyan-300/40 bg-cyan-300/10 px-3 py-1 text-xs font-medium text-cyan-100">
                {status?.version ?? "v7.0"} · Personal Production & Showcase
              </div>
              <h1 className="mt-5 max-w-3xl text-3xl font-semibold leading-tight md:text-5xl">
                {showcase?.headline ?? "AIHome.law Personal Production Console"}
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300">
                {showcase?.subheadline ?? "Controlled AI-assisted legal workflow for personal production validation."}
              </p>
              <div className="mt-5 flex flex-wrap gap-2">
                {(showcase?.trust_badges ?? ["AI-assisted draft", "Lawyer review required", "Source-traced", "Controlled runtime", "Manual final lock"]).map((badge) => (
                  <SafetyBadge key={badge} label={badge} />
                ))}
              </div>
            </div>
            <div className="rounded-md border border-slate-700 bg-white/5 p-5">
              <div className="text-xs uppercase tracking-wide text-cyan-200">Runtime posture</div>
              <div className="mt-4 grid gap-3">
                <HeroMetric label="Showcase ready" value={status?.showcase_ready ?? true} />
                <HeroMetric label="Real provider live" value={status?.real_provider_call_enabled ?? false} invert />
                <HeroMetric label="Team workspace" value={status?.team_workspace_enabled ?? false} invert />
                <HeroMetric label="External delivery" value={status?.external_client_delivery_ready ?? false} invert />
              </div>
              <button
                type="button"
                onClick={() => void loadConsole()}
                disabled={loading}
                className="mt-5 w-full rounded-md bg-cyan-300 px-3 py-2 text-sm font-semibold text-slate-950 disabled:opacity-60"
              >
                {loading ? "Refreshing" : "Refresh Console"}
              </button>
            </div>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-10">
          {readinessCards.map((card) => (
            <ReadinessCard key={card.label} label={card.label} ready={card.value} />
          ))}
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
          <Panel title="Runtime Capability Grid">
            <div className="grid gap-3 md:grid-cols-2">
              {(runtimeRegistry?.runtimes ?? []).map((runtime) => (
                <RuntimeCard key={runtime.runtime_id} runtime={runtime} />
              ))}
            </div>
          </Panel>

          <Panel title="Provider Capability Preview">
            <div className="grid gap-3">
              {(providerCapabilities?.providers ?? []).map((provider) => (
                <CapabilityCard key={provider.provider_id} provider={provider} />
              ))}
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-[1fr_0.9fr]">
          <Panel title="Controlled Workflow Stepper">
            <div className="grid gap-3 md:grid-cols-4">
              {workflowSteps.map((step, index) => (
                <div key={step} className="rounded-md border border-line bg-white p-4">
                  <div className="flex h-8 w-8 items-center justify-center rounded-md bg-slate-900 text-sm font-semibold text-white">
                    {index + 1}
                  </div>
                  <div className="mt-3 text-sm font-semibold text-ink">{step}</div>
                  <div className="mt-2 text-xs text-muted">Controlled · Review gated</div>
                </div>
              ))}
            </div>
          </Panel>

          <Panel title="Safety & Trust Panel">
            <div className="grid gap-2">
              {safetyMessages.map((message) => (
                <div key={message} className="flex items-center justify-between rounded-md border border-line bg-white px-3 py-2">
                  <span className="text-sm text-ink">{message}</span>
                  <StatusBadge tone="safe" label="enabled" />
                </div>
              ))}
            </div>
            <div className="mt-4 grid gap-2 text-xs text-muted">
              <span>personal_production_mode: {mode?.personal_production_mode ?? "controlled_ready"}</span>
              <span>manual_final_lock_required: {String(mode?.manual_final_lock_required ?? true)}</span>
              <span>next_action: {readiness?.next_action ?? "configure_ai_provider_gateway_in_v7_1"}</span>
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
          <Panel title="Next v7 Roadmap">
            <div className="grid gap-3">
              {(consoleSummary?.next_steps ?? [
                "v7.1 AI Provider Gateway & Prompt Runtime",
                "v7.2 Controlled Material Parsing & PaddleOCR Runtime",
                "v7.3 Legal & Enterprise Intelligence Gateway",
                "v7.4 Experience Package Skill Studio",
                "v7.5 Real Case Production Workflow"
              ]).map((step) => (
                <div key={step} className="rounded-md border border-line bg-white px-4 py-3 text-sm font-medium text-ink">
                  {step}
                  {step.includes("v7.5") ? <span className="ml-2 text-xs text-emerald-700">current stage</span> : null}
                </div>
              ))}
            </div>
          </Panel>

          <Panel title="Developer Diagnostics">
            <details className="rounded-md border border-line bg-slate-950 text-slate-100">
              <summary className="cursor-pointer px-4 py-3 text-sm font-medium text-slate-200">
                API metadata
              </summary>
              <pre className="max-h-96 overflow-auto border-t border-slate-800 p-4 text-xs leading-5">
                {JSON.stringify(
                  {
                    status,
                    mode,
                    showcase,
                    runtime_registry: runtimeRegistry,
                    provider_capabilities: providerCapabilities,
                    readiness,
                    safety,
                    console_summary: consoleSummary
                  },
                  null,
                  2
                )}
              </pre>
            </details>
          </Panel>
        </section>
      </div>
    </AppShell>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="rounded-md border border-line bg-paper p-5">
      <h2 className="text-base font-semibold text-ink">{title}</h2>
      <div className="mt-4">{children}</div>
    </section>
  );
}

function SafetyBadge({ label }: { label: string }) {
  return <span className="rounded-md border border-white/20 bg-white/10 px-3 py-1 text-xs text-slate-100">{label}</span>;
}

function StatusBadge({ label, tone }: { label: string; tone: "safe" | "blocked" | "preview" }) {
  const tones = {
    safe: "border-emerald-200 bg-emerald-50 text-emerald-800",
    blocked: "border-amber-200 bg-amber-50 text-amber-800",
    preview: "border-cyan-200 bg-cyan-50 text-cyan-800"
  };
  return <span className={`rounded-md border px-2 py-1 text-xs font-medium ${tones[tone]}`}>{label}</span>;
}

function HeroMetric({ label, value, invert = false }: { label: string; value: boolean; invert?: boolean }) {
  const positive = invert ? !value : value;
  return (
    <div className="flex items-center justify-between rounded-md border border-slate-700 bg-slate-950/40 px-3 py-2">
      <span className="text-sm text-slate-300">{label}</span>
      <StatusBadge tone={positive ? "safe" : "blocked"} label={String(value)} />
    </div>
  );
}

function ReadinessCard({ label, ready }: { label: string; ready: boolean }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 shadow-sm">
      <div className="text-xs uppercase tracking-wide text-muted">{label}</div>
      <div className="mt-3 flex items-center justify-between">
        <div className="text-xl font-semibold text-ink">{ready ? "Ready" : "Pending"}</div>
        <StatusBadge tone={ready ? "safe" : "preview"} label={ready ? "pass" : "preview"} />
      </div>
    </div>
  );
}

function RuntimeCard({ runtime }: { runtime: { label: string; category: string; status: string; live_enabled: boolean; controlled_available: boolean; production_ready: boolean; gateway_registered?: boolean; target_route?: string } }) {
  const gatewayRuntime = ["ai", "ocr", "material_parser", "legal_search", "enterprise_intelligence", "skill_studio", "case_production", "delivery_packet", "showcase_pack"].includes(runtime.category);
  return (
    <div className="rounded-md border border-line bg-white p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm font-semibold text-ink">{runtime.label}</div>
          <div className="mt-1 text-xs text-muted">{runtime.category}</div>
        </div>
        <StatusBadge tone={runtime.live_enabled ? "blocked" : "preview"} label={runtime.status} />
      </div>
      <div className="mt-4 grid gap-2 text-xs text-muted">
        <span>controlled_available: {String(runtime.controlled_available)}</span>
        <span>live_enabled: {String(runtime.live_enabled)}</span>
        <span>production_ready: {String(runtime.production_ready)}</span>
        {gatewayRuntime ? <span>gateway_registered: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {runtime.category === "ocr" ? <span>PaddleOCR-ready: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {runtime.category === "material_parser" ? <span>MinerU / Docling placeholder: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {runtime.category === "legal_search" ? <span>快查 365 LawSkills placeholder: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {runtime.category === "enterprise_intelligence" ? <span>天眼查 AI placeholder: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {runtime.category === "skill_studio" ? <span>Skill Studio draft-only: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {runtime.category === "case_production" ? <span>Case Production controlled: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {runtime.category === "delivery_packet" ? <span>Delivery Packet metadata-only: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {runtime.category === "showcase_pack" ? <span>Showcase Pack synthetic-only: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {gatewayRuntime ? <span>target_route: {runtime.target_route}</span> : null}
      </div>
    </div>
  );
}

function CapabilityCard({ provider }: { provider: { label: string; category: string; configured: boolean; live_enabled: boolean; api_key_visible: boolean; next_action: string; gateway_registered?: boolean; target_route?: string } }) {
  const gatewayProvider = ["ai_model", "ocr", "file_parser", "legal_search", "enterprise_intelligence", "skill_studio", "case_production"].includes(provider.category);
  return (
    <div className="rounded-md border border-line bg-white p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm font-semibold text-ink">{provider.label}</div>
          <div className="mt-1 text-xs text-muted">{provider.category}</div>
        </div>
        <StatusBadge tone="preview" label="placeholder" />
      </div>
      <div className="mt-3 grid gap-2 text-xs text-muted">
        <span>configured: {String(provider.configured)}</span>
        <span>live_enabled: {String(provider.live_enabled)}</span>
        <span>secrets_visible: {String(provider.api_key_visible)}</span>
        {gatewayProvider ? <span>gateway_registered: {String(Boolean(provider.gateway_registered))}</span> : null}
        {gatewayProvider ? <span>target_route: {provider.target_route}</span> : null}
        <span>next_action: {provider.next_action}</span>
      </div>
    </div>
  );
}
