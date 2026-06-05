"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DarkSafetyBadge,
  DiagnosticsPanel,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  createPersonalProductionCase,
  createPersonalStageRun,
  createPersonalWorkflowRun,
  getPersonalCaseProductionAudit,
  getPersonalCaseProductionReviewGates,
  getPersonalCaseProductionSafety,
  getPersonalCaseProductionStatus,
  listPersonalCaseProductionReadiness,
  listPersonalCaseProductionSourceTraces,
  listPersonalCaseProductionWorkflowStages,
  listPersonalProductionCases,
  listPersonalStageRuns,
  listPersonalWorkflowRuns,
  submitPersonalCaseProductionReviewGateAction
} from "@/services/api";

const reviewActions = ["approve_for_final_gate", "request_revision", "reject", "mark_not_ready", "mark_low_confidence"];

export default function PersonalCaseProductionPage() {
  const [data, setData] = useState<Record<string, any>>({});
  const [confirmed, setConfirmed] = useState(true);
  const [error, setError] = useState("");
  const [caseId, setCaseId] = useState("case_v55_approve_all");
  const [productionCaseId, setProductionCaseId] = useState("");
  const [workflowRunId, setWorkflowRunId] = useState("");
  const [stageId, setStageId] = useState("case_intake_stage");
  const [reviewAction, setReviewAction] = useState("approve_for_final_gate");

  async function loadWorkflow() {
    setError("");
    try {
      const [status, stages, cases, workflows, stageRuns, readiness, gates, traces, audit, safety] = await Promise.all([
        getPersonalCaseProductionStatus(),
        listPersonalCaseProductionWorkflowStages(),
        listPersonalProductionCases(),
        listPersonalWorkflowRuns(),
        listPersonalStageRuns(),
        listPersonalCaseProductionReadiness(),
        getPersonalCaseProductionReviewGates(),
        listPersonalCaseProductionSourceTraces(),
        getPersonalCaseProductionAudit(),
        getPersonalCaseProductionSafety()
      ]);
      setData({ status, stages, cases, workflows, stage_runs: stageRuns, readiness, gates, traces, audit, safety });
      setProductionCaseId((current) => current || cases.production_cases?.[0]?.production_case_id || "");
      setWorkflowRunId((current) => current || workflows.workflow_runs?.[0]?.workflow_run_id || "");
    } catch {
      setError("受控案件生产工作流 API 暂不可用，请确认后端服务已启动。");
    }
  }

  useEffect(() => {
    void loadWorkflow();
  }, []);

  async function createCase() {
    const result = await createPersonalProductionCase({
      case_id: caseId,
      production_title: "受控案件生产记录草案",
      case_type: "civil",
      client_alias: "client_demo",
      jurisdiction: "中国大陆",
      legal_area: "合同纠纷",
      desensitization_status: "metadata_only",
      explicit_mock_confirmation: confirmed,
      explicit_no_raw_content_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed,
      explicit_no_external_delivery_confirmation: confirmed
    });
    setProductionCaseId(result.production_case_id);
    await loadWorkflow();
  }

  async function createWorkflow() {
    const stageIds = (data.stages?.workflow_stages ?? []).map((stage: any) => stage.stage_id);
    const result = await createPersonalWorkflowRun({
      production_case_id: productionCaseId,
      workflow_scope: "full_controlled_mock_workflow",
      selected_stage_ids: stageIds,
      explicit_mock_confirmation: confirmed,
      explicit_lawyer_review_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed,
      explicit_no_external_delivery_confirmation: confirmed
    });
    setWorkflowRunId(result.workflow_run_id);
    await loadWorkflow();
  }

  async function createStageRun() {
    await createPersonalStageRun({
      workflow_run_id: workflowRunId,
      stage_id: stageId,
      linked_runtime_object_ids: [],
      stage_note: "模拟阶段运行 metadata",
      explicit_mock_confirmation: confirmed,
      explicit_no_live_provider_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed
    });
    await loadWorkflow();
  }

  async function submitReview() {
    await submitPersonalCaseProductionReviewGateAction(productionCaseId, {
      action: reviewAction,
      reviewer_id: "local_demo_lawyer",
      reviewer_note: "仅更新复核门禁 metadata",
      explicit_lawyer_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed,
      explicit_no_external_delivery_confirmation: confirmed
    });
    await loadWorkflow();
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <div className="rounded-md border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800">{error}</div> : null}
        <Hero title="受控案件生产工作流" subtitle="把材料处理、AI 草稿、信息核验与律师复核串联为 metadata-only 受控生产流程" badges={["受控编排", "仅模拟结果", "律师复核必需", "不自动对外交付"]} />
        <section className="grid gap-4 md:grid-cols-6">{["工作流状态", "案件生产记录", "阶段运行", "准备度检查", "律师复核", "最终门禁"].map((label) => <StatusCard key={label} label={label} />)}</section>
        <Panel title="工作流阶段卡片">
          <div className="grid gap-3 md:grid-cols-4">{(data.stages?.workflow_stages ?? []).map((stage: any) => <Card key={stage.stage_id} title={stage.display_name} lines={[stage.stage_id, `final_gate=${stage.final_gate_required}`, `auto_delivery=${stage.auto_delivery_enabled}`]} />)}</div>
        </Panel>
        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="创建生产案件记录"><FormGrid><Text label="案件 ID" value={caseId} onChange={setCaseId} /><Confirm checked={confirmed} onChange={setConfirmed} /><Button label="创建生产案件记录" onClick={() => void createCase()} /></FormGrid></Panel>
          <Panel title="创建模拟工作流"><FormGrid><Text label="Production Case ID" value={productionCaseId} onChange={setProductionCaseId} /><Confirm checked={confirmed} onChange={setConfirmed} /><Button label="创建模拟工作流" onClick={() => void createWorkflow()} /></FormGrid></Panel>
          <Panel title="运行模拟阶段"><FormGrid><Text label="Workflow Run ID" value={workflowRunId} onChange={setWorkflowRunId} /><Select value={stageId} options={(data.stages?.workflow_stages ?? []).map((stage: any) => stage.stage_id)} onChange={setStageId} /><Confirm checked={confirmed} onChange={setConfirmed} /><Button label="运行模拟阶段" onClick={() => void createStageRun()} /></FormGrid></Panel>
        </section>
        <Panel title="准备度面板">
          <div className="grid gap-3 md:grid-cols-3">{(data.readiness?.readiness ?? []).map((item: any) => <Card key={item.production_case_id} title={item.production_case_id} lines={[item.readiness_status, `completed=${item.completed_stage_count}/${item.required_stage_count}`, `delivery_ready=${item.delivery_ready}`]} />)}</div>
        </Panel>
        <Panel title="律师复核门禁队列"><FormGrid><Select value={reviewAction} options={reviewActions} onChange={setReviewAction} /><Button label="提交复核门禁动作" onClick={() => void submitReview()} /></FormGrid></Panel>
        <Panel title="Source Trace / 来源追踪"><div className="grid gap-3 md:grid-cols-3">{(data.traces?.source_traces ?? []).slice(0, 6).map((trace: any) => <Card key={trace.source_trace_id} title={trace.source_trace_id} lines={[trace.source_type, trace.source_label, `raw_content_returned=${trace.raw_content_returned}`]} />)}</div></Panel>
        <TrustSafetyPanel items={data.safety?.safety_checklist ?? []} title="安全清单" />
        <Panel title="Developer Diagnostics"><DiagnosticsPanel data={data} /></Panel>
      </div>
    </AppShell>
  );
}

function Hero({ title, subtitle, badges }: { title: string; subtitle: string; badges: string[] }) { return <section className="rounded-md border border-slate-800 bg-[#202426] p-8 text-white"><h1 className="text-4xl font-semibold">{title}</h1><p className="mt-4 text-slate-300">{subtitle}</p><div className="mt-5 flex flex-wrap gap-2">{badges.map((badge) => <DarkSafetyBadge key={badge} label={badge} />)}</div></section>; }
function Panel({ title, children }: { title: string; children: React.ReactNode }) { return <section className="rounded-md border border-line bg-paper p-5"><h2 className="text-base font-semibold text-ink">{title}</h2><div className="mt-4">{children}</div></section>; }
function StatusCard({ label }: { label: string }) { return <div className="rounded-md border border-line bg-white p-4"><div className="text-xs text-muted">{label}</div><div className="mt-2 text-xl font-semibold text-ink">已就绪</div></div>; }
function Card({ title, lines }: { title: string; lines: string[] }) { return <div className="rounded-md border border-line bg-white p-4"><div className="text-sm font-semibold text-ink">{title}</div><div className="mt-2 grid gap-1 text-xs text-muted">{lines.map((line) => <span key={line}>{line}</span>)}</div></div>; }
function FormGrid({ children }: { children: React.ReactNode }) { return <div className="grid gap-3">{children}</div>; }
function Text({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) { return <label className="grid gap-2 text-sm"><span>{label}</span><input className="rounded-md border border-line px-3 py-2" value={value} onChange={(event) => onChange(event.target.value)} /></label>; }
function Select({ value, options, onChange }: { value: string; options: string[]; onChange: (value: string) => void }) { return <select className="rounded-md border border-line px-3 py-2 text-sm" value={value} onChange={(event) => onChange(event.target.value)}>{options.map((option) => <option key={option}>{option}</option>)}</select>; }
function Confirm({ checked, onChange }: { checked: boolean; onChange: (value: boolean) => void }) { return <label className="flex gap-2 text-sm"><input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />明确确认：仅 metadata、无最终意见、无最终报告、不对外交付</label>; }
function Button({ label, onClick }: { label: string; onClick: () => void }) { return <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={onClick}>{label}</button>; }
