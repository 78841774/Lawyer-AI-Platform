"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DarkSafetyBadge,
  DiagnosticsPanel,
  InfoRows,
  RuntimeCard,
  SafeErrorNotice,
  ShowcaseStepper,
  StatusCard,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  createPersonalProductionPilotOwnerDownload,
  createPersonalProductionPilotOutput,
  createPersonalProductionPilotRun,
  getPersonalCaseWorkspaceFactInputReadiness,
  getPersonalCaseWorkspaceFactPreviewQuality,
  getPersonalCaseAnalysisLegalDraftQuality,
  getPersonalProductionPilotAudit,
  getPersonalProductionPilotCaseAnalysisSummary,
  getPersonalProductionPilotDashboardMetrics,
  getPersonalProductionPilotDashboardQuality,
  getPersonalProductionPilotDashboardSafety,
  getPersonalProductionPilotDashboardStatus,
  getPersonalProductionPilotExportBoundary,
  getPersonalProductionPilotProviderGates,
  getPersonalProductionPilotReadiness,
  getPersonalProductionPilotReviewQueue,
  getPersonalProductionPilotSafety,
  getPersonalProductionPilotStatus,
  getPersonalProductionPilotWorkflow,
  getPersonalOwnerOutputCenterStatus,
  getPersonalTrialReadinessStatus,
  getPersonalTrialReadinessChecklist,
  getPersonalTrialReadinessSafety,
  listPersonalTrialReadinessTrials,
  listPersonalTrialReadinessIssues,
  listPersonalTrialReadinessOptimizationBacklog,
  getPersonalProviderReadinessStatus,
  listPersonalProviderReadinessProviders,
  listPersonalProviderReadinessCategories,
  listPersonalProviderReadinessLiveGates,
  getPersonalMaterialLiveStatus,
  getPersonalMaterialLiveProviders,
  getPersonalMaterialLiveSafety,
  listPersonalMaterialLiveGates,
  getPersonalLiveConnectionStatus,
  listPersonalLiveConnectionProviders,
  getPersonalLiveConnectionAudit,
  getPersonalLiveConnectionSafety,
  getPersonalLegalEnterpriseStatus,
  listPersonalLegalEnterpriseProviders,
  getPersonalLegalEnterpriseReviewQueue,
  getPersonalLegalEnterpriseSourceTraces,
  getPersonalTrainingArtifactStatus,
  getPersonalTrainingArtifactCaseCauseTaxonomy,
  listPersonalTrainingArtifactPackages,
  listPersonalTrainingArtifactSkills,
  listPersonalTrainingArtifactLoadDryRuns,
  listPersonalTrainingArtifactSkillContexts,
  getPersonalTrainingArtifactSafety,
  listPersonalCodexTrainingRuns,
  getPersonalRealClosedCaseIntakeStatus,
  listPersonalRealClosedCaseIntakes,
  listPersonalSkillFinalDrafts,
  listPersonalOwnerOutputCenterDownloads,
  listPersonalOwnerOutputCenterOutputs,
  listPersonalProductionPilotOutputs,
  listPersonalProductionPilotOwnerDownloads,
  listPersonalProductionPilotRuntimes,
  listPersonalProductionPilotRuns,
  listPersonalProductionPilotSkillFinalDrafts,
  listPersonalCaseWorkspaceFactPreviews,
  listPersonalCaseAnalysisLegalDrafts,
  listPersonalProductionPilotSourceTraces,
  submitPersonalProductionPilotReviewAction
} from "@/services/api";

const reviewActions = ["approve_owner_download_metadata", "request_revision", "mark_low_confidence", "mark_not_ready", "reject"];

export default function PersonalProductionPilotPage() {
  const [data, setData] = useState<Record<string, any>>({});
  const [error, setError] = useState("");
  const [confirmed, setConfirmed] = useState(true);
  const [caseId, setCaseId] = useState("open_case_pilot_mock_001");
  const [caseAlias, setCaseAlias] = useState("未结案件实战 Pilot 样本");
  const [outputId, setOutputId] = useState("");
  const [downloadFormat, setDownloadFormat] = useState("Markdown");
  const [reviewAction, setReviewAction] = useState("request_revision");

  async function loadPilot() {
    setError("");
    try {
      const [
        status,
        readiness,
        workflow,
        runtimes,
        providerGates,
        safety,
        runs,
        summary,
        skills,
        outputs,
        downloads,
        queue,
        traces,
        audit,
        exportBoundary,
        dashboardStatus,
        dashboardMetrics,
        dashboardQuality,
        dashboardSafety,
        factPreviews,
        factInputReadiness,
        factPreviewQuality,
        legalDrafts,
        legalDraftQuality,
        skillStudioFinalDrafts,
        ownerOutputCenterStatus,
        ownerOutputCenterOutputs,
        ownerOutputCenterDownloads,
        trialReadinessStatus,
        trialReadinessChecklist,
        trialReadinessSafety,
        trialReadinessTrials,
        trialReadinessIssues,
        trialReadinessBacklog,
        providerReadinessStatus,
        providerReadinessProviders,
        providerReadinessCategories,
        providerReadinessLiveGates,
        materialLiveStatus,
        materialLiveProviders,
        materialLiveSafety,
        materialLiveGates,
        liveConnectionStatus,
        liveConnectionProviders,
        liveConnectionAudit,
        liveConnectionSafety,
        legalEnterpriseStatus,
        legalEnterpriseProviders,
        legalEnterpriseReviewQueue,
        legalEnterpriseSourceTraces,
        trainingArtifactStatus,
        trainingArtifactTaxonomy,
        trainingArtifactPackages,
        trainingArtifactSkills,
        trainingArtifactDryRuns,
        trainingArtifactSkillContexts,
        trainingArtifactSafety,
        codexTrainingRuns,
        realClosedCaseIntakeStatus,
        realClosedCaseIntakes
      ] =
        await Promise.all([
          getPersonalProductionPilotStatus(),
          getPersonalProductionPilotReadiness(),
          getPersonalProductionPilotWorkflow(),
          listPersonalProductionPilotRuntimes(),
          getPersonalProductionPilotProviderGates(),
          getPersonalProductionPilotSafety(),
          listPersonalProductionPilotRuns(),
          getPersonalProductionPilotCaseAnalysisSummary(),
          listPersonalProductionPilotSkillFinalDrafts(),
          listPersonalProductionPilotOutputs(),
          listPersonalProductionPilotOwnerDownloads(),
          getPersonalProductionPilotReviewQueue(),
          listPersonalProductionPilotSourceTraces(),
          getPersonalProductionPilotAudit(),
          getPersonalProductionPilotExportBoundary(),
          getPersonalProductionPilotDashboardStatus(),
          getPersonalProductionPilotDashboardMetrics(),
          getPersonalProductionPilotDashboardQuality(),
          getPersonalProductionPilotDashboardSafety(),
          listPersonalCaseWorkspaceFactPreviews(),
          getPersonalCaseWorkspaceFactInputReadiness(),
          getPersonalCaseWorkspaceFactPreviewQuality("fact_preview_mock_001"),
          listPersonalCaseAnalysisLegalDrafts(),
          getPersonalCaseAnalysisLegalDraftQuality("legal_analysis_draft_mock_001").catch(() => ({})),
          listPersonalSkillFinalDrafts(),
          getPersonalOwnerOutputCenterStatus(),
          listPersonalOwnerOutputCenterOutputs(),
          listPersonalOwnerOutputCenterDownloads(),
          getPersonalTrialReadinessStatus(),
          getPersonalTrialReadinessChecklist(),
          getPersonalTrialReadinessSafety(),
          listPersonalTrialReadinessTrials(),
          listPersonalTrialReadinessIssues(),
          listPersonalTrialReadinessOptimizationBacklog(),
          getPersonalProviderReadinessStatus(),
          listPersonalProviderReadinessProviders(),
          listPersonalProviderReadinessCategories(),
          listPersonalProviderReadinessLiveGates(),
          getPersonalMaterialLiveStatus(),
          getPersonalMaterialLiveProviders(),
          getPersonalMaterialLiveSafety(),
          listPersonalMaterialLiveGates(),
          getPersonalLiveConnectionStatus(),
          listPersonalLiveConnectionProviders(),
          getPersonalLiveConnectionAudit(),
          getPersonalLiveConnectionSafety(),
          getPersonalLegalEnterpriseStatus(),
          listPersonalLegalEnterpriseProviders(),
          getPersonalLegalEnterpriseReviewQueue(),
          getPersonalLegalEnterpriseSourceTraces(),
          getPersonalTrainingArtifactStatus(),
          getPersonalTrainingArtifactCaseCauseTaxonomy(),
          listPersonalTrainingArtifactPackages(),
          listPersonalTrainingArtifactSkills(),
          listPersonalTrainingArtifactLoadDryRuns(),
          listPersonalTrainingArtifactSkillContexts(),
          getPersonalTrainingArtifactSafety(),
          listPersonalCodexTrainingRuns(),
          getPersonalRealClosedCaseIntakeStatus(),
          listPersonalRealClosedCaseIntakes()
        ]);
      setData({
        status,
        readiness,
        workflow,
        runtimes,
        providerGates,
        safety,
        runs,
        summary,
        skills,
        outputs,
        downloads,
        queue,
        traces,
        audit,
        exportBoundary,
        dashboardStatus,
        dashboardMetrics,
        dashboardQuality,
        dashboardSafety,
        factPreviews,
        factInputReadiness,
        factPreviewQuality,
        legalDrafts,
        legalDraftQuality,
        skillStudioFinalDrafts,
        ownerOutputCenterStatus,
        ownerOutputCenterOutputs,
        ownerOutputCenterDownloads,
        trialReadinessStatus,
        trialReadinessChecklist,
        trialReadinessSafety,
        trialReadinessTrials,
        trialReadinessIssues,
        trialReadinessBacklog,
        providerReadinessStatus,
        providerReadinessProviders,
        providerReadinessCategories,
        providerReadinessLiveGates,
        materialLiveStatus,
        materialLiveProviders,
        materialLiveSafety,
        materialLiveGates,
        liveConnectionStatus,
        liveConnectionProviders,
        liveConnectionAudit,
        liveConnectionSafety,
        legalEnterpriseStatus,
        legalEnterpriseProviders,
        legalEnterpriseReviewQueue,
        legalEnterpriseSourceTraces,
        trainingArtifactStatus,
        trainingArtifactTaxonomy,
        trainingArtifactPackages,
        trainingArtifactSkills,
        trainingArtifactDryRuns,
        trainingArtifactSkillContexts,
        trainingArtifactSafety,
        codexTrainingRuns,
        realClosedCaseIntakeStatus,
        realClosedCaseIntakes
      });
      setOutputId((current) => current || outputs.outputs?.[0]?.output_id || "");
    } catch {
      setError("个人生产实战 Pilot API 暂不可用。页面保持安全 fallback，不展示密钥值，不调用真实 provider，不显示原始内容。");
    }
  }

  useEffect(() => {
    void loadPilot();
  }, []);

  async function createRun() {
    const result = await createPersonalProductionPilotRun({
      case_id: caseId,
      case_alias: caseAlias,
      workflow_scope: "personal_production_pilot",
      selected_runtime_ids: [],
      explicit_owner_confirmation: confirmed,
      explicit_provider_gated_confirmation: confirmed,
      explicit_no_external_delivery_confirmation: confirmed,
      explicit_no_training_data_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed
    });
    setOutputId(result.output_ids?.[0] ?? "");
    await loadPilot();
  }

  async function createOutput() {
    const result = await createPersonalProductionPilotOutput({
      run_id: null,
      output_type: "case_analysis_draft",
      title: "案件分析草稿",
      format: downloadFormat,
      explicit_owner_confirmation: confirmed,
      explicit_no_external_delivery_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed
    });
    setOutputId(result.output_id);
    await loadPilot();
  }

  async function createOwnerDownload() {
    if (!outputId) return;
    await createPersonalProductionPilotOwnerDownload(outputId, {
      requested_format: downloadFormat,
      explicit_owner_confirmation: confirmed,
      explicit_no_public_link_confirmation: confirmed,
      explicit_no_email_confirmation: confirmed,
      explicit_no_external_delivery_confirmation: confirmed
    });
    await loadPilot();
  }

  async function submitReview() {
    const reviewItemId = data.queue?.review_items?.[0]?.review_item_id;
    if (!reviewItemId) return;
    await submitPersonalProductionPilotReviewAction(reviewItemId, {
      action: reviewAction,
      reviewer_id: "local_demo_lawyer",
      reviewer_note: "仅更新 owner-download pilot review metadata",
      explicit_lawyer_confirmation: confirmed,
      explicit_no_external_delivery_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed
    });
    await loadPilot();
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}
        <section className="rounded-md border border-slate-800 bg-[#1d2228] p-8 text-white">
          <div className="text-sm font-medium text-cyan-200">v7.19 Personal Production Pilot Dashboard Enhancement</div>
          <h1 className="mt-3 text-4xl font-semibold">个人生产实战 Pilot Dashboard</h1>
          <p className="mt-4 max-w-4xl text-sm leading-6 text-slate-300">
            串联 AI / OCR / 法律检索 / 企业信息 / Skill / 案件分析 / 交付包与案件材料工作台的个人版实战 Pilot。Dashboard 仅展示质量评分、门控、优化建议和安全边界 metadata，不自动外发、不公开链接、不定性为最终法律意见。
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            {["质量评分仅参考", "live 默认关闭", "用户本人下载", "不自动外发", "不公开链接", "不生成最终法律意见"].map((badge) => (
              <DarkSafetyBadge key={badge} label={badge} />
            ))}
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-4">
          <StatusCard label="Pilot" value={data.readiness?.pilot_ready ?? true} detail="ready / gated / owner-download-only" />
          <StatusCard label="Provider" value="disabled" detail="external provider requires confirmation" tone="warning" />
          <StatusCard label="Dashboard" value={data.dashboardStatus?.dashboard_ready ?? true} detail="quality score / gate / suggestions" tone="safe" />
          <StatusCard label="Avg Score" value={data.dashboardQuality?.average_quality_score ?? "81.7"} detail="reference-only, not final quality guarantee" tone="info" />
        </section>

        <Panel title="Pilot Dashboard Overview">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Review Queue" value={data.dashboardMetrics?.review_queue?.pending_count ?? data.queue?.pending_count ?? 0} detail="pending lawyer review" tone="warning" />
            <StatusCard label="Source Trace" value={data.dashboardMetrics?.source_trace_summary?.total ?? data.traces?.source_trace_count ?? 0} detail="confirmed / unconfirmed visible" tone="info" />
            <StatusCard label="Owner Download" value={data.dashboardMetrics?.export_boundary?.owner_download_ready ?? true} detail="gated dry-run default" tone="safe" />
            <StatusCard label="External Boundary" value={String(data.dashboardMetrics?.export_boundary?.external_delivery_triggered ?? false)} detail="email=false / public_link=false" tone="safe" />
          </div>
        </Panel>

        <Panel title="v7.20 Fact Preview / Correction Readiness">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Fact Preview" value={data.factPreviews?.fact_preview_count ?? 0} detail="事实预览 draft metadata" tone="info" />
            <StatusCard label="Fact Score" value={data.factPreviewQuality?.overall_score ?? 82} detail="reference-only, not final fact finding" tone="safe" />
            <StatusCard label="Input Ready" value={data.factInputReadiness?.readiness_count ?? 0} detail="进入法律分析需显式确认" tone="warning" />
            <StatusCard label="Auto Legal Analysis" value={String(data.factInputReadiness?.legal_analysis_auto_triggered ?? false)} detail="legal_analysis_auto_triggered=false" tone="safe" />
          </div>
          <div className="mt-4 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
            Pilot Dashboard 可以展示事实草稿质量、用户纠正和输入准备度；这些值仅为模拟元数据，不生成最终事实认定、不自动创建法律分析、不写训练集。
          </div>
        </Panel>

        <Panel title="v7.21 Legal Analysis Draft Readiness">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Legal Drafts" value={data.legalDrafts?.draft_count ?? 0} detail="法律分析草稿 metadata" tone="info" />
            <StatusCard label="Draft Score" value={data.legalDraftQuality?.overall_score ?? "pending"} detail="reference-only" tone="safe" />
            <StatusCard label="Final Opinion" value="blocked" detail="final_legal_opinion_generated=false" tone="safe" />
            <StatusCard label="Final Report" value="blocked" detail="final_report_generated=false" tone="safe" />
          </div>
          <div className="mt-4 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
            Pilot Dashboard 仅展示法律分析草稿 readiness 和质量参考，不生成最终法律意见、正式报告、真实文件或外部交付。
          </div>
        </Panel>

        <Panel title="v7.22 Skill Final Draft Readiness">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Final Drafts" value={data.skillStudioFinalDrafts?.draft_count ?? 0} detail="两个 Skill final draft metadata" tone="info" />
            <StatusCard label="Baseline Complete" value={String(data.skillStudioFinalDrafts?.baseline_complete ?? false)} detail="缺失时返回 missing_baseline_report" tone="warning" />
            <StatusCard label="Owner Download" value={String(data.skillStudioFinalDrafts?.downloadable_by_owner_only ?? true)} detail="owner-only metadata" tone="safe" />
            <StatusCard label="Auto Publish" value={String(data.skillStudioFinalDrafts?.skill_auto_published ?? false)} detail="skill_auto_published=false" tone="safe" />
          </div>
          <div className="mt-4 rounded-md border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs leading-5 text-emerald-900">
            两个 Skill 最终稿仅汇总既有 Skill / evaluation / gate / test case metadata，不自动发布 Skill，不训练未结案件，不创建公开链接或外部交付。
          </div>
        </Panel>

        <Panel title="v7.23 用户本人产出下载中心 Readiness">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Output Center" value={String(data.ownerOutputCenterStatus?.output_center_ready ?? true)} detail="owner-only output center ready" tone="safe" />
            <StatusCard label="Outputs" value={data.ownerOutputCenterOutputs?.output_count ?? 0} detail="Skill / Fact / Legal / Pilot" tone="info" />
            <StatusCard label="Owner Downloads" value={data.ownerOutputCenterDownloads?.download_count ?? 0} detail="仅用户本人下载 metadata" tone="safe" />
            <StatusCard label="External Delivery" value={String(data.ownerOutputCenterStatus?.external_delivery_triggered ?? false)} detail="external_delivery_triggered=false" tone="safe" />
          </div>
          <div className="mt-4 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
            v7.23 将 Skill 最终稿、事实产出、法律分析草稿、Pilot / Delivery 草稿集中到用户本人产出下载中心；gate 仅作为质量评分和优化建议，不阻断用户本人下载。
          </div>
        </Panel>

        <Panel title="v7.25 个人版实战试运行准备">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Trial Readiness" value={String(data.trialReadinessStatus?.trial_readiness_ready ?? true)} detail="进入真实办案前试运行 metadata" tone="safe" />
            <StatusCard label="Trial Sessions" value={data.trialReadinessTrials?.trial_count ?? 1} detail="owner-only / metadata-only" tone="info" />
            <StatusCard label="Checklist" value={data.trialReadinessChecklist?.checked_item_count ?? 12} detail="12 项路径检查" tone="safe" />
            <StatusCard label="Issue Log" value={data.trialReadinessIssues?.issue_count ?? 0} detail="只用于优化，不阻断下一步" tone="warning" />
          </div>
          <div className="mt-4 rounded-md border border-slate-300 bg-slate-50 px-3 py-2 text-xs leading-5 text-slate-900">
            v7.25 记录 trial session、checklist、observation、issue log、quality review、safety confirmation 与 optimization backlog；不读取真实案件原文、不调用真实 provider、不训练未结案件、不自动发布 Skill、不自动对外交付。
          </div>
        </Panel>

        <Panel title="v7.26 真实接口接入准备">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Provider Readiness" value={String(data.providerReadinessStatus?.provider_readiness_ready ?? true)} detail="registry / boundary / gate" tone="safe" />
            <StatusCard label="Providers" value={data.providerReadinessProviders?.provider_count ?? 13} detail="AI / OCR / Document / Legal / Enterprise" tone="info" />
            <StatusCard label="Live Gates" value={data.providerReadinessLiveGates?.live_gate_count ?? 0} detail="live_call_allowed=false" tone="warning" />
            <StatusCard label="Real Calls" value={String(data.providerReadinessStatus?.real_provider_calls_still_disabled ?? true)} detail="真实 provider 仍关闭" tone="safe" />
          </div>
          <div className="mt-4 rounded-md border border-violet-200 bg-violet-50 px-3 py-2 text-xs leading-5 text-violet-900">
            v7.26 只做真实接口接入前 readiness：key_loaded 只返回 boolean，不读取密钥值；dry-run health 不访问 provider network；Pilot 仍不上传案件材料、不训练、不生成最终法律意见或正式报告。
          </div>
        </Panel>

        <Panel title="v7.27 OCR / Document Provider 接入准备">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Material Live" value={String(data.materialLiveStatus?.metadata_only ?? true)} detail="metadata-only / draft-only" tone="safe" />
            <StatusCard label="Providers" value={data.materialLiveProviders?.provider_count ?? 4} detail="PaddleOCR / MinerU / Docling" tone="info" />
            <StatusCard label="Live Gates" value={data.materialLiveGates?.live_gate_count ?? 0} detail="blocked_by_default" tone="warning" />
            <StatusCard label="Live Allowed" value={String(data.materialLiveStatus?.live_call_allowed ?? false)} detail="live_call_allowed=false" tone="safe" />
          </div>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <StatusCard label="Raw OCR" value={String(data.materialLiveStatus?.raw_ocr_text_exposed ?? false)} detail="raw_ocr_text_exposed=false" tone="safe" />
            <StatusCard label="Raw Document" value={String(data.materialLiveStatus?.raw_document_content_exposed ?? false)} detail="raw_document_content_exposed=false" tone="safe" />
            <StatusCard label="AI Prompt" value={String(data.materialLiveStatus?.ai_prompt_injected ?? false)} detail="不自动进入 AI Prompt" tone="safe" />
          </div>
          <div className="mt-4 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
            v7.27 只做 OCR / 文档 Provider live connection metadata：dry-run 默认开启，health check 不访问网络，不上传材料，不生成最终 PDF/DOCX，不生成最终法律意见或报告。
          </div>
        </Panel>

        <Panel title="v7.28 个人生产受控接口接入">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Live Connection" value={String(data.liveConnectionStatus?.live_connection_ready ?? true)} detail="AI / OCR / Legal / Enterprise" tone="safe" />
            <StatusCard label="Providers" value={data.liveConnectionProviders?.provider_count ?? 0} detail="统一 provider readiness" tone="info" />
            <StatusCard label="Dry-run Ready" value={data.liveConnectionStatus?.dry_run_ready_count ?? 0} detail="dry-run 默认开启" tone="safe" />
            <StatusCard label="Network Call" value={String(data.liveConnectionStatus?.network_call_executed ?? false)} detail="network_call_executed=false" tone="safe" />
          </div>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <StatusCard label="Audit" value={data.liveConnectionAudit?.event_count ?? 0} detail="metadata-only audit" tone="info" />
            <StatusCard label="Safety" value={String(data.liveConnectionSafety?.all_safety_checks_passed ?? true)} detail="Trust / Safety ready" tone="safe" />
            <StatusCard label="External Delivery" value={String(data.liveConnectionStatus?.external_delivery_triggered ?? false)} detail="不自动对外交付" tone="safe" />
          </div>
        </Panel>

        <Panel title="v7.29 法律与企业信息 API 受控接入">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Legal Gateway" value={String(data.legalEnterpriseStatus?.legal_gateway_ready ?? true)} detail="法律检索 dry-run metadata" tone="safe" />
            <StatusCard label="Enterprise Gateway" value={String(data.legalEnterpriseStatus?.enterprise_gateway_ready ?? true)} detail="企业信息 verification metadata" tone="safe" />
            <StatusCard label="Providers" value={data.legalEnterpriseProviders?.provider_count ?? 0} detail="legal / enterprise providers" tone="info" />
            <StatusCard label="Review Queue" value={data.legalEnterpriseReviewQueue?.item_count ?? 0} detail="律师复核必需" tone="warning" />
          </div>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <StatusCard label="Source Trace" value={data.legalEnterpriseSourceTraces?.source_trace_count ?? 0} detail="结果进入 source trace" tone="safe" />
            <StatusCard label="Final Citation" value="false" detail="不自动选择最终引用" tone="safe" />
            <StatusCard label="Final Fact Finding" value={String(data.legalEnterpriseStatus?.final_fact_finding ?? false)} detail="不自动形成最终事实认定" tone="safe" />
          </div>
        </Panel>

        <Panel title="v7.30 Codex 训练产物加载器">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Training Artifacts" value={String(data.trainingArtifactStatus?.training_artifact_loader_ready ?? true)} detail="loader metadata ready" tone="safe" />
            <StatusCard label="Case Cause Taxonomy" value={data.trainingArtifactTaxonomy?.node_count ?? 0} detail="multi-level case cause" tone="info" />
            <StatusCard label="Packages" value={data.trainingArtifactPackages?.artifact_count ?? 0} detail="exact / fallback / overlay" tone="info" />
            <StatusCard label="Load Dry-runs" value={data.trainingArtifactDryRuns?.run_count ?? 0} detail="load_executed=false" tone="safe" />
          </div>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <StatusCard label="Skill Manifests" value={data.trainingArtifactSkills?.artifact_count ?? 0} detail="fact + legal Skill metadata" tone="safe" />
            <StatusCard label="Skill Context" value={data.trainingArtifactSkillContexts?.skill_context_count ?? 0} detail="loaded skill metadata dry-run" tone="safe" />
            <StatusCard label="Open Case Training" value={String(data.trainingArtifactStatus?.open_case_data_used ?? false)} detail="open_case_data_used=false" tone="safe" />
          </div>
          <div className="mt-4 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
            Pilot 仅展示 v7.30 训练产物 readiness 和案由匹配 dry-run 状态；不训练未结案件，不执行模型微调，不更新或自动发布 Skill。
          </div>
        </Panel>

        <Panel title="v7.31 已结案件 Codex 训练执行">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Training Runs" value={data.codexTrainingRuns?.run_count ?? 0} detail="synthetic closed-case metadata" tone="info" />
            <StatusCard label="Closed Case Only" value={String(data.codexTrainingRuns?.closed_case_only ?? true)} detail="open_case_data_used=false" tone="safe" />
            <StatusCard label="Fine Tune" value={String(data.codexTrainingRuns?.fine_tune_model_training ?? false)} detail="Codex 训练不是模型微调" tone="safe" />
            <StatusCard label="Skill Publish" value={String(data.codexTrainingRuns?.skill_published ?? false)} detail="skill_published=false" tone="safe" />
          </div>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <StatusCard label="Experience Packages" value={data.codexTrainingRuns?.training_runs?.[0]?.experience_packages?.length ?? 0} detail="generated metadata packages" tone="info" />
            <StatusCard label="Generated Skills" value={data.codexTrainingRuns?.training_runs?.[0]?.generated_skills?.length ?? 0} detail="fact + legal Skill manifests" tone="safe" />
            <StatusCard label="Loader Dry-run" value={String(data.codexTrainingRuns?.training_runs?.[0]?.load_dry_run_result?.load_executed ?? false)} detail="load_executed=false" tone="safe" />
          </div>
          <div className="mt-4 rounded-md border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs leading-5 text-emerald-900">
            v7.31 仅生成训练执行 metadata 与加载清单；synthetic closed-case samples 不被表述为真实案件，不写训练集，不更新或自动发布 Skill。
          </div>
        </Panel>

        <Panel title="v7.31a 真实已结案件训练材料导入与脱敏">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Intake Ready" value={String(data.realClosedCaseIntakeStatus?.intake_pipeline_ready ?? true)} detail="real_closed_case_intake=true" tone="safe" />
            <StatusCard label="Redaction" value={String(data.realClosedCaseIntakeStatus?.redaction_pipeline_ready ?? true)} detail="脱敏管线 metadata ready" tone="safe" />
            <StatusCard label="Classification" value={String(data.realClosedCaseIntakeStatus?.case_cause_classification_ready ?? true)} detail="多层级案由归类" tone="info" />
            <StatusCard label="Ready For Training" value={String(data.realClosedCaseIntakeStatus?.ready_for_codex_training ?? false)} detail="v7.31a 不执行训练" tone="warning" />
          </div>
          <div className="mt-4 grid gap-3 md:grid-cols-4">
            <StatusCard label="Intakes" value={data.realClosedCaseIntakes?.intake_count ?? 0} detail="owner-only metadata" tone="info" />
            <StatusCard label="Authorization" value={String(data.realClosedCaseIntakes?.intakes?.[0]?.authorization_confirmed ?? true)} detail="authorization_confirmed" tone="safe" />
            <StatusCard label="Closed Case" value={String(data.realClosedCaseIntakes?.intakes?.[0]?.case_closed_confirmed ?? true)} detail="case_closed_confirmed" tone="safe" />
            <StatusCard label="Open Case Used" value={String(data.realClosedCaseIntakeStatus?.open_case_data_used ?? false)} detail="open_case_data_used=false" tone="safe" />
          </div>
          <div className="mt-4 rounded-md border border-sky-200 bg-sky-50 px-3 py-2 text-xs leading-5 text-sky-900">
            Pilot 只展示真实闭案训练材料 intake readiness；原文不返回，未结案件不参与训练，后续 v7.31b 才会进入真实闭案 Codex training。
          </div>
        </Panel>

        <ShowcaseStepper
          columns="lg:grid-cols-4"
          steps={(data.workflow?.steps ?? []).map((step: any) => ({
            label: step.display_name,
            detail: `${step.target_runtime_id} · ${step.stage}`,
            status: step.status
          }))}
        />

        <section className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
          <Panel title="创建 Pilot Run">
            <div className="grid gap-3">
              <Text label="Open Case ID" value={caseId} onChange={setCaseId} />
              <Text label="案件代号" value={caseAlias} onChange={setCaseAlias} />
              <Confirm checked={confirmed} onChange={setConfirmed} />
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void createRun()}>
                创建实战 Pilot metadata
              </button>
            </div>
          </Panel>
          <Panel title="Provider Gate Summary">
            <div className="grid gap-3 md:grid-cols-2">
              {(data.providerGates?.provider_gates ?? []).map((gate: any) => (
                <RuntimeCard
                  key={gate.provider_id}
                  title={gate.display_name}
                  category={gate.category}
                  status={gate.live_enabled ? "live" : "disabled"}
                  items={[
                    ["dry_run_ready", gate.dry_run_ready],
                    ["requires_confirmation", gate.external_provider_requires_confirmation],
                    ["api_key_frontend_visible", gate.api_key_frontend_visible],
                    ["adapter_status", gate.adapter_status]
                  ]}
                />
              ))}
            </div>
          </Panel>
        </section>

        <Panel title="Quality Score / Gate / 优化建议">
          <div className="grid gap-4 lg:grid-cols-3">
            {(data.dashboardQuality?.quality_items ?? []).map((item: any) => (
              <div key={item.output_id} className="rounded-md border border-line bg-slate-50 p-5">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold text-ink">{item.title}</div>
                    <div className="mt-1 text-xs text-muted">{item.output_type} · {item.gate_status}</div>
                  </div>
                  <div className="rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-right">
                    <div className="text-xs text-cyan-800">质量评分</div>
                    <div className="text-2xl font-semibold text-cyan-950">{item.quality_score}</div>
                  </div>
                </div>
                <div className="mt-4 rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-xs leading-5 text-amber-900">
                  {item.score_label}；gate_reference_only={String(item.gate_reference_only)}，blocks_next_stage={String(item.blocks_next_stage)}
                </div>
                <div className="mt-4 space-y-2">
                  {(item.optimization_suggestions ?? []).map((suggestion: string) => (
                    <div key={suggestion} className="rounded-md border border-line bg-white px-3 py-2 text-xs leading-5 text-ink">
                      {suggestion}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Panel>

        <Panel title="Skill Final Draft Panel">
          <div className="grid gap-3 md:grid-cols-2">
            {(data.skills?.skill_final_drafts ?? []).map((draft: any) => (
              <RuntimeCard
                key={draft.draft_id}
                title={draft.title}
                category={draft.skill_key}
                status="owner download only"
                items={[
                  ["source_skill_id", draft.source_skill_id],
                  ["owner_download_ready", draft.owner_download_ready],
                  ["publish_action_available", draft.publish_action_available],
                  ["formats", draft.available_formats?.join(" / ")]
                ]}
              />
            ))}
          </div>
        </Panel>

        <Panel title="Skill Studio Final Draft Workbench">
          <div className="grid gap-3 md:grid-cols-2">
            {(data.skillStudioFinalDrafts?.final_drafts ?? []).map((draft: any) => (
              <RuntimeCard
                key={draft.skill_id}
                title={draft.skill_name}
                category={draft.skill_type}
                status={draft.gate_status}
                items={[
                  ["quality_score", draft.quality_score],
                  ["baseline_complete", draft.baseline_complete],
                  ["downloadable_by_owner_only", draft.downloadable_by_owner_only],
                  ["final_skill_published", draft.final_skill_published],
                  ["writes_to_training_set", draft.writes_to_training_set]
                ]}
              />
            ))}
          </div>
        </Panel>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="Case Analysis Output / 办案辅助文档">
            <div className="grid gap-3">
              <InfoRows
                rows={[
                  ["事实部分", "事实预览与纠正稿，可用户本人查看和下载，不写训练集"],
                  ["法律分析部分", "法律分析草稿，可用户本人修改和下载，不标记为最终法律意见"],
                  ["output_count", data.outputs?.output_count ?? 0],
                  ["downloadable_by_owner_only", data.outputs?.downloadable_by_owner_only ?? true]
                ]}
              />
              <Text label="Output ID" value={outputId} onChange={setOutputId} />
              <select className="rounded-md border border-line px-3 py-2 text-sm" value={downloadFormat} onChange={(event) => setDownloadFormat(event.target.value)}>
                {["Markdown", "JSON", "PDF draft", "DOCX draft"].map((format) => <option key={format}>{format}</option>)}
              </select>
              <button className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void createOutput()}>
                生成办案辅助文档 metadata
              </button>
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void createOwnerDownload()}>
                生成用户本人下载 metadata
              </button>
            </div>
          </Panel>
          <Panel title="Owner Download Boundary">
            <InfoRows
              rows={[
                ["download_count", data.downloads?.download_count ?? 0],
                ["owner_only", data.downloads?.owner_only ?? true],
                ["public_link_created", data.downloads?.public_link_created ?? false],
                ["email_sent", data.downloads?.email_sent ?? false],
                ["external_delivery_triggered", data.downloads?.external_delivery_triggered ?? false],
                ["third_party_share_enabled", data.downloads?.third_party_share_enabled ?? false],
                ["client_auto_delivery", data.downloads?.client_auto_delivery ?? false]
              ]}
            />
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Runtime Readiness">
            <InfoRows
              rows={[
                ["AI Gateway", data.readiness?.readiness?.ai_gateway_connected ?? true],
                ["OCR / Document Gateway", data.readiness?.readiness?.ocr_document_gateway_connected ?? true],
                ["Legal / Enterprise Gateway", data.readiness?.readiness?.legal_enterprise_gateway_connected ?? true],
                ["Skill Training Runtime", data.readiness?.readiness?.skill_training_runtime_connected ?? true],
                ["Training Artifact Loader", data.trainingArtifactStatus?.training_artifact_loader_ready ?? true],
                ["Case Cause Match Dry-run", data.trainingArtifactStatus?.multi_level_loader_ready ?? true],
                ["Loaded Skill Metadata Dry-run", data.trainingArtifactStatus?.skill_context_dry_run_ready ?? true],
                ["Case Analysis Runtime", data.readiness?.readiness?.case_analysis_runtime_connected ?? true],
                ["Delivery Packet", data.readiness?.readiness?.delivery_packet_connected ?? true],
                ["Owner Output Center", data.readiness?.readiness?.owner_output_center_ready ?? true],
                ["Skill Final Drafts Aggregated", data.readiness?.readiness?.skill_final_drafts_aggregated ?? true],
                ["Fact Outputs Aggregated", data.readiness?.readiness?.fact_outputs_aggregated ?? true],
                ["Legal Drafts Aggregated", data.readiness?.readiness?.legal_drafts_aggregated ?? true],
                ["Owner Download", data.readiness?.readiness?.owner_download_ready ?? true]
              ]}
            />
          </Panel>
          <Panel title="Review Queue">
            <div className="grid gap-3">
              <InfoRows rows={[["pending_count", data.queue?.pending_count ?? 0], ["item_count", data.queue?.item_count ?? 0]]} />
              <select className="rounded-md border border-line px-3 py-2 text-sm" value={reviewAction} onChange={(event) => setReviewAction(event.target.value)}>
                {reviewActions.map((action) => <option key={action}>{action}</option>)}
              </select>
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void submitReview()}>
                提交复核动作
              </button>
            </div>
          </Panel>
          <Panel title="Source Trace Summary">
            <InfoRows
              rows={[
                ["source_trace_count", data.traces?.source_trace_count ?? 0],
                ["raw_content_returned", false],
                ["diagnostics_content_included", false],
                ["raw_content_written_to_regression_output", data.traces?.raw_content_written_to_regression_output ?? false]
              ]}
            />
          </Panel>
        </section>

        <Panel title="Export Boundary">
          <InfoRows
            rows={[
              ["owner_download_enabled", data.exportBoundary?.owner_download_enabled ?? true],
              ["public_share_disabled", data.exportBoundary?.public_share_disabled ?? true],
              ["email_disabled", data.exportBoundary?.email_disabled ?? true],
              ["external_delivery_disabled", data.exportBoundary?.external_delivery_disabled ?? true],
              ["final_labeling_disabled", data.exportBoundary?.final_labeling_disabled ?? true]
            ]}
          />
        </Panel>

        <TrustSafetyPanel
          title="信任与安全面板"
          note="v7.19 Dashboard 统一 12 项安全边界：评分、门控、优化建议全部是 metadata，不生成最终法律意见、最终报告或真实 PDF/DOCX。"
          items={data.dashboardSafety?.safety_checklist ?? data.safety?.safety_checklist ?? []}
        />
        <DiagnosticsPanel data={data} />
      </div>
    </AppShell>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return <section className="rounded-md border border-line bg-white p-5 shadow-sm"><h2 className="text-base font-semibold text-ink">{title}</h2><div className="mt-4">{children}</div></section>;
}

function Text({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return <label className="grid gap-2 text-sm"><span>{label}</span><input className="rounded-md border border-line px-3 py-2" value={value} onChange={(event) => onChange(event.target.value)} /></label>;
}

function Confirm({ checked, onChange }: { checked: boolean; onChange: (value: boolean) => void }) {
  return <label className="flex gap-2 text-sm"><input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />明确确认：用户本人下载、provider gated、不外发、不写训练集、不定性最终法律意见</label>;
}
