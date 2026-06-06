"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DiagnosticsPanel,
  SafeErrorNotice,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  PersonalMaterialAuditTimeline,
  PersonalMaterialLiveAuditTimeline,
  PersonalMaterialLiveGatewayStatus,
  PersonalMaterialLiveGateList,
  PersonalMaterialLiveGateStatus,
  PersonalMaterialLiveHealthDryRun,
  PersonalMaterialLiveProviderReadinessList,
  PersonalMaterialLiveReviewActionResult,
  PersonalMaterialLiveReviewQueue,
  PersonalMaterialLiveRunList,
  PersonalMaterialLiveRunRecord,
  PersonalMaterialLiveSafetyStatus,
  PersonalMaterialLiveSecretBoundary,
  PersonalMaterialLiveSourceTraceList,
  PersonalMaterialParseJobList,
  PersonalMaterialParseJobResult,
  PersonalMaterialProviderList,
  PersonalMaterialRuntimeStatus,
  PersonalMaterialSafetyStatus,
  PersonalMaterialSourceTraceList,
  PersonalOCRJobList,
  PersonalOCRJobResult,
  PersonalOCRPreview,
  PersonalOCRReviewActionResult,
  PersonalOCRReviewQueue,
  createPersonalMaterialDocumentLiveDryRun,
  createPersonalMaterialLiveGateMock,
  createPersonalMaterialDocumentLiveRun,
  createPersonalMaterialOCRLiveDryRun,
  createPersonalMaterialOCRLiveRun,
  createPersonalMaterialParseJob,
  createPersonalOCRJob,
  getPersonalMaterialAudit,
  getPersonalMaterialLiveAudit,
  getPersonalMaterialLiveGate,
  getPersonalMaterialLiveHealthDryRun,
  getPersonalMaterialLiveProviders,
  getPersonalMaterialLiveReviewQueue,
  getPersonalMaterialLiveSafety,
  getPersonalMaterialLiveSecretBoundary,
  getPersonalMaterialLiveSourceTraces,
  getPersonalMaterialLiveStatus,
  getPersonalMaterialRuntimeProviders,
  getPersonalMaterialRuntimeStatus,
  getPersonalMaterialSafety,
  getPersonalMaterialSourceTraces,
  getPersonalOCRPreview,
  getPersonalOCRReviewQueue,
  listPersonalMaterialDocumentLiveRuns,
  listPersonalMaterialLiveGates,
  listPersonalMaterialOCRLiveRuns,
  listPersonalMaterialParseJobs,
  listPersonalOCRJobs,
  submitPersonalMaterialLiveReviewAction,
  submitPersonalOCRReviewAction
} from "@/services/api";

const defaultCaseId = "case_v55_approve_all";
const defaultMaterialId = "material_demo_001";
const parseTypes = [
  "pdf_text_extract_preview",
  "pdf_to_images_preview",
  "docx_structure_preview",
  "excel_table_preview",
  "image_metadata_preview",
  "archive_listing_preview"
];
const ocrJobTypes = [
  "image_ocr_preview",
  "scanned_pdf_ocr_preview",
  "table_ocr_preview",
  "layout_analysis_preview",
  "key_information_preview"
];
const reviewActions = [
  "approve_preview_for_analysis",
  "request_manual_correction",
  "reject_ocr_preview",
  "mark_low_confidence"
];
const liveReviewActions = [
  "approve_metadata_only",
  "request_manual_review",
  "reject",
  "mark_low_confidence",
  "allow_redacted_preview",
  "block_raw_content"
];

export default function PersonalMaterialRuntimePage() {
  const [status, setStatus] = useState<PersonalMaterialRuntimeStatus | null>(null);
  const [providers, setProviders] = useState<PersonalMaterialProviderList | null>(null);
  const [parseJobs, setParseJobs] = useState<PersonalMaterialParseJobList | null>(null);
  const [ocrJobs, setOCRJobs] = useState<PersonalOCRJobList | null>(null);
  const [reviewQueue, setReviewQueue] = useState<PersonalOCRReviewQueue | null>(null);
  const [sourceTraces, setSourceTraces] = useState<PersonalMaterialSourceTraceList | null>(null);
  const [audit, setAudit] = useState<PersonalMaterialAuditTimeline | null>(null);
  const [safety, setSafety] = useState<PersonalMaterialSafetyStatus | null>(null);
  const [liveStatus, setLiveStatus] = useState<PersonalMaterialLiveGatewayStatus | null>(null);
  const [liveProviders, setLiveProviders] = useState<PersonalMaterialLiveProviderReadinessList | null>(null);
  const [liveSecretBoundary, setLiveSecretBoundary] = useState<PersonalMaterialLiveSecretBoundary | null>(null);
  const [liveGate, setLiveGate] = useState<PersonalMaterialLiveGateStatus | null>(null);
  const [liveGateList, setLiveGateList] = useState<PersonalMaterialLiveGateList | null>(null);
  const [liveHealth, setLiveHealth] = useState<PersonalMaterialLiveHealthDryRun | null>(null);
  const [documentLiveRuns, setDocumentLiveRuns] = useState<PersonalMaterialLiveRunList | null>(null);
  const [ocrLiveRuns, setOCRLiveRuns] = useState<PersonalMaterialLiveRunList | null>(null);
  const [liveReviewQueue, setLiveReviewQueue] = useState<PersonalMaterialLiveReviewQueue | null>(null);
  const [liveSourceTraces, setLiveSourceTraces] = useState<PersonalMaterialLiveSourceTraceList | null>(null);
  const [liveAudit, setLiveAudit] = useState<PersonalMaterialLiveAuditTimeline | null>(null);
  const [liveSafety, setLiveSafety] = useState<PersonalMaterialLiveSafetyStatus | null>(null);
  const [parseResult, setParseResult] = useState<PersonalMaterialParseJobResult | null>(null);
  const [ocrResult, setOCRResult] = useState<PersonalOCRJobResult | null>(null);
  const [ocrPreview, setOCRPreview] = useState<PersonalOCRPreview | null>(null);
  const [reviewResult, setReviewResult] = useState<PersonalOCRReviewActionResult | null>(null);
  const [documentLiveResult, setDocumentLiveResult] = useState<PersonalMaterialLiveRunRecord | null>(null);
  const [ocrLiveResult, setOCRLiveResult] = useState<PersonalMaterialLiveRunRecord | null>(null);
  const [liveReviewResult, setLiveReviewResult] = useState<PersonalMaterialLiveReviewActionResult | null>(null);
  const [caseId, setCaseId] = useState(defaultCaseId);
  const [materialId, setMaterialId] = useState(defaultMaterialId);
  const [parserProvider, setParserProvider] = useState("mineru_file_parser_provider");
  const [ocrProvider, setOCRProvider] = useState("paddleocr_provider");
  const [parseType, setParseType] = useState("pdf_text_extract_preview");
  const [ocrJobType, setOCRJobType] = useState("scanned_pdf_ocr_preview");
  const [reviewAction, setReviewAction] = useState("approve_preview_for_analysis");
  const [liveDocumentProvider, setLiveDocumentProvider] = useState("mineru");
  const [liveOCRProvider, setLiveOCRProvider] = useState("paddleocr");
  const [liveFileType, setLiveFileType] = useState("pdf");
  const [liveByteSize, setLiveByteSize] = useState(1200000);
  const [liveReviewAction, setLiveReviewAction] = useState("approve_metadata_only");
  const [selectedLiveReviewItemId, setSelectedLiveReviewItemId] = useState("");
  const [selectedLiveProviderId, setSelectedLiveProviderId] = useState("paddleocr");
  const [selectedOCRJobId, setSelectedOCRJobId] = useState("");
  const [parseConfirmed, setParseConfirmed] = useState(true);
  const [ocrConfirmed, setOCRConfirmed] = useState(true);
  const [reviewConfirmed, setReviewConfirmed] = useState(true);
  const [liveConfirmed, setLiveConfirmed] = useState(false);
  const [liveReviewConfirmed, setLiveReviewConfirmed] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadRuntime() {
    setLoading(true);
    setError("");
    try {
      const [
        nextStatus,
        nextProviders,
        nextParseJobs,
        nextOCRJobs,
        nextQueue,
        nextTraces,
        nextAudit,
        nextSafety,
        nextLiveStatus,
        nextLiveProviders,
        nextLiveSecretBoundary,
        nextLiveGate,
        nextLiveGateList,
        nextLiveHealth,
        nextDocumentRuns,
        nextOCRRuns,
        nextLiveQueue,
        nextLiveTraces,
        nextLiveAudit,
        nextLiveSafety
      ] =
        await Promise.all([
          getPersonalMaterialRuntimeStatus(),
          getPersonalMaterialRuntimeProviders(),
          listPersonalMaterialParseJobs(),
          listPersonalOCRJobs(),
          getPersonalOCRReviewQueue(),
          getPersonalMaterialSourceTraces(),
          getPersonalMaterialAudit(),
          getPersonalMaterialSafety(),
          getPersonalMaterialLiveStatus(),
          getPersonalMaterialLiveProviders(),
          getPersonalMaterialLiveSecretBoundary(selectedLiveProviderId),
          getPersonalMaterialLiveGate(selectedLiveProviderId),
          listPersonalMaterialLiveGates(),
          getPersonalMaterialLiveHealthDryRun(selectedLiveProviderId),
          listPersonalMaterialDocumentLiveRuns(),
          listPersonalMaterialOCRLiveRuns(),
          getPersonalMaterialLiveReviewQueue(),
          getPersonalMaterialLiveSourceTraces(),
          getPersonalMaterialLiveAudit(),
          getPersonalMaterialLiveSafety()
        ]);
      setStatus(nextStatus);
      setProviders(nextProviders);
      setParseJobs(nextParseJobs);
      setOCRJobs(nextOCRJobs);
      setReviewQueue(nextQueue);
      setSourceTraces(nextTraces);
      setAudit(nextAudit);
      setSafety(nextSafety);
      setLiveStatus(nextLiveStatus);
      setLiveProviders(nextLiveProviders);
      setLiveSecretBoundary(nextLiveSecretBoundary);
      setLiveGate(nextLiveGate);
      setLiveGateList(nextLiveGateList);
      setLiveHealth(nextLiveHealth);
      setDocumentLiveRuns(nextDocumentRuns);
      setOCRLiveRuns(nextOCRRuns);
      setLiveReviewQueue(nextLiveQueue);
      setLiveSourceTraces(nextLiveTraces);
      setLiveAudit(nextLiveAudit);
      setLiveSafety(nextLiveSafety);
      setParserProvider((current) => current || nextProviders.providers.find((provider) => provider.category === "file_parser")?.provider_id || "mineru_file_parser_provider");
      setOCRProvider((current) => current || nextProviders.providers.find((provider) => provider.category === "ocr")?.provider_id || "paddleocr_provider");
      setSelectedOCRJobId((current) => current || nextOCRJobs.ocr_jobs[0]?.ocr_job_id || "");
      setLiveDocumentProvider(
        (current) => current || nextLiveProviders.providers.find((provider) => provider.provider_type === "document_parser")?.provider_id || "mineru"
      );
      setLiveOCRProvider((current) => current || nextLiveProviders.providers.find((provider) => provider.provider_type === "ocr")?.provider_id || "paddleocr");
      setSelectedLiveProviderId((current) => current || nextLiveProviders.providers[0]?.provider_id || "paddleocr");
      setSelectedLiveReviewItemId((current) => current || nextLiveQueue.items[0]?.review_item_id || "");
    } catch {
      setError("Material Runtime API 暂不可用，请确认后端服务已启动。");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadRuntime();
  }, []);

  const parserProviders = useMemo(
    () => providers?.providers.filter((provider) => provider.category === "file_parser") ?? [],
    [providers]
  );
  const ocrProviders = useMemo(
    () => providers?.providers.filter((provider) => provider.category === "ocr") ?? [],
    [providers]
  );
  const liveDocumentProviders = useMemo(
    () => liveProviders?.providers.filter((provider) => provider.provider_type === "document_parser") ?? [],
    [liveProviders]
  );
  const liveOCRProviders = useMemo(
    () => liveProviders?.providers.filter((provider) => provider.provider_type === "ocr") ?? [],
    [liveProviders]
  );
  const selectedReviewJobId = selectedOCRJobId || reviewQueue?.items[0]?.ocr_job_id || "";
  const selectedLiveReviewId = selectedLiveReviewItemId || liveReviewQueue?.items[0]?.review_item_id || "";
  const activePreview = ocrPreview ?? ocrResult?.ocr_preview ?? ocrJobs?.ocr_jobs[0]?.ocr_preview ?? null;

  async function handleParseJob() {
    setError("");
    setParseResult(null);
    try {
      const result = await createPersonalMaterialParseJob({
        case_id: caseId,
        material_id: materialId,
        parser_provider_id: parserProvider,
        parse_type: parseType,
        manual_approval_confirmed: parseConfirmed,
        mock_data_only_confirmation: parseConfirmed,
        no_raw_content_confirmation: parseConfirmed,
        no_external_upload_confirmation: parseConfirmed
      });
      setParseResult(result);
      await loadRuntime();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Parse job failed.");
    }
  }

  async function handleOCRJob() {
    setError("");
    setOCRResult(null);
    setOCRPreview(null);
    try {
      const result = await createPersonalOCRJob({
        case_id: caseId,
        material_id: materialId,
        ocr_provider_id: ocrProvider,
        ocr_job_type: ocrJobType,
        manual_approval_confirmed: ocrConfirmed,
        lawyer_review_required_confirmation: ocrConfirmed,
        source_trace_required_confirmation: ocrConfirmed,
        no_raw_ocr_exposure_confirmation: ocrConfirmed,
        no_final_legal_opinion_confirmation: ocrConfirmed,
        no_final_report_generation_confirmation: ocrConfirmed
      });
      setOCRResult(result);
      if (result.ocr_job_id) {
        setSelectedOCRJobId(result.ocr_job_id);
        const preview = await getPersonalOCRPreview(result.ocr_job_id);
        setOCRPreview(preview);
      }
      await loadRuntime();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "OCR job failed.");
    }
  }

  async function handleReviewAction() {
    setError("");
    setReviewResult(null);
    if (!selectedReviewJobId) {
      setError("请先创建或选择 OCR job。");
      return;
    }
    try {
      const result = await submitPersonalOCRReviewAction(selectedReviewJobId, {
        action: reviewAction,
        reviewer_id: "local_demo_lawyer",
        manual_review_confirmed: reviewConfirmed,
        no_raw_ocr_exposure_confirmation: reviewConfirmed,
        lawyer_review_required_confirmation: reviewConfirmed
      });
      setReviewResult(result);
      await loadRuntime();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Review action failed.");
    }
  }

  function buildLivePayload(providerId: string, dryRun: boolean) {
    return {
      provider_id: providerId,
      case_id: caseId,
      material_id: materialId,
      file_name: "controlled_demo_material.pdf",
      file_type: liveFileType,
      byte_size: Number(liveByteSize) || 0,
      page_range: "1-2",
      actor_id: "local_demo_lawyer",
      dry_run: dryRun,
      explicit_live_confirmation: liveConfirmed,
      material_owner_confirmation: liveConfirmed,
      raw_content_handling_acknowledged: liveConfirmed,
      no_ai_prompt_injection_acknowledged: liveConfirmed,
      lawyer_review_acknowledged: liveConfirmed,
      draft_only_acknowledged: liveConfirmed
    };
  }

  async function handleDocumentDryRun() {
    setError("");
    setDocumentLiveResult(null);
    try {
      const result = await createPersonalMaterialDocumentLiveDryRun(buildLivePayload(liveDocumentProvider, true));
      setDocumentLiveResult(result);
      await loadRuntime();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Document dry-run failed.");
    }
  }

  async function handleDocumentLiveRun() {
    setError("");
    setDocumentLiveResult(null);
    try {
      const result = await createPersonalMaterialDocumentLiveRun(buildLivePayload(liveDocumentProvider, false));
      setDocumentLiveResult(result);
      await loadRuntime();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Document live run failed.");
    }
  }

  async function handleOCRDryRun() {
    setError("");
    setOCRLiveResult(null);
    try {
      const result = await createPersonalMaterialOCRLiveDryRun(buildLivePayload(liveOCRProvider, true));
      setOCRLiveResult(result);
      await loadRuntime();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "OCR dry-run failed.");
    }
  }

  async function handleOCRLiveRun() {
    setError("");
    setOCRLiveResult(null);
    try {
      const result = await createPersonalMaterialOCRLiveRun(buildLivePayload(liveOCRProvider, false));
      setOCRLiveResult(result);
      await loadRuntime();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "OCR live run failed.");
    }
  }

  async function handleLiveReviewAction() {
    setError("");
    setLiveReviewResult(null);
    const reviewItemId = selectedLiveReviewItemId || liveReviewQueue?.items[0]?.review_item_id || "";
    if (!reviewItemId) {
      setError("请先创建 document / OCR dry-run metadata，再进行 live review action。");
      return;
    }
    try {
      const result = await submitPersonalMaterialLiveReviewAction(reviewItemId, {
        action: liveReviewAction,
        actor_id: "local_demo_lawyer",
        explicit_review_confirmation: liveReviewConfirmed,
        raw_content_handling_acknowledged: liveReviewConfirmed,
        no_ai_prompt_injection_acknowledged: liveReviewConfirmed
      });
      setLiveReviewResult(result);
      await loadRuntime();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Live review action failed.");
    }
  }

  async function handleLiveGateMock() {
    setError("");
    try {
      const gate = await createPersonalMaterialLiveGateMock({
        provider_id: selectedLiveProviderId,
        explicit_live_confirmation: false,
        owner_authorized: false,
        raw_content_boundary_acknowledged: true,
        no_ai_prompt_injection_acknowledged: true,
        audit_acknowledged: true
      });
      setLiveGate(gate);
      const gates = await listPersonalMaterialLiveGates();
      setLiveGateList(gates);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Live gate metadata failed.");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}

        <section className="overflow-hidden rounded-md border border-slate-800 bg-[#10201c] text-white shadow-sm">
          <div className="grid gap-6 p-6 md:grid-cols-[1.35fr_0.75fr] md:p-8">
            <div>
              <div className="inline-flex items-center rounded-md border border-lime-300/40 bg-lime-300/10 px-3 py-1 text-xs font-medium text-lime-100">
                {liveStatus?.version ?? "v7.27"} · OCR Live Gateway · dry-run only
              </div>
              <h1 className="mt-5 max-w-3xl text-3xl font-semibold leading-tight md:text-5xl">
                AIHome.law OCR Live Gateway
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300">
                OCR / Document Provider 接入准备层，仅返回 provider registry、secret boundary、live gate、dry-run health、source trace 与 audit metadata。默认不调用真实服务，不上传材料，不展示 OCR / 文档原文。
              </p>
              <div className="mt-5 flex flex-wrap gap-2">
                {["owner-only", "metadata-only", "draft-only", "live disabled", "不暴露 raw OCR"].map((badge) => (
                  <SafetyBadge key={badge} label={badge} />
                ))}
              </div>
            </div>
            <div className="rounded-md border border-slate-700 bg-white/5 p-5">
              <div className="text-xs uppercase tracking-wide text-lime-200">Runtime posture</div>
              <div className="mt-4 grid gap-3">
                <HeroMetric label="材料解析 Runtime" value={status?.material_parser_runtime_enabled ?? true} />
                <HeroMetric label="OCR Runtime" value={status?.ocr_runtime_enabled ?? true} />
                <HeroMetric label="live call allowed" value={liveStatus?.live_call_allowed ?? false} invert />
                <HeroMetric label="OCR / 文档原文暴露" value={(liveStatus?.raw_ocr_text_exposed || liveStatus?.raw_document_content_exposed) ?? false} invert />
              </div>
              <button
                type="button"
                onClick={() => void loadRuntime()}
                disabled={loading}
                className="mt-5 w-full rounded-md bg-lime-300 px-3 py-2 text-sm font-semibold text-slate-950 disabled:opacity-60"
              >
                {loading ? "刷新中" : "刷新 Runtime"}
              </button>
            </div>
          </div>
        </section>

        <Panel title="Provider Cards / Provider 状态">
          <div className="grid gap-3 md:grid-cols-3">
            {(providers?.providers ?? []).map((provider) => (
              <div key={provider.provider_id} className="rounded-md border border-line bg-white p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold text-ink">{provider.label}</div>
                    <div className="mt-1 text-xs text-muted">{provider.provider_id}</div>
                  </div>
                  <StatusBadge tone="preview" label={provider.status} />
                </div>
                <div className="mt-4 grid gap-2 text-xs text-muted">
                  <span>category: {provider.category}</span>
                  <span>live_enabled: {String(provider.live_enabled)}</span>
                  <span>api_key_visible: {String(provider.api_key_visible)}</span>
                  <span>next_action: {provider.next_action}</span>
                </div>
              </div>
            ))}
          </div>
        </Panel>

        <Panel title="OCR Live Gateway / 文档 Provider 接入准备">
          <div className="grid gap-4">
            <div className="grid gap-3 md:grid-cols-4">
              <StatusTile label="OCR live mode" value={liveStatus?.ocr_live_mode_enabled ?? false} invert />
              <StatusTile label="Document live mode" value={liveStatus?.document_live_mode_enabled ?? false} invert />
              <StatusTile label="live_call_allowed" value={liveStatus?.live_call_allowed ?? false} invert />
              <StatusTile label="AI Prompt 注入" value={liveStatus?.ai_prompt_injected ?? false} invert />
            </div>
            <div className="rounded-md border border-cyan-200 bg-cyan-50 p-4 text-sm leading-6 text-cyan-950">
              v7.27 只完成 OCR / Document Provider live connection readiness。API Key 仅返回 key_loaded boolean，前端不可输入或查看密钥；OCR 原文和文档原文默认不展示，不自动进入 AI Prompt，不自动触发事实抽取或法律分析。律师复核、来源追踪与审计保持必需。
            </div>
            <div className="grid gap-3 lg:grid-cols-[0.95fr_1.05fr]">
              <div className="rounded-md border border-line bg-white p-4">
                <SelectField
                  label="selected provider"
                  value={selectedLiveProviderId}
                  options={(liveProviders?.providers ?? []).map((provider) => provider.provider_id)}
                  onChange={(nextProviderId) => {
                    setSelectedLiveProviderId(nextProviderId);
                    void Promise.all([
                      getPersonalMaterialLiveSecretBoundary(nextProviderId).then(setLiveSecretBoundary),
                      getPersonalMaterialLiveGate(nextProviderId).then(setLiveGate),
                      getPersonalMaterialLiveHealthDryRun(nextProviderId).then(setLiveHealth)
                    ]);
                  }}
                />
                <ActionButton label="生成 live gate mock metadata" onClick={() => void handleLiveGateMock()} />
              </div>
              <div className="grid gap-2 rounded-md border border-slate-200 bg-slate-50 p-4 text-xs text-slate-700 md:grid-cols-2">
                <MetadataRow label="secret key_loaded" value={String(liveSecretBoundary?.key_loaded ?? false)} />
                <MetadataRow label="secret returned" value={String(liveSecretBoundary?.secret_value_returned ?? false)} />
                <MetadataRow label="live gate status" value={liveGate?.live_gate_status ?? "blocked_by_default"} />
                <MetadataRow label="network call" value={String(liveHealth?.network_call_executed ?? false)} />
                <MetadataRow label="upload executed" value={String(liveHealth?.upload_executed ?? false)} />
                <MetadataRow label="raw uploaded" value={String(liveHealth?.raw_content_uploaded ?? false)} />
              </div>
            </div>
            <div className="grid gap-3 md:grid-cols-4">
              {(liveProviders?.providers ?? []).map((provider) => (
                <div key={provider.provider_id} className="rounded-md border border-line bg-white p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <div className="text-sm font-semibold text-ink">{provider.display_name}</div>
                      <div className="mt-1 text-xs text-muted">{provider.provider_id}</div>
                    </div>
                    <StatusBadge tone={provider.live_enabled ? "blocked" : "preview"} label={provider.status} />
                  </div>
                  <div className="mt-4 grid gap-2 text-xs text-muted">
                    <span>dry_run_ready: {String(provider.dry_run_ready)}</span>
                    <span>live_enabled: {String(provider.live_enabled)}</span>
                    <span>key_loaded: {String(provider.key_loaded)}</span>
                    <span>key_source: {provider.key_source}</span>
                    <span>adapter_registered: {String(provider.adapter_registered)}</span>
                    <span>max_file_size_mb: {provider.max_file_size_mb}</span>
                    <span>supports_bbox: {String(provider.supports_bbox)}</span>
                  </div>
                </div>
              ))}
            </div>
            <div className="grid gap-3 md:grid-cols-3">
              <div className="rounded-md border border-line bg-white p-4">
                <div className="text-sm font-semibold text-ink">Secret Boundary</div>
                <ResultFlags
                  flags={{
                    key_loaded: liveSecretBoundary?.key_loaded ?? false,
                    key_value_exposed: liveSecretBoundary?.key_value_exposed ?? false,
                    masked_key_returned: liveSecretBoundary?.masked_key_returned ?? false,
                    frontend_key_input_enabled: liveSecretBoundary?.frontend_key_input_enabled ?? false
                  }}
                />
              </div>
              <div className="rounded-md border border-line bg-white p-4">
                <div className="text-sm font-semibold text-ink">Live Gate</div>
                <ResultFlags
                  flags={{
                    live_gate_status: liveGate?.live_gate_status ?? "blocked_by_default",
                    global_live_enabled: liveGate?.global_live_enabled ?? false,
                    provider_live_enabled: liveGate?.provider_live_enabled ?? false,
                    live_call_allowed: liveGate?.live_call_allowed ?? false,
                    live_call_executed: liveGate?.live_call_executed ?? false
                  }}
                />
                <p className="mt-3 text-xs leading-5 text-muted">{liveGate?.live_blocked_reason ?? "global_live_disabled"}</p>
              </div>
              <div className="rounded-md border border-line bg-white p-4">
                <div className="text-sm font-semibold text-ink">Dry-run Health</div>
                <ResultFlags
                  flags={{
                    dry_run_ready: liveHealth?.dry_run_ready ?? true,
                    network_call_executed: liveHealth?.network_call_executed ?? false,
                    upload_executed: liveHealth?.upload_executed ?? false,
                    raw_content_uploaded: liveHealth?.raw_content_uploaded ?? false
                  }}
                />
              </div>
            </div>
            <div className="rounded-md border border-line bg-white p-4">
              <div className="text-sm font-semibold text-ink">Live Gate Queue / 门禁 metadata</div>
              <div className="mt-3 grid gap-2 md:grid-cols-2">
                {(liveGateList?.live_gates ?? []).slice(0, 6).map((gate) => (
                  <MetadataRow key={gate.gate_id} label={gate.provider_id} value={`${gate.live_gate_status} · live=${String(gate.live_call_executed)}`} />
                ))}
              </div>
            </div>
          </div>
        </Panel>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="Document dry-run / 文档解析 dry-run">
            <div className="grid gap-4">
              <SelectField label="provider" value={liveDocumentProvider} options={liveDocumentProviders.map((provider) => provider.provider_id)} onChange={setLiveDocumentProvider} />
              <SelectField label="file_type" value={liveFileType} options={["pdf", "docx", "pptx", "xlsx", "html", "md", "txt"]} onChange={setLiveFileType} />
              <NumberField label="byte_size" value={liveByteSize} onChange={setLiveByteSize} />
              <ActionButton label="生成文档解析 dry-run metadata" onClick={() => void handleDocumentDryRun()} />
              <ConfirmField label="Gated live confirmations · 不读取原文 · 不进入 AI Prompt · 草稿 metadata only" checked={liveConfirmed} onChange={setLiveConfirmed} />
              <ActionButton label="尝试 gated document live run" onClick={() => void handleDocumentLiveRun()} />
            </div>
            {documentLiveResult ? (
              <ResultPanel title="Document Live Result">
                <ResultFlags
                  flags={{
                    status: documentLiveResult.status,
                    dry_run: documentLiveResult.dry_run,
                    live_call_executed: documentLiveResult.live_call_executed,
                    raw_content_exposed: documentLiveResult.raw_content_exposed,
                    ai_prompt_injected: documentLiveResult.ai_prompt_injected,
                    fact_extraction_triggered: documentLiveResult.fact_extraction_triggered,
                    legal_analysis_triggered: documentLiveResult.legal_analysis_triggered
                  }}
                />
                <MetricGrid
                  metrics={{
                    page_count_estimate: documentLiveResult.document_metadata.page_count_estimate,
                    table_count: documentLiveResult.document_metadata.table_count,
                    layout_blocks_count: documentLiveResult.document_metadata.layout_blocks_count,
                    redacted_preview_available: String(documentLiveResult.document_metadata.redacted_preview_available)
                  }}
                />
                <BlockedReasons reasons={documentLiveResult.blocked_reasons} />
              </ResultPanel>
            ) : null}
          </Panel>

          <Panel title="OCR dry-run / OCR dry-run">
            <div className="grid gap-4">
              <SelectField label="provider" value={liveOCRProvider} options={liveOCRProviders.map((provider) => provider.provider_id)} onChange={setLiveOCRProvider} />
              <SelectField label="file_type" value={liveFileType} options={["pdf", "png", "jpg", "jpeg", "tiff"]} onChange={setLiveFileType} />
              <NumberField label="byte_size" value={liveByteSize} onChange={setLiveByteSize} />
              <ActionButton label="生成 OCR dry-run metadata" onClick={() => void handleOCRDryRun()} />
              <ConfirmField label="Gated live confirmations · OCR 原文不展示 · 不进入 AI Prompt · 律师复核必需" checked={liveConfirmed} onChange={setLiveConfirmed} />
              <ActionButton label="尝试 gated OCR live run" onClick={() => void handleOCRLiveRun()} />
            </div>
            {ocrLiveResult ? (
              <ResultPanel title="OCR Live Result">
                <ResultFlags
                  flags={{
                    status: ocrLiveResult.status,
                    dry_run: ocrLiveResult.dry_run,
                    live_call_executed: ocrLiveResult.live_call_executed,
                    raw_ocr_text_exposed: ocrLiveResult.raw_ocr_text_exposed,
                    ai_prompt_injected: ocrLiveResult.ai_prompt_injected,
                    final_report_generated: ocrLiveResult.final_report_generated
                  }}
                />
                <MetricGrid
                  metrics={{
                    page_count_estimate: ocrLiveResult.ocr_metadata.page_count_estimate,
                    supports_bbox: String(ocrLiveResult.ocr_metadata.supports_bbox),
                    supports_confidence: String(ocrLiveResult.ocr_metadata.supports_confidence),
                    image_count: ocrLiveResult.ocr_metadata.image_count
                  }}
                />
                <BlockedReasons reasons={ocrLiveResult.blocked_reasons} />
              </ResultPanel>
            ) : null}
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Live Review Queue / Live 复核队列">
            <div className="grid gap-3">
              <SelectField
                label="review_item_id"
                value={selectedLiveReviewId}
                options={(liveReviewQueue?.items ?? []).map((item) => item.review_item_id)}
                onChange={setSelectedLiveReviewItemId}
              />
              <SelectField label="action" value={liveReviewAction} options={liveReviewActions} onChange={setLiveReviewAction} />
              <ConfirmField label="人工复核确认 · 原始内容仍阻断 · 不进入 AI Prompt" checked={liveReviewConfirmed} onChange={setLiveReviewConfirmed} />
              <ActionButton label="提交 live review action" onClick={() => void handleLiveReviewAction()} />
              {liveReviewResult ? (
                <ResultFlags
                  flags={{
                    status: liveReviewResult.status,
                    review_status: liveReviewResult.review_status,
                    raw_content_exposed: liveReviewResult.raw_content_exposed,
                    ai_prompt_injected: liveReviewResult.ai_prompt_injected
                  }}
                />
              ) : null}
              {(liveReviewQueue?.items ?? []).slice(0, 4).map((item) => (
                <MetadataRow key={item.review_item_id} label={item.review_item_id} value={`${item.review_status} · raw_blocked=${String(item.raw_content_blocked)}`} />
              ))}
            </div>
          </Panel>

          <Panel title="Live Source Trace / Live 来源追踪">
            <div className="grid gap-3">
              {(liveSourceTraces?.source_traces ?? []).slice(0, 6).map((trace) => (
                <MetadataRow key={trace.source_trace_id} label={trace.source_trace_id} value={`${trace.run_type} · raw=${String(trace.raw_content_exposed)} · prompt=${String(trace.ai_prompt_injected)}`} />
              ))}
              {liveSourceTraces?.source_traces.length ? null : <EmptyState label="No live source traces yet" />}
            </div>
          </Panel>

          <Panel title="Live Audit Timeline / Live 审计 metadata">
            <div className="grid gap-3">
              {(liveAudit?.events ?? []).slice(0, 6).map((event) => (
                <MetadataRow key={event.event_id} label={event.action} value={`${event.provider_id} · live=${String(event.live_call_executed)}`} />
              ))}
              {liveAudit?.events.length ? null : <EmptyState label="No live audit events yet" />}
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="Parse Job Mock Form / 材料解析草案">
            <div className="grid gap-4">
              <SelectField label="provider" value={parserProvider} options={parserProviders.map((provider) => provider.provider_id)} onChange={setParserProvider} />
              <SelectField label="parse_type" value={parseType} options={parseTypes} onChange={setParseType} />
              <TextField label="case_id" value={caseId} onChange={setCaseId} />
              <TextField label="material_id" value={materialId} onChange={setMaterialId} />
              <ConfirmField label="人工批准 · 仅模拟数据 · 不含原始内容 · 不外部上传" checked={parseConfirmed} onChange={setParseConfirmed} />
              <ActionButton label="Create Parse Job" onClick={() => void handleParseJob()} />
            </div>
            {parseResult ? (
              <ResultPanel title="Parse Result">
                <ResultFlags
                  flags={{
                    status: parseResult.status,
                    would_call_provider: parseResult.would_call_provider,
                    live_call_executed: parseResult.live_call_executed,
                    raw_content_included: parseResult.raw_content_included,
                    raw_material_text_exposed: parseResult.raw_material_text_exposed,
                    controlled_preview_only: parseResult.controlled_preview_only,
                    final_legal_opinion_generated: parseResult.final_legal_opinion_generated,
                    final_report_generated: parseResult.final_report_generated
                  }}
                />
                <MetricGrid
                  metrics={{
                    page_count: parseResult.parse_summary.page_count,
                    section_count: parseResult.parse_summary.section_count,
                    table_count: parseResult.parse_summary.table_count,
                    image_count: parseResult.parse_summary.image_count
                  }}
                />
                <BlockedReasons reasons={parseResult.blocked_reasons} />
              </ResultPanel>
            ) : null}
          </Panel>

          <Panel title="OCR Job Mock Form / OCR 预览草案">
            <div className="grid gap-4">
              <SelectField label="provider" value={ocrProvider} options={ocrProviders.map((provider) => provider.provider_id)} onChange={setOCRProvider} />
              <SelectField label="ocr_job_type" value={ocrJobType} options={ocrJobTypes} onChange={setOCRJobType} />
              <TextField label="case_id" value={caseId} onChange={setCaseId} />
              <TextField label="material_id" value={materialId} onChange={setMaterialId} />
              <ConfirmField label="Manual approval · lawyer review · source trace · no final output" checked={ocrConfirmed} onChange={setOCRConfirmed} />
              <ActionButton label="Create OCR Job" onClick={() => void handleOCRJob()} />
            </div>
            {ocrResult ? (
              <ResultPanel title="OCR Result">
                <ResultFlags
                  flags={{
                    status: ocrResult.status,
                    review_status: ocrResult.review_status,
                    would_call_provider: ocrResult.would_call_provider,
                    live_call_executed: ocrResult.live_call_executed,
                    raw_ocr_text_exposed: ocrResult.raw_ocr_text_exposed,
                    used_in_ai_prompt: ocrResult.used_in_ai_prompt,
                    final_legal_opinion_generated: ocrResult.final_legal_opinion_generated,
                    final_report_generated: ocrResult.final_report_generated
                  }}
                />
                <BlockedReasons reasons={ocrResult.blocked_reasons} />
              </ResultPanel>
            ) : null}
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
          <Panel title="OCR Preview Panel / OCR 预览状态">
            <MetricGrid
              metrics={{
                page_count: activePreview?.page_count ?? 0,
                recognized_block_count: activePreview?.recognized_block_count ?? 0,
                average_confidence: activePreview?.average_confidence ?? 0,
                low_confidence_block_count: activePreview?.low_confidence_block_count ?? 0
              }}
            />
            <div className="mt-4 grid gap-2">
              <MetadataRow label="table_detected" value={String(activePreview?.table_detected ?? false)} />
              <MetadataRow label="layout_detected" value={String(activePreview?.layout_detected ?? false)} />
              <MetadataRow label="key_information_detected" value={String(activePreview?.key_information_detected ?? false)} />
              <MetadataRow label="raw_ocr_text_exposed" value={String(activePreview?.raw_ocr_text_exposed ?? false)} />
            </div>
          </Panel>

          <Panel title="OCR Review Queue / OCR 复核队列">
            <div className="grid gap-3">
              <SelectField
                label="ocr_job_id"
                value={selectedReviewJobId}
                options={(reviewQueue?.items ?? []).map((item) => item.ocr_job_id)}
                onChange={setSelectedOCRJobId}
              />
              <SelectField label="action" value={reviewAction} options={reviewActions} onChange={setReviewAction} />
              <ConfirmField label="Manual review confirmed · no source text exposure · lawyer review required" checked={reviewConfirmed} onChange={setReviewConfirmed} />
              <ActionButton label="Submit Review Action" onClick={() => void handleReviewAction()} />
              {reviewResult ? (
                <ResultFlags
                  flags={{
                    status: reviewResult.status,
                    review_status: reviewResult.review_status,
                    used_in_ai_prompt: reviewResult.used_in_ai_prompt,
                    used_in_final_output: reviewResult.used_in_final_output,
                    eligible_for_ai_prompt_after_review: reviewResult.eligible_for_ai_prompt_after_review
                  }}
                />
              ) : null}
              {(reviewQueue?.items ?? []).slice(0, 4).map((item) => (
                <MetadataRow key={item.ocr_job_id} label={item.ocr_job_id} value={`${item.review_status} · used_in_ai_prompt=${String(item.used_in_ai_prompt)}`} />
              ))}
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Source Trace Panel / 来源追踪">
            <div className="grid gap-3">
              {(sourceTraces?.source_traces ?? []).slice(0, 6).map((trace) => (
                <div key={trace.source_trace_id} className="rounded-md border border-line bg-white p-3 text-xs text-muted">
                  <div className="font-semibold text-ink">{trace.source_trace_id}</div>
                  <div className="mt-2 grid gap-1">
                    <span>material_id: {trace.material_id}</span>
                    <span>job_id: {trace.job_id}</span>
                    <span>provider_id: {trace.provider_id}</span>
                    <span>confidence: {trace.confidence}</span>
                    <span>used_in_ai_prompt: {String(trace.used_in_ai_prompt)}</span>
                    <span>used_in_final_output: {String(trace.used_in_final_output)}</span>
                  </div>
                </div>
              ))}
              {sourceTraces?.source_traces.length ? null : <EmptyState label="No source traces yet" />}
            </div>
          </Panel>

          <Panel title="Audit Metadata / 审计 metadata">
            <div className="grid gap-3">
              {(audit?.events ?? []).slice(0, 6).map((event) => (
                <MetadataRow key={event.event_id} label={event.event_type} value={`${event.job_id} · live=${String(event.live_call_executed)}`} />
              ))}
              {audit?.events.length ? null : <EmptyState label="No audit events yet" />}
            </div>
          </Panel>

          <TrustSafetyPanel title="信任与安全面板" />
        </section>

        <Panel title="开发诊断（默认折叠）">
          <DiagnosticsPanel
            data={{
              status,
              providers,
              parse_result: parseResult,
              ocr_result: ocrResult,
              ocr_preview: ocrPreview,
              parse_jobs: parseJobs,
              ocr_jobs: ocrJobs,
              review_queue: reviewQueue,
              source_traces: sourceTraces,
              audit,
              safety,
              live_status: liveStatus,
              live_providers: liveProviders,
              document_live_result: documentLiveResult,
              ocr_live_result: ocrLiveResult,
              document_live_runs: documentLiveRuns,
              ocr_live_runs: ocrLiveRuns,
              live_review_queue: liveReviewQueue,
              live_source_traces: liveSourceTraces,
              live_audit: liveAudit,
              live_safety: liveSafety
            }}
          />
        </Panel>
      </div>
    </AppShell>
  );
}

function SelectField({ label, value, options, onChange }: { label: string; value: string; options: string[]; onChange: (value: string) => void }) {
  return (
    <label className="grid gap-2 text-sm text-ink">
      <span className="font-medium">{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)} className="rounded-md border border-line bg-white px-3 py-2 text-sm">
        {options.length ? null : <option value="">No options</option>}
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
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

function NumberField({ label, value, onChange }: { label: string; value: number; onChange: (value: number) => void }) {
  return (
    <label className="grid gap-2 text-sm text-ink">
      <span className="font-medium">{label}</span>
      <input
        type="number"
        min={0}
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        className="rounded-md border border-line bg-white px-3 py-2 text-sm"
      />
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

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="rounded-md border border-line bg-paper p-5">
      <h2 className="text-base font-semibold text-ink">{title}</h2>
      <div className="mt-4">{children}</div>
    </section>
  );
}

function ResultPanel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mt-5 rounded-md border border-lime-200 bg-lime-50 p-4">
      <div className="text-sm font-semibold text-lime-950">{title}</div>
      <div className="mt-3 grid gap-3">{children}</div>
    </div>
  );
}

function MetricGrid({ metrics }: { metrics: Record<string, string | number> }) {
  return (
    <div className="grid gap-3 md:grid-cols-2">
      {Object.entries(metrics).map(([label, value]) => (
        <div key={label} className="rounded-md border border-line bg-white p-4">
          <div className="text-xs uppercase tracking-wide text-muted">{label}</div>
          <div className="mt-2 text-2xl font-semibold text-ink">{String(value)}</div>
        </div>
      ))}
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

function MetadataRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-3 rounded-md border border-line bg-white px-3 py-2">
      <span className="truncate text-xs font-medium text-ink">{label}</span>
      <span className="text-right text-xs text-muted">{value}</span>
    </div>
  );
}

function BlockedReasons({ reasons }: { reasons: string[] }) {
  if (!reasons.length) {
    return null;
  }
  return <div className="rounded-md border border-amber-200 bg-amber-50 p-3 text-xs leading-5 text-amber-900">{reasons.join(" · ")}</div>;
}

function EmptyState({ label }: { label: string }) {
  return <div className="rounded-md border border-dashed border-line bg-white px-3 py-6 text-center text-sm text-muted">{label}</div>;
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

function HeroMetric({ label, value, invert = false }: { label: string; value: boolean; invert?: boolean }) {
  const positive = invert ? !value : value;
  return (
    <div className="flex items-center justify-between rounded-md border border-slate-700 bg-slate-950/40 px-3 py-2">
      <span className="text-sm text-slate-300">{label}</span>
      <StatusBadge tone={positive ? "safe" : "blocked"} label={String(value)} />
    </div>
  );
}
