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
  confirmPersonalCaseWorkspaceFactPreviewForLegalAnalysis,
  createPersonalCaseWorkspaceFactPreview,
  createPersonalCaseWorkspaceFactPreviewCorrection,
  createPersonalCaseWorkspaceFactPreviewVersion,
  createPersonalCaseWorkspaceOwnerRawView,
  getPersonalCaseWorkspaceAudit,
  getPersonalCaseWorkspaceFactAudit,
  getPersonalCaseWorkspaceFactInput,
  getPersonalCaseWorkspaceFactInputReadiness,
  getPersonalCaseWorkspaceFactPreview,
  getPersonalCaseWorkspaceFactPreviewGate,
  getPersonalCaseWorkspaceFactPreviewQuality,
  getPersonalCaseWorkspaceFactPreviewSourceTraces,
  getPersonalCaseWorkspaceFactSafety,
  getPersonalCaseWorkspaceMaterial,
  getPersonalCaseWorkspaceMaterialSourceTraces,
  getPersonalCaseWorkspaceOCRStatus,
  getPersonalCaseWorkspaceSafety,
  getPersonalCaseWorkspaceStatus,
  listPersonalCaseWorkspaceCases,
  listPersonalCaseWorkspaceFactPreviewCorrections,
  listPersonalCaseWorkspaceFactPreviewVersions,
  listPersonalCaseWorkspaceFactPreviews,
  listPersonalCaseWorkspaceMaterials,
  listPersonalCaseWorkspaceSourceTraces
} from "@/services/api";

const fallbackCaseId = "case_workspace_mock_001";
const fallbackMaterialId = "material_contract_metadata_001";
const fallbackFactPreviewId = "fact_preview_mock_001";

export default function PersonalCaseWorkspacePage() {
  const [data, setData] = useState<Record<string, any>>({});
  const [error, setError] = useState("");
  const [caseId, setCaseId] = useState(fallbackCaseId);
  const [materialId, setMaterialId] = useState(fallbackMaterialId);
  const [factPreviewId, setFactPreviewId] = useState(fallbackFactPreviewId);
  const [confirmed, setConfirmed] = useState(true);
  const [ownerDownloadNote, setOwnerDownloadNote] = useState("尚未请求");

  async function loadWorkspace(nextCaseId = caseId, nextMaterialId = materialId, nextFactPreviewId = factPreviewId) {
    setError("");
    try {
      const [
        status,
        cases,
        materials,
        material,
        ocr,
        factInput,
        materialTraces,
        traces,
        audit,
        safety,
        factPreviews,
        factInputReadiness,
        factAudit,
        factSafety
      ] = await Promise.all([
        getPersonalCaseWorkspaceStatus(),
        listPersonalCaseWorkspaceCases(),
        listPersonalCaseWorkspaceMaterials(nextCaseId),
        getPersonalCaseWorkspaceMaterial(nextMaterialId),
        getPersonalCaseWorkspaceOCRStatus(nextMaterialId),
        getPersonalCaseWorkspaceFactInput(nextMaterialId),
        getPersonalCaseWorkspaceMaterialSourceTraces(nextMaterialId),
        listPersonalCaseWorkspaceSourceTraces(),
        getPersonalCaseWorkspaceAudit(),
        getPersonalCaseWorkspaceSafety(),
        listPersonalCaseWorkspaceFactPreviews(),
        getPersonalCaseWorkspaceFactInputReadiness(),
        getPersonalCaseWorkspaceFactAudit(),
        getPersonalCaseWorkspaceFactSafety()
      ]);
      const firstPreviewId = String((factPreviews.fact_previews as Array<Record<string, any>> | undefined)?.[0]?.fact_preview_id ?? nextFactPreviewId);
      const selectedPreviewId = nextFactPreviewId || firstPreviewId;
      const [factPreview, corrections, versions, quality, gate, factPreviewTraces] = await Promise.all([
        getPersonalCaseWorkspaceFactPreview(selectedPreviewId),
        listPersonalCaseWorkspaceFactPreviewCorrections(selectedPreviewId),
        listPersonalCaseWorkspaceFactPreviewVersions(selectedPreviewId),
        getPersonalCaseWorkspaceFactPreviewQuality(selectedPreviewId),
        getPersonalCaseWorkspaceFactPreviewGate(selectedPreviewId),
        getPersonalCaseWorkspaceFactPreviewSourceTraces(selectedPreviewId)
      ]);
      setData({
        status,
        cases,
        materials,
        material,
        ocr,
        factInput,
        materialTraces,
        traces,
        audit,
        safety,
        factPreviews,
        factPreview,
        corrections,
        versions,
        quality,
        gate,
        factPreviewTraces,
        factInputReadiness,
        factAudit,
        factSafety
      });
      const firstCase = String((cases.cases as Array<Record<string, any>> | undefined)?.[0]?.case_id ?? nextCaseId);
      const firstMaterial = String((materials.materials as Array<Record<string, any>> | undefined)?.[0]?.material_id ?? nextMaterialId);
      setCaseId(firstCase || fallbackCaseId);
      setMaterialId(firstMaterial || fallbackMaterialId);
      setFactPreviewId(selectedPreviewId || fallbackFactPreviewId);
    } catch {
      setError("事实预览与输入纠正工作台 API 暂不可用。页面保持安全 fallback，不展示密钥值，不显示原始内容，不调用真实 provider。");
    }
  }

  useEffect(() => {
    void loadWorkspace();
  }, []);

  async function triggerOwnerRawView() {
    const result = await createPersonalCaseWorkspaceOwnerRawView(materialId, {
      explicit_owner_confirmation: confirmed,
      explicit_no_external_delivery_confirmation: confirmed,
      explicit_no_training_data_confirmation: confirmed,
      explicit_no_ai_prompt_confirmation: confirmed
    });
    setData((current) => ({ ...current, ownerRawView: result }));
  }

  async function createFactPreview() {
    const result = await createPersonalCaseWorkspaceFactPreview({
      case_id: caseId,
      material_ids: [materialId],
      explicit_owner_confirmation: confirmed,
      explicit_no_training_data_confirmation: confirmed,
      explicit_no_auto_legal_analysis_confirmation: confirmed
    });
    const nextId = String(result.fact_preview_id ?? fallbackFactPreviewId);
    setFactPreviewId(nextId);
    await loadWorkspace(caseId, materialId, nextId);
  }

  async function createFactCorrection() {
    const result = await createPersonalCaseWorkspaceFactPreviewCorrection(factPreviewId, {
      corrected_sections: ["fact_summary_draft", "timeline_draft"],
      correction_reason: "用户本人纠正事实预览 metadata",
      correction_type: "owner_fact_correction",
      explicit_owner_confirmation: confirmed,
      explicit_no_training_data_confirmation: confirmed,
      explicit_no_skill_update_confirmation: confirmed,
      explicit_no_auto_legal_analysis_confirmation: confirmed
    });
    setData((current) => ({ ...current, latestCorrection: result }));
    await loadWorkspace(caseId, materialId, factPreviewId);
  }

  async function createFactVersion() {
    const result = await createPersonalCaseWorkspaceFactPreviewVersion(factPreviewId, {
      created_from: "owner_correction",
      change_summary: "用户本人确认事实纠正后生成版本 metadata",
      explicit_owner_confirmation: confirmed,
      explicit_no_training_data_confirmation: confirmed
    });
    setData((current) => ({ ...current, latestVersion: result }));
    await loadWorkspace(caseId, materialId, factPreviewId);
  }

  async function confirmForLegalAnalysis() {
    const result = await confirmPersonalCaseWorkspaceFactPreviewForLegalAnalysis(factPreviewId, {
      explicit_owner_confirmation: confirmed,
      explicit_source_trace_confirmation: confirmed,
      explicit_no_auto_legal_analysis_confirmation: confirmed,
      explicit_no_training_data_confirmation: confirmed
    });
    setData((current) => ({ ...current, legalAnalysisInputConfirmation: result }));
    await loadWorkspace(caseId, materialId, factPreviewId);
  }

  const cases = (data.cases?.cases ?? []) as Array<Record<string, any>>;
  const materials = (data.materials?.materials ?? []) as Array<Record<string, any>>;
  const factPreviews = (data.factPreviews?.fact_previews ?? []) as Array<Record<string, any>>;
  const corrections = (data.corrections?.corrections ?? []) as Array<Record<string, any>>;
  const versions = (data.versions?.versions ?? []) as Array<Record<string, any>>;
  const readinessItems = (data.factInputReadiness?.readiness_items ?? []) as Array<Record<string, any>>;
  const dimensionScores = useMemo(() => Object.entries(data.quality?.dimension_scores ?? {}), [data.quality]);
  const sourceTraceIds = (data.factPreview?.source_trace_ids ?? []) as string[];

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}

        <section className="overflow-hidden rounded-md border border-slate-800 bg-[#121a22] text-white shadow-sm">
          <div className="grid gap-6 p-6 md:grid-cols-[1.35fr_0.75fr] md:p-8">
            <div>
              <div className="text-sm font-medium text-cyan-200">v7.20 Fact Preview & Correction Workbench</div>
              <h1 className="mt-3 text-4xl font-semibold">事实预览与输入纠正工作台</h1>
              <p className="mt-4 max-w-4xl text-sm leading-6 text-slate-300">
                在案件与材料 metadata 之上生成事实预览草稿，允许用户本人查看、纠正、确认版本，并在明确确认后作为后续法律分析输入 metadata。这里不自动触发法律分析，不写训练集，不更新或发布 Skill，不生成最终事实认定。
              </p>
              <div className="mt-5 flex flex-wrap gap-2">
                {["事实预览", "用户本人纠正", "版本历史", "质量参考", "法律分析输入需确认", "不自动法律分析", "不写训练集", "不发布 Skill"].map((badge) => (
                  <DarkSafetyBadge key={badge} label={badge} />
                ))}
              </div>
            </div>
            <div className="rounded-md border border-slate-700 bg-white/5 p-5">
              <div className="text-xs uppercase tracking-wide text-cyan-200">Fact posture</div>
              <div className="mt-4 grid gap-3">
                <StatusLine label="owner_correction_allowed" value={data.factSafety?.owner_correction_allowed ?? true} />
                <StatusLine label="legal_analysis_input_allowed" value={data.factSafety?.legal_analysis_input_allowed ?? true} />
                <StatusLine label="legal_analysis_auto_triggered" value={data.factSafety?.legal_analysis_auto_triggered ?? false} invert />
                <StatusLine label="final_fact_finding" value={data.factSafety?.final_fact_finding ?? false} invert />
              </div>
            </div>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-4">
          <StatusCard label="Fact Preview" value={data.factPreviews?.fact_preview_count ?? factPreviews.length} detail="AI draft metadata only" tone="info" />
          <StatusCard label="Quality Score" value={data.quality?.overall_score ?? 82} detail="reference-only gate" tone="safe" />
          <StatusCard label="Correction" value={data.factPreview?.correction_status ?? "correction_allowed"} detail="owner-only metadata" tone="warning" />
          <StatusCard label="Legal Analysis" value={String(data.legalAnalysisInputConfirmation?.legal_analysis_input_ready ?? false)} detail="ready does not auto-trigger" tone="safe" />
        </section>

        <ShowcaseStepper
          columns="lg:grid-cols-5"
          steps={[
            { label: "材料 metadata", detail: "材料与 OCR 状态只返回 metadata", status: "raw hidden" },
            { label: "事实预览", detail: "事实摘要、证据映射、时间线、争议事实", status: "draft" },
            { label: "用户纠正", detail: "用户本人确认后保存纠正 metadata", status: "owner-only" },
            { label: "版本历史", detail: "AI 草稿、用户纠正、用户确认版本", status: "traceable" },
            { label: "法律分析输入", detail: "仅标记 ready，不自动启动分析", status: "gated" }
          ]}
        />

        <section className="grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
          <Panel title="选择案件 / 材料 / 事实预览" eyebrow="Workspace">
            <div className="grid gap-3">
              <Select label="Case ID" value={caseId} onChange={(value) => void loadWorkspace(value, materialId, factPreviewId)} options={cases.map((item) => [String(item.case_id), String(item.case_alias)])} fallback={[fallbackCaseId, "个人本地试点案件 metadata"]} />
              <Select label="Material ID" value={materialId} onChange={(value) => void loadWorkspace(caseId, value, factPreviewId)} options={materials.map((item) => [String(item.material_id), String(item.material_title)])} fallback={[fallbackMaterialId, "合同类材料 metadata"]} />
              <Select label="Fact Preview ID" value={factPreviewId} onChange={(value) => void loadWorkspace(caseId, materialId, value)} options={factPreviews.map((item) => [String(item.fact_preview_id), String(item.preview_status)])} fallback={[fallbackFactPreviewId, "事实预览模拟元数据"]} />
              <label className="flex gap-2 text-sm">
                <input type="checkbox" checked={confirmed} onChange={(event) => setConfirmed(event.target.checked)} />
                明确确认：仅用户本人查看与纠正，不写训练集、不更新 Skill、不自动触发法律分析、不对外交付。
              </label>
            </div>
          </Panel>

          <Panel title="Fact Draft Cards" eyebrow="事实草稿">
            <div className="grid gap-3 md:grid-cols-2">
              <FactCard title="事实摘要" content={data.factPreview?.fact_summary_draft} score={data.quality?.dimension_scores?.fact_summary ?? 84} />
              <FactCard title="证据映射" content={data.factPreview?.evidence_mapping_draft} score={data.quality?.dimension_scores?.evidence_mapping ?? 80} />
              <FactCard title="时间线" content={data.factPreview?.timeline_draft} score={data.quality?.dimension_scores?.timeline ?? 78} />
              <FactCard title="争议与缺失事实" content={`${data.factPreview?.disputed_facts_draft ?? "争议事实待确认"} / ${data.factPreview?.missing_facts_draft ?? "缺失事实待补充"}`} score={data.quality?.dimension_scores?.missing_fact_coverage ?? 76} />
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Correction Panel" eyebrow="用户纠正">
            <div className="grid gap-3">
              <InfoRows
                rows={[
                  ["correction_count", data.corrections?.correction_count ?? corrections.length],
                  ["latest_correction_status", data.latestCorrection?.correction_status ?? data.factPreview?.correction_status ?? "correction_allowed"],
                  ["training_data_generated", data.latestCorrection?.training_data_generated ?? false],
                  ["skill_updated", data.latestCorrection?.skill_updated ?? false],
                  ["legal_analysis_auto_triggered", data.latestCorrection?.legal_analysis_auto_triggered ?? false]
                ]}
              />
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void createFactCorrection()}>
                保存事实纠正
              </button>
              <button className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void createFactVersion()}>
                查看版本历史
              </button>
              <button className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void confirmForLegalAnalysis()}>
                标记为法律分析输入
              </button>
              <button className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => setOwnerDownloadNote("已生成用户本人留存 metadata；未创建真实文件、公开链接或邮件。")}>
                下载本人留存
              </button>
              <div className="rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">{ownerDownloadNote}</div>
            </div>
          </Panel>

          <Panel title="Quality / Gate Panel" eyebrow="质量参考">
            <div className="grid gap-3">
              <InfoRows
                rows={[
                  ["overall_score", data.quality?.overall_score ?? 82],
                  ["gate_status", data.gate?.gate_status ?? "yellow"],
                  ["gate_score", data.gate?.gate_score ?? 80],
                  ["gate_reference_only", data.gate?.gate_reference_only ?? true],
                  ["blocks_next_stage", data.gate?.blocks_next_stage ?? false],
                  ["final_fact_finding", data.gate?.final_fact_finding ?? false]
                ]}
              />
              <div className="grid gap-2">
                {dimensionScores.map(([label, value]) => (
                  <div key={label} className="rounded-md border border-line bg-slate-50 px-3 py-2 text-sm">
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-ink">{label}</span>
                      <span className="text-cyan-800">{String(value)}</span>
                    </div>
                  </div>
                ))}
              </div>
              {(data.quality?.optimization_suggestions ?? data.gate?.optimization_suggestions ?? []).map((suggestion: string) => (
                <div key={suggestion} className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-xs leading-5 text-amber-900">{suggestion}</div>
              ))}
              <div className="rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
                门控仅作为质量参考，不阻断下一步；进入法律分析仍需用户本人显式确认。
              </div>
            </div>
          </Panel>

          <Panel title="Legal Analysis Input Readiness" eyebrow="输入准备度">
            <InfoRows
              rows={[
                ["readiness_count", data.factInputReadiness?.readiness_count ?? readinessItems.length],
                ["confirmed_ready", data.legalAnalysisInputConfirmation?.legal_analysis_input_ready ?? false],
                ["owner_confirmed", data.legalAnalysisInputConfirmation?.owner_confirmed ?? false],
                ["source_trace_ready", data.legalAnalysisInputConfirmation?.source_trace_ready ?? true],
                ["legal_analysis_auto_triggered", data.legalAnalysisInputConfirmation?.legal_analysis_auto_triggered ?? false],
                ["training_data_generated", data.legalAnalysisInputConfirmation?.training_data_generated ?? false]
              ]}
            />
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Fact Version Timeline">
            <div className="grid gap-3">
              {versions.map((version) => (
                <RuntimeCard
                  key={String(version.version_id)}
                  title={`版本 ${String(version.version_number)} · ${String(version.version_type)}`}
                  category={String(version.created_from)}
                  status={String(version.legal_analysis_input_ready ? "input ready" : "draft metadata")}
                  items={[
                    ["version_id", version.version_id],
                    ["owner_confirmed", version.owner_confirmed],
                    ["training_data_generated", version.training_data_generated],
                    ["skill_published", version.skill_published],
                    ["change_summary", version.change_summary]
                  ]}
                />
              ))}
              {versions.length === 0 ? <div className="rounded-md border border-dashed border-line bg-slate-50 p-4 text-sm text-muted">暂无版本历史，可点击“查看版本历史”生成模拟元数据。</div> : null}
            </div>
          </Panel>

          <Panel title="Source Trace Panel">
            <InfoRows
              rows={[
                ["source_trace_count", sourceTraceIds.length || data.traces?.source_trace_count || 0],
                ["confirmed_count", data.factPreviewTraces?.confirmed_count ?? data.traces?.confirmed_count ?? 0],
                ["source_trace_required", data.factPreview?.source_trace_required ?? true],
                ["raw_content_returned", data.factPreview?.raw_content_returned ?? false],
                ["used_in_ai_prompt", false]
              ]}
            />
            <div className="mt-3 grid gap-2">
              {sourceTraceIds.slice(0, 6).map((traceId) => (
                <div key={traceId} className="rounded-md border border-line bg-slate-50 px-3 py-2 text-xs text-ink">{traceId}</div>
              ))}
            </div>
          </Panel>

          <Panel title="Owner Download Boundary">
            <InfoRows
              rows={[
                ["downloadable_by_owner_only", data.factPreview?.downloadable_by_owner_only ?? true],
                ["export_allowed", data.factPreview?.export_allowed ?? true],
                ["real_pdf_docx_generated", data.factPreview?.real_pdf_docx_generated ?? false],
                ["public_link_created", data.factPreview?.public_link_created ?? false],
                ["email_sent", data.factPreview?.email_sent ?? false],
                ["external_delivery_triggered", data.factPreview?.external_delivery_triggered ?? false]
              ]}
            />
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="材料与 OCR metadata">
            <InfoRows
              rows={[
                ["material_id", data.material?.material_id ?? materialId],
                ["ocr_status", data.ocr?.ocr_status ?? "mock_metadata_ready"],
                ["ocr_provider_called", data.ocr?.ocr_provider_called ?? false],
                ["raw_ocr_text_returned", data.ocr?.raw_ocr_text_returned ?? false],
                ["fact_input_status", data.factInput?.fact_input_status ?? "draft_metadata_ready"]
              ]}
            />
            <div className="mt-3">
              <button className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void triggerOwnerRawView()}>
                请求用户本人原文查看 metadata
              </button>
            </div>
          </Panel>
          <Panel title="Fact Audit">
            <InfoRows
              rows={[
                ["event_count", data.factAudit?.event_count ?? 0],
                ["audit_required", data.factAudit?.audit_required ?? true],
                ["raw_content_written_to_diagnostics", data.factAudit?.raw_content_written_to_diagnostics ?? false],
                ["local_path_visible", data.factAudit?.local_path_visible ?? false]
              ]}
            />
          </Panel>
          <Panel title="创建事实预览">
            <div className="grid gap-3">
              <InfoRows rows={[["case_id", caseId], ["material_id", materialId], ["explicit_owner_confirmation", confirmed]]} />
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void createFactPreview()}>
                创建事实预览 mock
              </button>
            </div>
          </Panel>
        </section>

        <TrustSafetyPanel
          title="信任与安全面板"
          note="v7.20 只处理事实层：用户本人可查看、纠正、确认和下载 metadata；事实可作为法律分析输入，但不会自动触发法律分析，不训练未结案件，不更新或发布 Skill。"
          items={data.factSafety?.safety_checklist ?? data.safety?.safety_checklist ?? []}
        />
        <DiagnosticsPanel data={data} />
      </div>
    </AppShell>
  );
}

function Select({
  label,
  value,
  onChange,
  options,
  fallback
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: string[][];
  fallback: string[];
}) {
  const renderedOptions = options.length ? options : [fallback];
  return (
    <label className="grid gap-2 text-sm">
      <span>{label}</span>
      <select className="rounded-md border border-line px-3 py-2" value={value} onChange={(event) => onChange(event.target.value)}>
        {renderedOptions.map(([optionValue, optionLabel]) => (
          <option key={optionValue} value={optionValue}>{optionLabel}</option>
        ))}
      </select>
    </label>
  );
}

function FactCard({ title, content, score }: { title: string; content?: string; score: number }) {
  return (
    <div className="rounded-md border border-line bg-slate-50 p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm font-semibold text-ink">{title}</div>
          <div className="mt-2 text-xs leading-5 text-muted">{content ?? "事实 draft metadata 待加载"}</div>
        </div>
        <div className="rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-right">
          <div className="text-xs text-cyan-800">score</div>
          <div className="text-xl font-semibold text-cyan-950">{score}</div>
        </div>
      </div>
      <div className="mt-3 text-xs text-amber-800">仅供事实核对，不是最终事实认定。</div>
    </div>
  );
}

function StatusLine({ label, value, invert = false }: { label: string; value: boolean; invert?: boolean }) {
  const safe = invert ? !value : value;
  return (
    <div className="flex items-center justify-between rounded-md border border-slate-700 bg-slate-950/40 px-3 py-2">
      <span className="text-xs text-slate-300">{label}</span>
      <span className={`rounded-md border px-2 py-1 text-xs font-medium ${safe ? "border-emerald-300/40 bg-emerald-300/10 text-emerald-100" : "border-amber-300/40 bg-amber-300/10 text-amber-100"}`}>
        {String(value)}
      </span>
    </div>
  );
}
