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
  confirmPersonalCaseAnalysisLegalDraftForReview,
  createPersonalCaseAnalysisLegalDraft,
  createPersonalCaseAnalysisLegalDraftVersion,
  getPersonalCaseAnalysisAudit,
  getPersonalCaseAnalysisLegalDraft,
  getPersonalCaseAnalysisLegalDraftGate,
  getPersonalCaseAnalysisLegalDraftQuality,
  getPersonalCaseAnalysisReviewQueue,
  getPersonalCaseAnalysisSafety,
  listPersonalCaseAnalysisLegalDraftVersions,
  listPersonalCaseAnalysisLegalDrafts,
  listPersonalCaseAnalysisSourceTraces
} from "@/services/api";

const defaultCaseId = "open_case_mock_001";

export default function PersonalLegalDraftWorkbenchPage() {
  const [data, setData] = useState<Record<string, any>>({});
  const [error, setError] = useState("");
  const [caseId, setCaseId] = useState(defaultCaseId);
  const [draftId, setDraftId] = useState("");
  const [confirmed, setConfirmed] = useState(true);
  const [downloadNote, setDownloadNote] = useState("尚未生成下载 metadata");

  async function loadWorkbench(nextDraftId = draftId) {
    setError("");
    try {
      const [drafts, queue, traces, audit, safety] = await Promise.all([
        listPersonalCaseAnalysisLegalDrafts(),
        getPersonalCaseAnalysisReviewQueue(),
        listPersonalCaseAnalysisSourceTraces(),
        getPersonalCaseAnalysisAudit(),
        getPersonalCaseAnalysisSafety()
      ]);
      const selectedDraftId = nextDraftId || String(drafts.legal_drafts?.[0]?.legal_draft_id ?? "");
      const [draft, versions, quality, gate] = selectedDraftId
        ? await Promise.all([
            getPersonalCaseAnalysisLegalDraft(selectedDraftId),
            listPersonalCaseAnalysisLegalDraftVersions(selectedDraftId),
            getPersonalCaseAnalysisLegalDraftQuality(selectedDraftId),
            getPersonalCaseAnalysisLegalDraftGate(selectedDraftId)
          ])
        : [null, null, null, null];
      setDraftId(selectedDraftId);
      setData({ drafts, draft, versions, quality, gate, queue, traces, audit, safety });
    } catch {
      setError("法律分析草稿工作台 API 暂不可用。页面保持安全 fallback，不展示密钥值，不显示原始内容，不调用真实 provider。");
    }
  }

  useEffect(() => {
    void loadWorkbench();
  }, []);

  async function createDraft() {
    const result = await createPersonalCaseAnalysisLegalDraft({
      case_id: caseId,
      fact_draft_id: null,
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
    const nextDraftId = String(result.legal_draft_id ?? "");
    setDraftId(nextDraftId);
    await loadWorkbench(nextDraftId);
  }

  async function createVersion() {
    if (!draftId) return;
    await createPersonalCaseAnalysisLegalDraftVersion(draftId, {
      created_from: "owner_correction",
      change_summary: "用户本人修订法律分析草稿 metadata",
      explicit_owner_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed,
      explicit_no_training_data_confirmation: confirmed
    });
    await loadWorkbench(draftId);
  }

  async function confirmForReview() {
    if (!draftId) return;
    const result = await confirmPersonalCaseAnalysisLegalDraftForReview(draftId, {
      reviewer_id: "local_demo_lawyer",
      reviewer_note: "仅确认进入律师复核队列 metadata",
      explicit_owner_confirmation: confirmed,
      explicit_lawyer_review_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed,
      explicit_no_final_report_confirmation: confirmed,
      explicit_no_external_delivery_confirmation: confirmed
    });
    setData((current) => ({ ...current, reviewConfirmation: result }));
    await loadWorkbench(draftId);
  }

  const drafts = (data.drafts?.legal_drafts ?? []) as Array<Record<string, any>>;
  const versions = (data.versions?.versions ?? []) as Array<Record<string, any>>;
  const dimensionScores = useMemo(() => Object.entries(data.quality?.dimension_scores ?? {}), [data.quality]);

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}

        <section className="rounded-md border border-slate-800 bg-[#131b25] p-8 text-white shadow-sm">
          <div className="text-sm font-medium text-cyan-200">v7.21 Legal Analysis Draft Workbench</div>
          <h1 className="mt-3 text-4xl font-semibold">法律分析草稿工作台</h1>
          <p className="mt-4 max-w-4xl text-sm leading-6 text-slate-300">
            基于 v7.20 已确认的事实输入 metadata 生成法律分析草稿，展示争议焦点、请求权基础、抗辩路径、风险提示和下一步清单。输出仅为 draft metadata，不生成最终法律意见、不生成最终报告、不自动对外交付。
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            {["法律分析草稿", "仅元数据", "草稿状态", "律师复核必需", "来源追踪必需", "不生成最终法律意见", "不生成最终报告", "不自动交付"].map((badge) => (
              <DarkSafetyBadge key={badge} label={badge} />
            ))}
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-4">
          <StatusCard label="Legal Drafts" value={data.drafts?.draft_count ?? drafts.length} detail="legal_analysis_draft_only=true" tone="info" />
          <StatusCard label="Quality Score" value={data.quality?.overall_score ?? "pending"} detail="reference-only" tone="safe" />
          <StatusCard label="Gate" value={data.gate?.gate_status ?? "reference_only"} detail="blocks_next_stage=false" tone="warning" />
          <StatusCard label="Review Ready" value={String(data.reviewConfirmation?.review_ready ?? false)} detail="review queue only" tone="safe" />
        </section>

        <ShowcaseStepper
          columns="lg:grid-cols-5"
          steps={[
            { label: "事实输入", detail: "来自 v7.20 fact input metadata", status: "confirmed metadata" },
            { label: "法律分析草稿", detail: "争议、请求权、抗辩、风险", status: "draft" },
            { label: "版本管理", detail: "AI draft / owner corrected / owner confirmed", status: "traceable" },
            { label: "质量与门控", detail: "参考评分，不阻断下一步", status: "reference only" },
            { label: "律师复核", detail: "不生成最终意见或报告", status: "required" }
          ]}
        />

        <section className="grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
          <Panel title="创建 / 选择法律分析草稿" eyebrow="Legal Draft">
            <div className="grid gap-3">
              <label className="grid gap-2 text-sm">
                <span>Open Case ID</span>
                <input className="rounded-md border border-line px-3 py-2" value={caseId} onChange={(event) => setCaseId(event.target.value)} />
              </label>
              <label className="grid gap-2 text-sm">
                <span>Legal Draft ID</span>
                <select className="rounded-md border border-line px-3 py-2" value={draftId} onChange={(event) => void loadWorkbench(event.target.value)}>
                  {drafts.map((draft) => (
                    <option key={String(draft.legal_draft_id)} value={String(draft.legal_draft_id)}>{String(draft.legal_draft_id)}</option>
                  ))}
                  {drafts.length === 0 ? <option value="">暂无 legal draft</option> : null}
                </select>
              </label>
              <label className="flex gap-2 text-sm">
                <input type="checkbox" checked={confirmed} onChange={(event) => setConfirmed(event.target.checked)} />
                明确确认：仅生成法律分析草稿 metadata，不生成最终法律意见、最终报告或外部交付。
              </label>
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void createDraft()}>
                创建法律分析草稿
              </button>
            </div>
          </Panel>

          <Panel title="Draft Cards" eyebrow="法律分析草稿">
            <div className="grid gap-3 md:grid-cols-2">
              <DraftCard title="法律分析摘要" content={data.draft?.legal_analysis_summary_draft} />
              <DraftCard title="争议焦点" content={(data.draft?.dispute_focus_draft ?? data.draft?.issue_spotting_draft ?? []).join(" / ")} />
              <DraftCard title="请求权基础" content={(data.draft?.claim_basis_draft ?? []).join(" / ")} />
              <DraftCard title="抗辩路径" content={(data.draft?.defense_path_draft ?? []).join(" / ")} />
              <DraftCard title="风险提示" content={(data.draft?.risk_flags_draft ?? []).join(" / ")} />
              <DraftCard title="下一步清单" content={(data.draft?.next_action_checklist_draft ?? []).join(" / ")} />
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="版本管理">
            <div className="grid gap-3">
              {versions.map((version) => (
                <RuntimeCard
                  key={String(version.version_id)}
                  title={`版本 ${String(version.version_number)}`}
                  category={String(version.created_from)}
                  status={String(version.review_ready ? "review ready" : "draft metadata")}
                  items={[
                    ["version_id", version.version_id],
                    ["owner_confirmed", version.owner_confirmed],
                    ["legal_analysis_draft_only", version.legal_analysis_draft_only],
                    ["final_legal_opinion_generated", version.final_legal_opinion_generated],
                    ["change_summary", version.change_summary]
                  ]}
                />
              ))}
              <button className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void createVersion()}>
                生成用户修订版本 metadata
              </button>
            </div>
          </Panel>

          <Panel title="Quality / Gate Panel">
            <InfoRows
              rows={[
                ["overall_score", data.quality?.overall_score ?? "pending"],
                ["gate_status", data.gate?.gate_status ?? "reference_only"],
                ["gate_score", data.gate?.gate_score ?? "pending"],
                ["gate_reference_only", data.gate?.gate_reference_only ?? true],
                ["blocks_next_stage", data.gate?.blocks_next_stage ?? false],
                ["final_legal_opinion_generated", data.gate?.final_legal_opinion_generated ?? false]
              ]}
            />
            <div className="mt-3 grid gap-2">
              {dimensionScores.map(([label, value]) => (
                <div key={label} className="rounded-md border border-line bg-slate-50 px-3 py-2 text-sm">
                  <div className="flex items-center justify-between gap-3">
                    <span>{label}</span>
                    <span className="font-semibold text-cyan-800">{String(value)}</span>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-3 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
              门控仅作为质量评分与优化方向，不阻断下一步。
            </div>
          </Panel>

          <Panel title="Review Queue">
            <div className="grid gap-3">
              <InfoRows rows={[["pending_count", data.queue?.pending_count ?? 0], ["item_count", data.queue?.item_count ?? 0], ["review_ready", data.reviewConfirmation?.review_ready ?? false]]} />
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void confirmForReview()}>
                确认进入律师复核
              </button>
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Optimization Suggestions">
            <div className="grid gap-2">
              {(data.quality?.optimization_suggestions ?? data.gate?.missing_information_checklist ?? []).map((item: string) => (
                <div key={item} className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-xs leading-5 text-amber-900">{item}</div>
              ))}
            </div>
          </Panel>
          <Panel title="Source Trace Panel">
            <InfoRows
              rows={[
                ["source_trace_count", data.traces?.source_trace_count ?? 0],
                ["source_trace_required", data.traces?.source_trace_required ?? true],
                ["raw_content_included", data.traces?.raw_content_included ?? false],
                ["raw_ocr_text_included", data.traces?.raw_ocr_text_included ?? false],
                ["ai_prompt_injected", data.traces?.ai_prompt_injected ?? false]
              ]}
            />
          </Panel>
          <Panel title="Owner Download Boundary">
            <InfoRows
              rows={[
                ["owner_only", data.draft?.owner_only ?? true],
                ["owner_download_ready", data.draft?.owner_download_ready ?? true],
                ["public_link_created", data.draft?.public_link_created ?? false],
                ["email_sent", data.draft?.email_sent ?? false],
                ["external_delivery_triggered", data.draft?.external_delivery_triggered ?? false],
                ["real_pdf_docx_generated", data.draft?.real_pdf_docx_generated ?? false]
              ]}
            />
            <button className="mt-3 rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => setDownloadNote("已生成 owner-only 下载 metadata；未创建真实文件、公开链接或邮件。")}>
              生成用户本人下载 metadata
            </button>
            <div className="mt-3 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">{downloadNote}</div>
          </Panel>
        </section>

        <TrustSafetyPanel
          title="信任与安全面板"
          note="v7.21 仅生成法律分析草稿 metadata；不生成最终法律意见、最终报告、真实 PDF/DOCX、邮件、公开链接或外部交付。"
          items={data.safety?.safety_checklist ?? []}
        />
        <DiagnosticsPanel data={data} />
      </div>
    </AppShell>
  );
}

function DraftCard({ title, content }: { title: string; content?: string }) {
  return (
    <div className="rounded-md border border-line bg-slate-50 p-4">
      <div className="text-sm font-semibold text-ink">{title}</div>
      <div className="mt-2 text-xs leading-5 text-muted">{content || "法律分析草稿 metadata 待加载"}</div>
      <div className="mt-3 text-xs text-amber-800">仅供律师复核，不是最终法律意见。</div>
    </div>
  );
}
