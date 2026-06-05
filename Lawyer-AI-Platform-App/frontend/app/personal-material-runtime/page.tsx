"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  PersonalMaterialAuditTimeline,
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
  createPersonalMaterialParseJob,
  createPersonalOCRJob,
  getPersonalMaterialAudit,
  getPersonalMaterialRuntimeProviders,
  getPersonalMaterialRuntimeStatus,
  getPersonalMaterialSafety,
  getPersonalMaterialSourceTraces,
  getPersonalOCRPreview,
  getPersonalOCRReviewQueue,
  listPersonalMaterialParseJobs,
  listPersonalOCRJobs,
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

export default function PersonalMaterialRuntimePage() {
  const [status, setStatus] = useState<PersonalMaterialRuntimeStatus | null>(null);
  const [providers, setProviders] = useState<PersonalMaterialProviderList | null>(null);
  const [parseJobs, setParseJobs] = useState<PersonalMaterialParseJobList | null>(null);
  const [ocrJobs, setOCRJobs] = useState<PersonalOCRJobList | null>(null);
  const [reviewQueue, setReviewQueue] = useState<PersonalOCRReviewQueue | null>(null);
  const [sourceTraces, setSourceTraces] = useState<PersonalMaterialSourceTraceList | null>(null);
  const [audit, setAudit] = useState<PersonalMaterialAuditTimeline | null>(null);
  const [safety, setSafety] = useState<PersonalMaterialSafetyStatus | null>(null);
  const [parseResult, setParseResult] = useState<PersonalMaterialParseJobResult | null>(null);
  const [ocrResult, setOCRResult] = useState<PersonalOCRJobResult | null>(null);
  const [ocrPreview, setOCRPreview] = useState<PersonalOCRPreview | null>(null);
  const [reviewResult, setReviewResult] = useState<PersonalOCRReviewActionResult | null>(null);
  const [caseId, setCaseId] = useState(defaultCaseId);
  const [materialId, setMaterialId] = useState(defaultMaterialId);
  const [parserProvider, setParserProvider] = useState("mineru_file_parser_provider");
  const [ocrProvider, setOCRProvider] = useState("paddleocr_provider");
  const [parseType, setParseType] = useState("pdf_text_extract_preview");
  const [ocrJobType, setOCRJobType] = useState("scanned_pdf_ocr_preview");
  const [reviewAction, setReviewAction] = useState("approve_preview_for_analysis");
  const [selectedOCRJobId, setSelectedOCRJobId] = useState("");
  const [parseConfirmed, setParseConfirmed] = useState(true);
  const [ocrConfirmed, setOCRConfirmed] = useState(true);
  const [reviewConfirmed, setReviewConfirmed] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadRuntime() {
    setLoading(true);
    setError("");
    try {
      const [nextStatus, nextProviders, nextParseJobs, nextOCRJobs, nextQueue, nextTraces, nextAudit, nextSafety] =
        await Promise.all([
          getPersonalMaterialRuntimeStatus(),
          getPersonalMaterialRuntimeProviders(),
          listPersonalMaterialParseJobs(),
          listPersonalOCRJobs(),
          getPersonalOCRReviewQueue(),
          getPersonalMaterialSourceTraces(),
          getPersonalMaterialAudit(),
          getPersonalMaterialSafety()
        ]);
      setStatus(nextStatus);
      setProviders(nextProviders);
      setParseJobs(nextParseJobs);
      setOCRJobs(nextOCRJobs);
      setReviewQueue(nextQueue);
      setSourceTraces(nextTraces);
      setAudit(nextAudit);
      setSafety(nextSafety);
      setParserProvider((current) => current || nextProviders.providers.find((provider) => provider.category === "file_parser")?.provider_id || "mineru_file_parser_provider");
      setOCRProvider((current) => current || nextProviders.providers.find((provider) => provider.category === "ocr")?.provider_id || "paddleocr_provider");
      setSelectedOCRJobId((current) => current || nextOCRJobs.ocr_jobs[0]?.ocr_job_id || "");
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
  const selectedReviewJobId = selectedOCRJobId || reviewQueue?.items[0]?.ocr_job_id || "";
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

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <div className="rounded-md border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800">{error}</div> : null}

        <section className="overflow-hidden rounded-md border border-slate-800 bg-[#10201c] text-white shadow-sm">
          <div className="grid gap-6 p-6 md:grid-cols-[1.35fr_0.75fr] md:p-8">
            <div>
              <div className="inline-flex items-center rounded-md border border-lime-300/40 bg-lime-300/10 px-3 py-1 text-xs font-medium text-lime-100">
                {status?.version ?? "v7.2"} · Mock-first provider runtime
              </div>
              <h1 className="mt-5 max-w-3xl text-3xl font-semibold leading-tight md:text-5xl">
                AIHome.law Material Runtime
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300">
                Controlled file parsing and PaddleOCR-ready runtime for metadata-only material processing. OCR previews stay controlled and lawyer review remains required.
              </p>
              <div className="mt-5 flex flex-wrap gap-2">
                {["Controlled file parsing", "PaddleOCR-ready", "OCR review required", "Source trace required", "No raw OCR exposure"].map((badge) => (
                  <SafetyBadge key={badge} label={badge} />
                ))}
              </div>
            </div>
            <div className="rounded-md border border-slate-700 bg-white/5 p-5">
              <div className="text-xs uppercase tracking-wide text-lime-200">Runtime posture</div>
              <div className="mt-4 grid gap-3">
                <HeroMetric label="Material runtime" value={status?.material_parser_runtime_enabled ?? true} />
                <HeroMetric label="OCR runtime" value={status?.ocr_runtime_enabled ?? true} />
                <HeroMetric label="Live provider call" value={status?.live_provider_call_enabled ?? false} invert />
                <HeroMetric label="OCR source text exposed" value={status?.raw_ocr_text_exposed ?? false} invert />
              </div>
              <button
                type="button"
                onClick={() => void loadRuntime()}
                disabled={loading}
                className="mt-5 w-full rounded-md bg-lime-300 px-3 py-2 text-sm font-semibold text-slate-950 disabled:opacity-60"
              >
                {loading ? "Refreshing" : "Refresh Runtime"}
              </button>
            </div>
          </div>
        </section>

        <Panel title="Provider Cards">
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

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="Parse Job Mock Form">
            <div className="grid gap-4">
              <SelectField label="provider" value={parserProvider} options={parserProviders.map((provider) => provider.provider_id)} onChange={setParserProvider} />
              <SelectField label="parse_type" value={parseType} options={parseTypes} onChange={setParseType} />
              <TextField label="case_id" value={caseId} onChange={setCaseId} />
              <TextField label="material_id" value={materialId} onChange={setMaterialId} />
              <ConfirmField label="Manual approval · mock data only · no raw content · no external upload" checked={parseConfirmed} onChange={setParseConfirmed} />
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

          <Panel title="OCR Job Mock Form">
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
          <Panel title="OCR Preview Panel">
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

          <Panel title="OCR Review Queue">
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
          <Panel title="Source Trace Panel">
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

          <Panel title="Audit Metadata">
            <div className="grid gap-3">
              {(audit?.events ?? []).slice(0, 6).map((event) => (
                <MetadataRow key={event.event_id} label={event.event_type} value={`${event.job_id} · live=${String(event.live_call_executed)}`} />
              ))}
              {audit?.events.length ? null : <EmptyState label="No audit events yet" />}
            </div>
          </Panel>

          <Panel title="Safety Panel">
            <div className="grid gap-2">
              {Object.entries(safety?.safety ?? {}).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between rounded-md border border-line bg-white px-3 py-2">
                  <span className="text-sm text-ink">{key}</span>
                  <StatusBadge tone={value ? "safe" : "blocked"} label={String(value)} />
                </div>
              ))}
            </div>
          </Panel>
        </section>

        <Panel title="Developer Diagnostics">
          <details className="rounded-md border border-line bg-slate-950 text-slate-100">
            <summary className="cursor-pointer px-4 py-3 text-sm font-medium text-slate-200">
              API metadata
            </summary>
            <pre className="max-h-96 overflow-auto border-t border-slate-800 p-4 text-xs leading-5">
              {JSON.stringify(
                {
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
                  safety
                },
                null,
                2
              )}
            </pre>
          </details>
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

function HeroMetric({ label, value, invert = false }: { label: string; value: boolean; invert?: boolean }) {
  const positive = invert ? !value : value;
  return (
    <div className="flex items-center justify-between rounded-md border border-slate-700 bg-slate-950/40 px-3 py-2">
      <span className="text-sm text-slate-300">{label}</span>
      <StatusBadge tone={positive ? "safe" : "blocked"} label={String(value)} />
    </div>
  );
}
