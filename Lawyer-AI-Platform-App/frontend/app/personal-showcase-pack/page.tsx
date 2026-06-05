"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DarkSafetyBadge,
  DiagnosticsPanel,
  ShowcaseStepper,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  PilotSampleList,
  ShowcaseMetrics,
  ShowcaseRuntimeList,
  ShowcaseSafetyStatus,
  StoryFlowList,
  StoryFlowRecord,
  TrustPanel,
  personalShowcasePackApi
} from "@/services/api";

const storyStages = [
  { id: "case_intake", label: "案件录入" },
  { id: "material_processing", label: "材料处理" },
  { id: "ai_draft", label: "AI 草稿" },
  { id: "legal_enterprise_check", label: "法律/企业信息核验" },
  { id: "skill_studio", label: "技能沉淀" },
  { id: "delivery_packet", label: "交付包" },
  { id: "final_lock", label: "最终锁定" }
];

const sampleTypes = ["contract_dispute_demo", "labor_dispute_demo", "debt_collection_demo", "enterprise_risk_demo", "general_civil_demo"];

export default function PersonalShowcasePackPage() {
  const [status, setStatus] = useState<Record<string, unknown> | null>(null);
  const [runtimes, setRuntimes] = useState<ShowcaseRuntimeList | null>(null);
  const [metrics, setMetrics] = useState<ShowcaseMetrics | null>(null);
  const [trustPanel, setTrustPanel] = useState<TrustPanel | null>(null);
  const [safety, setSafety] = useState<ShowcaseSafetyStatus | null>(null);
  const [samples, setSamples] = useState<PilotSampleList | null>(null);
  const [flows, setFlows] = useState<StoryFlowList | null>(null);
  const [selectedSampleId, setSelectedSampleId] = useState("");
  const [selectedFlow, setSelectedFlow] = useState<StoryFlowRecord | null>(null);
  const [sampleConfirmed, setSampleConfirmed] = useState(true);
  const [flowConfirmed, setFlowConfirmed] = useState(true);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const [sampleForm, setSampleForm] = useState({
    sample_title: "合同纠纷试点样本",
    sample_type: "contract_dispute_demo",
    legal_area: "民商事",
    case_cause: "合同纠纷",
    risk_level: "controlled_demo",
    demo_persona: "试点演示律师"
  });
  const [flowForm, setFlowForm] = useState({
    story_title: "受控生产到交付包展示流程",
    story_scope: "v7.3-v7.6 能力串联的 mock metadata 演示",
    selected_stage_ids: storyStages.map((stage) => stage.id).join(",")
  });

  async function loadShowcase(nextSampleId?: string, nextFlow?: StoryFlowRecord | null) {
    setLoading(true);
    setError("");
    try {
      const [statusData, runtimeData, metricsData, trustData, safetyData, sampleData, flowData] = await Promise.all([
        personalShowcasePackApi.getStatus(),
        personalShowcasePackApi.listRuntimes(),
        personalShowcasePackApi.getMetrics(),
        personalShowcasePackApi.getTrustPanel(),
        personalShowcasePackApi.getSafety(),
        personalShowcasePackApi.listPilotSamples(),
        personalShowcasePackApi.listStoryFlows()
      ]);
      setStatus(statusData);
      setRuntimes(runtimeData);
      setMetrics(metricsData);
      setTrustPanel(trustData);
      setSafety(safetyData);
      setSamples(sampleData);
      setFlows(flowData);
      const preferredSampleId = nextSampleId || selectedSampleId || sampleData.pilot_samples?.[0]?.pilot_sample_id || "";
      setSelectedSampleId(preferredSampleId);
      setSelectedFlow(nextFlow || flowData.story_flows?.[0] || null);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "无法加载个人生产试点与展示包");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadShowcase();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const metricCards = [
    ["试点样本", metrics?.pilot_sample_count ?? 0],
    ["故事流程", metrics?.story_flow_count ?? 0],
    ["来源追踪覆盖", `${String(metrics?.source_trace_coverage_rate ?? 0)}%`],
    ["律师复核", String(metrics?.lawyer_review_required_count ?? 0)],
    ["最终锁定", String(metrics?.final_lock_ready_count ?? 0)],
    ["外部交付", "0"]
  ];

  const stageCards = useMemo(() => {
    const cards = selectedFlow?.stage_cards;
    if (Array.isArray(cards) && cards.length > 0) {
      return cards as Array<Record<string, unknown>>;
    }
    return storyStages.map((stage) => ({
      stage_id: stage.id,
      display_name: stage.label,
      status: "mock_metadata_pending",
      linked_runtime: "pending",
      source_trace_required: true,
      lawyer_review_required: true,
      final_output_generated: false
    }));
  }, [selectedFlow]);

  async function createSample(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    const sample = await personalShowcasePackApi.createPilotSample({
      ...sampleForm,
      linked_runtime_ids: ["personal_intelligence_gateway", "personal_skill_studio", "personal_case_production", "personal_delivery_packet"],
      explicit_mock_confirmation: sampleConfirmed,
      explicit_no_real_case_confirmation: sampleConfirmed,
      explicit_no_raw_content_confirmation: sampleConfirmed,
      explicit_no_final_opinion_confirmation: sampleConfirmed,
      explicit_no_external_delivery_confirmation: sampleConfirmed
    });
    setMessage(`已创建 mock 试点样本：${sample.pilot_sample_id}`);
    await loadShowcase(sample.pilot_sample_id, selectedFlow);
  }

  async function createStoryFlow(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selectedSampleId) {
      setError("请先创建或选择试点样本");
      return;
    }
    const flow = await personalShowcasePackApi.createStoryFlow({
      pilot_sample_id: selectedSampleId,
      story_title: flowForm.story_title,
      story_scope: flowForm.story_scope,
      selected_stage_ids: splitIds(flowForm.selected_stage_ids),
      explicit_mock_confirmation: flowConfirmed,
      explicit_no_real_case_confirmation: flowConfirmed,
      explicit_no_final_opinion_confirmation: flowConfirmed,
      explicit_no_external_delivery_confirmation: flowConfirmed
    });
    setMessage(`已生成 mock Story Flow：${flow.story_flow_id}`);
    await loadShowcase(selectedSampleId, flow);
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <div className="rounded-md border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800">{error}</div> : null}
        {message ? <div className="rounded-md border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">{message}</div> : null}

        <section className="overflow-hidden rounded-md border border-slate-800 bg-[#111827] text-white shadow-sm">
          <div className="grid gap-6 p-6 lg:grid-cols-[1.2fr_0.8fr] lg:p-8">
            <div>
              <div className="flex flex-wrap gap-2">
                {["试点展示", "mock metadata", "律师复核必需", "来源可追踪", "不自动对外交付"].map((badge) => (
                  <DarkSafetyBadge key={badge} label={badge} />
                ))}
              </div>
              <h1 className="mt-5 text-3xl font-semibold leading-tight md:text-5xl">个人生产试点与展示包</h1>
              <p className="mt-4 max-w-3xl text-sm leading-6 text-slate-300 md:text-base">
                把受控信息核验、技能沉淀、案件生产和交付包流程串联为可演示的 mock metadata 展示。
              </p>
            </div>
            <div className="rounded-md border border-white/10 bg-white/5 p-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-cyan-100">Trust / Safety</div>
              <div className="mt-4 grid gap-2 text-sm text-slate-200">
                <span>未调用真实 provider</span>
                <span>未读取 API key</span>
                <span>未读取真实案件材料</span>
                <span>未生成最终法律意见</span>
                <span>未生成最终报告</span>
                <span>未自动对外交付</span>
                <span>不生成真实 PDF/DOCX</span>
              </div>
            </div>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-6">
          {metricCards.map(([label, value]) => (
            <div key={label} className="rounded-md border border-line bg-white p-4 shadow-sm">
              <div className="text-xs text-muted">{label}</div>
              <div className="mt-2 text-2xl font-semibold text-ink">{String(value)}</div>
            </div>
          ))}
        </section>

        <section className="rounded-md border border-line bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between gap-3">
            <h2 className="text-lg font-semibold text-ink">演示故事线 Stepper</h2>
            <span className="text-xs text-muted">方向 C · 演示故事线</span>
          </div>
          <div className="mt-5">
            <ShowcaseStepper
              steps={stageCards.map((stage) => ({
                label: String(stage.display_name),
                detail: `${String(stage.linked_runtime)} · 来源追踪=${String(stage.source_trace_required ?? true)} · 律师复核=${String(stage.lawyer_review_required ?? true)}`,
                status: String(stage.status)
              }))}
            />
          </div>
        </section>

        <section className="grid gap-6 xl:grid-cols-[1fr_1fr]">
          <Panel title="Pilot Sample Cards / 试点样本">
            <div className="grid gap-3">
              {(samples?.pilot_samples ?? []).slice(0, 3).map((sample) => (
                <div key={sample.pilot_sample_id} className="rounded-md border border-line bg-slate-50 p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <div className="text-sm font-semibold text-ink">{sample.sample_title}</div>
                      <div className="mt-1 text-xs text-muted">{sample.sample_type}</div>
                    </div>
                    <span className="rounded-md bg-cyan-50 px-2 py-1 text-xs font-semibold text-cyan-700">mock</span>
                  </div>
                  <InfoRows
                    rows={[
                      ["法律领域", sample.legal_area],
                      ["案由", sample.case_cause],
                      ["风险等级", sample.risk_level],
                      ["workflow progress", readNested(sample, "workflow_progress", "progress_percent") + "%"],
                      ["readiness status", sample.readiness_status],
                      ["review status", sample.review_status],
                      ["final lock status", sample.final_lock_status],
                      ["source trace coverage", String(sample.source_trace_coverage ?? 0) + "%"]
                    ]}
                  />
                </div>
              ))}
              {!(samples?.pilot_samples ?? []).length ? <div className="text-sm text-muted">暂无试点样本，创建后会显示 1-3 个低风险 mock sample。</div> : null}
            </div>
          </Panel>

          <Panel title="展示摘要">
            <InfoRows
              rows={[
                ["页面用途", "仅用于试点展示和产品演示"],
                ["样本类型", "synthetic mock metadata"],
                ["真实客户信息", "false"],
                ["真实案件材料", "false"],
                ["真实交付触发", "false"],
                ["runtime_count", runtimes?.runtime_count ?? 0],
                ["version", status?.version ?? "v7.7"]
              ]}
            />
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="创建试点样本">
            <form className="grid gap-4" onSubmit={createSample}>
              <Field label="样本标题" value={sampleForm.sample_title} onChange={(value) => setSampleForm({ ...sampleForm, sample_title: value })} />
              <label className="grid gap-2 text-sm">
                <span className="font-medium text-ink">样本类型</span>
                <select className="rounded-md border border-line bg-white px-3 py-2 text-sm text-ink" value={sampleForm.sample_type} onChange={(event) => setSampleForm({ ...sampleForm, sample_type: event.target.value })}>
                  {sampleTypes.map((type) => <option key={type} value={type}>{type}</option>)}
                </select>
              </label>
              <Field label="法律领域" value={sampleForm.legal_area} onChange={(value) => setSampleForm({ ...sampleForm, legal_area: value })} />
              <Field label="案由" value={sampleForm.case_cause} onChange={(value) => setSampleForm({ ...sampleForm, case_cause: value })} />
              <Field label="风险等级" value={sampleForm.risk_level} onChange={(value) => setSampleForm({ ...sampleForm, risk_level: value })} />
              <Field label="Demo persona" value={sampleForm.demo_persona} onChange={(value) => setSampleForm({ ...sampleForm, demo_persona: value })} />
              <Confirm checked={sampleConfirmed} onChange={setSampleConfirmed} label="我确认当前仅创建 synthetic mock metadata，不包含真实客户、真实案件或 raw content。" />
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:bg-slate-300" disabled={!sampleConfirmed || loading}>
                创建 mock 试点样本
              </button>
            </form>
          </Panel>

          <Panel title="生成 mock Story Flow">
            <form className="grid gap-4" onSubmit={createStoryFlow}>
              <label className="grid gap-2 text-sm">
                <span className="font-medium text-ink">Pilot Sample ID</span>
                <select className="rounded-md border border-line bg-white px-3 py-2 text-sm text-ink" value={selectedSampleId} onChange={(event) => setSelectedSampleId(event.target.value)}>
                  <option value="">未选择</option>
                  {(samples?.pilot_samples ?? []).map((sample) => <option key={sample.pilot_sample_id} value={sample.pilot_sample_id}>{sample.pilot_sample_id}</option>)}
                </select>
              </label>
              <Field label="Story title" value={flowForm.story_title} onChange={(value) => setFlowForm({ ...flowForm, story_title: value })} />
              <Field label="Story scope" value={flowForm.story_scope} onChange={(value) => setFlowForm({ ...flowForm, story_scope: value })} />
              <Field label="Selected stage IDs" value={flowForm.selected_stage_ids} onChange={(value) => setFlowForm({ ...flowForm, selected_stage_ids: value })} />
              <Confirm checked={flowConfirmed} onChange={setFlowConfirmed} label="我确认 Story Flow 仅为 mock metadata 展示，不生成最终法律意见、最终报告或外部交付。" />
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:bg-slate-300" disabled={!flowConfirmed || !selectedSampleId}>
                生成 mock Story Flow
              </button>
            </form>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          <TrustSafetyPanel items={trustPanel?.trust_items?.length ? trustPanel.trust_items : safety?.safety_checklist ?? []} />

          <Panel title="Safety Flags / 安全标记">
            <InfoRows
              rows={[
                ["real_provider_called", trustPanel?.flags?.real_provider_called],
                ["api_key_accessed", trustPanel?.flags?.api_key_accessed],
                ["real_case_data_included", trustPanel?.flags?.real_case_data_included],
                ["raw_content_included", trustPanel?.flags?.raw_content_included],
                ["final_legal_opinion_generated", trustPanel?.flags?.final_legal_opinion_generated],
                ["final_report_generated", trustPanel?.flags?.final_report_generated],
                ["external_delivery_triggered", trustPanel?.flags?.external_delivery_triggered],
                ["email_sent", trustPanel?.flags?.email_sent],
                ["final_file_generated", trustPanel?.flags?.final_file_generated]
              ]}
            />
          </Panel>
        </section>

        <Panel title="Developer Diagnostics">
          <DiagnosticsPanel data={{ status, runtimes, metrics, trustPanel, safety, samples, flows, selectedFlow }} />
        </Panel>
      </div>
    </AppShell>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-md border border-line bg-white p-5 shadow-sm">
      <h2 className="text-lg font-semibold text-ink">{title}</h2>
      <div className="mt-4">{children}</div>
    </div>
  );
}

function Field({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return (
    <label className="grid gap-2 text-sm">
      <span className="font-medium text-ink">{label}</span>
      <input className="rounded-md border border-line bg-white px-3 py-2 text-sm text-ink" value={value} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function Confirm({ checked, label, onChange }: { checked: boolean; label: string; onChange: (checked: boolean) => void }) {
  return (
    <label className="flex items-start gap-3 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-sm text-cyan-900">
      <input className="mt-1" type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
      <span>{label}</span>
    </label>
  );
}

function InfoRows({ rows }: { rows: Array<[string, unknown]> }) {
  return (
    <div className="mt-3 grid gap-2">
      {rows.map(([label, value]) => (
        <div key={label} className="grid gap-1 rounded-md border border-line bg-slate-50 px-3 py-2 text-sm md:grid-cols-[190px_1fr]">
          <span className="font-medium text-muted">{label}</span>
          <span className="break-words text-ink">{String(value ?? "pending")}</span>
        </div>
      ))}
    </div>
  );
}

function splitIds(value: string) {
  return value.split(",").map((item) => item.trim()).filter(Boolean);
}

function readNested(record: Record<string, unknown>, key: string, nestedKey: string) {
  const value = record[key];
  if (value && typeof value === "object" && nestedKey in value) {
    return String((value as Record<string, unknown>)[nestedKey] ?? 0);
  }
  return "0";
}
