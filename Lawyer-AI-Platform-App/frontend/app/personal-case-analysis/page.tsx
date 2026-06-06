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
  createPersonalCaseAnalysisFactDraft,
  createPersonalCaseAnalysisLegalDraft,
  createPersonalCaseAnalysisRun,
  getPersonalCaseAnalysisAudit,
  getPersonalCaseAnalysisSafety,
  getPersonalCaseAnalysisSkillBaselines,
  getPersonalCaseAnalysisStatus,
  getPersonalCaseAnalysisReviewQueue,
  getPersonalCaseWorkspaceFactInputReadiness,
  listPersonalCaseAnalysisEvaluations,
  listPersonalCaseAnalysisFactDrafts,
  listPersonalCaseAnalysisGates,
  listPersonalCaseAnalysisLegalDrafts,
  listPersonalCaseAnalysisRuntimes,
  listPersonalCaseAnalysisRuns,
  listPersonalCaseAnalysisSourceTraces,
  submitPersonalCaseAnalysisReviewAction
} from "@/services/api";

const defaultCaseId = "open_case_mock_001";
const reviewActions = ["approve_draft_metadata", "request_revision", "mark_low_confidence", "mark_not_ready", "reject"];

export default function PersonalCaseAnalysisPage() {
  const [data, setData] = useState<Record<string, any>>({});
  const [error, setError] = useState("");
  const [caseId, setCaseId] = useState(defaultCaseId);
  const [caseAlias, setCaseAlias] = useState("未结案件本地试点样本");
  const [confirmed, setConfirmed] = useState(true);
  const [factDraftId, setFactDraftId] = useState("");
  const [legalDraftId, setLegalDraftId] = useState("");
  const [reviewAction, setReviewAction] = useState("request_revision");

  async function loadRuntime() {
    setError("");
    try {
      const [status, runtimes, baselines, runs, factDrafts, legalDrafts, queue, evaluations, gates, traces, audit, safety, factInputReadiness] =
        await Promise.all([
          getPersonalCaseAnalysisStatus(),
          listPersonalCaseAnalysisRuntimes(),
          getPersonalCaseAnalysisSkillBaselines(),
          listPersonalCaseAnalysisRuns(),
          listPersonalCaseAnalysisFactDrafts(),
          listPersonalCaseAnalysisLegalDrafts(),
          getPersonalCaseAnalysisReviewQueue(),
          listPersonalCaseAnalysisEvaluations(),
          listPersonalCaseAnalysisGates(),
          listPersonalCaseAnalysisSourceTraces(),
          getPersonalCaseAnalysisAudit(),
          getPersonalCaseAnalysisSafety(),
          getPersonalCaseWorkspaceFactInputReadiness()
        ]);
      setData({ status, runtimes, baselines, runs, factDrafts, legalDrafts, queue, evaluations, gates, traces, audit, safety, factInputReadiness });
      setFactDraftId((current) => current || factDrafts.fact_drafts?.[0]?.fact_draft_id || "");
      setLegalDraftId((current) => current || legalDrafts.legal_drafts?.[0]?.legal_draft_id || "");
    } catch {
      setError("受控案件分析 Runtime API 暂不可用。页面保持安全 fallback，不调用 provider，不显示敏感信息。");
    }
  }

  useEffect(() => {
    void loadRuntime();
  }, []);

  async function createRun() {
    const result = await createPersonalCaseAnalysisRun({
      case_id: caseId,
      case_alias: caseAlias,
      analysis_scope: "fact_and_legal_analysis",
      material_metadata_ids: ["material_metadata_mock_001"],
      source_trace_ids: [],
      selected_skill_ids: ["case_fact_extraction_skill", "case_legal_analysis_skill"],
      explicit_mock_confirmation: confirmed,
      explicit_open_case_confirmation: confirmed,
      explicit_no_training_data_confirmation: confirmed,
      explicit_no_raw_content_confirmation: confirmed,
      explicit_lawyer_review_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed
    });
    setFactDraftId(String(result.fact_draft_id ?? ""));
    setLegalDraftId(String(result.legal_draft_id ?? ""));
    await loadRuntime();
  }

  async function createFactDraft() {
    const result = await createPersonalCaseAnalysisFactDraft({
      case_id: caseId,
      run_id: null,
      source_trace_ids: [],
      material_metadata_ids: ["material_metadata_mock_001"],
      case_fact_extraction_skill_id: "case_fact_extraction_skill",
      explicit_mock_confirmation: confirmed,
      explicit_no_training_data_confirmation: confirmed,
      explicit_no_raw_content_confirmation: confirmed,
      explicit_lawyer_review_confirmation: confirmed
    });
    setFactDraftId(result.fact_draft_id);
    await loadRuntime();
  }

  async function createLegalDraft() {
    const result = await createPersonalCaseAnalysisLegalDraft({
      case_id: caseId,
      fact_draft_id: factDraftId || null,
      source_trace_ids: [],
      legal_search_metadata_ids: ["legal_search_metadata_mock_001"],
      enterprise_metadata_ids: ["enterprise_metadata_mock_001"],
      case_legal_analysis_skill_id: "case_legal_analysis_skill",
      explicit_mock_confirmation: confirmed,
      explicit_no_training_data_confirmation: confirmed,
      explicit_no_raw_content_confirmation: confirmed,
      explicit_lawyer_review_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed
    });
    setLegalDraftId(result.legal_draft_id);
    await loadRuntime();
  }

  async function submitReview() {
    const reviewItemId = data.queue?.review_items?.[0]?.review_item_id;
    if (!reviewItemId) {
      return;
    }
    await submitPersonalCaseAnalysisReviewAction(reviewItemId, {
      action: reviewAction,
      reviewer_id: "local_demo_lawyer",
      reviewer_note: "仅更新 v7.16 review metadata",
      explicit_lawyer_confirmation: confirmed,
      explicit_no_training_data_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed
    });
    await loadRuntime();
  }

  const safetyItems = data.safety?.safety_checklist ?? [
    "未结案件实战分析不产生训练数据",
    "训练阶段与实战阶段严格分离",
    "不自动更新 Skill",
    "不自动发布 Skill",
    "不生成最终法律意见",
    "来源追踪必需",
    "律师复核必需"
  ];

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}
        <section className="rounded-md border border-slate-800 bg-[#182026] p-8 text-white">
          <div className="text-sm font-medium text-cyan-200">v7.16 Controlled Case Analysis Runtime</div>
          <h1 className="mt-3 text-4xl font-semibold">受控案件分析 Runtime</h1>
          <p className="mt-4 max-w-4xl text-sm leading-6 text-slate-300">
            面向未结案件的实战分析 draft：调用已有案件事实提炼 Skill 与案件法律分析 Skill，仅生成事实分析和法律分析 metadata 草案。训练阶段与实战阶段严格分离，不产生训练数据，不自动更新或发布 Skill。
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            {["未结案件分析", "调用已有 Skill", "草稿状态", "不产生训练数据", "律师复核必需", "来源追踪必需"].map((badge) => (
              <DarkSafetyBadge key={badge} label={badge} />
            ))}
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-4">
          <StatusCard label="Runtime" value={data.status?.mode ?? "personal_case_analysis"} detail="open_case_runtime=true" />
          <StatusCard label="训练数据" value="disabled" detail="training_data_generated=false" tone="safe" />
          <StatusCard label="Skill 更新" value="disabled" detail="skill_updated=false / skill_published=false" tone="safe" />
          <StatusCard label="Review" value="required" detail="lawyer_review_required=true" tone="warning" />
        </section>

        <Panel title="v7.20 Fact Input Readiness / 事实输入准备度">
          <div className="grid gap-4 md:grid-cols-3">
            <StatusCard label="Readiness Items" value={data.factInputReadiness?.readiness_count ?? 0} detail="来自事实预览与输入纠正工作台" tone="info" />
            <StatusCard label="Auto Legal Analysis" value={String(data.factInputReadiness?.legal_analysis_auto_triggered ?? false)} detail="ready 不等于自动创建法律分析" tone="safe" />
            <StatusCard label="Training Data" value={String(data.factInputReadiness?.training_data_generated ?? false)} detail="未结案件事实不写训练集" tone="safe" />
          </div>
          <div className="mt-4 grid gap-3">
            {(data.factInputReadiness?.readiness_items ?? []).map((item: any) => (
              <RuntimeCard
                key={item.readiness_id}
                title={item.readiness_id}
                category={item.fact_preview_id}
                status={item.legal_analysis_input_ready ? "input ready" : "pending owner confirmation"}
                items={[
                  ["owner_confirmed", item.owner_confirmed],
                  ["source_trace_ready", item.source_trace_ready],
                  ["legal_analysis_auto_triggered", item.legal_analysis_auto_triggered],
                  ["gate_reference_only", item.gate_reference_only],
                  ["blocks_next_stage", item.blocks_next_stage]
                ]}
              />
            ))}
          </div>
          <div className="mt-4 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
            v7.20 事实预览可被用户本人确认后作为法律分析输入 metadata，但本页不会自动触发法律分析；创建 draft 仍需用户动作和律师复核边界。
          </div>
        </Panel>

        <ShowcaseStepper
          columns="lg:grid-cols-3"
          steps={[
            { label: "Fact Analysis Stage", detail: "生成事实摘要、证据映射、时间线、争议事实和缺失事实 draft。", status: "draft metadata" },
            { label: "Legal Analysis Stage", detail: "基于事实 draft、source trace 和法律/企业 metadata 生成法律分析 draft。", status: "no final opinion" },
            { label: "Review & Readiness Stage", detail: "进入律师复核、低置信度提示、来源完整性和交付包准备度 metadata。", status: "reference only" }
          ]}
        />

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="创建受控案件分析 Run">
            <div className="grid gap-3">
              <Text label="Open Case ID" value={caseId} onChange={setCaseId} />
              <Text label="案件代号" value={caseAlias} onChange={setCaseAlias} />
              <Confirm checked={confirmed} onChange={setConfirmed} />
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void createRun()}>
                创建事实与法律分析 draft
              </button>
            </div>
          </Panel>
          <Panel title="单独创建 Draft">
            <div className="grid gap-3">
              <Text label="Fact Draft ID" value={factDraftId} onChange={setFactDraftId} />
              <Text label="Legal Draft ID" value={legalDraftId} onChange={setLegalDraftId} />
              <button className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void createFactDraft()}>
                创建事实分析 draft
              </button>
              <button className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void createLegalDraft()}>
                创建法律分析 draft
              </button>
            </div>
          </Panel>
        </section>

        <Panel title="Skill Baseline / 已有 Skill 引用">
          <div className="grid gap-3 lg:grid-cols-2">
            {(data.baselines?.baselines ?? []).map((baseline: any) => (
              <RuntimeCard
                key={baseline.skill_key}
                title={baseline.skill_title_cn}
                category={baseline.skill_key}
                status={baseline.baseline_detected ? "metadata detected" : "placeholder lineage"}
                items={[
                  ["source_skill_id", baseline.source_skill_id],
                  ["source_package_id", baseline.source_package_id ?? "missing"],
                  ["evaluation_detected", baseline.evaluation_detected],
                  ["gate_detected", baseline.gate_detected],
                  ["writes_to_training_set", baseline.writes_to_training_set],
                  ["skill_published", baseline.skill_published]
                ]}
              />
            ))}
          </div>
          <div className="mt-4">
            <InfoRows rows={[["missing_baseline_report", (data.baselines?.missing_baseline_report ?? []).join("; ") || "none"], ["derived_from", "v7.15 Skill Training Runtime metadata"]]} />
          </div>
        </Panel>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="Fact Analysis Stage / 事实分析 Draft">
            <DraftCards items={data.factDrafts?.fact_drafts ?? []} idKey="fact_draft_id" fields={["fact_summary_draft", "disputed_facts_draft", "missing_facts_draft"]} />
          </Panel>
          <Panel title="Legal Analysis Stage / 法律分析 Draft">
            <DraftCards items={data.legalDrafts?.legal_drafts ?? []} idKey="legal_draft_id" fields={["legal_relationship_draft", "issue_spotting_draft", "risk_flags_draft"]} />
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Evaluation / Gate">
            <InfoRows
              rows={[
                ["evaluation_count", data.evaluations?.evaluation_count ?? 0],
                ["gate_count", data.gates?.gate_count ?? 0],
                ["gate_reference_only", data.gates?.gate_reference_only ?? true],
                ["blocks_next_stage", data.gates?.blocks_next_stage ?? false],
                ["training_data_generated", data.evaluations?.training_data_generated ?? false]
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
          <Panel title="Source Trace">
            <InfoRows rows={[["source_trace_count", data.traces?.source_trace_count ?? 0], ["raw_content_returned", false], ["used_in_ai_prompt", false]]} />
          </Panel>
        </section>

        <Panel title="Runtime Cards">
          <div className="grid gap-3 lg:grid-cols-4">
            {(data.runtimes?.runtimes ?? []).map((runtime: any) => (
              <RuntimeCard
                key={runtime.runtime_id}
                title={runtime.display_name}
                category={runtime.runtime_type}
                status={runtime.stage}
                targetRoute={runtime.target_route}
                items={[
                  ["live_enabled", runtime.live_enabled],
                  ["training_data_generated", runtime.training_data_generated],
                  ["skill_updated", runtime.skill_updated],
                  ["gate_reference_only", runtime.gate_reference_only]
                ]}
              />
            ))}
          </div>
        </Panel>

        <TrustSafetyPanel
          title="信任与安全面板"
          note="v7.16 仅返回未结案件分析元数据草案；不读取原始材料、密钥值或本地路径，不产生训练数据，不生成最终法律意见。"
          items={safetyItems}
        />
        <DiagnosticsPanel data={data} />
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

function Text({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return (
    <label className="grid gap-2 text-sm">
      <span>{label}</span>
      <input className="rounded-md border border-line px-3 py-2" value={value} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function Confirm({ checked, onChange }: { checked: boolean; onChange: (value: boolean) => void }) {
  return (
    <label className="flex gap-2 text-sm">
      <input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
      明确确认：未结案件仅生成 draft metadata，不产生训练数据，不生成最终法律意见
    </label>
  );
}

function DraftCards({ items, idKey, fields }: { items: any[]; idKey: string; fields: string[] }) {
  if (!items.length) {
    return <div className="rounded-md border border-dashed border-line bg-slate-50 p-4 text-sm text-muted">暂无 draft。可先创建受控案件分析 Run。</div>;
  }
  return (
    <div className="grid gap-3">
      {items.slice(0, 4).map((item) => (
        <div key={item[idKey]} className="rounded-md border border-line bg-slate-50 p-4">
          <div className="text-sm font-semibold text-ink">{item[idKey]}</div>
          <div className="mt-3 grid gap-2 text-xs leading-5 text-muted">
            {fields.map((field) => <span key={field}>{field}: {Array.isArray(item[field]) ? item[field].join(" / ") : String(item[field] ?? "pending")}</span>)}
            <span>training_data_generated: {String(item.training_data_generated)}</span>
            <span>final_legal_opinion_generated: {String(item.final_legal_opinion_generated)}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
