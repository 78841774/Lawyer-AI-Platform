import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  getControlledLegalSearchStatus,
  getControlledFinalReviewStatus,
  getControlledLawyerReviewStatus,
  getControlledMaterialStatus,
  getControlledOCRStatus,
  getControlledReportDraftStatus,
  getControlledRevisionStatus,
  getLegalSearchStatus,
  getInternalAlphaStatus,
  getLLMStatus,
  getLocalSandboxStatus,
  getOCRStatus,
  getPersonalAlphaStatus,
  getSourceRefsStatus
} from "@/services/api";

export const dynamic = "force-dynamic";

export default async function RuntimePage() {
  const { runtime, ocr, legalSearch, sourceRefs, localSandbox, internalAlpha, personalAlpha, controlledMaterial, controlledOCR, controlledLegalSearch, controlledReportDraft, controlledReview, controlledRevision, controlledFinalReview, error } =
    await loadRuntime();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 运行状态"
          title="运行状态"
          description="运行状态用于确认模型、OCR、法律检索和 source refs foundation 的 mock / connected 边界。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <div className="grid gap-6 lg:grid-cols-3">
          <StatusCard
            title="模型状态"
            provider={runtime?.provider ?? "-"}
            connected={runtime?.configured ?? false}
            rows={[
              ["模型", runtime?.model ?? "-"],
              ["已配置", formatBoolean(runtime?.configured)],
              ["Base URL 已配置", formatBoolean(runtime?.base_url_configured)],
              ["llm_status", runtime?.configured ? "configured" : "not_configured"]
            ]}
          />
          <StatusCard
            title="OCR Adapter"
            provider={ocr?.provider ?? "mock_ocr"}
            connected={ocr?.connected ?? false}
            rows={[
              ["connected", formatBoolean(ocr?.connected)],
              ["mock_only", formatBoolean(ocr?.mock_only)],
              ["supports_pdf", formatBoolean(ocr?.supports_pdf)],
              ["supports_images", formatBoolean(ocr?.supports_images)],
              ["notes", ocr?.notes ?? "Real OCR provider not connected."]
            ]}
            actionHref="/ocr"
          />
          <StatusCard
            title="Legal Search Adapter"
            provider={legalSearch?.provider ?? "mock_legal_search"}
            connected={legalSearch?.connected ?? false}
            rows={[
              ["connected", formatBoolean(legalSearch?.connected)],
              ["mock_only", formatBoolean(legalSearch?.mock_only)],
              ["supports_case_law", formatBoolean(legalSearch?.supports_case_law)],
              ["supports_statutes", formatBoolean(legalSearch?.supports_statutes)],
              ["notes", legalSearch?.notes ?? "Real legal database not connected."]
            ]}
            actionHref="/legal-search"
          />
          <StatusCard
            title="Source Trace"
            provider="source_refs"
            connected={sourceRefs?.source_trace_enabled ?? false}
            rows={[
              ["source_refs_enabled", formatBoolean(sourceRefs?.source_refs_enabled)],
              ["citation_resolver_enabled", formatBoolean(sourceRefs?.citation_resolver_enabled)],
              ["source_trace_enabled", formatBoolean(sourceRefs?.source_trace_enabled)],
              ["mock_only", formatBoolean(sourceRefs?.mock_only)],
              ["real_material_reading_enabled", formatBoolean(sourceRefs?.real_material_reading_enabled)],
              ["real_ocr_connected", formatBoolean(sourceRefs?.real_ocr_connected)],
              ["real_legal_search_connected", formatBoolean(sourceRefs?.real_legal_search_connected)],
              ["notes", sourceRefs?.notes ?? "Source refs mock trace not loaded."]
            ]}
            actionHref="/source-refs"
          />
          <StatusCard
            title="Local Sandbox"
            provider={localSandbox?.mode ?? "local_only"}
            connected={localSandbox?.enabled ?? false}
            rows={[
              ["mode", localSandbox?.mode ?? "local_only"],
              ["real_case_processing_enabled", formatBoolean(localSandbox?.real_case_processing_enabled)],
              ["live_provider_enabled", formatBoolean(localSandbox?.live_provider_enabled)],
              ["deepseek_live_enabled", formatBoolean(localSandbox?.deepseek_live_enabled)],
              ["real_ocr_enabled", formatBoolean(localSandbox?.real_ocr_enabled)],
              ["real_legal_search_enabled", formatBoolean(localSandbox?.real_legal_search_enabled)],
              ["requires_manual_review", formatBoolean(localSandbox?.requires_manual_review)],
              ["mock_only", formatBoolean(localSandbox?.mock_only)]
            ]}
            actionHref="/local-sandbox"
          />
          <StatusCard
            title="Internal Alpha"
            provider={internalAlpha?.mode ?? "local_internal_alpha"}
            connected={internalAlpha?.enabled ?? false}
            rows={[
              ["mode", internalAlpha?.mode ?? "local_internal_alpha"],
              ["production_enabled", formatBoolean(internalAlpha?.production_enabled)],
              ["team_mode_enabled", formatBoolean(internalAlpha?.team_mode_enabled)],
              ["real_case_processing_enabled", formatBoolean(internalAlpha?.real_case_processing_enabled)],
              ["workspace_runtime_auto_enable", formatBoolean(internalAlpha?.workspace_runtime_auto_enable)],
              ["skill_aware_case_processing_auto_enable", formatBoolean(internalAlpha?.skill_aware_case_processing_auto_enable)],
              ["local_only", formatBoolean(internalAlpha?.local_only)],
              ["requires_manual_review", formatBoolean(internalAlpha?.requires_manual_review)]
            ]}
            actionHref="/internal-alpha"
          />
          <StatusCard
            title="Personal Alpha"
            provider={personalAlpha?.mode ?? "personal_local_alpha"}
            connected={personalAlpha?.enabled ?? false}
            rows={[
              ["mode", personalAlpha?.mode ?? "personal_local_alpha"],
              ["real_case_processing_enabled", formatBoolean(personalAlpha?.real_case_processing_enabled)],
              ["material_content_reading_enabled", formatBoolean(personalAlpha?.material_content_reading_enabled)],
              ["ocr_live_enabled", formatBoolean(personalAlpha?.ocr_live_enabled)],
              ["legal_search_live_enabled", formatBoolean(personalAlpha?.legal_search_live_enabled)],
              ["llm_live_enabled", formatBoolean(personalAlpha?.llm_live_enabled)],
              ["deepseek_live_enabled", formatBoolean(personalAlpha?.deepseek_live_enabled)],
              ["local_only", formatBoolean(personalAlpha?.local_only)],
              ["dry_run_only", formatBoolean(personalAlpha?.dry_run_only)],
              ["requires_manual_review", formatBoolean(personalAlpha?.requires_manual_review)]
            ]}
            actionHref="/personal-alpha"
          />
          <StatusCard
            title="Controlled Material"
            provider={controlledMaterial?.mode ?? "local_only_controlled"}
            connected={controlledMaterial?.enabled ?? false}
            rows={[
              ["mode", controlledMaterial?.mode ?? "local_only_controlled"],
              ["production_enabled", formatBoolean(controlledMaterial?.production_enabled)],
              ["real_material_reading_enabled", formatBoolean(controlledMaterial?.real_material_reading_enabled)],
              ["real_material_reading_default", formatBoolean(controlledMaterial?.real_material_reading_default)],
              ["allowed_file_extensions", controlledMaterial?.allowed_file_extensions?.join(" / ") ?? ".txt / .md / .json"],
              ["max_file_size_bytes", String(controlledMaterial?.max_file_size_bytes ?? 200000)],
              ["read_pdf_enabled", formatBoolean(controlledMaterial?.read_pdf_enabled)],
              ["read_docx_enabled", formatBoolean(controlledMaterial?.read_docx_enabled)],
              ["read_image_enabled", formatBoolean(controlledMaterial?.read_image_enabled)],
              ["requires_explicit_read_confirmation", formatBoolean(controlledMaterial?.requires_explicit_read_confirmation)],
              ["requires_manual_review", formatBoolean(controlledMaterial?.requires_manual_review)],
              ["ocr_live_enabled", formatBoolean(controlledMaterial?.ocr_live_enabled)],
              ["llm_live_enabled", formatBoolean(controlledMaterial?.llm_live_enabled)],
              ["legal_search_live_enabled", formatBoolean(controlledMaterial?.legal_search_live_enabled)],
              ["deepseek_live_enabled", formatBoolean(controlledMaterial?.deepseek_live_enabled)],
              ["store_material_content_in_git", formatBoolean(controlledMaterial?.store_material_content_in_git)],
              ["store_extracted_text_in_git", formatBoolean(controlledMaterial?.store_extracted_text_in_git)],
              ["runtime_storage_enabled", formatBoolean(controlledMaterial?.runtime_storage_enabled)],
              ["runtime_storage_path", controlledMaterial?.runtime_storage_path ?? "storage/runtime/controlled_material_previews"],
              ["final_legal_opinion_enabled", formatBoolean(controlledMaterial?.final_legal_opinion_enabled)]
            ]}
            actionHref="/controlled-material"
          />
          <StatusCard
            title="Controlled OCR"
            provider={controlledOCR?.mode ?? "local_only_controlled_ocr"}
            connected={controlledOCR?.enabled ?? false}
            rows={[
              ["mode", controlledOCR?.mode ?? "local_only_controlled_ocr"],
              ["production_enabled", formatBoolean(controlledOCR?.production_enabled)],
              ["ocr_live_enabled", formatBoolean(controlledOCR?.ocr_live_enabled)],
              ["ocr_live_default", formatBoolean(controlledOCR?.ocr_live_default)],
              ["mock_ocr_enabled", formatBoolean(controlledOCR?.mock_ocr_enabled)],
              ["requires_explicit_ocr_confirmation", formatBoolean(controlledOCR?.requires_explicit_ocr_confirmation)],
              ["requires_manual_review", formatBoolean(controlledOCR?.requires_manual_review)],
              ["allowed_file_extensions", controlledOCR?.allowed_file_extensions?.join(" / ") ?? ".pdf / .png / .jpg / .jpeg / .txt"],
              ["max_file_size_bytes", String(controlledOCR?.max_file_size_bytes ?? 5000000)],
              ["read_pdf_binary_enabled", formatBoolean(controlledOCR?.read_pdf_binary_enabled)],
              ["read_image_binary_enabled", formatBoolean(controlledOCR?.read_image_binary_enabled)],
              ["extract_real_ocr_text_enabled", formatBoolean(controlledOCR?.extract_real_ocr_text_enabled)],
              ["runtime_storage_enabled", formatBoolean(controlledOCR?.runtime_storage_enabled)],
              ["runtime_storage_path", controlledOCR?.runtime_storage_path ?? "storage/runtime/controlled_ocr_previews"],
              ["final_legal_opinion_enabled", formatBoolean(controlledOCR?.final_legal_opinion_enabled)]
            ]}
            actionHref="/controlled-ocr"
          />
          <StatusCard
            title="Controlled Legal Search"
            provider={controlledLegalSearch?.mode ?? "local_only_controlled_legal_search"}
            connected={controlledLegalSearch?.enabled ?? false}
            rows={[
              ["mode", controlledLegalSearch?.mode ?? "local_only_controlled_legal_search"],
              ["production_enabled", formatBoolean(controlledLegalSearch?.production_enabled)],
              ["legal_search_live_enabled", formatBoolean(controlledLegalSearch?.legal_search_live_enabled)],
              ["legal_search_live_default", formatBoolean(controlledLegalSearch?.legal_search_live_default)],
              ["mock_legal_search_enabled", formatBoolean(controlledLegalSearch?.mock_legal_search_enabled)],
              ["requires_explicit_legal_search_confirmation", formatBoolean(controlledLegalSearch?.requires_explicit_legal_search_confirmation)],
              ["requires_manual_review", formatBoolean(controlledLegalSearch?.requires_manual_review)],
              ["query_redaction_enabled", formatBoolean(controlledLegalSearch?.query_redaction_enabled)],
              ["citation_resolver_enabled", formatBoolean(controlledLegalSearch?.citation_resolver_enabled)],
              ["runtime_storage_enabled", formatBoolean(controlledLegalSearch?.runtime_storage_enabled)],
              ["runtime_storage_path", controlledLegalSearch?.runtime_storage_path ?? "storage/runtime/controlled_legal_search_previews"],
              ["final_legal_opinion_enabled", formatBoolean(controlledLegalSearch?.final_legal_opinion_enabled)]
            ]}
            actionHref="/controlled-legal-search"
          />
          <StatusCard
            title="Controlled Report Draft"
            provider={controlledReportDraft?.mode ?? "local_only_controlled_report_draft"}
            connected={controlledReportDraft?.enabled ?? false}
            rows={[
              ["mode", controlledReportDraft?.mode ?? "local_only_controlled_report_draft"],
              ["production_enabled", formatBoolean(controlledReportDraft?.production_enabled)],
              ["mock_report_assembly_enabled", formatBoolean(controlledReportDraft?.mock_report_assembly_enabled)],
              ["requires_explicit_assembly_confirmation", formatBoolean(controlledReportDraft?.requires_explicit_assembly_confirmation)],
              ["requires_manual_review", formatBoolean(controlledReportDraft?.requires_manual_review)],
              ["llm_live_enabled", formatBoolean(controlledReportDraft?.llm_live_enabled)],
              ["deepseek_live_enabled", formatBoolean(controlledReportDraft?.deepseek_live_enabled)],
              ["ocr_live_enabled", formatBoolean(controlledReportDraft?.ocr_live_enabled)],
              ["legal_search_live_enabled", formatBoolean(controlledReportDraft?.legal_search_live_enabled)],
              ["runtime_storage_enabled", formatBoolean(controlledReportDraft?.runtime_storage_enabled)],
              ["runtime_storage_path", controlledReportDraft?.runtime_storage_path ?? "storage/runtime/controlled_report_drafts"],
              ["source_trace_enabled", formatBoolean(controlledReportDraft?.source_trace_enabled)],
              ["final_legal_opinion_enabled", formatBoolean(controlledReportDraft?.final_legal_opinion_enabled)]
            ]}
            actionHref="/controlled-report-draft"
          />
          <StatusCard
            title="Controlled Review"
            provider={controlledReview?.mode ?? "local_only_controlled_lawyer_review"}
            connected={controlledReview?.enabled ?? false}
            rows={[
              ["mode", controlledReview?.mode ?? "local_only_controlled_lawyer_review"],
              ["production_enabled", formatBoolean(controlledReview?.production_enabled)],
              ["mock_review_enabled", formatBoolean(controlledReview?.mock_review_enabled)],
              ["requires_explicit_review_confirmation", formatBoolean(controlledReview?.requires_explicit_review_confirmation)],
              ["requires_explicit_assembly_confirmation", formatBoolean(controlledReview?.requires_explicit_assembly_confirmation)],
              ["requires_manual_review", formatBoolean(controlledReview?.requires_manual_review)],
              ["llm_live_enabled", formatBoolean(controlledReview?.llm_live_enabled)],
              ["deepseek_live_enabled", formatBoolean(controlledReview?.deepseek_live_enabled)],
              ["ocr_live_enabled", formatBoolean(controlledReview?.ocr_live_enabled)],
              ["legal_search_live_enabled", formatBoolean(controlledReview?.legal_search_live_enabled)],
              ["skill_publish_enabled", formatBoolean(controlledReview?.skill_publish_enabled)],
              ["workspace_runtime_auto_enable", formatBoolean(controlledReview?.workspace_runtime_auto_enable)],
              ["runtime_storage_path", controlledReview?.runtime_storage_path ?? "storage/runtime/controlled_lawyer_reviews"],
              ["final_legal_opinion_enabled", formatBoolean(controlledReview?.final_legal_opinion_enabled)]
            ]}
            actionHref="/controlled-review"
          />
          <StatusCard
            title="Controlled Revision"
            provider={controlledRevision?.mode ?? "local_only_controlled_revision"}
            connected={controlledRevision?.enabled ?? false}
            rows={[
              ["mode", controlledRevision?.mode ?? "local_only_controlled_revision"],
              ["production_enabled", formatBoolean(controlledRevision?.production_enabled)],
              ["mock_revision_enabled", formatBoolean(controlledRevision?.mock_revision_enabled)],
              ["requires_review_id", formatBoolean(controlledRevision?.requires_review_id)],
              ["requires_explicit_revision_confirmation", formatBoolean(controlledRevision?.requires_explicit_revision_confirmation)],
              ["requires_manual_review", formatBoolean(controlledRevision?.requires_manual_review)],
              ["llm_live_enabled", formatBoolean(controlledRevision?.llm_live_enabled)],
              ["deepseek_live_enabled", formatBoolean(controlledRevision?.deepseek_live_enabled)],
              ["ocr_live_enabled", formatBoolean(controlledRevision?.ocr_live_enabled)],
              ["legal_search_live_enabled", formatBoolean(controlledRevision?.legal_search_live_enabled)],
              ["runtime_storage_path", controlledRevision?.runtime_storage_path ?? "storage/runtime/controlled_revisions"],
              ["source_trace_enabled", formatBoolean(controlledRevision?.source_trace_enabled)],
              ["final_legal_opinion_enabled", formatBoolean(controlledRevision?.final_legal_opinion_enabled)]
            ]}
            actionHref="/controlled-revision"
          />
          <StatusCard
            title="Controlled Final Review"
            provider={controlledFinalReview?.mode ?? "local_only_controlled_final_review_lock"}
            connected={controlledFinalReview?.enabled ?? false}
            rows={[
              ["mode", controlledFinalReview?.mode ?? "local_only_controlled_final_review_lock"],
              ["production_enabled", formatBoolean(controlledFinalReview?.production_enabled)],
              ["mock_final_lock_enabled", formatBoolean(controlledFinalReview?.mock_final_lock_enabled)],
              ["requires_draft_id", formatBoolean(controlledFinalReview?.requires_draft_id)],
              ["requires_review_id", formatBoolean(controlledFinalReview?.requires_review_id)],
              ["requires_revision_id", formatBoolean(controlledFinalReview?.requires_revision_id)],
              ["requires_explicit_final_lock_confirmation", formatBoolean(controlledFinalReview?.requires_explicit_final_lock_confirmation)],
              ["requires_manual_final_confirmation", formatBoolean(controlledFinalReview?.requires_manual_final_confirmation)],
              ["llm_live_enabled", formatBoolean(controlledFinalReview?.llm_live_enabled)],
              ["deepseek_live_enabled", formatBoolean(controlledFinalReview?.deepseek_live_enabled)],
              ["ocr_live_enabled", formatBoolean(controlledFinalReview?.ocr_live_enabled)],
              ["legal_search_live_enabled", formatBoolean(controlledFinalReview?.legal_search_live_enabled)],
              ["runtime_storage_path", controlledFinalReview?.runtime_storage_path ?? "storage/runtime/controlled_final_review_locks"],
              ["immutable_snapshot_enabled", formatBoolean(controlledFinalReview?.immutable_snapshot_enabled)],
              ["final_legal_opinion_enabled", formatBoolean(controlledFinalReview?.final_legal_opinion_enabled)]
            ]}
            actionHref="/controlled-final-review"
          />
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Source Refs Foundation</h2>
            <div className="mt-4 space-y-3">
              <InfoRow label="source_ref_types" value="material / ocr / legal_search / skill_runtime / report / mock" />
              <InfoRow label="report.citations" value="prepared as optional array" />
              <InfoRow label="report.trace" value="prepared as optional object" />
              <InfoRow label="citation_summary" value="prepared as optional object" />
              <InfoRow label="citation_persistence" value="mock resolver only" />
            </div>
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}

async function loadRuntime() {
  try {
    const [runtime, ocr, legalSearch, sourceRefs, localSandbox, internalAlpha, personalAlpha, controlledMaterial, controlledOCR, controlledLegalSearch, controlledReportDraft, controlledReview, controlledRevision, controlledFinalReview] = await Promise.all([
      getLLMStatus(),
      getOCRStatus(),
      getLegalSearchStatus(),
      getSourceRefsStatus(),
      getLocalSandboxStatus(),
      getInternalAlphaStatus(),
      getPersonalAlphaStatus(),
      getControlledMaterialStatus(),
      getControlledOCRStatus(),
      getControlledLegalSearchStatus(),
      getControlledReportDraftStatus(),
      getControlledLawyerReviewStatus(),
      getControlledRevisionStatus(),
      getControlledFinalReviewStatus()
    ]);
    return { runtime, ocr, legalSearch, sourceRefs, localSandbox, internalAlpha, personalAlpha, controlledMaterial, controlledOCR, controlledLegalSearch, controlledReportDraft, controlledReview, controlledRevision, controlledFinalReview, error: null };
  } catch {
    return {
      runtime: null,
      ocr: null,
      legalSearch: null,
      sourceRefs: null,
      localSandbox: null,
      internalAlpha: null,
      personalAlpha: null,
      controlledMaterial: null,
      controlledOCR: null,
      controlledLegalSearch: null,
      controlledReportDraft: null,
      controlledReview: null,
      controlledRevision: null,
      controlledFinalReview: null,
      error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。"
    };
  }
}

function StatusCard({
  title,
  provider,
  connected,
  rows,
  actionHref
}: {
  title: string;
  provider: string;
  connected: boolean;
  rows: Array<[string, string]>;
  actionHref?: string;
}) {
  return (
    <Card>
      <CardBody>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div className="text-xs uppercase tracking-wide text-muted">{title}</div>
            <div className="mt-2 text-lg font-semibold text-ink">{provider}</div>
          </div>
          <Badge tone={connected ? "gold" : "muted"}>{connected ? "connected" : "not connected"}</Badge>
        </div>
        <div className="mt-5 space-y-3">
          {rows.map(([label, value]) => (
            <InfoRow key={label} label={label} value={value} />
          ))}
        </div>
        {actionHref ? (
          <Link href={actionHref} className="mt-5 inline-flex rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
            打开测试页
          </Link>
        ) : null}
      </CardBody>
    </Card>
  );
}

function formatBoolean(value: boolean | undefined) {
  if (typeof value !== "boolean") {
    return "-";
  }
  return value ? "true" : "false";
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
