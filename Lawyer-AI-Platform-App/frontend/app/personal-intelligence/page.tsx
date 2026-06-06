"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DiagnosticsPanel,
  SafeErrorNotice,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  PersonalEnterpriseQueryList,
  PersonalEnterpriseQueryResult,
  PersonalIntelligenceAuditTimeline,
  PersonalIntelligenceConfirmationActionResult,
  PersonalIntelligenceLiveAuditTimeline,
  PersonalIntelligenceLiveGatewayStatus,
  PersonalIntelligenceLiveProviderConfigList,
  PersonalIntelligenceLiveReviewActionResult,
  PersonalIntelligenceLiveReviewQueue,
  PersonalIntelligenceLiveRunList,
  PersonalIntelligenceLiveRunRecord,
  PersonalIntelligenceLiveSafetyStatus,
  PersonalIntelligenceLiveSourceTraceList,
  PersonalIntelligenceProviderList,
  PersonalIntelligenceSafetyStatus,
  PersonalIntelligenceSourceTraceList,
  PersonalIntelligenceStatus,
  PersonalLegalSearchList,
  PersonalLegalSearchResult,
  createPersonalIntelligenceEnterpriseLiveDryRun,
  createPersonalIntelligenceEnterpriseLiveRun,
  createPersonalIntelligenceLegalLiveDryRun,
  createPersonalIntelligenceLegalLiveRun,
  createPersonalEnterpriseQueryMock,
  createPersonalLegalSearchMock,
  getPersonalIntelligenceAudit,
  getPersonalIntelligenceConfirmationQueue,
  getPersonalIntelligenceLiveAudit,
  getPersonalIntelligenceLiveProviders,
  getPersonalIntelligenceLiveReviewQueue,
  getPersonalIntelligenceLiveSafety,
  getPersonalIntelligenceLiveStatus,
  getPersonalIntelligenceProviders,
  getPersonalIntelligenceSafety,
  getPersonalIntelligenceStatus,
  listPersonalIntelligenceEnterpriseLiveRuns,
  listPersonalIntelligenceLegalLiveRuns,
  listPersonalIntelligenceLiveSourceTraces,
  listPersonalEnterpriseQuery,
  listPersonalIntelligenceSourceTraces,
  listPersonalLegalSearch,
  submitPersonalIntelligenceLiveReviewAction,
  submitPersonalIntelligenceConfirmationAction
} from "@/services/api";

const defaultCaseId = "case_v55_approve_all";
const legalScopes = ["regulation_search", "case_law_search", "judgment_rule_search", "article_detail_preview", "case_detail_preview"];
const enterpriseScopes = [
  "business_profile_preview",
  "shareholder_officer_preview",
  "operating_status_preview",
  "judicial_risk_preview",
  "enforcement_signal_preview"
];
const confirmationActions = [
  { id: "confirm", label: "确认" },
  { id: "reject", label: "驳回" },
  { id: "request_verification", label: "请求核验" },
  { id: "mark_low_confidence", label: "标记低置信度" },
  { id: "mark_not_relevant", label: "标记不相关" }
];
const liveReviewActions = [
  "approve_metadata_only",
  "request_manual_review",
  "reject",
  "mark_low_confidence",
  "mark_irrelevant",
  "request_source_verification",
  "block_raw_content",
  "block_ai_prompt_injection"
];

export default function PersonalIntelligencePage() {
  const [status, setStatus] = useState<PersonalIntelligenceStatus | null>(null);
  const [providers, setProviders] = useState<PersonalIntelligenceProviderList | null>(null);
  const [legalSearch, setLegalSearch] = useState<PersonalLegalSearchList | null>(null);
  const [enterpriseQuery, setEnterpriseQuery] = useState<PersonalEnterpriseQueryList | null>(null);
  const [sourceTraces, setSourceTraces] = useState<PersonalIntelligenceSourceTraceList | null>(null);
  const [confirmationQueue, setConfirmationQueue] = useState<PersonalIntelligenceSourceTraceList | null>(null);
  const [audit, setAudit] = useState<PersonalIntelligenceAuditTimeline | null>(null);
  const [safety, setSafety] = useState<PersonalIntelligenceSafetyStatus | null>(null);
  const [liveStatus, setLiveStatus] = useState<PersonalIntelligenceLiveGatewayStatus | null>(null);
  const [liveProviders, setLiveProviders] = useState<PersonalIntelligenceLiveProviderConfigList | null>(null);
  const [legalLiveRuns, setLegalLiveRuns] = useState<PersonalIntelligenceLiveRunList | null>(null);
  const [enterpriseLiveRuns, setEnterpriseLiveRuns] = useState<PersonalIntelligenceLiveRunList | null>(null);
  const [liveReviewQueue, setLiveReviewQueue] = useState<PersonalIntelligenceLiveReviewQueue | null>(null);
  const [liveSourceTraces, setLiveSourceTraces] = useState<PersonalIntelligenceLiveSourceTraceList | null>(null);
  const [liveAudit, setLiveAudit] = useState<PersonalIntelligenceLiveAuditTimeline | null>(null);
  const [liveSafety, setLiveSafety] = useState<PersonalIntelligenceLiveSafetyStatus | null>(null);
  const [legalResult, setLegalResult] = useState<PersonalLegalSearchResult | null>(null);
  const [enterpriseResult, setEnterpriseResult] = useState<PersonalEnterpriseQueryResult | null>(null);
  const [confirmationResult, setConfirmationResult] = useState<PersonalIntelligenceConfirmationActionResult | null>(null);
  const [legalLiveResult, setLegalLiveResult] = useState<PersonalIntelligenceLiveRunRecord | null>(null);
  const [enterpriseLiveResult, setEnterpriseLiveResult] = useState<PersonalIntelligenceLiveRunRecord | null>(null);
  const [liveReviewResult, setLiveReviewResult] = useState<PersonalIntelligenceLiveReviewActionResult | null>(null);
  const [caseId, setCaseId] = useState(defaultCaseId);
  const [legalQuery, setLegalQuery] = useState("买卖合同逾期付款责任");
  const [legalArea, setLegalArea] = useState("合同纠纷");
  const [jurisdiction, setJurisdiction] = useState("中国大陆");
  const [legalProvider, setLegalProvider] = useState("kuaicha365_lawskills_provider");
  const [legalScope, setLegalScope] = useState("case_law_search");
  const [companyName, setCompanyName] = useState("示例科技有限公司");
  const [creditCode, setCreditCode] = useState("");
  const [enterpriseProvider, setEnterpriseProvider] = useState("tianyancha_ai_provider");
  const [enterpriseScope, setEnterpriseScope] = useState("judicial_risk_preview");
  const [selectedTraceId, setSelectedTraceId] = useState("");
  const [selectedAction, setSelectedAction] = useState("confirm");
  const [liveLegalProvider, setLiveLegalProvider] = useState("kuaicha365_lawskills_provider");
  const [liveEnterpriseProvider, setLiveEnterpriseProvider] = useState("tianyancha_ai_provider");
  const [selectedLiveReviewItemId, setSelectedLiveReviewItemId] = useState("");
  const [liveReviewAction, setLiveReviewAction] = useState("approve_metadata_only");
  const [legalConfirmed, setLegalConfirmed] = useState(true);
  const [enterpriseConfirmed, setEnterpriseConfirmed] = useState(true);
  const [reviewConfirmed, setReviewConfirmed] = useState(true);
  const [liveConfirmed, setLiveConfirmed] = useState(false);
  const [liveReviewConfirmed, setLiveReviewConfirmed] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadGateway() {
    setLoading(true);
    setError("");
    try {
      const [
        nextStatus,
        nextProviders,
        nextLegal,
        nextEnterprise,
        nextTraces,
        nextQueue,
        nextAudit,
        nextSafety,
        nextLiveStatus,
        nextLiveProviders,
        nextLegalLiveRuns,
        nextEnterpriseLiveRuns,
        nextLiveQueue,
        nextLiveTraces,
        nextLiveAudit,
        nextLiveSafety
      ] =
        await Promise.all([
          getPersonalIntelligenceStatus(),
          getPersonalIntelligenceProviders(),
          listPersonalLegalSearch(),
          listPersonalEnterpriseQuery(),
          listPersonalIntelligenceSourceTraces(),
          getPersonalIntelligenceConfirmationQueue(),
          getPersonalIntelligenceAudit(),
          getPersonalIntelligenceSafety(),
          getPersonalIntelligenceLiveStatus(),
          getPersonalIntelligenceLiveProviders(),
          listPersonalIntelligenceLegalLiveRuns(),
          listPersonalIntelligenceEnterpriseLiveRuns(),
          getPersonalIntelligenceLiveReviewQueue(),
          listPersonalIntelligenceLiveSourceTraces(),
          getPersonalIntelligenceLiveAudit(),
          getPersonalIntelligenceLiveSafety()
        ]);
      setStatus(nextStatus);
      setProviders(nextProviders);
      setLegalSearch(nextLegal);
      setEnterpriseQuery(nextEnterprise);
      setSourceTraces(nextTraces);
      setConfirmationQueue(nextQueue);
      setAudit(nextAudit);
      setSafety(nextSafety);
      setLiveStatus(nextLiveStatus);
      setLiveProviders(nextLiveProviders);
      setLegalLiveRuns(nextLegalLiveRuns);
      setEnterpriseLiveRuns(nextEnterpriseLiveRuns);
      setLiveReviewQueue(nextLiveQueue);
      setLiveSourceTraces(nextLiveTraces);
      setLiveAudit(nextLiveAudit);
      setLiveSafety(nextLiveSafety);
      setSelectedTraceId((current) => current || nextQueue.source_traces[0]?.source_trace_id || "");
      setLiveLegalProvider((current) => current || nextLiveProviders.providers.find((provider) => provider.provider_type === "legal_search")?.provider_id || "kuaicha365_lawskills_provider");
      setLiveEnterpriseProvider((current) => current || nextLiveProviders.providers.find((provider) => provider.provider_type === "enterprise_info")?.provider_id || "tianyancha_ai_provider");
      setSelectedLiveReviewItemId((current) => current || nextLiveQueue.items[0]?.review_item_id || "");
    } catch {
      setError("法律与企业信息网关 API 暂不可用，请确认后端服务已启动。");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadGateway();
  }, []);

  const legalProviders = useMemo(
    () => providers?.providers.filter((provider) => provider.category === "legal_search") ?? [],
    [providers]
  );
  const enterpriseProviders = useMemo(
    () => providers?.providers.filter((provider) => provider.category === "enterprise_intelligence") ?? [],
    [providers]
  );
  const liveLegalProviders = useMemo(
    () => liveProviders?.providers.filter((provider) => provider.provider_type === "legal_search") ?? [],
    [liveProviders]
  );
  const liveEnterpriseProviders = useMemo(
    () => liveProviders?.providers.filter((provider) => provider.provider_type === "enterprise_info") ?? [],
    [liveProviders]
  );
  const activeTraceId = selectedTraceId || confirmationQueue?.source_traces[0]?.source_trace_id || "";
  const activeLiveReviewItemId = selectedLiveReviewItemId || liveReviewQueue?.items[0]?.review_item_id || "";

  async function handleLegalSearch() {
    setError("");
    setLegalResult(null);
    try {
      const result = await createPersonalLegalSearchMock({
        case_id: caseId,
        query: legalQuery,
        search_scope: legalScope,
        jurisdiction,
        legal_area: legalArea,
        provider_id: legalProvider,
        explicit_mock_confirmation: legalConfirmed,
        explicit_no_live_call_confirmation: legalConfirmed,
        explicit_no_final_opinion_confirmation: legalConfirmed
      });
      setLegalResult(result);
      setSelectedTraceId(result.source_trace_ids[0] || "");
      await loadGateway();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "模拟法律检索未完成。");
    }
  }

  async function handleEnterpriseQuery() {
    setError("");
    setEnterpriseResult(null);
    try {
      const result = await createPersonalEnterpriseQueryMock({
        case_id: caseId,
        company_name: companyName,
        unified_social_credit_code: creditCode || null,
        query_scope: enterpriseScope,
        provider_id: enterpriseProvider,
        explicit_mock_confirmation: enterpriseConfirmed,
        explicit_no_live_call_confirmation: enterpriseConfirmed,
        explicit_no_final_opinion_confirmation: enterpriseConfirmed
      });
      setEnterpriseResult(result);
      setSelectedTraceId(result.source_trace_ids[0] || "");
      await loadGateway();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "模拟企业查询未完成。");
    }
  }

  async function handleConfirmation() {
    setError("");
    setConfirmationResult(null);
    if (!activeTraceId) {
      setError("请先创建或选择 Source Trace。");
      return;
    }
    try {
      const result = await submitPersonalIntelligenceConfirmationAction(activeTraceId, {
        action: selectedAction,
        reviewer_id: "local_demo_lawyer",
        reviewer_note: "仅确认 metadata 状态",
        explicit_lawyer_confirmation: reviewConfirmed,
        explicit_no_final_opinion_confirmation: reviewConfirmed
      });
      setConfirmationResult(result);
      await loadGateway();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "律师确认动作未完成。");
    }
  }

  function buildLivePayload(providerId: string, queryText: string, queryType: string, dryRun: boolean) {
    return {
      provider_id: providerId,
      query_text: queryText,
      query_type: queryType,
      case_id: caseId,
      jurisdiction,
      actor_id: "local_demo_lawyer",
      dry_run: dryRun,
      explicit_live_confirmation: liveConfirmed,
      query_owner_confirmation: liveConfirmed,
      raw_content_handling_acknowledged: liveConfirmed,
      no_ai_prompt_injection_acknowledged: liveConfirmed,
      lawyer_review_acknowledged: liveConfirmed,
      draft_only_acknowledged: liveConfirmed,
      no_final_citation_acknowledged: liveConfirmed
    };
  }

  async function handleLegalLiveDryRun() {
    setError("");
    setLegalLiveResult(null);
    try {
      const result = await createPersonalIntelligenceLegalLiveDryRun(buildLivePayload(liveLegalProvider, legalQuery, legalScope, true));
      setLegalLiveResult(result);
      await loadGateway();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Legal live dry-run 未完成。");
    }
  }

  async function handleLegalLiveRun() {
    setError("");
    setLegalLiveResult(null);
    try {
      const result = await createPersonalIntelligenceLegalLiveRun(buildLivePayload(liveLegalProvider, legalQuery, legalScope, false));
      setLegalLiveResult(result);
      await loadGateway();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Legal live run 未完成。");
    }
  }

  async function handleEnterpriseLiveDryRun() {
    setError("");
    setEnterpriseLiveResult(null);
    try {
      const result = await createPersonalIntelligenceEnterpriseLiveDryRun(buildLivePayload(liveEnterpriseProvider, companyName, enterpriseScope, true));
      setEnterpriseLiveResult(result);
      await loadGateway();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Enterprise live dry-run 未完成。");
    }
  }

  async function handleEnterpriseLiveRun() {
    setError("");
    setEnterpriseLiveResult(null);
    try {
      const result = await createPersonalIntelligenceEnterpriseLiveRun(buildLivePayload(liveEnterpriseProvider, companyName, enterpriseScope, false));
      setEnterpriseLiveResult(result);
      await loadGateway();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Enterprise live run 未完成。");
    }
  }

  async function handleLiveReviewAction() {
    setError("");
    setLiveReviewResult(null);
    if (!activeLiveReviewItemId) {
      setError("请先创建 legal / enterprise dry-run metadata，再进行 live review action。");
      return;
    }
    try {
      const result = await submitPersonalIntelligenceLiveReviewAction(activeLiveReviewItemId, {
        action: liveReviewAction,
        actor_id: "local_demo_lawyer",
        explicit_review_confirmation: liveReviewConfirmed,
        raw_content_handling_acknowledged: liveReviewConfirmed,
        no_ai_prompt_injection_acknowledged: liveReviewConfirmed,
        no_final_citation_acknowledged: liveReviewConfirmed
      });
      setLiveReviewResult(result);
      await loadGateway();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Live review action 未完成。");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}

        <section className="overflow-hidden rounded-md border border-slate-800 bg-[#18231f] text-white shadow-sm">
          <div className="grid gap-6 p-6 md:grid-cols-[1.35fr_0.75fr] md:p-8">
            <div>
              <div className="inline-flex items-center rounded-md border border-emerald-300/40 bg-emerald-300/10 px-3 py-1 text-xs font-medium text-emerald-100">
                {status?.version ?? "v7.3"} · 受控运行
              </div>
              <h1 className="mt-5 max-w-3xl text-3xl font-semibold leading-tight md:text-5xl">法律与企业信息网关</h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300">
                受控检索、来源追踪、律师确认后使用。当前仅返回模拟 metadata，未调用真实法律或企业信息服务。
              </p>
              <div className="mt-5 flex flex-wrap gap-2">
                {["仅模拟结果", "Provider gated", "律师确认必需", "不生成最终法律意见"].map((badge) => (
                  <SafetyBadge key={badge} label={badge} />
                ))}
              </div>
            </div>
            <div className="rounded-md border border-slate-700 bg-white/5 p-5">
              <div className="text-xs uppercase tracking-wide text-emerald-200">Runtime status</div>
              <div className="mt-4 grid gap-3">
                <HeroMetric label="网关状态" value={status?.enabled ?? true} />
                <HeroMetric label="法律检索" value={status?.legal_search_runtime_enabled ?? true} />
                <HeroMetric label="企业信息" value={status?.enterprise_intelligence_runtime_enabled ?? true} />
                <HeroMetric label="真实服务调用" value={status?.live_provider_call_enabled ?? false} invert />
              </div>
              <button
                type="button"
                onClick={() => void loadGateway()}
                disabled={loading}
                className="mt-5 w-full rounded-md bg-emerald-300 px-3 py-2 text-sm font-semibold text-slate-950 disabled:opacity-60"
              >
                {loading ? "刷新中" : "刷新网关"}
              </button>
            </div>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-5">
          <StatusCard label="网关状态" value={status?.enabled ?? true} />
          <StatusCard label="法律检索" value={status?.legal_search_runtime_enabled ?? true} />
          <StatusCard label="企业信息" value={status?.enterprise_intelligence_runtime_enabled ?? true} />
          <StatusCard label="来源追踪" value={status?.source_trace_enabled ?? true} />
          <StatusCard label="律师确认" value={status?.confirmation_queue_enabled ?? true} />
        </section>

        <Panel title="Provider Cards / Provider 状态">
          <div className="grid gap-3 md:grid-cols-5">
            {(providers?.providers ?? []).map((provider) => (
              <div key={provider.provider_id} className="rounded-md border border-line bg-white p-4">
                <div className="text-sm font-semibold text-ink">{provider.label}</div>
                <div className="mt-1 text-xs text-muted">{provider.provider_id}</div>
                <div className="mt-3 grid gap-1 text-xs text-muted">
                  <span>category: {provider.category}</span>
                  <span>live_enabled: {String(provider.live_enabled)}</span>
                  <span>api_key_visible: {String(provider.api_key_visible)}</span>
                  <span>provider_gated: {String(provider.provider_gated)}</span>
                </div>
              </div>
            ))}
          </div>
        </Panel>

        <Panel title="法律检索与企业信息 API 受控接入">
          <div className="grid gap-4">
            <div className="grid gap-3 md:grid-cols-4">
              <StatusTile label="Legal live mode" value={liveStatus?.legal_live_mode_enabled ?? false} invert />
              <StatusTile label="Enterprise live mode" value={liveStatus?.enterprise_live_mode_enabled ?? false} invert />
              <StatusTile label="API Key 前端可见" value={liveProviders?.api_key_exposed ?? false} invert />
              <StatusTile label="Citation finalized" value={liveStatus?.citation_finalized ?? false} invert />
            </div>
            <div className="rounded-md border border-cyan-200 bg-cyan-50 p-4 text-sm leading-6 text-cyan-950">
              法律/企业 API 真实接口默认关闭。API Key 仅后端读取，前端不可见；法律检索原文和企业信息原文默认不展示。Citation 仅为候选 metadata，不自动进入 AI Prompt，不自动触发事实抽取或法律分析，不自动作为最终引用。律师复核与来源追踪保持必需。
            </div>
            <div className="grid gap-3 md:grid-cols-5">
              {(liveProviders?.providers ?? []).map((provider) => (
                <div key={provider.provider_id} className="rounded-md border border-line bg-white p-4">
                  <div className="text-sm font-semibold text-ink">{provider.display_name}</div>
                  <div className="mt-1 text-xs text-muted">{provider.provider_id}</div>
                  <div className="mt-3 grid gap-1 text-xs text-muted">
                    <span>provider_type: {provider.provider_type}</span>
                    <span>live_enabled: {String(provider.live_enabled)}</span>
                    <span>key_loaded: {String(provider.key_loaded)}</span>
                    <span>key_source: {provider.key_source}</span>
                    <span>citation_metadata: {String(provider.supports_citation_metadata)}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Panel>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="Legal search dry-run / 法律检索 dry-run">
            <div className="grid gap-4">
              <SelectField label="Live provider" value={liveLegalProvider} options={liveLegalProviders.map((provider) => provider.provider_id)} onChange={setLiveLegalProvider} />
              <SelectField label="query_type" value={legalScope} options={legalScopes} onChange={setLegalScope} />
              <TextField label="query_text" value={legalQuery} onChange={setLegalQuery} />
              <ActionButton label="生成法律检索 dry-run metadata" onClick={() => void handleLegalLiveDryRun()} />
              <ConfirmField label="Gated live confirmations · 不展示原文 · 不进入 AI Prompt · 不作为最终引用" checked={liveConfirmed} onChange={setLiveConfirmed} />
              <ActionButton label="尝试 gated legal live run" onClick={() => void handleLegalLiveRun()} />
            </div>
            {legalLiveResult ? (
              <ResultPanel title="Legal Live Result">
                <ResultFlags
                  flags={{
                    status: legalLiveResult.status,
                    dry_run: legalLiveResult.dry_run,
                    live_call_executed: legalLiveResult.live_call_executed,
                    legal_raw_content_exposed: legalLiveResult.legal_raw_content_exposed,
                    ai_prompt_injected: legalLiveResult.ai_prompt_injected,
                    citation_finalized: legalLiveResult.citation_finalized
                  }}
                />
                <MetadataRow label="query_text_redacted" value={legalLiveResult.metadata_preview.query_text_redacted} />
                <MetadataRow label="citation_candidate_count" value={String(legalLiveResult.metadata_preview.citation_candidate_count)} />
              </ResultPanel>
            ) : null}
          </Panel>

          <Panel title="Enterprise query dry-run / 企业信息 dry-run">
            <div className="grid gap-4">
              <SelectField label="Live provider" value={liveEnterpriseProvider} options={liveEnterpriseProviders.map((provider) => provider.provider_id)} onChange={setLiveEnterpriseProvider} />
              <SelectField label="query_type" value={enterpriseScope} options={enterpriseScopes} onChange={setEnterpriseScope} />
              <TextField label="company/query_text" value={companyName} onChange={setCompanyName} />
              <ActionButton label="生成企业信息 dry-run metadata" onClick={() => void handleEnterpriseLiveDryRun()} />
              <ConfirmField label="Gated live confirmations · 企业原文不展示 · 不进入 AI Prompt · 不生成最终报告" checked={liveConfirmed} onChange={setLiveConfirmed} />
              <ActionButton label="尝试 gated enterprise live run" onClick={() => void handleEnterpriseLiveRun()} />
            </div>
            {enterpriseLiveResult ? (
              <ResultPanel title="Enterprise Live Result">
                <ResultFlags
                  flags={{
                    status: enterpriseLiveResult.status,
                    dry_run: enterpriseLiveResult.dry_run,
                    live_call_executed: enterpriseLiveResult.live_call_executed,
                    enterprise_raw_content_exposed: enterpriseLiveResult.enterprise_raw_content_exposed,
                    ai_prompt_injected: enterpriseLiveResult.ai_prompt_injected,
                    final_report_generated: enterpriseLiveResult.final_report_generated
                  }}
                />
                <MetadataRow label="query_text_redacted" value={enterpriseLiveResult.metadata_preview.query_text_redacted} />
                <MetadataRow label="enterprise_candidate_count" value={String(enterpriseLiveResult.metadata_preview.enterprise_candidate_count)} />
              </ResultPanel>
            ) : null}
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Live Review Queue / Live 复核队列">
            <div className="grid gap-3">
              <SelectField
                label="review_item_id"
                value={activeLiveReviewItemId}
                options={(liveReviewQueue?.items ?? []).map((item) => item.review_item_id)}
                onChange={setSelectedLiveReviewItemId}
              />
              <SelectField label="action" value={liveReviewAction} options={liveReviewActions} onChange={setLiveReviewAction} />
              <ConfirmField label="人工复核确认 · 原始内容阻断 · 不进入 AI Prompt · 不最终引用" checked={liveReviewConfirmed} onChange={setLiveReviewConfirmed} />
              <ActionButton label="提交 live review action" onClick={() => void handleLiveReviewAction()} />
              {liveReviewResult ? (
                <ResultFlags flags={{ status: String(liveReviewResult.status), review_status: String(liveReviewResult.review_status) }} />
              ) : null}
            </div>
          </Panel>

          <Panel title="Live Source Trace / Live 来源追踪">
            <div className="grid gap-3">
              {(liveSourceTraces?.source_traces ?? []).slice(0, 6).map((trace) => (
                <MetadataRow key={trace.source_trace_id} label={trace.source_trace_id} value={`${String(trace.source_type)} · final=${String(trace.citation_finalized ?? false)}`} />
              ))}
              {liveSourceTraces?.source_traces.length ? null : <EmptyState label="No live source traces yet" />}
            </div>
          </Panel>

          <Panel title="Live Audit Timeline / Live 审计 metadata">
            <div className="grid gap-3">
              {(liveAudit?.events ?? []).slice(0, 6).map((event) => (
                <MetadataRow key={String(event.event_id)} label={String(event.action)} value={`${String(event.provider_id)} · live=${String(event.live_call_executed)}`} />
              ))}
              {liveAudit?.events.length ? null : <EmptyState label="No live audit events yet" />}
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="模拟法律检索">
            <div className="grid gap-4">
              <TextField label="查询词" value={legalQuery} onChange={setLegalQuery} />
              <TextField label="案由/领域" value={legalArea} onChange={setLegalArea} />
              <TextField label="地域/管辖" value={jurisdiction} onChange={setJurisdiction} />
              <SelectField label="search_scope" value={legalScope} options={legalScopes} onChange={setLegalScope} />
              <SelectField label="Provider" value={legalProvider} options={legalProviders.map((provider) => provider.provider_id)} onChange={setLegalProvider} />
              <ConfirmField label="确认仅运行模拟检索、未调用真实服务、不生成最终法律意见" checked={legalConfirmed} onChange={setLegalConfirmed} />
              <ActionButton label="运行模拟法律检索" onClick={() => void handleLegalSearch()} />
            </div>
            {legalResult ? (
              <ResultPanel title="模拟法律检索结果">
                <MetadataRow label="legal_search_id" value={legalResult.legal_search_id} />
                <MetadataRow label="query_summary" value={legalResult.query_summary} />
                <ResultFlags
                  flags={{
                    live_call_executed: legalResult.live_call_executed,
                    raw_external_content_included: legalResult.raw_external_content_included,
                    requires_lawyer_confirmation: legalResult.requires_lawyer_confirmation,
                    final_legal_opinion_generated: legalResult.final_legal_opinion_generated,
                    final_report_generated: legalResult.final_report_generated
                  }}
                />
              </ResultPanel>
            ) : null}
          </Panel>

          <Panel title="模拟企业查询">
            <div className="grid gap-4">
              <TextField label="企业名称" value={companyName} onChange={setCompanyName} />
              <TextField label="统一社会信用代码 optional" value={creditCode} onChange={setCreditCode} />
              <SelectField label="query_scope" value={enterpriseScope} options={enterpriseScopes} onChange={setEnterpriseScope} />
              <SelectField
                label="Provider"
                value={enterpriseProvider}
                options={enterpriseProviders.map((provider) => provider.provider_id)}
                onChange={setEnterpriseProvider}
              />
              <ConfirmField label="确认仅运行模拟查询、未调用真实服务、不生成最终法律意见" checked={enterpriseConfirmed} onChange={setEnterpriseConfirmed} />
              <ActionButton label="运行模拟企业查询" onClick={() => void handleEnterpriseQuery()} />
            </div>
            {enterpriseResult ? (
              <ResultPanel title="模拟企业查询结果">
                <MetadataRow label="enterprise_query_id" value={enterpriseResult.enterprise_query_id} />
                <MetadataRow label="company_match_summary" value={enterpriseResult.company_match_summary} />
                <MetadataRow label="risk_signal_summary" value={enterpriseResult.risk_signal_summary} />
                <ResultFlags
                  flags={{
                    live_call_executed: enterpriseResult.live_call_executed,
                    raw_external_content_included: enterpriseResult.raw_external_content_included,
                    requires_lawyer_confirmation: enterpriseResult.requires_lawyer_confirmation,
                    final_legal_opinion_generated: enterpriseResult.final_legal_opinion_generated,
                    final_report_generated: enterpriseResult.final_report_generated
                  }}
                />
              </ResultPanel>
            ) : null}
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
          <Panel title="Citation Candidates / Source Trace / 来源追踪候选">
            <div className="grid gap-3">
              {(sourceTraces?.source_traces ?? []).slice(0, 8).map((trace) => (
                <div key={trace.source_trace_id} className="rounded-md border border-line bg-white p-3 text-xs text-muted">
                  <div className="font-semibold text-ink">{trace.source_trace_id}</div>
                  <div className="mt-2 grid gap-1">
                    <span>source_type: {trace.source_type}</span>
                    <span>source_category: {trace.source_category}</span>
                    <span>citation_status: {trace.citation_status}</span>
                    <span>lawyer_confirmed: {String(trace.lawyer_confirmed)}</span>
                    <span>raw_content_returned: {String(trace.raw_content_returned)}</span>
                    <span>used_in_ai_prompt: {String(trace.used_in_ai_prompt)}</span>
                  </div>
                </div>
              ))}
              {sourceTraces?.source_traces.length ? null : <EmptyState label="暂无 Source Trace metadata" />}
            </div>
          </Panel>

          <Panel title="律师确认队列">
            <div className="grid gap-4">
              <SelectField
                label="source_trace_id"
                value={activeTraceId}
                options={(confirmationQueue?.source_traces ?? []).map((trace) => trace.source_trace_id)}
                onChange={setSelectedTraceId}
              />
              <SelectField label="action" value={selectedAction} options={confirmationActions.map((action) => action.id)} onChange={setSelectedAction} />
              <div className="flex flex-wrap gap-2">
                {confirmationActions.map((action) => (
                  <button
                    key={action.id}
                    type="button"
                    onClick={() => setSelectedAction(action.id)}
                    className={`rounded-md border px-3 py-2 text-xs font-medium ${
                      selectedAction === action.id ? "border-slate-900 bg-slate-900 text-white" : "border-line bg-white text-ink"
                    }`}
                  >
                    {action.label}
                  </button>
                ))}
              </div>
              <ConfirmField label="确认律师已复核，且不生成最终法律意见" checked={reviewConfirmed} onChange={setReviewConfirmed} />
              <ActionButton label="提交确认动作" onClick={() => void handleConfirmation()} />
              {confirmationResult ? (
                <ResultFlags
                  flags={{
                    status: confirmationResult.status,
                    citation_status: confirmationResult.citation_status,
                    lawyer_confirmed: confirmationResult.lawyer_confirmed,
                    used_in_ai_prompt: confirmationResult.used_in_ai_prompt,
                    final_legal_opinion_generated: confirmationResult.final_legal_opinion_generated
                  }}
                />
              ) : null}
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
          <TrustSafetyPanel items={safety?.safety_checklist ?? []} title="安全清单" />

          <Panel title="开发诊断（默认折叠）">
            <DiagnosticsPanel
              data={{
                status,
                providers,
                legal_search: legalSearch,
                enterprise_query: enterpriseQuery,
                source_traces: sourceTraces,
                confirmation_queue: confirmationQueue,
                audit,
                safety,
                live_status: liveStatus,
                live_providers: liveProviders,
                legal_live_result: legalLiveResult,
                enterprise_live_result: enterpriseLiveResult,
                legal_live_runs: legalLiveRuns,
                enterprise_live_runs: enterpriseLiveRuns,
                live_review_queue: liveReviewQueue,
                live_source_traces: liveSourceTraces,
                live_audit: liveAudit,
                live_safety: liveSafety
              }}
            />
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

function TextField({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return (
    <label className="grid gap-2 text-sm text-ink">
      <span className="font-medium">{label}</span>
      <input value={value} onChange={(event) => onChange(event.target.value)} className="rounded-md border border-line bg-white px-3 py-2 text-sm" />
    </label>
  );
}

function SelectField({ label, value, options, onChange }: { label: string; value: string; options: string[]; onChange: (value: string) => void }) {
  return (
    <label className="grid gap-2 text-sm text-ink">
      <span className="font-medium">{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)} className="rounded-md border border-line bg-white px-3 py-2 text-sm">
        {options.length ? null : <option value="">暂无选项</option>}
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}

function ConfirmField({ label, checked, onChange }: { label: string; checked: boolean; onChange: (value: boolean) => void }) {
  return (
    <label className="flex items-center gap-2 rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
      <input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
      <span>{label}</span>
    </label>
  );
}

function ActionButton({ label, onClick }: { label: string; onClick: () => void }) {
  return (
    <button type="button" onClick={onClick} className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white">
      {label}
    </button>
  );
}

function ResultPanel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mt-5 rounded-md border border-emerald-200 bg-emerald-50 p-4">
      <div className="text-sm font-semibold text-emerald-950">{title}</div>
      <div className="mt-3 grid gap-3">{children}</div>
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

function ResultFlags({ flags }: { flags: Record<string, string | boolean> }) {
  return (
    <div className="grid gap-2 md:grid-cols-2">
      {Object.entries(flags).map(([key, value]) => (
        <MetadataRow key={key} label={key} value={String(value)} />
      ))}
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

function StatusCard({ label, value }: { label: string; value: boolean }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 shadow-sm">
      <div className="text-xs text-muted">{label}</div>
      <div className="mt-3 flex items-center justify-between">
        <div className="text-xl font-semibold text-ink">{value ? "已就绪" : "待确认"}</div>
        <StatusBadge tone={value ? "safe" : "preview"} label={value ? "通过" : "预览"} />
      </div>
    </div>
  );
}

function StatusTile({ label, value, invert = false }: { label: string; value: boolean; invert?: boolean }) {
  const positive = invert ? !value : value;
  return (
    <div className="rounded-md border border-line bg-white p-4">
      <div className="text-xs font-medium text-muted">{label}</div>
      <div className="mt-2 text-xl font-semibold text-ink">{String(value)}</div>
      <div className="mt-3">
        <StatusBadge tone={positive ? "safe" : "blocked"} label={positive ? "受控" : "需阻断"} />
      </div>
    </div>
  );
}

function EmptyState({ label }: { label: string }) {
  return <div className="rounded-md border border-dashed border-line bg-white px-3 py-6 text-center text-sm text-muted">{label}</div>;
}
