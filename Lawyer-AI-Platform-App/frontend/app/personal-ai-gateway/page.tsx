"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DiagnosticsPanel,
  SafeErrorNotice,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  PersonalAIAuditTimeline,
  PersonalAIGatewayStatus,
  PersonalAILiveAuditTimeline,
  PersonalAILiveGatewayStatus,
  PersonalAILiveProviderConfigList,
  PersonalAILiveRunList,
  PersonalAILiveRunRecord,
  PersonalAILiveSafetyStatus,
  PersonalAIMockRunResult,
  PersonalAIProviderList,
  PersonalAIPromptRenderPreviewResult,
  PersonalAIPromptTemplateList,
  PersonalAIRunList,
  PersonalAISafetyStatus,
  PersonalAITokenUsageSummary,
  createPersonalAILiveDryRun,
  createPersonalAILiveRun,
  createPersonalAIMockRun,
  getPersonalAIAudit,
  getPersonalAIGatewayStatus,
  getPersonalAILiveAudit,
  getPersonalAILiveProviders,
  getPersonalAILiveSafety,
  getPersonalAILiveStatus,
  getPersonalAIProviders,
  getPersonalAIPromptTemplates,
  getPersonalAISafety,
  getPersonalAITokenUsageSummary,
  listPersonalAILiveRuns,
  listPersonalAIRuns,
  renderPersonalAIPromptPreview
} from "@/services/api";

const defaultCaseId = "case_v55_approve_all";
const defaultVariables = JSON.stringify({ case_type: "civil", task: "fact summary" }, null, 2);

export default function PersonalAIGatewayPage() {
  const [status, setStatus] = useState<PersonalAIGatewayStatus | null>(null);
  const [providers, setProviders] = useState<PersonalAIProviderList | null>(null);
  const [templates, setTemplates] = useState<PersonalAIPromptTemplateList | null>(null);
  const [runs, setRuns] = useState<PersonalAIRunList | null>(null);
  const [audit, setAudit] = useState<PersonalAIAuditTimeline | null>(null);
  const [tokenUsage, setTokenUsage] = useState<PersonalAITokenUsageSummary | null>(null);
  const [safety, setSafety] = useState<PersonalAISafetyStatus | null>(null);
  const [liveStatus, setLiveStatus] = useState<PersonalAILiveGatewayStatus | null>(null);
  const [liveProviders, setLiveProviders] = useState<PersonalAILiveProviderConfigList | null>(null);
  const [liveRuns, setLiveRuns] = useState<PersonalAILiveRunList | null>(null);
  const [liveAudit, setLiveAudit] = useState<PersonalAILiveAuditTimeline | null>(null);
  const [liveSafety, setLiveSafety] = useState<PersonalAILiveSafetyStatus | null>(null);
  const [previewResult, setPreviewResult] = useState<PersonalAIPromptRenderPreviewResult | null>(null);
  const [mockRunResult, setMockRunResult] = useState<PersonalAIMockRunResult | null>(null);
  const [liveRunResult, setLiveRunResult] = useState<PersonalAILiveRunRecord | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState("fact_summary_draft");
  const [selectedProvider, setSelectedProvider] = useState("openai_provider");
  const [selectedLiveProvider, setSelectedLiveProvider] = useState("openai");
  const [selectedLiveModel, setSelectedLiveModel] = useState("gpt-4.1-mini");
  const [liveConfirmed, setLiveConfirmed] = useState(false);
  const [caseId, setCaseId] = useState(defaultCaseId);
  const [variablesText, setVariablesText] = useState(defaultVariables);
  const [previewConfirmed, setPreviewConfirmed] = useState(true);
  const [mockRunConfirmed, setMockRunConfirmed] = useState(true);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadGateway() {
    setLoading(true);
    setError("");
    try {
      const [
        nextStatus,
        nextProviders,
        nextTemplates,
        nextRuns,
        nextAudit,
        nextTokenUsage,
        nextSafety,
        nextLiveStatus,
        nextLiveProviders,
        nextLiveRuns,
        nextLiveAudit,
        nextLiveSafety
      ] =
        await Promise.all([
          getPersonalAIGatewayStatus(),
          getPersonalAIProviders(),
          getPersonalAIPromptTemplates(),
          listPersonalAIRuns(),
          getPersonalAIAudit(),
          getPersonalAITokenUsageSummary(),
          getPersonalAISafety(),
          getPersonalAILiveStatus(),
          getPersonalAILiveProviders(),
          listPersonalAILiveRuns(),
          getPersonalAILiveAudit(),
          getPersonalAILiveSafety()
        ]);
      setStatus(nextStatus);
      setProviders(nextProviders);
      setTemplates(nextTemplates);
      setRuns(nextRuns);
      setAudit(nextAudit);
      setTokenUsage(nextTokenUsage);
      setSafety(nextSafety);
      setLiveStatus(nextLiveStatus);
      setLiveProviders(nextLiveProviders);
      setLiveRuns(nextLiveRuns);
      setLiveAudit(nextLiveAudit);
      setLiveSafety(nextLiveSafety);
      setSelectedTemplate((current) => current || nextTemplates.templates[0]?.template_id || "fact_summary_draft");
      setSelectedProvider((current) => current || nextProviders.providers[0]?.provider_id || "openai_provider");
      setSelectedLiveProvider((current) => current || nextLiveProviders.providers[0]?.provider_id || "openai");
      setSelectedLiveModel((current) => current || nextLiveProviders.providers[0]?.model_options[0] || "gpt-4.1-mini");
    } catch {
      setError("AI Gateway API 暂不可用，请确认后端服务已启动。");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadGateway();
  }, []);

  const selectedTemplateRecord = useMemo(
    () => templates?.templates.find((template) => template.template_id === selectedTemplate) ?? null,
    [selectedTemplate, templates]
  );

  async function handlePreview() {
    setError("");
    setPreviewResult(null);
    try {
      const variables = parseVariables(variablesText);
      const result = await renderPersonalAIPromptPreview({
        template_id: selectedTemplate,
        case_id: caseId,
        variables,
        manual_review_confirmed: previewConfirmed,
        mock_data_only_confirmation: previewConfirmed,
        no_raw_content_confirmation: previewConfirmed
      });
      setPreviewResult(result);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Prompt preview failed.");
    }
  }

  async function handleMockRun() {
    setError("");
    setMockRunResult(null);
    try {
      const result = await createPersonalAIMockRun({
        provider_id: selectedProvider,
        template_id: selectedTemplate,
        case_id: caseId,
        manual_approval_confirmed: mockRunConfirmed,
        lawyer_review_required_confirmation: mockRunConfirmed,
        draft_only_confirmation: mockRunConfirmed,
        source_trace_required_confirmation: mockRunConfirmed,
        no_final_legal_opinion_confirmation: mockRunConfirmed,
        no_final_report_generation_confirmation: mockRunConfirmed
      });
      setMockRunResult(result);
      await loadGateway();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Mock AI run failed.");
    }
  }

  async function handleLiveDryRun() {
    setError("");
    setLiveRunResult(null);
    try {
      const result = await createPersonalAILiveDryRun(buildLivePayload(true));
      setLiveRunResult(result);
      await loadGateway();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "AI Live dry-run 未完成。");
    }
  }

  async function handleLiveRun() {
    setError("");
    setLiveRunResult(null);
    try {
      const result = await createPersonalAILiveRun(buildLivePayload(false));
      setLiveRunResult(result);
      await loadGateway();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "AI Live run 未完成。");
    }
  }

  function buildLivePayload(dryRun: boolean) {
    return {
      provider_id: selectedLiveProvider,
      model: selectedLiveModel,
      prompt_template_id: selectedTemplate,
      prompt_purpose: selectedTemplateRecord?.purpose ?? "fact_summary_draft",
      case_id: caseId,
      source_trace_ids: ["trace_ai_live_demo"],
      dry_run: dryRun,
      actor_id: "local_demo_lawyer",
      explicit_live_confirmation: liveConfirmed,
      lawyer_review_acknowledged: liveConfirmed,
      draft_only_acknowledged: liveConfirmed,
      no_final_opinion_acknowledged: liveConfirmed,
      no_final_report_acknowledged: liveConfirmed,
      no_external_delivery_acknowledged: liveConfirmed,
      raw_content_included: false,
      final_legal_opinion_requested: false,
      final_report_requested: false
    };
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}

        <section className="overflow-hidden rounded-md border border-slate-800 bg-[#0f172a] text-white shadow-sm">
          <div className="grid gap-6 p-6 md:grid-cols-[1.35fr_0.75fr] md:p-8">
            <div>
              <div className="inline-flex items-center rounded-md border border-teal-300/40 bg-teal-300/10 px-3 py-1 text-xs font-medium text-teal-100">
                {status?.version ?? "v7.1"} · mock-first provider gateway
              </div>
              <h1 className="mt-5 max-w-3xl text-3xl font-semibold leading-tight md:text-5xl">
                AIHome.law AI 网关与草稿 Runtime
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300">
                受控 prompt runtime 仅用于草稿流程验证。真实 provider 调用保持关闭，provider 密钥值不展示，输出始终保持草稿状态。
              </p>
              <div className="mt-5 flex flex-wrap gap-2">
                {["仅模拟结果", "受控草稿", "律师复核必需", "来源可追踪", "不生成最终法律意见"].map((badge) => (
                  <SafetyBadge key={badge} label={badge} />
                ))}
              </div>
            </div>
            <div className="rounded-md border border-slate-700 bg-white/5 p-5">
              <div className="text-xs uppercase tracking-wide text-teal-200">Gateway posture</div>
              <div className="mt-4 grid gap-3">
                <HeroMetric label="网关启用" value={status?.enabled ?? true} />
                <HeroMetric label="真实 provider 调用" value={status?.live_provider_call_enabled ?? false} invert />
                <HeroMetric label="外部交付" value={status?.external_delivery_enabled ?? false} invert />
                <HeroMetric label="最终法律意见" value={status?.final_legal_opinion_generated ?? false} invert />
              </div>
              <button
                type="button"
                onClick={() => void loadGateway()}
                disabled={loading}
                className="mt-5 w-full rounded-md bg-teal-300 px-3 py-2 text-sm font-semibold text-slate-950 disabled:opacity-60"
              >
                {loading ? "刷新中" : "刷新 AI 网关"}
              </button>
            </div>
          </div>
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
          <Panel title="Provider Cards / Provider 状态">
            <div className="grid gap-3 md:grid-cols-3">
              {(providers?.providers ?? []).map((provider) => (
                <div key={provider.provider_id} className="rounded-md border border-line bg-white p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <div className="text-sm font-semibold text-ink">{provider.label}</div>
                      <div className="mt-1 text-xs text-muted">{provider.provider_id}</div>
                    </div>
                    <StatusBadge tone="preview" label={provider.status} />
                  </div>
                  <div className="mt-4 grid gap-2 text-xs text-muted">
                    <span>configured: {String(provider.configured)}</span>
                    <span>live_enabled: {String(provider.live_enabled)}</span>
                    <span>api_key_visible: {String(provider.api_key_visible)}</span>
                    <span>target_route: {provider.target_route}</span>
                  </div>
                </div>
              ))}
            </div>
          </Panel>

          <Panel title="Prompt Template Registry / 草稿模板">
            <div className="grid gap-3 md:grid-cols-2">
              {(templates?.templates ?? []).map((template) => (
                <div key={template.template_id} className="rounded-md border border-line bg-white p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <div className="text-sm font-semibold text-ink">{template.template_id}</div>
                      <div className="mt-1 text-xs leading-5 text-muted">{template.purpose}</div>
                    </div>
                    <StatusBadge tone={template.enabled ? "safe" : "blocked"} label={template.enabled ? "enabled" : "disabled"} />
                  </div>
                  <div className="mt-3 grid gap-2 text-xs text-muted">
                    <span>draft_only: {String(template.draft_only)}</span>
                    <span>requires_lawyer_review: {String(template.requires_lawyer_review)}</span>
                    <span>source_trace_required: {String(template.source_trace_required)}</span>
                  </div>
                </div>
              ))}
            </div>
          </Panel>
        </section>

        <section className="rounded-md border border-slate-800 bg-white p-5 shadow-sm">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <div className="text-xs font-semibold uppercase tracking-wide text-muted">v7.12 AI Live Gateway</div>
              <h2 className="mt-2 text-lg font-semibold text-ink">AI Live Gateway 受控接入</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-muted">
                真实 AI 接口默认关闭。API Key 仅后端读取，前端不可见。Live Call 需要显式确认，输出类型仅为 AI 草稿 metadata，不是最终法律意见。
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              {["live provider disabled", "API Key 前端不可见", "Live Call 需要显式确认", "AI 草稿，不是最终法律意见", "律师复核必需", "来源追踪必需"].map((item) => (
                <span key={item} className="rounded-md border border-cyan-200 bg-cyan-50 px-3 py-1 text-xs font-semibold text-cyan-800">{item}</span>
              ))}
            </div>
          </div>

          <div className="mt-5 grid gap-4 md:grid-cols-4">
            <MetricCard label="live_mode_enabled" value={String(liveStatus?.live_mode_enabled ?? false)} />
            <MetricCard label="provider_count" value={String(liveStatus?.provider_count ?? 0)} />
            <MetricCard label="key_loaded_count" value={String(liveStatus?.key_loaded_count ?? 0)} />
            <MetricCard label="live_call_executed" value={String(liveStatus?.live_call_executed ?? false)} />
          </div>

          <div className="mt-6 grid gap-6 xl:grid-cols-[1fr_1fr]">
            <div>
              <h3 className="text-sm font-semibold text-ink">Provider Cards / 真实接口状态</h3>
              <div className="mt-3 grid gap-3 md:grid-cols-3">
                {(liveProviders?.providers ?? []).map((provider) => (
                  <div key={provider.provider_id} className="rounded-md border border-line bg-slate-50 p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <div className="text-sm font-semibold text-ink">{provider.display_name}</div>
                        <div className="mt-1 text-xs text-muted">{provider.provider_id}</div>
                      </div>
                      <StatusBadge tone={provider.live_enabled ? "safe" : "preview"} label={provider.live_enabled ? "gated" : "disabled"} />
                    </div>
                    <div className="mt-4 grid gap-2 text-xs text-muted">
                      <span>key_required: {String(provider.key_required)}</span>
                      <span>key_loaded: {String(provider.key_loaded)}</span>
                      <span>key_source: {provider.key_source}</span>
                      <span>api_key_exposed: {String(provider.api_key_exposed)}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-sm font-semibold text-ink">Dry-run / Gated Live Run</h3>
              <div className="mt-3 grid gap-3">
                <label className="grid gap-2 text-sm text-ink">
                  <span className="font-medium">Live Provider</span>
                  <select className="rounded-md border border-line bg-white px-3 py-2 text-sm" value={selectedLiveProvider} onChange={(event) => setSelectedLiveProvider(event.target.value)}>
                    {(liveProviders?.providers ?? []).map((provider) => <option key={provider.provider_id} value={provider.provider_id}>{provider.display_name}</option>)}
                  </select>
                </label>
                <label className="grid gap-2 text-sm text-ink">
                  <span className="font-medium">Model</span>
                  <input className="rounded-md border border-line bg-white px-3 py-2 text-sm" value={selectedLiveModel} onChange={(event) => setSelectedLiveModel(event.target.value)} />
                </label>
                <label className="flex items-start gap-3 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-sm text-cyan-900">
                  <input className="mt-1" type="checkbox" checked={liveConfirmed} onChange={(event) => setLiveConfirmed(event.target.checked)} />
                  <span>我确认：显式 live gate、律师复核必需、草稿状态、不生成最终法律意见、不生成最终报告、不自动对外交付。</span>
                </label>
                <div className="grid gap-2 md:grid-cols-2">
                  <button type="button" onClick={() => void handleLiveDryRun()} className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white">执行 dry-run</button>
                  <button type="button" onClick={() => void handleLiveRun()} className="rounded-md border border-line bg-white px-4 py-2 text-sm font-semibold text-ink">提交 gated live run</button>
                </div>
              </div>
            </div>
          </div>

          {liveRunResult ? (
            <ResultPanel title="AI Live Gateway Result">
              <ResultFlags
                flags={{
                  status: liveRunResult.status,
                  dry_run: liveRunResult.dry_run,
                  would_call_provider: liveRunResult.would_call_provider,
                  live_call_requested: liveRunResult.live_call_requested,
                  live_call_executed: liveRunResult.live_call_executed,
                  api_key_exposed: liveRunResult.api_key_exposed,
                  raw_content_included: liveRunResult.raw_content_included,
                  draft_only: liveRunResult.draft_only,
                  final_legal_opinion_generated: liveRunResult.final_legal_opinion_generated,
                  final_report_generated: liveRunResult.final_report_generated,
                  external_delivery_triggered: liveRunResult.external_delivery_triggered
                }}
              />
              {liveRunResult.blocked_reason ? <BlockedReasons reasons={[liveRunResult.blocked_reason]} /> : null}
              <div className="rounded-md border border-line bg-white p-4 text-sm leading-6 text-ink">
                {liveRunResult.draft_output_metadata?.ai_draft ?? "No draft metadata returned."}
              </div>
            </ResultPanel>
          ) : null}
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="Prompt Render Preview / 草稿预览">
            <GatewayForm
              providers={providers}
              templates={templates}
              selectedProvider={selectedProvider}
              selectedTemplate={selectedTemplate}
              caseId={caseId}
              variablesText={variablesText}
              confirmationLabel="仅模拟数据 · 不含原始内容 · 已确认人工复核"
              confirmed={previewConfirmed}
              showProvider={false}
              onProviderChange={setSelectedProvider}
              onTemplateChange={setSelectedTemplate}
              onCaseIdChange={setCaseId}
              onVariablesTextChange={setVariablesText}
              onConfirmedChange={setPreviewConfirmed}
              onSubmit={() => void handlePreview()}
              submitLabel="Render Preview"
            />
            {previewResult ? (
              <ResultPanel title="Rendered Preview">
                <div className="rounded-md border border-line bg-white p-4 text-sm leading-6 text-ink">
                  {previewResult.rendered_prompt_preview || "Preview blocked before rendering."}
                </div>
                <ResultFlags
                  flags={{
                    status: previewResult.status,
                    would_call_provider: previewResult.would_call_provider,
                    raw_content_included: previewResult.raw_content_included,
                    draft_only: previewResult.draft_only,
                    requires_lawyer_review: previewResult.requires_lawyer_review
                  }}
                />
                <BlockedReasons reasons={previewResult.blocked_reasons} />
              </ResultPanel>
            ) : null}
          </Panel>

          <Panel title="Mock AI Run / 模拟运行">
            <GatewayForm
              providers={providers}
              templates={templates}
              selectedProvider={selectedProvider}
              selectedTemplate={selectedTemplate}
              caseId={caseId}
              variablesText={variablesText}
              confirmationLabel="人工批准 · 草稿状态 · 律师复核 · 不生成最终报告"
              confirmed={mockRunConfirmed}
              showProvider
              onProviderChange={setSelectedProvider}
              onTemplateChange={setSelectedTemplate}
              onCaseIdChange={setCaseId}
              onVariablesTextChange={setVariablesText}
              onConfirmedChange={setMockRunConfirmed}
              onSubmit={() => void handleMockRun()}
              submitLabel="Create Mock Run"
            />
            {mockRunResult ? (
              <ResultPanel title="Run Result">
                <div className="rounded-md border border-line bg-white p-4">
                  <div className="text-sm font-semibold text-ink">{mockRunResult.draft_output?.title ?? mockRunResult.status}</div>
                  <div className="mt-2 text-sm leading-6 text-muted">
                    {mockRunResult.draft_output?.content ?? "Run blocked before creation."}
                  </div>
                </div>
                <ResultFlags
                  flags={{
                    status: mockRunResult.status,
                    would_call_provider: mockRunResult.would_call_provider,
                    live_call_executed: mockRunResult.live_call_executed,
                    raw_content_included: mockRunResult.raw_content_included,
                    final_legal_opinion_generated: mockRunResult.final_legal_opinion_generated,
                    final_report_generated: mockRunResult.final_report_generated
                  }}
                />
                <BlockedReasons reasons={mockRunResult.blocked_reasons} />
              </ResultPanel>
            ) : null}
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-[1fr_0.9fr_0.9fr]">
          <Panel title="Runs / 模拟运行记录">
            <div className="grid gap-3">
              {(runs?.runs ?? []).slice(0, 5).map((run) => (
                <MetadataRow key={run.ai_run_id} label={run.ai_run_id} value={`${run.provider_id} · ${run.template_id}`} />
              ))}
              {runs?.runs.length ? null : <EmptyState label="No mock runs yet" />}
            </div>
          </Panel>

          <Panel title="Audit Metadata / 审计 metadata">
            <div className="grid gap-3">
              {(audit?.events ?? []).slice(0, 5).map((event) => (
                <MetadataRow key={event.ai_run_id} label={event.ai_run_id} value={`${event.mode} · live_call_executed=${String(event.live_call_executed)}`} />
              ))}
              {audit?.events.length ? null : <EmptyState label="No audit events yet" />}
            </div>
          </Panel>

          <Panel title="Token Usage / 估算用量">
            <div className="grid gap-3">
              <MetricCard label="run_count" value={String(tokenUsage?.run_count ?? 0)} />
              <MetricCard label="estimated_total_tokens" value={String(tokenUsage?.estimated_total_tokens ?? 0)} />
              <MetricCard label="live_usage_available" value={String(tokenUsage?.live_usage_available ?? false)} />
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="Live Audit Timeline / 受控调用审计">
            <div className="grid gap-3">
              {(liveAudit?.events ?? []).slice(0, 5).map((event) => (
                <MetadataRow key={event.event_id} label={event.event_id} value={`${event.action} · live_call_executed=${String(event.live_call_executed)}`} />
              ))}
              {liveAudit?.events.length ? null : <EmptyState label="No live audit events yet" />}
            </div>
          </Panel>
          <Panel title="Live Run Metadata / 草稿输出记录">
            <div className="grid gap-3">
              {(liveRuns?.runs ?? []).slice(0, 5).map((run) => (
                <MetadataRow key={run.run_id} label={run.run_id} value={`${run.status} · ${run.provider_id} · draft_only=${String(run.draft_only)}`} />
              ))}
              {liveRuns?.runs.length ? null : <EmptyState label="No live gateway runs yet" />}
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
          <TrustSafetyPanel title="信任与安全面板" />

          <Panel title="开发诊断（默认折叠）">
            <DiagnosticsPanel
              data={{
                status,
                providers,
                templates,
                selected_template: selectedTemplateRecord,
                preview_result: previewResult,
                mock_run_result: mockRunResult,
                live_status: liveStatus,
                live_providers: liveProviders,
                live_run_result: liveRunResult,
                live_runs: liveRuns,
                live_audit: liveAudit,
                live_safety: liveSafety,
                runs,
                audit,
                token_usage: tokenUsage,
                safety
              }}
            />
          </Panel>
        </section>
      </div>
    </AppShell>
  );
}

function GatewayForm({
  providers,
  templates,
  selectedProvider,
  selectedTemplate,
  caseId,
  variablesText,
  confirmationLabel,
  confirmed,
  showProvider,
  onProviderChange,
  onTemplateChange,
  onCaseIdChange,
  onVariablesTextChange,
  onConfirmedChange,
  onSubmit,
  submitLabel
}: {
  providers: PersonalAIProviderList | null;
  templates: PersonalAIPromptTemplateList | null;
  selectedProvider: string;
  selectedTemplate: string;
  caseId: string;
  variablesText: string;
  confirmationLabel: string;
  confirmed: boolean;
  showProvider: boolean;
  onProviderChange: (value: string) => void;
  onTemplateChange: (value: string) => void;
  onCaseIdChange: (value: string) => void;
  onVariablesTextChange: (value: string) => void;
  onConfirmedChange: (value: boolean) => void;
  onSubmit: () => void;
  submitLabel: string;
}) {
  return (
    <div className="grid gap-4">
      {showProvider ? (
        <label className="grid gap-2 text-sm text-ink">
          <span className="font-medium">Provider</span>
          <select
            value={selectedProvider}
            onChange={(event) => onProviderChange(event.target.value)}
            className="rounded-md border border-line bg-white px-3 py-2 text-sm"
          >
            {(providers?.providers ?? []).map((provider) => (
              <option key={provider.provider_id} value={provider.provider_id}>
                {provider.label}
              </option>
            ))}
          </select>
        </label>
      ) : null}
      <label className="grid gap-2 text-sm text-ink">
        <span className="font-medium">Template</span>
        <select
          value={selectedTemplate}
          onChange={(event) => onTemplateChange(event.target.value)}
          className="rounded-md border border-line bg-white px-3 py-2 text-sm"
        >
          {(templates?.templates ?? []).map((template) => (
            <option key={template.template_id} value={template.template_id}>
              {template.template_id}
            </option>
          ))}
        </select>
      </label>
      <label className="grid gap-2 text-sm text-ink">
        <span className="font-medium">case_id</span>
        <input
          value={caseId}
          onChange={(event) => onCaseIdChange(event.target.value)}
          className="rounded-md border border-line bg-white px-3 py-2 text-sm"
        />
      </label>
      {!showProvider ? (
        <label className="grid gap-2 text-sm text-ink">
          <span className="font-medium">variables</span>
          <textarea
            value={variablesText}
            onChange={(event) => onVariablesTextChange(event.target.value)}
            rows={5}
            className="rounded-md border border-line bg-white px-3 py-2 font-mono text-xs leading-5"
          />
        </label>
      ) : null}
      <label className="flex items-center gap-2 rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
        <input type="checkbox" checked={confirmed} onChange={(event) => onConfirmedChange(event.target.checked)} />
        <span>{confirmationLabel}</span>
      </label>
      <button
        type="button"
        onClick={onSubmit}
        className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white"
      >
        {submitLabel}
      </button>
    </div>
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

function ResultPanel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mt-5 rounded-md border border-teal-200 bg-teal-50 p-4">
      <div className="text-sm font-semibold text-teal-950">{title}</div>
      <div className="mt-3 grid gap-3">{children}</div>
    </div>
  );
}

function ResultFlags({ flags }: { flags: Record<string, string | boolean> }) {
  return (
    <div className="grid gap-2 md:grid-cols-2">
      {Object.entries(flags).map(([key, value]) => (
        <MetadataRow key={key} label={key} value={String(value)} />
      ))}
    </div>
  );
}

function BlockedReasons({ reasons }: { reasons: string[] }) {
  if (!reasons.length) {
    return null;
  }
  return (
    <div className="rounded-md border border-amber-200 bg-amber-50 p-3 text-xs leading-5 text-amber-900">
      {reasons.join(" · ")}
    </div>
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

function MetadataRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-3 rounded-md border border-line bg-white px-3 py-2">
      <span className="truncate text-xs font-medium text-ink">{label}</span>
      <span className="text-right text-xs text-muted">{value}</span>
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4">
      <div className="text-xs uppercase tracking-wide text-muted">{label}</div>
      <div className="mt-2 text-2xl font-semibold text-ink">{value}</div>
    </div>
  );
}

function EmptyState({ label }: { label: string }) {
  return <div className="rounded-md border border-dashed border-line bg-white px-3 py-6 text-center text-sm text-muted">{label}</div>;
}

function parseVariables(text: string) {
  try {
    const parsed = JSON.parse(text);
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
  } catch {
    return {};
  }
}
