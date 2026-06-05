"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  PersonalEnterpriseQueryList,
  PersonalEnterpriseQueryResult,
  PersonalIntelligenceAuditTimeline,
  PersonalIntelligenceConfirmationActionResult,
  PersonalIntelligenceProviderList,
  PersonalIntelligenceSafetyStatus,
  PersonalIntelligenceSourceTraceList,
  PersonalIntelligenceStatus,
  PersonalLegalSearchList,
  PersonalLegalSearchResult,
  createPersonalEnterpriseQueryMock,
  createPersonalLegalSearchMock,
  getPersonalIntelligenceAudit,
  getPersonalIntelligenceConfirmationQueue,
  getPersonalIntelligenceProviders,
  getPersonalIntelligenceSafety,
  getPersonalIntelligenceStatus,
  listPersonalEnterpriseQuery,
  listPersonalIntelligenceSourceTraces,
  listPersonalLegalSearch,
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

export default function PersonalIntelligencePage() {
  const [status, setStatus] = useState<PersonalIntelligenceStatus | null>(null);
  const [providers, setProviders] = useState<PersonalIntelligenceProviderList | null>(null);
  const [legalSearch, setLegalSearch] = useState<PersonalLegalSearchList | null>(null);
  const [enterpriseQuery, setEnterpriseQuery] = useState<PersonalEnterpriseQueryList | null>(null);
  const [sourceTraces, setSourceTraces] = useState<PersonalIntelligenceSourceTraceList | null>(null);
  const [confirmationQueue, setConfirmationQueue] = useState<PersonalIntelligenceSourceTraceList | null>(null);
  const [audit, setAudit] = useState<PersonalIntelligenceAuditTimeline | null>(null);
  const [safety, setSafety] = useState<PersonalIntelligenceSafetyStatus | null>(null);
  const [legalResult, setLegalResult] = useState<PersonalLegalSearchResult | null>(null);
  const [enterpriseResult, setEnterpriseResult] = useState<PersonalEnterpriseQueryResult | null>(null);
  const [confirmationResult, setConfirmationResult] = useState<PersonalIntelligenceConfirmationActionResult | null>(null);
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
  const [legalConfirmed, setLegalConfirmed] = useState(true);
  const [enterpriseConfirmed, setEnterpriseConfirmed] = useState(true);
  const [reviewConfirmed, setReviewConfirmed] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadGateway() {
    setLoading(true);
    setError("");
    try {
      const [nextStatus, nextProviders, nextLegal, nextEnterprise, nextTraces, nextQueue, nextAudit, nextSafety] =
        await Promise.all([
          getPersonalIntelligenceStatus(),
          getPersonalIntelligenceProviders(),
          listPersonalLegalSearch(),
          listPersonalEnterpriseQuery(),
          listPersonalIntelligenceSourceTraces(),
          getPersonalIntelligenceConfirmationQueue(),
          getPersonalIntelligenceAudit(),
          getPersonalIntelligenceSafety()
        ]);
      setStatus(nextStatus);
      setProviders(nextProviders);
      setLegalSearch(nextLegal);
      setEnterpriseQuery(nextEnterprise);
      setSourceTraces(nextTraces);
      setConfirmationQueue(nextQueue);
      setAudit(nextAudit);
      setSafety(nextSafety);
      setSelectedTraceId((current) => current || nextQueue.source_traces[0]?.source_trace_id || "");
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
  const activeTraceId = selectedTraceId || confirmationQueue?.source_traces[0]?.source_trace_id || "";

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

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <div className="rounded-md border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800">{error}</div> : null}

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

        <Panel title="Provider Cards">
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
          <Panel title="Citation Candidates / Source Trace">
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
          <Panel title="安全清单">
            <div className="grid gap-2">
              {(safety?.safety_checklist ?? []).map((item) => (
                <div key={item} className="flex items-center justify-between rounded-md border border-line bg-white px-3 py-2">
                  <span className="text-sm text-ink">{item}</span>
                  <StatusBadge tone="safe" label="通过" />
                </div>
              ))}
            </div>
          </Panel>

          <Panel title="Developer Diagnostics">
            <details className="rounded-md border border-line bg-slate-950 text-slate-100">
              <summary className="cursor-pointer px-4 py-3 text-sm font-medium text-slate-200">JSON metadata</summary>
              <pre className="max-h-96 overflow-auto border-t border-slate-800 p-4 text-xs leading-5">
                {JSON.stringify(
                  {
                    status,
                    providers,
                    legal_search: legalSearch,
                    enterprise_query: enterpriseQuery,
                    source_traces: sourceTraces,
                    confirmation_queue: confirmationQueue,
                    audit,
                    safety
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

function EmptyState({ label }: { label: string }) {
  return <div className="rounded-md border border-dashed border-line bg-white px-3 py-6 text-center text-sm text-muted">{label}</div>;
}
