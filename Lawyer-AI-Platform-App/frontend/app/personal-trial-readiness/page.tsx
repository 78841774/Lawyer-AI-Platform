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
  ShowcaseStepper,
  StatusCard,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  createPersonalTrialReadinessIssue,
  createPersonalTrialReadinessOptimizationBacklog,
  createPersonalTrialReadinessQuality,
  createPersonalTrialReadinessSafetyConfirmation,
  createPersonalTrialReadinessTrial,
  createPersonalTrialReadinessTrialChecklist,
  getPersonalTrialReadinessAudit,
  getPersonalTrialReadinessChecklist,
  getPersonalTrialReadinessQuality,
  getPersonalTrialReadinessSafety,
  getPersonalTrialReadinessSafetyConfirmation,
  getPersonalTrialReadinessStatus,
  listPersonalTrialReadinessIssues,
  listPersonalTrialReadinessObservations,
  listPersonalTrialReadinessOptimizationBacklog,
  listPersonalTrialReadinessTrials
} from "@/services/api";
import type { IssueLogItem, OptimizationBacklogItem, StageObservation, TrialSession } from "@/types";

export default function PersonalTrialReadinessPage() {
  const [data, setData] = useState<Record<string, any>>({});
  const [selectedTrialId, setSelectedTrialId] = useState("trial_mock_001");
  const [error, setError] = useState("");

  const trials = (data.trials?.trials ?? []) as TrialSession[];
  const selectedTrial = useMemo(
    () => trials.find((trial) => trial.trial_id === selectedTrialId) ?? trials[0],
    [trials, selectedTrialId]
  );
  const trialId = selectedTrial?.trial_id ?? selectedTrialId;

  async function loadReadiness(nextTrialId = selectedTrialId) {
    setError("");
    try {
      const [status, checklist, safety, trialsResponse, allIssues, backlog, audit] = await Promise.all([
        getPersonalTrialReadinessStatus(),
        getPersonalTrialReadinessChecklist(),
        getPersonalTrialReadinessSafety(),
        listPersonalTrialReadinessTrials(),
        listPersonalTrialReadinessIssues(),
        listPersonalTrialReadinessOptimizationBacklog(),
        getPersonalTrialReadinessAudit()
      ]);
      const firstTrialId = nextTrialId || trialsResponse.trials?.[0]?.trial_id || "trial_mock_001";
      const [observations, quality, safetyConfirmation] = await Promise.all([
        listPersonalTrialReadinessObservations(firstTrialId),
        getPersonalTrialReadinessQuality(firstTrialId),
        getPersonalTrialReadinessSafetyConfirmation(firstTrialId)
      ]);
      setSelectedTrialId(firstTrialId);
      setData({ status, checklist, safety, trials: trialsResponse, allIssues, backlog, audit, observations, quality, safetyConfirmation });
    } catch {
      setError("个人版实战试运行准备 API 暂不可用。页面保持安全 fallback，不调用真实 provider，不读取案件原始内容，不显示密钥、本地路径或 raw content。");
    }
  }

  useEffect(() => {
    void loadReadiness();
  }, []);

  async function startMockTrial() {
    const result = await createPersonalTrialReadinessTrial({
      trial_name: "个人版实战试运行样本",
      case_mode: "synthetic_case",
      owner_user_id: "local_owner",
      case_reference_label: "合成试运行样本",
      explicit_owner_confirmation: true,
      explicit_no_raw_content_confirmation: true,
      explicit_no_provider_confirmation: true,
      explicit_no_training_confirmation: true,
      explicit_no_external_delivery_confirmation: true
    });
    await createPersonalTrialReadinessTrialChecklist(result.trial_id);
    setSelectedTrialId(result.trial_id);
    await loadReadiness(result.trial_id);
  }

  async function recordMockIssue() {
    await createPersonalTrialReadinessIssue(trialId, {
      stage_id: "owner_output_center",
      issue_type: "workflow",
      severity: "low",
      title: "本人下载边界提示可继续强化",
      description: "试运行中记录的优化点，仅用于 v7.26 参考。",
      suggested_fix: "在下载按钮附近强化 metadata-only / owner-only 文案。"
    });
    await loadReadiness(trialId);
  }

  async function refreshQualityAndSafety() {
    await Promise.all([
      createPersonalTrialReadinessQuality(trialId),
      createPersonalTrialReadinessSafetyConfirmation(trialId),
      createPersonalTrialReadinessOptimizationBacklog({
        source_trial_id: trialId,
        source_issue_ids: (data.allIssues?.issues ?? []).slice(0, 2).map((issue: IssueLogItem) => issue.issue_id),
        priority: "medium",
        target_area: "trial_readiness",
        title: "v7.26 试运行反馈优化",
        description: "汇总试运行观察、问题记录和安全确认，用于下一轮优化。",
        recommended_version: "v7.26"
      })
    ]);
    await loadReadiness(trialId);
  }

  const checklistRows = [
    ["案件工作台", data.checklist?.case_workspace_checked],
    ["材料工作台", data.checklist?.material_workspace_checked],
    ["OCR 状态", data.checklist?.ocr_status_checked],
    ["事实预览", data.checklist?.fact_preview_checked],
    ["事实纠正", data.checklist?.fact_correction_checked],
    ["法律草稿", data.checklist?.legal_draft_checked],
    ["Skill 最终稿", data.checklist?.skill_final_drafts_checked],
    ["本人产出中心", data.checklist?.owner_output_center_checked],
    ["来源追踪", data.checklist?.source_trace_checked],
    ["复核队列", data.checklist?.review_queue_checked],
    ["安全面板", data.checklist?.trust_safety_checked],
    ["诊断默认折叠", data.checklist?.diagnostics_collapsed_checked]
  ];

  const observations = (data.observations?.observations ?? []) as StageObservation[];
  const issues = (data.allIssues?.issues ?? []) as IssueLogItem[];
  const backlog = (data.backlog?.backlog_items ?? []) as OptimizationBacklogItem[];
  const stageScores = Object.entries(data.quality?.stage_scores ?? {});

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}

        <section className="rounded-md border border-slate-800 bg-[#121923] p-8 text-white shadow-sm">
          <div className="text-sm font-medium text-cyan-200">v7.25 Personal Practical Case Trial Readiness</div>
          <h1 className="mt-3 text-4xl font-semibold">个人版实战试运行准备</h1>
          <p className="mt-4 max-w-4xl text-sm leading-6 text-slate-300">
            用于进入真实办案前的个人版试运行准备。当前只记录试运行 metadata，不读取案件原始内容，不调用真实 provider，不训练未结案件，不自动发布 Skill，也不自动对外交付。
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            {["试运行 metadata", "不读取案件原始内容", "不调用真实 provider", "不训练未结案件", "不自动发布 Skill", "不自动对外交付"].map((badge) => (
              <DarkSafetyBadge key={badge} label={badge} />
            ))}
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-3 xl:grid-cols-6">
          <StatusCard label="Trial Readiness" value={data.status?.trial_readiness_ready ?? true} detail="personal practical trial metadata" tone="safe" />
          <StatusCard label="Trial Sessions" value={data.trials?.trial_count ?? 1} detail="owner-only / metadata-only" tone="info" />
          <StatusCard label="Checklist" value={data.checklist?.checked_item_count ?? 12} detail="12 项试运行检查" tone="safe" />
          <StatusCard label="Issue Log" value={data.allIssues?.issue_count ?? 0} detail="只用于优化，不阻断下一步" tone="warning" />
          <StatusCard label="Quality Score" value={data.quality?.overall_score ?? 82} detail="评分只作为优化参考" tone="info" />
          <StatusCard label="Provider Live" value="disabled" detail="provider_live_call_triggered=false" tone="safe" />
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
          <Panel title="Trial Session Cards" eyebrow="试运行会话">
            <div className="grid gap-3">
              {trials.map((trial) => (
                <button
                  key={trial.trial_id}
                  type="button"
                  onClick={() => void loadReadiness(trial.trial_id)}
                  className={`rounded-md border px-4 py-3 text-left transition ${trialId === trial.trial_id ? "border-cyan-400 bg-cyan-50" : "border-line bg-white hover:bg-slate-50"}`}
                >
                  <div className="flex flex-wrap justify-between gap-3">
                    <div>
                      <div className="text-sm font-semibold text-ink">{trial.trial_name}</div>
                      <div className="mt-1 text-xs text-muted">{trial.case_mode} / {trial.case_reference_label}</div>
                    </div>
                    <div className="rounded-md bg-slate-900 px-2 py-1 text-xs font-semibold text-white">{trial.trial_status}</div>
                  </div>
                  <div className="mt-3 grid gap-2 text-xs text-muted md:grid-cols-3">
                    <span>owner_only: {String(trial.owner_only)}</span>
                    <span>raw content: {String(trial.raw_case_content_included)}</span>
                    <span>provider live: {String(trial.provider_live_call_triggered)}</span>
                  </div>
                </button>
              ))}
              <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void startMockTrial()}>
                创建试运行 metadata
              </button>
            </div>
          </Panel>

          <Panel title="Trial Checklist Panel" eyebrow="全链路清单">
            <div className="grid gap-2 md:grid-cols-2">
              {checklistRows.map(([label, value]) => (
                <div key={label} className="flex min-h-11 items-center justify-between gap-3 rounded-md border border-line bg-stone-50 px-3 py-2">
                  <span className="text-sm text-ink">{label}</span>
                  <span className="rounded-md bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-800">{String(value ?? true)}</span>
                </div>
              ))}
            </div>
          </Panel>
        </section>

        <ShowcaseStepper
          columns="lg:grid-cols-5"
          steps={[
            { label: "案件录入", detail: "只确认试运行 metadata", status: "owner-only" },
            { label: "事实预览与纠正", detail: "不读取案件原始内容", status: "draft-only" },
            { label: "法律分析草稿", detail: "不生成最终法律意见", status: "reference" },
            { label: "Skill / 本人产出", detail: "不训练未结案件，不自动发布 Skill", status: "gated" },
            { label: "试运行反馈", detail: "问题与评分进入 v7.26 优化 backlog", status: "no delivery" }
          ]}
        />

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="Stage Observation Panel" eyebrow="阶段观察">
            <div className="grid gap-3">
              {observations.map((item) => (
                <RuntimeCard
                  key={`${item.stage_id}-${item.stage_name}`}
                  title={item.stage_name}
                  category={item.stage_id}
                  status={item.observation_status}
                  items={[
                    ["usability_score", item.usability_score],
                    ["quality_score", item.quality_score],
                    ["issue_count", item.issue_count],
                    ["notes", item.notes],
                    ["blocks_next_stage", item.blocks_next_stage]
                  ]}
                />
              ))}
            </div>
          </Panel>

          <Panel title="Issue Log Panel" eyebrow="问题记录">
            <div className="mb-3 rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-xs leading-5 text-amber-900">
              问题记录只用于优化，不自动阻断下一步。
            </div>
            <div className="grid gap-3">
              {issues.map((issue) => (
                <div key={issue.issue_id} className="rounded-md border border-line bg-white px-4 py-3">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <div className="text-sm font-semibold text-ink">{issue.title}</div>
                      <div className="mt-1 text-xs text-muted">{issue.issue_type} / {issue.severity} / {issue.status}</div>
                    </div>
                    <span className="rounded-md bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-700">blocks_trial={String(issue.blocks_trial)}</span>
                  </div>
                  <p className="mt-3 text-xs leading-5 text-muted">{issue.description}</p>
                  <p className="mt-2 text-xs leading-5 text-cyan-900">建议：{issue.suggested_fix}</p>
                </div>
              ))}
              <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void recordMockIssue()}>
                记录优化问题 metadata
              </button>
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Quality Review Panel">
            <div className="rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
              评分只作为优化参考，不构成最终法律意见。
            </div>
            <div className="mt-4 grid gap-3">
              <StatusCard label="overall_score" value={data.quality?.overall_score ?? 82} detail="reference-only" tone="info" />
              <InfoRows
                rows={[
                  ["fact_quality_score", data.quality?.fact_quality_score],
                  ["legal_draft_quality_score", data.quality?.legal_draft_quality_score],
                  ["skill_helpfulness_score", data.quality?.skill_helpfulness_score],
                  ["source_trace_score", data.quality?.source_trace_score],
                  ["owner_download_score", data.quality?.owner_download_score],
                  ["gate_reference_only", data.quality?.gate_reference_only ?? true],
                  ["blocks_next_stage", data.quality?.blocks_next_stage ?? false]
                ]}
              />
              <div className="grid gap-2">
                {stageScores.map(([label, value]) => (
                  <div key={label} className="rounded-md border border-line bg-stone-50 px-3 py-2 text-xs text-muted">
                    {label}: <span className="font-semibold text-cyan-900">{String(value)}</span>
                  </div>
                ))}
              </div>
            </div>
          </Panel>

          <Panel title="Safety Confirmation Panel">
            <InfoRows
              rows={[
                ["owner_only_confirmed", data.safetyConfirmation?.owner_only_confirmed],
                ["draft_only_confirmed", data.safetyConfirmation?.draft_only_confirmed],
                ["no_public_link_confirmed", data.safetyConfirmation?.no_public_link_confirmed],
                ["no_email_confirmed", data.safetyConfirmation?.no_email_confirmed],
                ["no_external_delivery_confirmed", data.safetyConfirmation?.no_external_delivery_confirmed],
                ["no_final_legal_opinion_confirmed", data.safetyConfirmation?.no_final_legal_opinion_confirmed],
                ["no_final_report_confirmed", data.safetyConfirmation?.no_final_report_confirmed],
                ["no_open_case_training_confirmed", data.safetyConfirmation?.no_open_case_training_confirmed],
                ["no_skill_auto_publish_confirmed", data.safetyConfirmation?.no_skill_auto_publish_confirmed],
                ["no_api_key_exposed_confirmed", data.safetyConfirmation?.no_api_key_exposed_confirmed]
              ]}
            />
            <button type="button" className="mt-4 rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void refreshQualityAndSafety()}>
              刷新质量 / 安全 / Backlog metadata
            </button>
          </Panel>

          <Panel title="Optimization Backlog Panel">
            <div className="grid gap-3">
              {backlog.map((item) => (
                <div key={item.backlog_id} className="rounded-md border border-line bg-stone-50 px-3 py-2 text-xs leading-5 text-muted">
                  <div className="font-semibold text-ink">{item.title}</div>
                  <div className="mt-1">{item.description}</div>
                  <div className="mt-2 text-cyan-900">priority={item.priority} / recommended_version={item.recommended_version}</div>
                </div>
              ))}
            </div>
          </Panel>
        </section>

        <TrustSafetyPanel
          items={data.safety?.safety_items ?? []}
          title="Trial Readiness Trust / Safety Panel"
          note="v7.25 只记录试运行 metadata；不显示 raw content、API key、本地路径，不生成最终法律意见或最终报告，不训练未结案件，不对外交付。"
        />

        <DiagnosticsPanel data={data} />
      </div>
    </AppShell>
  );
}
