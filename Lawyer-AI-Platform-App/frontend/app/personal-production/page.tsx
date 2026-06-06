"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DarkSafetyBadge,
  DiagnosticsPanel,
  LocalPilotPath,
  SafeErrorNotice,
  ShowcaseStepper,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
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
  "案件录入",
  "材料接入",
  "OCR",
  "事实提炼",
  "法律检索与企业信息核验",
  "草稿分析",
  "案件与材料工作台",
  "事实预览与输入纠正",
  "法律分析草稿",
  "Skill 最终稿与优化",
  "用户本人产出下载中心",
  "实战试运行准备",
  "真实接口接入准备",
  "OCR / Document 接入准备",
  "受控接口接入",
  "法律与企业信息接口",
  "Codex 训练产物加载器",
  "已结案件 Codex 训练执行",
  "真实已结案件训练材料导入与脱敏",
  "Skill Package 版本化封装与系统校验",
  "Internal Training / Experience Package Builder",
  "Practice Runtime Load Review Gate",
  "受控案件分析",
  "实战 Pilot 与本人下载",
  "Pilot Dashboard 增强",
  "律师复核",
  "个人生产交付包",
  "个人生产试点与展示包"
];

const safetyMessages = [
  "仅模拟结果",
  "律师复核必需",
  "来源可追踪",
  "受控运行",
  "最终锁定必需",
  "不自动对外交付",
  "团队版后置",
  "外部交付后置"
];

const nextRoute = [
  "v7.10 Personal Version Polish & Public Demo Readiness",
  "v7.11 Personal Production Stability & Local Pilot Hardening",
  "v7.12 AI Provider Live Gateway 后续受控接入",
  "v7.13 OCR / Document Provider Live Gateway 后续受控接入",
  "v7.14 Legal / Enterprise API Live Gateway 后续受控接入",
  "v7.15 Skill Training 后续受控训练",
  "v7.16 Controlled Case Analysis 受控案件分析",
  "v7.17 Personal Production Pilot with Real AI Gated Mode",
  "v7.18 Case Intake & Material Workspace Hardening",
  "v7.19 Personal Production Pilot Dashboard Enhancement",
  "v7.20 Fact Preview & Correction Workbench",
  "v7.21 Legal Analysis Draft Workbench",
  "v7.22 Skill Final Draft & Optimization Workbench",
  "v7.23 Owner-only Output Center",
  "v7.24 Personal Practical Production Workbench stable release",
  "v7.25 Personal Practical Case Trial Readiness",
  "v7.26 Provider Live Readiness & Secret Boundary",
  "v7.27 OCR / Document Provider Live Connection",
  "v7.30 Codex Training Scheme & Multi-Level Case-Cause Artifact Loader",
  "v7.31 Execute Codex Training on Closed Case Samples",
  "v7.31a Real Closed-Case Training Intake & Redaction Pipeline",
  "v7.31b Controlled Experience Extraction Pipeline",
  "v7.31c Skill Experience Pool & Codex Skill Draft Builder",
  "v7.31d Skill Package Versioning & System Validation Gate",
  "v7.31e Internal Training / Experience Package Builder",
  "v7.31f Practice Runtime Load Review Gate",
  "Final Security Audit for Personal Live Intelligence & Controlled Case Analysis",
  "Team Workspace deferred / 团队版后置",
  "External Client Delivery deferred / 外部交付后置"
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
      { label: "受控案件生产工作流", value: Boolean(readiness?.readiness.case_production_gateway_registered) },
      { label: "受控案件分析 Runtime", value: Boolean(readiness?.readiness.controlled_case_analysis_gateway_registered ?? true) },
      { label: "法律分析草稿工作台", value: Boolean(readiness?.readiness.legal_analysis_draft_workbench_gateway_registered ?? true) },
      { label: "Skill 最终稿工作台", value: Boolean(readiness?.readiness.skill_final_draft_workbench_gateway_registered ?? true) },
      { label: "用户本人产出下载中心", value: Boolean(readiness?.readiness.owner_output_center_ready ?? true) },
      { label: "实战试运行准备", value: Boolean(readiness?.readiness.personal_trial_readiness_gateway_registered ?? true) },
      { label: "真实接口接入准备", value: Boolean(readiness?.readiness.personal_provider_readiness_gateway_registered ?? true) },
      { label: "OCR / Document 接入准备", value: Boolean(readiness?.readiness.personal_material_live_connection_gateway_registered ?? true) },
      { label: "受控接口接入", value: Boolean(readiness?.readiness.personal_live_connection_gateway_registered ?? true) },
      { label: "法律与企业信息接口", value: Boolean(readiness?.readiness.personal_legal_enterprise_gateway_registered ?? true) },
      { label: "训练产物加载器", value: Boolean(readiness?.readiness.training_artifact_loader_gateway_registered ?? true) },
      { label: "已结案件 Codex 训练", value: Boolean(readiness?.readiness.codex_training_run_gateway_registered ?? true) },
      { label: "真实闭案 intake", value: Boolean(readiness?.readiness.real_closed_case_training_intake_gateway_registered ?? true) },
      { label: "Codex Skill 草案", value: Boolean(readiness?.readiness.codex_skill_draft_builder_gateway_registered ?? true) },
      { label: "内部训练经验包", value: Boolean(readiness?.readiness.internal_training_experience_package_gateway_registered ?? true) },
      { label: "实战加载前复核", value: Boolean(readiness?.readiness.practice_load_review_gateway_registered ?? true) },
      { label: "个人生产实战 Pilot", value: Boolean(readiness?.readiness.personal_production_pilot_gateway_registered ?? true) },
      { label: "个人案件与材料工作台", value: Boolean(readiness?.readiness.personal_case_workspace_gateway_registered ?? true) },
      { label: "Pilot Dashboard 增强", value: Boolean(readiness?.readiness.personal_production_pilot_dashboard_gateway_registered ?? true) },
      { label: "事实预览与输入纠正", value: Boolean(readiness?.readiness.fact_preview_correction_workbench_gateway_registered ?? true) },
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
        {error ? <SafeErrorNotice message={error} /> : null}

        <section className="overflow-hidden rounded-md border border-slate-800 bg-[#111827] text-white shadow-sm">
          <div className="grid gap-6 p-6 md:grid-cols-[1.4fr_0.8fr] md:p-8">
            <div>
              <div className="inline-flex items-center rounded-md border border-cyan-300/40 bg-cyan-300/10 px-3 py-1 text-xs font-medium text-cyan-100">
                {status?.version ?? "v7.22"} · 个人生产验证
              </div>
              <h1 className="mt-5 max-w-3xl text-3xl font-semibold leading-tight md:text-5xl">
                AIHome.law 个人生产总控台
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300">
                面向个人版生产验证和公开演示准备的受控运行总览，集中展示 readiness、runtime、来源追踪、律师复核和安全边界。当前仅为模拟元数据展示，不代表正式案件处理或外部交付。
              </p>
              <div className="mt-5 flex flex-wrap gap-2">
                {["个人生产试点", ...(showcase?.trust_badges ?? ["仅模拟结果", "律师复核必需", "来源可追踪", "受控运行", "最终锁定必需"]), "团队版后置", "外部交付后置"].map((badge) => (
                  <DarkSafetyBadge key={badge} label={badge} />
                ))}
              </div>
            </div>
            <div className="rounded-md border border-slate-700 bg-white/5 p-5">
              <div className="text-xs uppercase tracking-wide text-cyan-200">Runtime posture</div>
              <div className="mt-4 grid gap-3">
                <HeroMetric label="展示就绪" value={status?.showcase_ready ?? true} />
                <HeroMetric label="真实 provider 调用" value={status?.real_provider_call_enabled ?? false} invert />
                <HeroMetric label="团队工作区" value={status?.team_workspace_enabled ?? false} invert />
                <HeroMetric label="外部交付" value={status?.external_client_delivery_ready ?? false} invert />
              </div>
              <button
                type="button"
                onClick={() => void loadConsole()}
                disabled={loading}
                className="mt-5 w-full rounded-md bg-cyan-300 px-3 py-2 text-sm font-semibold text-slate-950 disabled:opacity-60"
              >
                {loading ? "刷新中" : "刷新总控台"}
              </button>
            </div>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-10">
          {readinessCards.map((card) => (
            <ReadinessCard key={card.label} label={card.label} ready={card.value} />
          ))}
        </section>

        <LocalPilotPath />

        <section className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
          <Panel title="Runtime 能力矩阵">
            <div className="grid gap-3 md:grid-cols-2">
              {(runtimeRegistry?.runtimes ?? []).map((runtime) => (
                <RuntimeCard key={runtime.runtime_id} runtime={runtime} />
              ))}
            </div>
          </Panel>

          <Panel title="Provider 能力预览">
            <div className="grid gap-3">
              {(providerCapabilities?.providers ?? []).map((provider) => (
                <CapabilityCard key={provider.provider_id} provider={provider} />
              ))}
            </div>
          </Panel>
        </section>

        <section className="rounded-md border border-cyan-200 bg-cyan-50 p-5 text-cyan-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.12 AI Provider Live Gateway</div>
          <h2 className="mt-2 text-lg font-semibold">受控真实接口地基</h2>
          <p className="mt-2 text-sm leading-6">
            AI Provider Live Gateway：planned / gated / disabled by default。dry-run ready，live call requires confirmation，输出保持草稿状态，不生成最终法律意见、不自动对外交付。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="ai_live_gateway_status" value={providerCapabilities?.ai_live_gateway_status ?? "planned_gated_disabled_by_default"} />
            <MetricTile label="live_provider_count" value={String(providerCapabilities?.live_provider_count ?? 0)} />
            <MetricTile label="key_loaded_count" value={String(providerCapabilities?.key_loaded_count ?? 0)} />
            <MetricTile label="dry_run_ready" value={String(providerCapabilities?.dry_run_ready ?? true)} />
          </div>
        </section>

        <section className="rounded-md border border-emerald-200 bg-emerald-50 p-5 text-emerald-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.13 OCR / Document Provider Live Gateway</div>
          <h2 className="mt-2 text-lg font-semibold">OCR 与文档解析受控接入地基</h2>
          <p className="mt-2 text-sm leading-6">
            OCR / Document Provider Live Gateway：planned / gated / disabled by default。document dry-run 与 OCR dry-run 可用；原始内容默认阻断，AI prompt injection 默认阻断，不自动触发事实抽取、法律分析、最终报告或对外交付。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="ocr_document_live_gateway_status" value={providerCapabilities?.ocr_document_live_gateway_status ?? "planned_gated_disabled_by_default"} />
            <MetricTile label="material_live_provider_count" value={String(providerCapabilities?.material_live_provider_count ?? 0)} />
            <MetricTile label="material_key_loaded_count" value={String(providerCapabilities?.material_key_loaded_count ?? 0)} />
            <MetricTile label="raw_content_blocked_by_default" value={String(providerCapabilities?.raw_content_blocked_by_default ?? true)} />
            <MetricTile label="document_dry_run_ready" value={String(providerCapabilities?.document_dry_run_ready ?? true)} />
            <MetricTile label="ocr_dry_run_ready" value={String(providerCapabilities?.ocr_dry_run_ready ?? true)} />
            <MetricTile label="ai_prompt_injection_blocked" value={String(providerCapabilities?.ai_prompt_injection_blocked_by_default ?? true)} />
            <MetricTile label="live_call_requires_confirmation" value={String(providerCapabilities?.live_call_requires_confirmation ?? true)} />
          </div>
        </section>

        <section className="rounded-md border border-violet-200 bg-violet-50 p-5 text-violet-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.14 Legal / Enterprise API Live Gateway</div>
          <h2 className="mt-2 text-lg font-semibold">法律检索与企业信息 API 受控接入地基</h2>
          <p className="mt-2 text-sm leading-6">
            Legal / Enterprise API Live Gateway：planned / gated / disabled by default。legal dry-run 与 enterprise dry-run 可用；原始内容默认阻断，AI prompt injection 默认阻断，citation finalization 默认阻断。候选结果不是最终引用，不自动触发案件分析或最终报告。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="legal_enterprise_live_gateway_status" value={providerCapabilities?.legal_enterprise_live_gateway_status ?? "planned_gated_disabled_by_default"} />
            <MetricTile label="intelligence_live_provider_count" value={String(providerCapabilities?.intelligence_live_provider_count ?? 0)} />
            <MetricTile label="intelligence_key_loaded_count" value={String(providerCapabilities?.intelligence_key_loaded_count ?? 0)} />
            <MetricTile label="citation_finalization_blocked" value={String(providerCapabilities?.citation_finalization_blocked_by_default ?? true)} />
            <MetricTile label="legal_dry_run_ready" value={String(providerCapabilities?.legal_dry_run_ready ?? true)} />
            <MetricTile label="enterprise_dry_run_ready" value={String(providerCapabilities?.enterprise_dry_run_ready ?? true)} />
            <MetricTile label="raw_content_blocked_by_default" value={String(providerCapabilities?.raw_content_blocked_by_default ?? true)} />
            <MetricTile label="ai_prompt_injection_blocked" value={String(providerCapabilities?.ai_prompt_injection_blocked_by_default ?? true)} />
          </div>
        </section>

        <section className="rounded-md border border-amber-200 bg-amber-50 p-5 text-amber-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.16 Controlled Case Analysis Runtime</div>
          <h2 className="mt-2 text-lg font-semibold">未结案件实战分析 draft 地基</h2>
          <p className="mt-2 text-sm leading-6">
            Controlled Case Analysis Runtime：planned / gated / 草稿状态。实战阶段调用已有 Skill metadata，生成事实分析 draft 与法律分析 draft；训练阶段与实战阶段分离，不产生训练数据，不自动更新或发布 Skill，不生成最终法律意见。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="controlled_case_analysis_status" value={providerCapabilities?.controlled_case_analysis_runtime_status ?? "planned_gated_draft_only"} />
            <MetricTile label="fact_skill_baseline_detected" value={String(providerCapabilities?.fact_skill_baseline_detected ?? false)} />
            <MetricTile label="legal_skill_baseline_detected" value={String(providerCapabilities?.legal_analysis_skill_baseline_detected ?? false)} />
            <MetricTile label="open_case_analysis_draft_ready" value={String(providerCapabilities?.open_case_analysis_draft_ready ?? true)} />
            <MetricTile label="training_data_generation_disabled" value={String(providerCapabilities?.training_data_generation_disabled ?? true)} />
            <MetricTile label="skill_auto_update_disabled" value={String(providerCapabilities?.skill_auto_update_disabled ?? true)} />
            <MetricTile label="evaluation_reference_only" value={String(providerCapabilities?.evaluation_reference_only ?? true)} />
            <MetricTile label="lawyer_review_required" value="true" />
          </div>
        </section>

        <section className="rounded-md border border-sky-200 bg-sky-50 p-5 text-sky-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.17 Personal Production Pilot</div>
          <h2 className="mt-2 text-lg font-semibold">实战 Pilot 与用户本人下载</h2>
          <p className="mt-2 text-sm leading-6">
            Personal Production Pilot：ready / gated / owner-download-only。串联 AI / OCR / Legal / Enterprise / Skill / Case Analysis / Delivery Packet；真实 provider 默认关闭，用户本人可下载草稿 metadata，系统不自动邮件、不创建公开链接、不对外交付、不自动定性最终法律意见或正式报告。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="pilot_status" value={providerCapabilities?.personal_production_pilot_status ?? "ready_gated_owner_download_only"} />
            <MetricTile label="connected_stack" value={String(providerCapabilities?.pilot_ai_ocr_legal_enterprise_skill_case_analysis_connected ?? true)} />
            <MetricTile label="owner_downloads_ready" value={String(providerCapabilities?.owner_only_downloads_ready ?? true)} />
            <MetricTile label="external_delivery_disabled" value={String(providerCapabilities?.external_delivery_disabled ?? true)} />
            <MetricTile label="public_link_disabled" value={String(providerCapabilities?.public_link_disabled ?? true)} />
            <MetricTile label="email_sending_disabled" value={String(providerCapabilities?.email_sending_disabled ?? true)} />
            <MetricTile label="final_opinion_auto_disabled" value={String(providerCapabilities?.final_legal_opinion_auto_generation_disabled ?? true)} />
            <MetricTile label="open_case_training_disabled" value={String(providerCapabilities?.open_case_training_data_generation_disabled ?? true)} />
          </div>
        </section>

        <section className="rounded-md border border-teal-200 bg-teal-50 p-5 text-teal-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.18 Case Intake & Material Workspace Hardening</div>
          <h2 className="mt-2 text-lg font-semibold">个人案件与材料工作台</h2>
          <p className="mt-2 text-sm leading-6">
            Case Workspace：用户本人 / 仅元数据。案件与材料列表、OCR 状态、事实输入纠正、来源追踪和审计统一展示；Owner 原文查看需要明确确认，但 API 不返回原始内容、不写训练集、不进入 AI prompt。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="case_workspace_status" value={providerCapabilities?.personal_case_workspace_status ?? "owner_only_metadata_ready"} />
            <MetricTile label="owner_raw_view_gated" value={String(providerCapabilities?.case_workspace_owner_raw_view_gated ?? true)} />
            <MetricTile label="source_trace_required" value="true" />
            <MetricTile label="raw_content_returned" value="false" />
          </div>
        </section>

        <section className="rounded-md border border-indigo-200 bg-indigo-50 p-5 text-indigo-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.19 Personal Production Pilot Dashboard Enhancement</div>
          <h2 className="mt-2 text-lg font-semibold">Pilot Dashboard 评分、门控与优化建议</h2>
          <p className="mt-2 text-sm leading-6">
            Dashboard Enhancement：dashboard metadata ready。每份 Skill / Case Analysis 产出可展示质量评分、参考门控和优化建议；评分不构成法律结论，不阻断下一阶段，不生成最终法律意见或正式报告。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="pilot_dashboard_status" value={providerCapabilities?.personal_production_pilot_dashboard_status ?? "dashboard_metadata_ready"} />
            <MetricTile label="quality_panels_ready" value={String(providerCapabilities?.pilot_dashboard_quality_panels_ready ?? true)} />
            <MetricTile label="suggestions_ready" value={String(providerCapabilities?.pilot_dashboard_optimization_suggestions_ready ?? true)} />
            <MetricTile label="external_delivery_disabled" value={String(providerCapabilities?.external_delivery_disabled ?? true)} />
          </div>
        </section>

        <section className="rounded-md border border-rose-200 bg-rose-50 p-5 text-rose-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.20 Fact Preview & Correction Workbench</div>
          <h2 className="mt-2 text-lg font-semibold">事实预览与输入纠正工作台</h2>
          <p className="mt-2 text-sm leading-6">
            Fact Preview & Correction：用户本人 / 草稿状态 / reference gate。用户本人可查看事实预览、纠正事实、查看版本历史、标记法律分析输入和下载本人留存 metadata；不会自动触发法律分析，不写训练集，不更新或发布 Skill，不生成最终事实认定。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="fact_workbench_status" value={providerCapabilities?.fact_preview_correction_workbench_status ?? "fact_preview_correction_metadata_ready"} />
            <MetricTile label="owner_correction_ready" value={String(providerCapabilities?.fact_preview_owner_correction_ready ?? true)} />
            <MetricTile label="legal_analysis_input_ready" value={String(providerCapabilities?.fact_preview_legal_analysis_input_ready ?? true)} />
            <MetricTile label="legal_analysis_auto_triggered" value={String(providerCapabilities?.fact_preview_legal_analysis_auto_triggered ?? false)} />
            <MetricTile label="gate_reference_only" value={String(providerCapabilities?.fact_preview_gate_reference_only ?? true)} />
            <MetricTile label="training_data_generated" value="false" />
            <MetricTile label="skill_published" value="false" />
            <MetricTile label="final_fact_finding" value="false" />
          </div>
        </section>

        <section className="rounded-md border border-fuchsia-200 bg-fuchsia-50 p-5 text-fuchsia-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.21 Legal Analysis Draft Workbench</div>
          <h2 className="mt-2 text-lg font-semibold">法律分析草稿工作台</h2>
          <p className="mt-2 text-sm leading-6">
            Legal Analysis Draft：基于 v7.20 事实输入 metadata 生成法律分析草稿，展示法律分析摘要、争议焦点、请求权基础、抗辩路径、风险提示和下一步清单。输出仅为 draft metadata，不生成最终法律意见、最终报告或外部交付。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="legal_draft_workbench_status" value={providerCapabilities?.legal_analysis_draft_workbench_status ?? "legal_analysis_draft_metadata_ready"} />
            <MetricTile label="legal_analysis_draft_only" value={String(providerCapabilities?.legal_analysis_draft_only ?? true)} />
            <MetricTile label="review_ready" value={String(providerCapabilities?.legal_analysis_draft_review_ready ?? true)} />
            <MetricTile label="final_opinion_blocked" value={String(providerCapabilities?.legal_analysis_final_opinion_blocked ?? true)} />
            <MetricTile label="final_report_blocked" value={String(providerCapabilities?.legal_analysis_final_report_blocked ?? true)} />
            <MetricTile label="owner_download_metadata_ready" value={String(providerCapabilities?.legal_analysis_owner_download_metadata_ready ?? true)} />
            <MetricTile label="training_data_generated" value="false" />
            <MetricTile label="external_delivery_triggered" value="false" />
          </div>
        </section>

        <section className="rounded-md border border-emerald-200 bg-emerald-50 p-5 text-emerald-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.22 Skill Final Draft & Optimization Workbench</div>
          <h2 className="mt-2 text-lg font-semibold">两个 Skill 最终稿与优化工作台</h2>
          <p className="mt-2 text-sm leading-6">
            Skill Final Draft：汇总既有 Skill、evaluation、gate、test case 与 prompt template metadata，生成案件事实提炼 Skill 和案件法律分析 Skill 的 final draft metadata。仅用户本人下载，不自动发布 Skill，不自动训练未结案件。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="skill_final_draft_status" value={providerCapabilities?.skill_final_draft_workbench_status ?? "skill_final_draft_metadata_ready"} />
            <MetricTile label="fact_skill_final_draft_ready" value={String(providerCapabilities?.fact_skill_final_draft_ready ?? true)} />
            <MetricTile label="legal_skill_final_draft_ready" value={String(providerCapabilities?.legal_analysis_skill_final_draft_ready ?? true)} />
            <MetricTile label="owner_download_ready" value={String(providerCapabilities?.skill_final_draft_owner_download_ready ?? true)} />
            <MetricTile label="auto_publish_disabled" value={String(providerCapabilities?.skill_final_draft_auto_publish_disabled ?? true)} />
            <MetricTile label="open_case_training_disabled" value={String(providerCapabilities?.skill_final_draft_open_case_training_disabled ?? true)} />
            <MetricTile label="gate_reference_only" value={String(providerCapabilities?.skill_final_draft_gate_reference_only ?? true)} />
            <MetricTile label="external_delivery_triggered" value="false" />
          </div>
        </section>

        <section className="rounded-md border border-cyan-200 bg-cyan-50 p-5 text-cyan-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.23 Owner-only Output Center</div>
          <h2 className="mt-2 text-lg font-semibold">用户本人产出下载中心</h2>
          <p className="mt-2 text-sm leading-6">
            Owner-only Output Center：集中聚合 Skill 最终稿、事实产出、法律分析草稿、Pilot / Delivery 草稿。所有产出仅用户本人查看和下载，不创建公开链接、不发送邮件、不自动对外交付、不自动标记最终法律意见或正式律师报告。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="owner_output_center_status" value={providerCapabilities?.owner_output_center_status ?? "owner_output_center_metadata_ready"} />
            <MetricTile label="skill_final_drafts_aggregated" value={String(providerCapabilities?.skill_final_drafts_aggregated ?? true)} />
            <MetricTile label="fact_outputs_aggregated" value={String(providerCapabilities?.fact_outputs_aggregated ?? true)} />
            <MetricTile label="legal_drafts_aggregated" value={String(providerCapabilities?.legal_drafts_aggregated ?? true)} />
            <MetricTile label="pilot_delivery_outputs_aggregated" value={String(providerCapabilities?.pilot_delivery_outputs_aggregated ?? true)} />
            <MetricTile label="owner_download_ready" value={String(providerCapabilities?.owner_output_center_download_ready ?? true)} />
            <MetricTile label="public_link_disabled" value={String(providerCapabilities?.public_link_disabled ?? true)} />
            <MetricTile label="external_delivery_disabled" value={String(providerCapabilities?.external_delivery_disabled ?? true)} />
          </div>
        </section>

        <section className="rounded-md border border-slate-300 bg-slate-50 p-5 text-slate-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.25 Personal Practical Case Trial Readiness</div>
          <h2 className="mt-2 text-lg font-semibold">个人版实战试运行准备</h2>
          <p className="mt-2 text-sm leading-6">
            Trial Readiness：进入真实办案前的个人版试运行 metadata。记录 trial session、checklist、stage observation、issue log、quality review、safety confirmation 和 optimization backlog；不读取真实案件原文、不调用真实 provider、不训练未结案件、不自动发布 Skill、不自动对外交付。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="trial_readiness_status" value={providerCapabilities?.personal_trial_readiness_status ?? "trial_readiness_metadata_ready"} />
            <MetricTile label="trial_checklist_ready" value={String(providerCapabilities?.trial_checklist_ready ?? true)} />
            <MetricTile label="issue_log_ready" value={String(providerCapabilities?.trial_issue_log_ready ?? true)} />
            <MetricTile label="quality_review_ready" value={String(providerCapabilities?.trial_quality_review_ready ?? true)} />
            <MetricTile label="safety_confirmation_ready" value={String(providerCapabilities?.trial_safety_confirmation_ready ?? true)} />
            <MetricTile label="optimization_backlog_ready" value={String(providerCapabilities?.trial_optimization_backlog_ready ?? true)} />
            <MetricTile label="issue_log_reference_only" value={String(providerCapabilities?.trial_issue_log_reference_only ?? true)} />
            <MetricTile label="quality_review_reference_only" value={String(providerCapabilities?.trial_quality_review_reference_only ?? true)} />
          </div>
        </section>

        <section className="rounded-md border border-violet-200 bg-violet-50 p-5 text-violet-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.26 Provider Live Readiness & Secret Boundary</div>
          <h2 className="mt-2 text-lg font-semibold">真实接口接入准备与密钥边界</h2>
          <p className="mt-2 text-sm leading-6">
            Provider Readiness：进入真实 OCR / AI / 法律 / 企业 API 前的统一 readiness 层。只展示 provider registry、key_loaded boolean、live gate、usage/cost metadata 与 dry-run health；不读取密钥值、不真实调用 provider、不上传案件材料。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="provider_readiness_status" value={providerCapabilities?.personal_provider_readiness_status ?? "provider_readiness_metadata_ready"} />
            <MetricTile label="provider_registry_ready" value={String(providerCapabilities?.provider_registry_ready ?? true)} />
            <MetricTile label="secret_boundary_ready" value={String(providerCapabilities?.secret_boundary_ready ?? true)} />
            <MetricTile label="live_gate_ready" value={String(providerCapabilities?.live_gate_ready ?? true)} />
            <MetricTile label="usage_cost_metadata_ready" value={String(providerCapabilities?.usage_cost_metadata_ready ?? true)} />
            <MetricTile label="dry_run_health_ready" value={String(providerCapabilities?.dry_run_health_ready ?? true)} />
            <MetricTile label="real_provider_calls_still_disabled" value={String(providerCapabilities?.real_provider_calls_still_disabled ?? true)} />
            <MetricTile label="frontend_key_input_enabled" value="false" />
          </div>
        </section>

        <section className="rounded-md border border-cyan-200 bg-cyan-50 p-5 text-cyan-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.27 OCR / Document Provider Live Connection</div>
          <h2 className="mt-2 text-lg font-semibold">OCR / 文档接口接入准备</h2>
          <p className="mt-2 text-sm leading-6">
            OCR / Document Live Connection：在 v7.26 密钥边界之后，补齐材料 Provider 的 secret boundary、live gate、dry-run health、source trace、audit 与 safety metadata。默认 dry-run，live_call_allowed=false，不上传文件、不返回 OCR / 文档原文、不进入 AI Prompt。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="material_live_connection_status" value={providerCapabilities?.personal_material_live_connection_status ?? "ocr_document_live_connection_metadata_ready"} />
            <MetricTile label="provider_registry_ready" value={String(providerCapabilities?.material_live_provider_registry_ready ?? true)} />
            <MetricTile label="secret_boundary_ready" value={String(providerCapabilities?.material_live_secret_boundary_ready ?? true)} />
            <MetricTile label="live_gate_ready" value={String(providerCapabilities?.material_live_gate_ready ?? true)} />
            <MetricTile label="dry_run_health_ready" value={String(providerCapabilities?.material_live_dry_run_health_ready ?? true)} />
            <MetricTile label="raw_content_blocked" value={String(providerCapabilities?.material_live_raw_content_blocked ?? true)} />
            <MetricTile label="ai_prompt_injection_blocked" value={String(providerCapabilities?.material_live_ai_prompt_injection_blocked ?? true)} />
            <MetricTile label="live_call_allowed" value="false" />
          </div>
        </section>

        <section className="rounded-md border border-emerald-200 bg-emerald-50 p-5 text-emerald-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.28 Personal Live AI/OCR/Legal/Enterprise Connection</div>
          <h2 className="mt-2 text-lg font-semibold">个人生产受控接口接入</h2>
          <p className="mt-2 text-sm leading-6">
            统一展示 AI / OCR / Document / Legal / Enterprise Provider readiness、secret boundary、live gate、usage/cost、health 与 audit。默认 dry-run，live disabled，不执行网络请求，不生成最终法律意见、最终报告、真实 PDF/DOCX、邮件或外部交付。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="live_connection_status" value={providerCapabilities?.personal_live_connection_status ?? "personal_live_connection_metadata_ready"} />
            <MetricTile label="provider_registry_ready" value={String(providerCapabilities?.personal_live_connection_provider_registry_ready ?? true)} />
            <MetricTile label="secret_boundary_ready" value={String(providerCapabilities?.personal_live_connection_secret_boundary_ready ?? true)} />
            <MetricTile label="live_gate_ready" value={String(providerCapabilities?.personal_live_connection_gate_ready ?? true)} />
            <MetricTile label="usage_cost_ready" value={String(providerCapabilities?.personal_live_connection_usage_cost_ready ?? true)} />
            <MetricTile label="health_ready" value={String(providerCapabilities?.personal_live_connection_health_ready ?? true)} />
            <MetricTile label="audit_ready" value={String(providerCapabilities?.personal_live_connection_audit_ready ?? true)} />
            <MetricTile label="network_call_executed" value="false" />
          </div>
        </section>

        <section className="rounded-md border border-amber-200 bg-amber-50 p-5 text-amber-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.29 Legal / Enterprise API Live Connection</div>
          <h2 className="mt-2 text-lg font-semibold">法律检索与企业信息 API 受控接入</h2>
          <p className="mt-2 text-sm leading-6">
            法律检索与企业信息接口只返回 dry-run metadata、source trace、review queue 与 audit。法律检索结果不自动作为最终引用，企业信息不自动形成最终事实认定，不写训练集、不更新 Skill、不自动对外交付。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="gateway_status" value={providerCapabilities?.personal_legal_enterprise_gateway_status ?? "legal_enterprise_gateway_metadata_ready"} />
            <MetricTile label="legal_provider_ready" value={String(providerCapabilities?.legal_provider_readiness_ready ?? true)} />
            <MetricTile label="enterprise_provider_ready" value={String(providerCapabilities?.enterprise_provider_readiness_ready ?? true)} />
            <MetricTile label="legal_source_trace_ready" value={String(providerCapabilities?.legal_source_trace_ready ?? true)} />
            <MetricTile label="enterprise_verification_ready" value={String(providerCapabilities?.enterprise_verification_ready ?? true)} />
            <MetricTile label="review_required" value={String(providerCapabilities?.legal_enterprise_review_required ?? true)} />
            <MetricTile label="real_provider_calls_disabled" value={String(providerCapabilities?.real_provider_calls_still_disabled ?? true)} />
            <MetricTile label="final_fact_finding" value="false" />
          </div>
        </section>

        <section className="rounded-md border border-cyan-200 bg-cyan-50 p-5 text-cyan-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.30 Codex Training Scheme & Multi-Level Case-Cause Artifact Loader</div>
          <h2 className="mt-2 text-lg font-semibold">Codex 训练方案与多层级案由产物加载器</h2>
          <p className="mt-2 text-sm leading-6">
            训练产物加载器只读取合成闭案训练产物 metadata，按案由层级匹配 common / ancestor / exact / evidence overlay 包，生成 Skill Context dry-run。Codex 训练不是模型微调，不训练未结案件，不写训练集，不自动更新或发布 Skill。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="loader_status" value={providerCapabilities?.training_artifact_loader_status ?? "training_artifact_loader_metadata_ready"} />
            <MetricTile label="codex_training_scheme_ready" value={String(providerCapabilities?.codex_training_scheme_ready ?? true)} />
            <MetricTile label="case_cause_taxonomy_ready" value={String(providerCapabilities?.case_cause_taxonomy_ready ?? true)} />
            <MetricTile label="multi_level_loader_ready" value={String(providerCapabilities?.multi_level_case_cause_loader_ready ?? true)} />
            <MetricTile label="experience_package_manifest_ready" value={String(providerCapabilities?.experience_package_manifest_ready ?? true)} />
            <MetricTile label="skill_manifest_loader_ready" value={String(providerCapabilities?.skill_manifest_loader_ready ?? true)} />
            <MetricTile label="fallback_ready" value={String(providerCapabilities?.case_cause_fallback_ready ?? true)} />
            <MetricTile label="skill_context_dry_run_ready" value={String(providerCapabilities?.skill_context_dry_run_ready ?? true)} />
            <MetricTile label="fine_tune_training" value={String(!(providerCapabilities?.codex_fine_tune_training_disabled ?? true))} />
            <MetricTile label="open_case_training" value={String(!(providerCapabilities?.training_artifact_open_case_training_disabled ?? true))} />
            <MetricTile label="skill_auto_publish" value={String(!(providerCapabilities?.training_artifact_skill_auto_publish_disabled ?? true))} />
            <MetricTile label="load_executed" value="false" />
          </div>
        </section>

        <section className="rounded-md border border-emerald-200 bg-emerald-50 p-5 text-emerald-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.31 Execute Codex Training on Closed Case Samples</div>
          <h2 className="mt-2 text-lg font-semibold">已结案件 Codex 训练执行</h2>
          <p className="mt-2 text-sm leading-6">
            使用 synthetic closed-case samples 生成 training run manifest、experience packages、两个核心 Skill manifests、evaluation / gate / test cases 与 loading manifest，并通过 v7.30 loader dry-run 校验。当前不读取真实案件材料，不训练未结案件，不执行模型微调，不写正式训练集。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="training_run_status" value={providerCapabilities?.codex_training_run_status ?? "codex_training_run_metadata_ready"} />
            <MetricTile label="closed_case_training_run_ready" value={String(providerCapabilities?.closed_case_training_run_ready ?? true)} />
            <MetricTile label="synthetic_samples_ready" value={String(providerCapabilities?.synthetic_closed_case_samples_ready ?? true)} />
            <MetricTile label="training_run_manifest_ready" value={String(providerCapabilities?.training_run_manifest_ready ?? true)} />
            <MetricTile label="experience_packages_ready" value={String(providerCapabilities?.generated_experience_packages_ready ?? true)} />
            <MetricTile label="skill_manifests_ready" value={String(providerCapabilities?.generated_skill_manifests_ready ?? true)} />
            <MetricTile label="eval_gate_tests_ready" value={String(providerCapabilities?.generated_evaluation_gate_test_cases_ready ?? true)} />
            <MetricTile label="loading_manifest_ready" value={String(providerCapabilities?.generated_loading_manifest_ready ?? true)} />
            <MetricTile label="loader_dry_run_ready" value={String(providerCapabilities?.training_run_load_dry_run_ready ?? true)} />
            <MetricTile label="open_case_training" value={String(!(providerCapabilities?.training_run_open_case_training_disabled ?? true))} />
            <MetricTile label="skill_auto_publish" value={String(!(providerCapabilities?.training_run_skill_auto_publish_disabled ?? true))} />
            <MetricTile label="fine_tune_training" value={String(!(providerCapabilities?.training_run_fine_tune_disabled ?? true))} />
          </div>
        </section>

        <section className="rounded-md border border-sky-200 bg-sky-50 p-5 text-sky-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.31a Real Closed-Case Training Intake & Redaction Pipeline</div>
          <h2 className="mt-2 text-lg font-semibold">真实已结案件训练材料导入与脱敏管线</h2>
          <p className="mt-2 text-sm leading-6">
            v7.31a 只准备已授权、已结案件训练材料的 intake、脱敏、案由归类、训练样本切分、source trace、audit 和 safety metadata，不执行 Codex 训练，不写训练集，不读取原文。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="intake_status" value={providerCapabilities?.real_closed_case_training_intake_status ?? "real_closed_case_training_intake_metadata_ready"} />
            <MetricTile label="intake_ready" value={String(providerCapabilities?.real_closed_case_training_intake_ready ?? true)} />
            <MetricTile label="redaction_pipeline_ready" value={String(providerCapabilities?.real_closed_case_redaction_pipeline_ready ?? true)} />
            <MetricTile label="classification_ready" value={String(providerCapabilities?.real_closed_case_classification_ready ?? true)} />
            <MetricTile label="sample_segmentation_ready" value={String(providerCapabilities?.real_closed_case_training_sample_segmentation_ready ?? true)} />
            <MetricTile label="source_trace_ready" value={String(providerCapabilities?.real_closed_case_source_trace_ready ?? true)} />
            <MetricTile label="review_queue_ready" value={String(providerCapabilities?.real_closed_case_review_queue_ready ?? true)} />
            <MetricTile label="open_case_training" value={String(!(providerCapabilities?.real_closed_case_open_case_training_disabled ?? true))} />
            <MetricTile label="raw_content_blocked" value={String(providerCapabilities?.real_closed_case_raw_content_blocked ?? true)} />
            <MetricTile label="ready_for_codex_training" value={String(providerCapabilities?.real_closed_case_ready_for_codex_training ?? false)} />
            <MetricTile label="skill_published" value="false" />
            <MetricTile label="external_delivery" value="false" />
          </div>
        </section>

        <section className="rounded-md border border-cyan-200 bg-cyan-50 p-5 text-cyan-950 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide">v7.31b / v7.31c / v7.31d / v7.31e / v7.31f Skill Experience Pipeline</div>
          <h2 className="mt-2 text-lg font-semibold">受控经验候选、Skill 草案、版本化 Package、内部训练经验包与加载前复核</h2>
          <p className="mt-2 text-sm leading-6">
            v7.31b 负责 OCR/文档解析、法律检索、脱敏经验候选和人工复核；v7.31c 形成 Skill Experience Pool 并生成待人工确认的 Codex Skill 草案；v7.31d 将已确认草案封装为版本化 package 并执行系统校验；v7.31e 从 system_validated package 构建内部训练任务和经验包；v7.31f 提供实战加载前律师复核与经验编辑。全程不发布 Skill、不调用 provider、不触发真实训练。
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <MetricTile label="draft_builder_status" value={providerCapabilities?.codex_skill_draft_builder_status ?? "codex_skill_draft_builder_metadata_ready"} />
            <MetricTile label="builder_ready" value={String(providerCapabilities?.codex_skill_draft_builder_ready ?? true)} />
            <MetricTile label="eligible_selection_ready" value={String(providerCapabilities?.codex_skill_draft_eligible_sample_selection_ready ?? true)} />
            <MetricTile label="draft_generation_ready" value={String(providerCapabilities?.codex_skill_draft_generation_ready ?? true)} />
            <MetricTile label="manual_review_ready" value={String(providerCapabilities?.codex_skill_draft_manual_review_ready ?? true)} />
            <MetricTile label="source_trace_ready" value={String(providerCapabilities?.codex_skill_draft_source_trace_ready ?? true)} />
            <MetricTile label="audit_ready" value={String(providerCapabilities?.codex_skill_draft_audit_ready ?? true)} />
            <MetricTile label="not_publishable" value={String(providerCapabilities?.codex_skill_draft_not_publishable ?? true)} />
            <MetricTile label="provider_call" value={String(!(providerCapabilities?.codex_skill_draft_provider_call_disabled ?? true))} />
            <MetricTile label="raw_content_blocked" value={String(providerCapabilities?.codex_skill_draft_raw_content_blocked ?? true)} />
            <MetricTile label="api_key_read" value={String(!(providerCapabilities?.codex_skill_draft_api_key_read_disabled ?? true))} />
            <MetricTile label="internal_training_status" value={providerCapabilities?.internal_training_experience_package_status ?? "internal_training_experience_package_metadata_ready"} />
            <MetricTile label="task_builder_ready" value={String(providerCapabilities?.internal_training_task_builder_ready ?? true)} />
            <MetricTile label="experience_package_builder_ready" value={String(providerCapabilities?.internal_experience_package_builder_ready ?? true)} />
            <MetricTile label="pending_practice_review" value={String(providerCapabilities?.internal_training_pending_practice_review_ready ?? true)} />
            <MetricTile label="real_training" value={String(!(providerCapabilities?.internal_training_real_training_disabled ?? true))} />
            <MetricTile label="skill_publish" value={String(!(providerCapabilities?.internal_training_skill_publish_disabled ?? true))} />
            <MetricTile label="practice_load_review" value={providerCapabilities?.practice_load_review_status ?? "practice_load_review_gate_metadata_ready"} />
            <MetricTile label="lawyer_editor_ready" value={String(providerCapabilities?.lawyer_experience_editor_ready ?? true)} />
            <MetricTile label="revalidation_ready" value={String(providerCapabilities?.practice_load_revalidation_ready ?? true)} />
            <MetricTile label="runtime_loading_deferred" value={String(providerCapabilities?.practice_runtime_loading_deferred_to_v731g ?? true)} />
            <MetricTile label="external_delivery" value="false" />
          </div>
        </section>

        <section className="grid gap-6 xl:grid-cols-[1fr_0.9fr]">
          <Panel title="受控工作流 Stepper">
            <ShowcaseStepper
              columns="md:grid-cols-3 xl:grid-cols-5"
              steps={workflowSteps.map((step) => ({
                label: step,
                detail: "受控运行 · 律师复核",
                status: "模拟元数据"
              }))}
            />
          </Panel>

          <Panel title="安全与信任摘要">
            <div className="grid gap-2">
              {safetyMessages.map((message) => (
                <div key={message} className="flex items-center justify-between rounded-md border border-line bg-white px-3 py-2">
                  <span className="text-sm text-ink">{message}</span>
                  <StatusBadge tone="safe" label="已启用" />
                </div>
              ))}
            </div>
            <div className="mt-4 grid gap-2 text-xs text-muted">
              <span>personal_production_mode: {mode?.personal_production_mode ?? "controlled_ready"}</span>
              <span>manual_final_lock_required: {String(mode?.manual_final_lock_required ?? true)}</span>
              <span>next_action: {readiness?.next_action ?? "v7.11_personal_production_stability_local_pilot_hardening"}</span>
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
          <Panel title="个人版路线总览">
            <div className="grid gap-3">
              {[
                "v7.1 AI Provider Gateway & Prompt Runtime",
                "v7.2 Controlled Material Parsing & PaddleOCR Runtime",
                "v7.3 Legal & Enterprise Intelligence Gateway",
                "v7.4 Experience Package Skill Studio",
                "v7.5 Real Case Production Workflow",
                "v7.6 Personal Delivery Packet",
                "v7.7 Personal Production Pilot & Showcase Pack",
                "v7.8 UI Polish & Showcase Hardening",
                "v7.9 Personal Production Demo Script & Screenshot Pack",
                ...nextRoute
              ].map((step) => (
                <div key={step} className="rounded-md border border-line bg-white px-4 py-3 text-sm font-medium text-ink">
                  {step}
                  {step.includes("v7.31a") ? <span className="ml-2 text-xs text-emerald-700">已完成</span> : null}
                  {step.includes("v7.31b") ? <span className="ml-2 text-xs text-emerald-700">已接入</span> : null}
                  {step.includes("v7.31c") ? <span className="ml-2 text-xs text-emerald-700">已接入</span> : null}
                  {step.includes("v7.31d") ? <span className="ml-2 text-xs text-emerald-700">已接入</span> : null}
                  {step.includes("v7.31e") ? <span className="ml-2 text-xs text-emerald-700">已接入</span> : null}
                  {step.includes("v7.31f") ? <span className="ml-2 text-xs text-emerald-700">已接入</span> : null}
                  {step.includes("后置") || step.includes("deferred") ? <span className="ml-2 text-xs text-amber-700">未进入</span> : null}
                </div>
              ))}
            </div>
          </Panel>

          <TrustSafetyPanel items={safetyMessages} />
        </section>

        <Panel title="开发诊断（默认折叠）">
          <DiagnosticsPanel
            data={{
              status,
              mode,
              showcase,
              runtime_registry: runtimeRegistry,
              provider_capabilities: providerCapabilities,
              readiness,
              safety,
              console_summary: consoleSummary
            }}
          />
        </Panel>
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
        <div className="text-xl font-semibold text-ink">{ready ? "已就绪" : "待确认"}</div>
        <StatusBadge tone={ready ? "safe" : "preview"} label={ready ? "通过" : "预览"} />
      </div>
    </div>
  );
}

function MetricTile({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-cyan-200 bg-white px-3 py-2">
      <div className="text-xs font-medium text-cyan-700">{label}</div>
      <div className="mt-1 break-words text-sm font-semibold text-ink">{value}</div>
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
        {runtime.category === "skill_studio" ? <span>Skill Studio 草稿状态: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {runtime.category === "case_production" ? <span>Case Production controlled: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {runtime.category === "case_analysis" ? <span>Case Analysis 草稿状态: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {runtime.category === "production_pilot" ? <span>Owner download only: {String(Boolean(runtime.gateway_registered))}</span> : null}
        {runtime.category === "delivery_packet" ? <span>Delivery Packet 仅元数据: {String(Boolean(runtime.gateway_registered))}</span> : null}
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
