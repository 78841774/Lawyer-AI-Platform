"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  PersonalAlphaCaseOSActionEligibility,
  PersonalAlphaCaseOSAuditTimeline,
  PersonalAlphaCaseOSAuditTimelineAvailableFilters,
  PersonalAlphaCaseOSAuditTimelineFilters,
  PersonalAlphaCaseOSAuditTimelineRedactionCheck,
  PersonalAlphaCaseOSAuditTimelineSummary,
  PersonalAlphaCaseOSBlockers,
  PersonalAlphaCaseOSCaseDetail,
  PersonalAlphaCaseOSExportPackageContent,
  PersonalAlphaCaseOSExportPackageCreateRequest,
  PersonalAlphaCaseOSExportPackageCreateResult,
  PersonalAlphaCaseOSExportPackageDetail,
  PersonalAlphaCaseOSExportPackageList,
  PersonalAlphaCaseOSExportPackageSafetyCheck,
  PersonalAlphaCaseOSExportPackageStatus,
  PersonalAlphaCaseOSExportPackageSummary,
  PersonalAlphaCaseOSFinalLockConsolidation,
  PersonalAlphaCaseOSMetadataClosure,
  PersonalAlphaCaseOSMetadataClosureBlockers,
  PersonalAlphaCaseOSMetadataClosureChecklist,
  PersonalAlphaCaseOSMetadataClosureExportPreview,
  PersonalAlphaCaseOSNextAction,
  PersonalAlphaCaseOSQualityChecklist,
  PersonalAlphaCaseOSQualityFindings,
  PersonalAlphaCaseOSQualityRecommendations,
  PersonalAlphaCaseOSQualityReportPreview,
  PersonalAlphaCaseOSQualityScore,
  PersonalAlphaCaseOSQualityStatus,
  PersonalAlphaCaseOSQualitySummary,
  PersonalAlphaCaseOSReviewState,
  PersonalAlphaCaseOSReviewStateHistory,
  PersonalAlphaCaseOSReviewStateSummary,
  PersonalAlphaCaseOSReviewStateTransitionValidation,
  PersonalAlphaCaseOSReviewStateTransitions,
  PersonalAlphaCaseOSStageOrchestration,
  PersonalAlphaCaseOSStageState,
  PersonalAlphaCaseOSStageTransitions,
  PersonalAlphaCaseOSUnifiedAuditTimeline,
  getPersonalAlphaCaseOSActionEligibility,
  getPersonalAlphaCaseOSAuditTimeline,
  getPersonalAlphaCaseOSAuditTimelineFilters,
  getPersonalAlphaCaseOSAuditTimelineRedactionCheck,
  getPersonalAlphaCaseOSAuditTimelineSummary,
  getPersonalAlphaCaseOSBlockers,
  getPersonalAlphaCaseOSCaseDetail,
  createPersonalAlphaCaseOSExportPackage,
  getPersonalAlphaCaseOSExportPackage,
  getPersonalAlphaCaseOSExportPackageContent,
  getPersonalAlphaCaseOSExportPackageSafetyCheck,
  getPersonalAlphaCaseOSExportPackageStatus,
  getPersonalAlphaCaseOSExportPackageSummary,
  getPersonalAlphaCaseOSFinalLockConsolidation,
  getPersonalAlphaCaseOSMetadataClosure,
  getPersonalAlphaCaseOSMetadataClosureBlockers,
  getPersonalAlphaCaseOSMetadataClosureChecklist,
  getPersonalAlphaCaseOSMetadataClosureExportPreview,
  getPersonalAlphaCaseOSNextAction,
  getPersonalAlphaCaseOSQualityChecklist,
  getPersonalAlphaCaseOSQualityFindings,
  getPersonalAlphaCaseOSQualityRecommendations,
  getPersonalAlphaCaseOSQualityReportPreview,
  getPersonalAlphaCaseOSQualityScore,
  getPersonalAlphaCaseOSQualityStatus,
  getPersonalAlphaCaseOSQualitySummary,
  getPersonalAlphaCaseOSReviewState,
  getPersonalAlphaCaseOSReviewStateHistory,
  getPersonalAlphaCaseOSReviewStateSummary,
  getPersonalAlphaCaseOSReviewStateTransitions,
  getPersonalAlphaCaseOSSafetyChecklist,
  getPersonalAlphaCaseOSStageOrchestration,
  getPersonalAlphaCaseOSStageTransitions,
  getPersonalAlphaCaseOSUnifiedAuditTimeline,
  listPersonalAlphaCaseOSExportPackages,
  validatePersonalAlphaCaseOSReviewStateTransition
} from "@/services/api";

const FALLBACK_STAGE_ORDER = [
  "workspace_run",
  "source_review",
  "source_review_decision",
  "final_readiness",
  "final_gate",
  "final_packet",
  "lawyer_final_review",
  "final_lock"
];

const DEFAULT_AUDIT_FILTERS: Partial<PersonalAlphaCaseOSAuditTimelineFilters> = {
  stage_id: "",
  event_type: "",
  result: "",
  safety_status: "",
  limit: 100,
  offset: 0
};

const REVIEW_STATE_OPTIONS = [
  "draft",
  "intake_ready",
  "workspace_run_ready",
  "source_review_pending",
  "source_reviewed",
  "source_decision_pending",
  "source_decision_completed",
  "final_readiness_pending",
  "final_readiness_ready",
  "final_gate_pending",
  "final_gate_approved",
  "final_packet_pending",
  "final_packet_created",
  "lawyer_final_review_pending",
  "lawyer_review_approved",
  "lawyer_review_revision_requested",
  "lawyer_review_rejected",
  "final_lock_pending",
  "final_lock_created",
  "completed_metadata_review",
  "blocked"
];

const DEFAULT_EXPORT_PACKAGE_FORM: PersonalAlphaCaseOSExportPackageCreateRequest = {
  format: "json",
  reviewer_id: "local_demo_lawyer",
  manual_review_confirmed: true,
  lawyer_review_confirmed: true,
  metadata_only_confirmation: true,
  redacted_only_confirmation: true,
  no_raw_content_confirmation: true,
  no_final_legal_opinion_confirmation: true,
  no_final_report_generation_confirmation: true
};

export default function PersonalAlphaCaseOSDetailPage() {
  const params = useParams<{ caseId: string }>();
  const caseId = decodeURIComponent(params.caseId);
  const [detail, setDetail] = useState<PersonalAlphaCaseOSCaseDetail | null>(null);
  const [timeline, setTimeline] = useState<PersonalAlphaCaseOSAuditTimeline | null>(null);
  const [nextAction, setNextAction] = useState<PersonalAlphaCaseOSNextAction | null>(null);
  const [stageOrchestration, setStageOrchestration] = useState<PersonalAlphaCaseOSStageOrchestration | null>(null);
  const [stageTransitions, setStageTransitions] = useState<PersonalAlphaCaseOSStageTransitions | null>(null);
  const [actionEligibility, setActionEligibility] = useState<PersonalAlphaCaseOSActionEligibility | null>(null);
  const [blockers, setBlockers] = useState<PersonalAlphaCaseOSBlockers | null>(null);
  const [unifiedAuditTimeline, setUnifiedAuditTimeline] = useState<PersonalAlphaCaseOSUnifiedAuditTimeline | null>(null);
  const [auditSummary, setAuditSummary] = useState<PersonalAlphaCaseOSAuditTimelineSummary | null>(null);
  const [redactionCheck, setRedactionCheck] = useState<PersonalAlphaCaseOSAuditTimelineRedactionCheck | null>(null);
  const [availableFilters, setAvailableFilters] = useState<PersonalAlphaCaseOSAuditTimelineAvailableFilters | null>(null);
  const [auditFilters, setAuditFilters] = useState<Partial<PersonalAlphaCaseOSAuditTimelineFilters>>(DEFAULT_AUDIT_FILTERS);
  const [reviewState, setReviewState] = useState<PersonalAlphaCaseOSReviewState | null>(null);
  const [reviewStateHistory, setReviewStateHistory] = useState<PersonalAlphaCaseOSReviewStateHistory | null>(null);
  const [reviewStateTransitions, setReviewStateTransitions] = useState<PersonalAlphaCaseOSReviewStateTransitions | null>(null);
  const [reviewStateSummary, setReviewStateSummary] = useState<PersonalAlphaCaseOSReviewStateSummary | null>(null);
  const [transitionValidation, setTransitionValidation] = useState<PersonalAlphaCaseOSReviewStateTransitionValidation | null>(null);
  const [finalLockConsolidation, setFinalLockConsolidation] = useState<PersonalAlphaCaseOSFinalLockConsolidation | null>(null);
  const [metadataClosure, setMetadataClosure] = useState<PersonalAlphaCaseOSMetadataClosure | null>(null);
  const [metadataClosureChecklist, setMetadataClosureChecklist] = useState<PersonalAlphaCaseOSMetadataClosureChecklist | null>(null);
  const [metadataClosureBlockers, setMetadataClosureBlockers] = useState<PersonalAlphaCaseOSMetadataClosureBlockers | null>(null);
  const [metadataClosureExportPreview, setMetadataClosureExportPreview] = useState<PersonalAlphaCaseOSMetadataClosureExportPreview | null>(null);
  const [exportPackageStatus, setExportPackageStatus] = useState<PersonalAlphaCaseOSExportPackageStatus | null>(null);
  const [exportPackageSummary, setExportPackageSummary] = useState<PersonalAlphaCaseOSExportPackageSummary | null>(null);
  const [exportPackageList, setExportPackageList] = useState<PersonalAlphaCaseOSExportPackageList | null>(null);
  const [exportPackageDetail, setExportPackageDetail] = useState<PersonalAlphaCaseOSExportPackageDetail | null>(null);
  const [exportPackageContent, setExportPackageContent] = useState<PersonalAlphaCaseOSExportPackageContent | null>(null);
  const [exportPackageSafetyCheck, setExportPackageSafetyCheck] = useState<PersonalAlphaCaseOSExportPackageSafetyCheck | null>(null);
  const [exportPackageCreateResult, setExportPackageCreateResult] = useState<PersonalAlphaCaseOSExportPackageCreateResult | null>(null);
  const [qualityStatus, setQualityStatus] = useState<PersonalAlphaCaseOSQualityStatus | null>(null);
  const [qualityChecklist, setQualityChecklist] = useState<PersonalAlphaCaseOSQualityChecklist | null>(null);
  const [qualityScore, setQualityScore] = useState<PersonalAlphaCaseOSQualityScore | null>(null);
  const [qualityFindings, setQualityFindings] = useState<PersonalAlphaCaseOSQualityFindings | null>(null);
  const [qualityRecommendations, setQualityRecommendations] = useState<PersonalAlphaCaseOSQualityRecommendations | null>(null);
  const [qualityReportPreview, setQualityReportPreview] = useState<PersonalAlphaCaseOSQualityReportPreview | null>(null);
  const [qualitySummary, setQualitySummary] = useState<PersonalAlphaCaseOSQualitySummary | null>(null);
  const [exportPackageForm, setExportPackageForm] = useState<PersonalAlphaCaseOSExportPackageCreateRequest>(DEFAULT_EXPORT_PACKAGE_FORM);
  const [transitionFromState, setTransitionFromState] = useState("final_lock_pending");
  const [transitionToState, setTransitionToState] = useState("final_lock_created");
  const [safetyResponse, setSafetyResponse] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadDetail() {
    setLoading(true);
    setError("");
    try {
      const [
        nextDetail,
        nextTimeline,
        nextActionValue,
        nextSafety,
        nextStageOrchestration,
        nextStageTransitions,
        nextActionEligibility,
        nextBlockers,
        nextUnifiedAuditTimeline,
        nextAuditSummary,
        nextRedactionCheck,
        nextAvailableFilters,
        nextReviewState,
        nextReviewStateHistory,
        nextReviewStateTransitions,
        nextReviewStateSummary,
        nextTransitionValidation,
        nextFinalLockConsolidation,
        nextMetadataClosure,
        nextMetadataClosureChecklist,
        nextMetadataClosureBlockers,
        nextMetadataClosureExportPreview,
        nextExportPackageStatus,
        nextExportPackageSummary,
        nextExportPackageList,
        nextQualityStatus,
        nextQualityChecklist,
        nextQualityScore,
        nextQualityFindings,
        nextQualityRecommendations,
        nextQualityReportPreview,
        nextQualitySummary
      ] = await Promise.all([
        getPersonalAlphaCaseOSCaseDetail(caseId),
        getPersonalAlphaCaseOSAuditTimeline(caseId),
        getPersonalAlphaCaseOSNextAction(caseId),
        getPersonalAlphaCaseOSSafetyChecklist(caseId),
        getPersonalAlphaCaseOSStageOrchestration(caseId),
        getPersonalAlphaCaseOSStageTransitions(caseId),
        getPersonalAlphaCaseOSActionEligibility(caseId),
        getPersonalAlphaCaseOSBlockers(caseId),
        getPersonalAlphaCaseOSUnifiedAuditTimeline(caseId, DEFAULT_AUDIT_FILTERS),
        getPersonalAlphaCaseOSAuditTimelineSummary(caseId),
        getPersonalAlphaCaseOSAuditTimelineRedactionCheck(caseId),
        getPersonalAlphaCaseOSAuditTimelineFilters(caseId),
        getPersonalAlphaCaseOSReviewState(caseId),
        getPersonalAlphaCaseOSReviewStateHistory(caseId),
        getPersonalAlphaCaseOSReviewStateTransitions(caseId),
        getPersonalAlphaCaseOSReviewStateSummary(caseId),
        validatePersonalAlphaCaseOSReviewStateTransition(caseId, transitionFromState, transitionToState),
        getPersonalAlphaCaseOSFinalLockConsolidation(caseId),
        getPersonalAlphaCaseOSMetadataClosure(caseId),
        getPersonalAlphaCaseOSMetadataClosureChecklist(caseId),
        getPersonalAlphaCaseOSMetadataClosureBlockers(caseId),
        getPersonalAlphaCaseOSMetadataClosureExportPreview(caseId),
        getPersonalAlphaCaseOSExportPackageStatus(caseId),
        getPersonalAlphaCaseOSExportPackageSummary(caseId),
        listPersonalAlphaCaseOSExportPackages(caseId),
        getPersonalAlphaCaseOSQualityStatus(caseId),
        getPersonalAlphaCaseOSQualityChecklist(caseId),
        getPersonalAlphaCaseOSQualityScore(caseId),
        getPersonalAlphaCaseOSQualityFindings(caseId),
        getPersonalAlphaCaseOSQualityRecommendations(caseId),
        getPersonalAlphaCaseOSQualityReportPreview(caseId),
        getPersonalAlphaCaseOSQualitySummary(caseId)
      ]);
      setDetail(nextDetail);
      setTimeline(nextTimeline);
      setNextAction(nextActionValue);
      setSafetyResponse(nextSafety);
      setStageOrchestration(nextStageOrchestration);
      setStageTransitions(nextStageTransitions);
      setActionEligibility(nextActionEligibility);
      setBlockers(nextBlockers);
      setUnifiedAuditTimeline(nextUnifiedAuditTimeline);
      setAuditSummary(nextAuditSummary);
      setRedactionCheck(nextRedactionCheck);
      setAvailableFilters(nextAvailableFilters);
      setReviewState(nextReviewState);
      setReviewStateHistory(nextReviewStateHistory);
      setReviewStateTransitions(nextReviewStateTransitions);
      setReviewStateSummary(nextReviewStateSummary);
      setTransitionValidation(nextTransitionValidation);
      setFinalLockConsolidation(nextFinalLockConsolidation);
      setMetadataClosure(nextMetadataClosure);
      setMetadataClosureChecklist(nextMetadataClosureChecklist);
      setMetadataClosureBlockers(nextMetadataClosureBlockers);
      setMetadataClosureExportPreview(nextMetadataClosureExportPreview);
      setExportPackageStatus(nextExportPackageStatus);
      setExportPackageSummary(nextExportPackageSummary);
      setExportPackageList(nextExportPackageList);
      setQualityStatus(nextQualityStatus);
      setQualityChecklist(nextQualityChecklist);
      setQualityScore(nextQualityScore);
      setQualityFindings(nextQualityFindings);
      setQualityRecommendations(nextQualityRecommendations);
      setQualityReportPreview(nextQualityReportPreview);
      setQualitySummary(nextQualitySummary);
    } catch {
      setError("Case OS detail 加载失败。若 case_id 不存在，后端会返回 safe not_found，不暴露本地路径或原文。");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadDetail();
  }, [caseId]);

  async function loadFilteredAuditTimeline(filters: Partial<PersonalAlphaCaseOSAuditTimelineFilters>) {
    setLoading(true);
    setError("");
    try {
      const nextTimeline = await getPersonalAlphaCaseOSUnifiedAuditTimeline(caseId, filters);
      setUnifiedAuditTimeline(nextTimeline);
    } catch {
      setError("Unified Audit Timeline 加载失败。后端会保持 metadata-only/redacted-only 安全边界。");
    } finally {
      setLoading(false);
    }
  }

  function updateAuditFilter(key: keyof PersonalAlphaCaseOSAuditTimelineFilters, value: string) {
    setAuditFilters((current) => ({
      ...current,
      [key]: key === "limit" || key === "offset" ? Number(value) : value
    }));
  }

  function resetAuditFilters() {
    setAuditFilters(DEFAULT_AUDIT_FILTERS);
    void loadFilteredAuditTimeline(DEFAULT_AUDIT_FILTERS);
  }

  async function validateTransition() {
    setLoading(true);
    setError("");
    try {
      const nextValidation = await validatePersonalAlphaCaseOSReviewStateTransition(caseId, transitionFromState, transitionToState);
      setTransitionValidation(nextValidation);
    } catch {
      setError("Transition validation 加载失败。v6.3 只做校验，不执行 workflow action。");
    } finally {
      setLoading(false);
    }
  }

  function updateExportPackageForm(key: keyof PersonalAlphaCaseOSExportPackageCreateRequest, value: string | boolean) {
    setExportPackageForm((current) => ({
      ...current,
      [key]: value
    }));
  }

  async function refreshExportPackages() {
    const [nextStatus, nextSummary, nextList] = await Promise.all([
      getPersonalAlphaCaseOSExportPackageStatus(caseId),
      getPersonalAlphaCaseOSExportPackageSummary(caseId),
      listPersonalAlphaCaseOSExportPackages(caseId)
    ]);
    setExportPackageStatus(nextStatus);
    setExportPackageSummary(nextSummary);
    setExportPackageList(nextList);
  }

  async function createExportPackage() {
    setLoading(true);
    setError("");
    try {
      const result = await createPersonalAlphaCaseOSExportPackage(caseId, exportPackageForm);
      setExportPackageCreateResult(result);
      await refreshExportPackages();
      if (result.package_id) {
        await viewExportPackage(result.package_id);
      }
    } catch {
      setError("Export package 创建失败。后端会在缺少确认、closure 未 ready 或 unsafe 输入时返回 blocked。");
    } finally {
      setLoading(false);
    }
  }

  async function viewExportPackage(packageId: string) {
    setLoading(true);
    setError("");
    try {
      const detailValue = await getPersonalAlphaCaseOSExportPackage(caseId, packageId);
      setExportPackageDetail(detailValue);
    } catch {
      setError("Export package detail 加载失败。");
    } finally {
      setLoading(false);
    }
  }

  async function viewExportPackageContent(packageId: string) {
    setLoading(true);
    setError("");
    try {
      const contentValue = await getPersonalAlphaCaseOSExportPackageContent(caseId, packageId);
      setExportPackageContent(contentValue);
    } catch {
      setError("Export package content 加载失败。");
    } finally {
      setLoading(false);
    }
  }

  async function viewExportPackageSafetyCheck(packageId: string) {
    setLoading(true);
    setError("");
    try {
      const safetyValue = await getPersonalAlphaCaseOSExportPackageSafetyCheck(caseId, packageId);
      setExportPackageSafetyCheck(safetyValue);
    } catch {
      setError("Export package safety check 加载失败。");
    } finally {
      setLoading(false);
    }
  }

  const stageCards = useMemo(() => {
    if (stageOrchestration?.stages?.length) {
      return stageOrchestration.stages;
    }
    const summary = detail?.stage_summary ?? {};
    return FALLBACK_STAGE_ORDER.map((stageId) => {
      const summaryKey = stageId === "workspace_run" ? "workspace" : stageId;
      return summary[summaryKey as keyof typeof summary] as PersonalAlphaCaseOSStageState | undefined;
    }).filter(Boolean) as PersonalAlphaCaseOSStageState[];
  }, [detail, stageOrchestration]);

  const actionHref = buildActionHref(stageOrchestration?.target_route ?? nextAction?.target_route, nextAction?.target_id);

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Personal Alpha Case OS"
          title={detail?.title ?? "Case OS Detail"}
          description="案件级 Personal Alpha workflow 总览：仅聚合 metadata、redacted 状态和审计事件，不显示原始材料、OCR 原文、法律检索原文或最终法律意见。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <div className="flex flex-wrap gap-3">
          <Link href="/case-os">
            <Button type="button" variant="secondary">Back to Case OS</Button>
          </Link>
          <Button type="button" onClick={() => void loadDetail()} disabled={loading}>
            {loading ? "刷新中..." : "Refresh Detail"}
          </Button>
          {actionHref ? (
            <Link href={actionHref}>
              <Button type="button">Open Next Action</Button>
            </Link>
          ) : null}
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Case Profile</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="case_id" value={detail?.profile?.case_id ?? detail?.case_id ?? caseId} />
              <InfoRow label="title" value={detail?.profile?.title ?? detail?.title ?? "-"} />
              <InfoRow label="case_type" value={detail?.profile?.case_type ?? "-"} />
              <InfoRow label="jurisdiction" value={detail?.profile?.jurisdiction ?? "-"} />
              <InfoRow label="client_name" value={detail?.profile?.client_name ?? "-"} />
              <InfoRow label="opposing_party" value={detail?.profile?.opposing_party ?? "-"} />
              <InfoRow label="workspace_id" value={detail?.workspace_id ?? "-"} />
              <InfoRow label="mock_or_redacted_only" value={String(detail?.mock_or_redacted_only ?? true)} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Stage Orchestration</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="current_stage" value={stageOrchestration?.current_stage ?? detail?.current_stage ?? "-"} />
              <InfoRow label="next_action" value={stageOrchestration?.next_action ?? detail?.next_action ?? "-"} />
              <InfoRow label="next_action_label" value={stageOrchestration?.next_action_label ?? nextAction?.next_action_label ?? "-"} />
              <InfoRow label="target_route" value={stageOrchestration?.target_route ?? nextAction?.target_route ?? "-"} />
              <InfoRow label="blocked" value={String(stageOrchestration?.blocked ?? detail?.blocked ?? false)} />
              <InfoRow label="raw_content_included" value={String(stageOrchestration?.raw_content_included ?? false)} />
              <InfoRow label="final_legal_opinion_generated" value={String(stageOrchestration?.final_legal_opinion_generated ?? false)} />
              <InfoRow label="final_report_generated" value={String(stageOrchestration?.final_report_generated ?? false)} />
            </div>
            <ReasonList reasons={stageOrchestration?.blocked_reasons ?? detail?.blocked_reasons ?? []} tone="danger" />
          </CardBody>
        </Card>

        <div id="next-action">
          <Card>
            <CardBody>
              <h2 className="text-base font-semibold text-ink">Next Action</h2>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <InfoRow label="action" value={nextAction?.next_action ?? "-"} />
                <InfoRow label="label" value={nextAction?.next_action_label ?? "-"} />
                <InfoRow label="target_route" value={nextAction?.target_route ?? "-"} />
                <InfoRow label="target_id" value={nextAction?.target_id ?? "-"} />
                <InfoRow label="blocked" value={String(nextAction?.blocked ?? false)} />
                <InfoRow label="raw_content_included" value={String(nextAction?.raw_content_included ?? false)} />
              </div>
              <ReasonList reasons={nextAction?.blocked_reasons ?? []} tone="danger" />
            </CardBody>
          </Card>
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Review State Machine</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="review_state" value={reviewState?.review_state ?? "-"} />
              <InfoRow label="review_state_label" value={reviewState?.review_state_label ?? "-"} />
              <InfoRow label="current_stage" value={reviewState?.current_stage ?? "-"} />
              <InfoRow label="next_action" value={reviewState?.next_action ?? "-"} />
              <InfoRow label="target_route" value={reviewState?.target_route ?? "-"} />
              <InfoRow label="blocked" value={String(reviewState?.blocked ?? false)} />
              <InfoRow label="terminal" value={String(reviewState?.terminal ?? false)} />
              <InfoRow label="completed_metadata_review" value={String(reviewState?.completed_metadata_review ?? false)} />
              <InfoRow label="would_execute_action" value="false" />
              <InfoRow label="raw_content_included" value={String(reviewState?.raw_content_included ?? false)} />
              <InfoRow label="final_legal_opinion_generated" value={String(reviewState?.final_legal_opinion_generated ?? false)} />
              <InfoRow label="final_report_generated" value={String(reviewState?.final_report_generated ?? false)} />
            </div>
            <ReasonList reasons={reviewState?.blocked_reasons ?? []} tone="danger" />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Review State Summary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="review_state" value={reviewStateSummary?.summary.review_state ?? "-"} />
              <InfoRow label="history_count" value={String(reviewStateSummary?.summary.history_count ?? 0)} />
              <InfoRow label="available_transition_count" value={String(reviewStateSummary?.summary.available_transition_count ?? 0)} />
              <InfoRow label="blocked_transition_count" value={String(reviewStateSummary?.summary.blocked_transition_count ?? 0)} />
              <InfoRow label="requires_manual_review" value={String(reviewStateSummary?.summary.requires_manual_review ?? true)} />
              <InfoRow label="requires_lawyer_review" value={String(reviewStateSummary?.summary.requires_lawyer_review ?? true)} />
              <InfoRow label="terminal" value={String(reviewStateSummary?.summary.terminal ?? false)} />
              <InfoRow label="blocked" value={String(reviewStateSummary?.summary.blocked ?? false)} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Final Lock Consolidation</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="consolidation_status" value={finalLockConsolidation?.consolidation_status ?? "-"} />
              <InfoRow label="final_lock_created" value={String(finalLockConsolidation?.final_lock_created ?? false)} />
              <InfoRow label="latest_lock_id" value={finalLockConsolidation?.latest_lock_id ?? "-"} />
              <InfoRow label="latest_packet_id" value={finalLockConsolidation?.latest_packet_id ?? "-"} />
              <InfoRow label="latest_lawyer_review_action" value={finalLockConsolidation?.latest_lawyer_review_action ?? "-"} />
              <InfoRow label="review_state" value={finalLockConsolidation?.review_state ?? "-"} />
              <InfoRow label="completed_metadata_review" value={String(finalLockConsolidation?.completed_metadata_review ?? false)} />
              <InfoRow label="raw_content_included" value={String(finalLockConsolidation?.raw_content_included ?? false)} />
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="lock_status" value={finalLockConsolidation?.final_lock_summary.lock_status ?? "-"} />
              <InfoRow label="workspace_run_id" value={finalLockConsolidation?.linked_metadata.workspace_run_id ?? "-"} />
              <InfoRow label="lawyer_review_action_id" value={finalLockConsolidation?.linked_metadata.lawyer_review_action_id ?? "-"} />
              <InfoRow label="created_at" value={finalLockConsolidation?.final_lock_summary.created_at ?? "-"} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Metadata Closure Summary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="closure_status" value={metadataClosure?.closure_status ?? "-"} />
              <InfoRow label="closure_ready" value={String(metadataClosure?.closure_ready ?? false)} />
              <InfoRow label="completed_metadata_review" value={String(metadataClosure?.completed_metadata_review ?? false)} />
              <InfoRow label="terminal" value={String(metadataClosure?.terminal ?? false)} />
              <InfoRow label="blocked" value={String(metadataClosure?.blocked ?? false)} />
              <InfoRow label="next_action" value={metadataClosure?.next_action ?? "-"} />
              <InfoRow label="target_route" value={metadataClosure?.target_route ?? "-"} />
              <InfoRow label="final_report_generated" value={String(metadataClosure?.final_report_generated ?? false)} />
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-5">
              {Object.entries(metadataClosure?.closure_summary ?? {}).map(([key, value]) => (
                <InfoRow key={key} label={key} value={String(value)} />
              ))}
            </div>
            <ReasonList reasons={metadataClosure?.blocked_reasons ?? []} tone="danger" />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Metadata Closure Checklist</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="passed_count" value={String(metadataClosureChecklist?.passed_count ?? 0)} />
              <InfoRow label="failed_count" value={String(metadataClosureChecklist?.failed_count ?? 0)} />
              <InfoRow label="required_failed_count" value={String(metadataClosureChecklist?.required_failed_count ?? 0)} />
              <InfoRow label="closure_ready" value={String(metadataClosureChecklist?.closure_ready ?? false)} />
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {(metadataClosureChecklist?.checklist ?? []).map((item) => (
                <div key={item.check_id} className={`rounded-md border p-3 ${item.passed ? "border-emerald-200 bg-emerald-50" : "border-rose-200 bg-rose-50"}`}>
                  <div className="text-sm font-semibold text-ink">{item.label}</div>
                  <div className="mt-2 grid gap-1 text-xs text-muted">
                    <span>check_id: {item.check_id}</span>
                    <span>passed: {String(item.passed)}</span>
                    <span>required: {String(item.required)}</span>
                    <span>source: {item.source}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Closure Blockers</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="blocked" value={String(metadataClosureBlockers?.blocked ?? false)} />
              <InfoRow label="required_blocker_count" value={String(metadataClosureBlockers?.required_blocker_count ?? 0)} />
              <InfoRow label="raw_content_included" value={String(metadataClosureBlockers?.raw_content_included ?? false)} />
              <InfoRow label="mock_or_redacted_only" value={String(metadataClosureBlockers?.mock_or_redacted_only ?? true)} />
            </div>
            <ReasonList reasons={metadataClosureBlockers?.blocked_reasons ?? []} tone="danger" />
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {(metadataClosureBlockers?.closure_blockers ?? []).map((item) => (
                <div key={`${item.stage_id}-${item.blocker_id}`} className="rounded-md border border-line bg-paper p-3">
                  <div className="text-sm font-semibold text-ink">{item.blocker_id}</div>
                  <div className="mt-2 grid gap-1 text-xs text-muted">
                    <span>stage_id: {item.stage_id}</span>
                    <span>blocked: {String(item.blocked)}</span>
                    <span>reason: {item.reason ?? "-"}</span>
                    <span>required_action: {item.required_action ?? "-"}</span>
                    <span>target_route: {item.target_route ?? "-"}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Export Preview</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="export_type" value={metadataClosureExportPreview?.export_preview.export_type ?? "-"} />
              <InfoRow label="can_export_metadata_preview" value={String(metadataClosureExportPreview?.can_export_metadata_preview ?? false)} />
              <InfoRow label="would_create_file" value={String(metadataClosureExportPreview?.would_create_file ?? false)} />
              <InfoRow label="would_include_raw_content" value={String(metadataClosureExportPreview?.would_include_raw_content ?? false)} />
              <InfoRow label="raw_content_included" value={String(metadataClosureExportPreview?.raw_content_included ?? false)} />
              <InfoRow label="final_legal_opinion_generated" value={String(metadataClosureExportPreview?.final_legal_opinion_generated ?? false)} />
              <InfoRow label="final_report_generated" value={String(metadataClosureExportPreview?.final_report_generated ?? false)} />
              <InfoRow label="sections" value={String(metadataClosureExportPreview?.export_preview.sections.length ?? 0)} />
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {(metadataClosureExportPreview?.export_preview.sections ?? []).map((section) => (
                <div key={section.section_id} className="rounded-md border border-line bg-paper p-3">
                  <div className="text-sm font-semibold text-ink">{section.title}</div>
                  <div className="mt-2 grid gap-1 text-xs text-muted">
                    <span>section_id: {section.section_id}</span>
                    <span>included: {String(section.included)}</span>
                    <span>item_count: {section.item_count}</span>
                    <span>raw_content_included: {String(section.raw_content_included)}</span>
                  </div>
                </div>
              ))}
            </div>
            <ReasonList reasons={metadataClosureExportPreview?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Quality Status</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="enabled" value={String(qualityStatus?.enabled ?? true)} />
              <InfoRow label="quality_check_available" value={String(qualityStatus?.quality_check_available ?? false)} />
              <InfoRow label="quality_result_is_advisory" value={String(qualityStatus?.quality_result_is_advisory ?? true)} />
              <InfoRow label="metadata_only" value={String(qualityStatus?.metadata_only ?? true)} />
              <InfoRow label="redacted_only" value={String(qualityStatus?.redacted_only ?? true)} />
              <InfoRow label="advisory_only" value={String(qualityStatus?.advisory_only ?? true)} />
              <InfoRow label="raw_content_included" value={String(qualityStatus?.raw_content_included ?? false)} />
              <InfoRow label="final_report_generated" value={String(qualityStatus?.final_report_generated ?? false)} />
            </div>
            <ReasonList reasons={qualityStatus?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Quality Score</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="quality_score" value={String(qualityScore?.score.quality_score ?? 0)} />
              <InfoRow label="quality_grade" value={qualityScore?.score.quality_grade ?? "-"} />
              <InfoRow label="ready_for_personal_alpha_review" value={String(qualityScore?.score.ready_for_personal_alpha_review ?? false)} />
              <InfoRow label="required_failed_count" value={String(qualityScore?.score.required_failed_count ?? 0)} />
              <InfoRow label="critical_failed_count" value={String(qualityScore?.score.critical_failed_count ?? 0)} />
              <InfoRow label="blocking_issue_count" value={String(qualityScore?.score.blocking_issue_count ?? 0)} />
              <InfoRow label="advisory_warning_count" value={String(qualityScore?.score.advisory_warning_count ?? 0)} />
              <InfoRow label="raw_content_included" value={String(qualityScore?.raw_content_included ?? false)} />
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-5">
              {Object.entries(qualityScore?.score_logic ?? {}).map(([key, value]) => (
                <InfoRow key={key} label={key} value={String(value)} />
              ))}
            </div>
            <ReasonList reasons={qualityScore?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Quality Checklist</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-5">
              <InfoRow label="passed_count" value={String(qualityChecklist?.passed_count ?? 0)} />
              <InfoRow label="failed_count" value={String(qualityChecklist?.failed_count ?? 0)} />
              <InfoRow label="required_failed_count" value={String(qualityChecklist?.required_failed_count ?? 0)} />
              <InfoRow label="critical_failed_count" value={String(qualityChecklist?.critical_failed_count ?? 0)} />
              <InfoRow label="warning_count" value={String(qualityChecklist?.warning_count ?? 0)} />
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {(qualityChecklist?.checklist ?? []).map((item) => (
                <div key={item.check_id} className={`rounded-md border p-3 ${item.passed ? "border-emerald-200 bg-emerald-50" : "border-rose-200 bg-rose-50"}`}>
                  <div className="text-sm font-semibold text-ink">{item.label}</div>
                  <div className="mt-2 grid gap-1 text-xs text-muted">
                    <span>check_id: {item.check_id}</span>
                    <span>category: {item.category}</span>
                    <span>passed: {String(item.passed)}</span>
                    <span>required: {String(item.required)}</span>
                    <span>severity: {item.severity}</span>
                    <span>source: {item.source}</span>
                    <span>target_route: {item.target_route}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Quality Findings</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="finding_count" value={String(qualityFindings?.finding_count ?? 0)} />
              <InfoRow label="blocking_finding_count" value={String(qualityFindings?.blocking_finding_count ?? 0)} />
              <InfoRow label="critical_finding_count" value={String(qualityFindings?.critical_finding_count ?? 0)} />
              <InfoRow label="high_finding_count" value={String(qualityFindings?.high_finding_count ?? 0)} />
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {(qualityFindings?.findings ?? []).map((finding) => (
                <div key={finding.finding_id} className={`rounded-md border p-4 ${finding.blocking ? "border-rose-200 bg-rose-50" : "border-line bg-white"}`}>
                  <div className="text-sm font-semibold text-ink">{finding.title}</div>
                  <div className="mt-1 text-xs text-muted">{finding.description}</div>
                  <div className="mt-3 grid gap-1 text-xs text-muted">
                    <span>finding_code: {finding.finding_code}</span>
                    <span>category: {finding.category}</span>
                    <span>severity: {finding.severity}</span>
                    <span>blocking: {String(finding.blocking)}</span>
                    <span>recommended_action: {finding.recommended_action}</span>
                    <span>target_route: {finding.target_route}</span>
                  </div>
                </div>
              ))}
            </div>
            <ReasonList reasons={qualityFindings?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Quality Recommendations</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="recommendation_count" value={String(qualityRecommendations?.recommendation_count ?? 0)} />
              <InfoRow label="would_execute_action" value="false" />
              <InfoRow label="raw_content_included" value={String(qualityRecommendations?.raw_content_included ?? false)} />
              <InfoRow label="mock_or_redacted_only" value={String(qualityRecommendations?.mock_or_redacted_only ?? true)} />
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {(qualityRecommendations?.recommendations ?? []).map((item) => (
                <div key={item.recommendation_id} className="rounded-md border border-line bg-white p-4">
                  <div className="text-sm font-semibold text-ink">{item.label}</div>
                  <div className="mt-1 text-xs text-muted">{item.reason}</div>
                  <div className="mt-3 grid gap-1 text-xs text-muted">
                    <span>priority: {item.priority}</span>
                    <span>action: {item.action}</span>
                    <span>target_route: {item.target_route}</span>
                    <span>would_execute_action: {String(item.would_execute_action)}</span>
                  </div>
                </div>
              ))}
            </div>
            <ReasonList reasons={qualityRecommendations?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Quality Report Preview</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="report_type" value={qualityReportPreview?.report_preview.report_type ?? "-"} />
              <InfoRow label="would_create_file" value={String(qualityReportPreview?.would_create_file ?? false)} />
              <InfoRow label="would_generate_final_report" value={String(qualityReportPreview?.would_generate_final_report ?? false)} />
              <InfoRow label="would_generate_legal_opinion" value={String(qualityReportPreview?.would_generate_legal_opinion ?? false)} />
              <InfoRow label="would_include_raw_content" value={String(qualityReportPreview?.would_include_raw_content ?? false)} />
              <InfoRow label="raw_content_included" value={String(qualityReportPreview?.raw_content_included ?? false)} />
              <InfoRow label="final_legal_opinion_generated" value={String(qualityReportPreview?.final_legal_opinion_generated ?? false)} />
              <InfoRow label="final_report_generated" value={String(qualityReportPreview?.final_report_generated ?? false)} />
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {(qualityReportPreview?.report_preview.sections ?? []).map((section) => (
                <div key={section.section_id} className="rounded-md border border-line bg-paper p-3">
                  <div className="text-sm font-semibold text-ink">{section.title}</div>
                  <div className="mt-2 grid gap-1 text-xs text-muted">
                    <span>section_id: {section.section_id}</span>
                    <span>included: {String(section.included)}</span>
                    <span>item_count: {section.item_count}</span>
                    <span>raw_content_included: {String(section.raw_content_included)}</span>
                  </div>
                </div>
              ))}
            </div>
            <ReasonList reasons={qualityReportPreview?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Quality Summary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="quality_score" value={String(qualitySummary?.summary.quality_score ?? 0)} />
              <InfoRow label="quality_grade" value={qualitySummary?.summary.quality_grade ?? "-"} />
              <InfoRow label="ready_for_personal_alpha_review" value={String(qualitySummary?.summary.ready_for_personal_alpha_review ?? false)} />
              <InfoRow label="required_failed_count" value={String(qualitySummary?.summary.required_failed_count ?? 0)} />
              <InfoRow label="critical_failed_count" value={String(qualitySummary?.summary.critical_failed_count ?? 0)} />
              <InfoRow label="blocking_finding_count" value={String(qualitySummary?.summary.blocking_finding_count ?? 0)} />
              <InfoRow label="metadata_closure_ready" value={String(qualitySummary?.summary.metadata_closure_ready ?? false)} />
              <InfoRow label="export_package_available" value={String(qualitySummary?.summary.export_package_available ?? false)} />
              <InfoRow label="redaction_check_passed" value={String(qualitySummary?.summary.redaction_check_passed ?? false)} />
              <InfoRow label="raw_content_included" value={String(qualitySummary?.raw_content_included ?? false)} />
            </div>
            <div className="mt-4 grid gap-4 xl:grid-cols-2">
              <InlineJsonBlock title="quality_summary.top_findings" value={qualitySummary?.summary.top_findings ?? []} />
              <InlineJsonBlock title="quality_summary.top_recommendations" value={qualitySummary?.summary.top_recommendations ?? []} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Export Package Status</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="enabled" value={String(exportPackageStatus?.enabled ?? true)} />
              <InfoRow label="can_create_export_package" value={String(exportPackageStatus?.can_create_export_package ?? false)} />
              <InfoRow label="supported_formats" value={(exportPackageStatus?.supported_formats ?? []).join(", ") || "-"} />
              <InfoRow label="storage_mode" value={exportPackageStatus?.storage_mode ?? "-"} />
              <InfoRow label="metadata_only" value={String(exportPackageStatus?.metadata_only ?? true)} />
              <InfoRow label="redacted_only" value={String(exportPackageStatus?.redacted_only ?? true)} />
              <InfoRow label="raw_content_included" value={String(exportPackageStatus?.raw_content_included ?? false)} />
              <InfoRow label="final_report_generated" value={String(exportPackageStatus?.final_report_generated ?? false)} />
            </div>
            <ReasonList reasons={exportPackageStatus?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Create Export Package</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <label className="grid gap-2 text-xs text-muted">
                <span className="uppercase tracking-wide">format</span>
                <select
                  value={exportPackageForm.format}
                  onChange={(event) => updateExportPackageForm("format", event.target.value)}
                  className="h-10 rounded-md border border-line bg-white px-3 text-sm text-ink"
                >
                  <option value="json">json</option>
                  <option value="markdown">markdown</option>
                </select>
              </label>
              <label className="grid gap-2 text-xs text-muted">
                <span className="uppercase tracking-wide">reviewer_id</span>
                <input
                  value={exportPackageForm.reviewer_id}
                  onChange={(event) => updateExportPackageForm("reviewer_id", event.target.value)}
                  className="h-10 rounded-md border border-line bg-white px-3 text-sm text-ink"
                />
              </label>
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              <ConfirmBox label="manual_review_confirmed" checked={exportPackageForm.manual_review_confirmed} onChange={(value) => updateExportPackageForm("manual_review_confirmed", value)} />
              <ConfirmBox label="lawyer_review_confirmed" checked={exportPackageForm.lawyer_review_confirmed} onChange={(value) => updateExportPackageForm("lawyer_review_confirmed", value)} />
              <ConfirmBox label="metadata_only_confirmation" checked={exportPackageForm.metadata_only_confirmation} onChange={(value) => updateExportPackageForm("metadata_only_confirmation", value)} />
              <ConfirmBox label="redacted_only_confirmation" checked={exportPackageForm.redacted_only_confirmation} onChange={(value) => updateExportPackageForm("redacted_only_confirmation", value)} />
              <ConfirmBox label="no_raw_content_confirmation" checked={exportPackageForm.no_raw_content_confirmation} onChange={(value) => updateExportPackageForm("no_raw_content_confirmation", value)} />
              <ConfirmBox label="no_final_legal_opinion_confirmation" checked={exportPackageForm.no_final_legal_opinion_confirmation} onChange={(value) => updateExportPackageForm("no_final_legal_opinion_confirmation", value)} />
              <ConfirmBox label="no_final_report_generation_confirmation" checked={exportPackageForm.no_final_report_generation_confirmation} onChange={(value) => updateExportPackageForm("no_final_report_generation_confirmation", value)} />
            </div>
            <div className="mt-4 flex flex-wrap gap-3">
              <Button type="button" onClick={() => void createExportPackage()} disabled={loading || !exportPackageStatus?.can_create_export_package}>
                Create Export Package
              </Button>
              <Button type="button" variant="secondary" onClick={() => void refreshExportPackages()} disabled={loading}>
                Refresh Packages
              </Button>
            </div>
            {exportPackageCreateResult ? (
              <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
                <InfoRow label="status" value={exportPackageCreateResult.status} />
                <InfoRow label="package_id" value={exportPackageCreateResult.package_id || "-"} />
                <InfoRow label="stored" value={String(exportPackageCreateResult.stored)} />
                <InfoRow label="file_created" value={String(exportPackageCreateResult.file_created)} />
                <InfoRow label="file_path_redacted" value={String(exportPackageCreateResult.file_path_redacted)} />
                <InfoRow label="raw_content_included" value={String(exportPackageCreateResult.raw_content_included)} />
                <InfoRow label="final_legal_opinion_generated" value={String(exportPackageCreateResult.final_legal_opinion_generated)} />
                <InfoRow label="final_report_generated" value={String(exportPackageCreateResult.final_report_generated)} />
              </div>
            ) : null}
            <ReasonList reasons={exportPackageCreateResult?.warnings ?? []} tone={exportPackageCreateResult?.status === "export_package_created" ? "default" : "danger"} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Export Package Summary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="package_count" value={String(exportPackageSummary?.summary.package_count ?? 0)} />
              <InfoRow label="json_package_count" value={String(exportPackageSummary?.summary.json_package_count ?? 0)} />
              <InfoRow label="markdown_package_count" value={String(exportPackageSummary?.summary.markdown_package_count ?? 0)} />
              <InfoRow label="latest_package_id" value={exportPackageSummary?.summary.latest_package_id ?? "-"} />
              <InfoRow label="unsafe_package_count" value={String(exportPackageSummary?.summary.unsafe_package_count ?? 0)} />
              <InfoRow label="raw_content_package_count" value={String(exportPackageSummary?.summary.raw_content_package_count ?? 0)} />
              <InfoRow label="all_packages_metadata_only" value={String(exportPackageSummary?.summary.all_packages_metadata_only ?? true)} />
              <InfoRow label="raw_content_included" value={String(exportPackageSummary?.raw_content_included ?? false)} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Export Package List</h2>
            <div className="mt-4 space-y-3">
              {(exportPackageList?.packages ?? []).map((item) => (
                <div key={item.package_id} className="rounded-md border border-line bg-white p-4">
                  <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
                    <InfoRow label="package_id" value={item.package_id} />
                    <InfoRow label="format" value={item.format} />
                    <InfoRow label="status" value={item.status} />
                    <InfoRow label="storage_mode" value={item.storage_mode} />
                    <InfoRow label="file_path_redacted" value={String(item.file_path_redacted)} />
                    <InfoRow label="raw_content_included" value={String(item.raw_content_included)} />
                    <InfoRow label="created_at" value={item.created_at || "-"} />
                    <InfoRow label="file_name" value={item.file_name || "-"} />
                  </div>
                  <div className="mt-4 flex flex-wrap gap-3">
                    <Button type="button" variant="secondary" onClick={() => void viewExportPackage(item.package_id)} disabled={loading}>
                      View Package
                    </Button>
                    <Button type="button" variant="secondary" onClick={() => void viewExportPackageContent(item.package_id)} disabled={loading}>
                      View Content
                    </Button>
                    <Button type="button" variant="secondary" onClick={() => void viewExportPackageSafetyCheck(item.package_id)} disabled={loading}>
                      Safety Check
                    </Button>
                  </div>
                </div>
              ))}
              {!(exportPackageList?.packages ?? []).length ? (
                <div className="rounded-md border border-dashed border-line p-5 text-sm text-muted">
                  暂无 metadata-only export package。
                </div>
              ) : null}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Export Package Detail</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="package_id" value={exportPackageDetail?.package?.package_id ?? "-"} />
              <InfoRow label="format" value={exportPackageDetail?.package?.format ?? "-"} />
              <InfoRow label="status" value={exportPackageDetail?.package?.status ?? "-"} />
              <InfoRow label="section_count" value={String(exportPackageDetail?.content_summary.section_count ?? 0)} />
              <InfoRow label="item_count" value={String(exportPackageDetail?.content_summary.item_count ?? 0)} />
              <InfoRow label="safety_passed" value={String(exportPackageDetail?.safety_check.passed ?? true)} />
              <InfoRow label="raw_content_included" value={String(exportPackageDetail?.raw_content_included ?? false)} />
              <InfoRow label="file_path_redacted" value={String(exportPackageDetail?.package?.file_path_redacted ?? true)} />
            </div>
            <ReasonList reasons={exportPackageDetail?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Export Package Content</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="package_id" value={exportPackageContent?.package_id ?? "-"} />
              <InfoRow label="content_type" value={exportPackageContent?.content_type ?? "-"} />
              <InfoRow label="raw_content_included" value={String(exportPackageContent?.raw_content_included ?? false)} />
              <InfoRow label="final_legal_opinion_generated" value={String(exportPackageContent?.final_legal_opinion_generated ?? false)} />
              <InfoRow label="final_report_generated" value={String(exportPackageContent?.final_report_generated ?? false)} />
            </div>
            <pre className="mt-4 max-h-96 overflow-auto rounded-md bg-slate-950 p-4 text-xs leading-5 text-slate-100">
              {typeof exportPackageContent?.content === "string"
                ? exportPackageContent.content
                : JSON.stringify(exportPackageContent?.content ?? {}, null, 2)}
            </pre>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Export Package Safety Check</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="passed" value={String(exportPackageSafetyCheck?.safety_check.passed ?? true)} />
              <InfoRow label="raw_content_included" value={String(exportPackageSafetyCheck?.safety_check.raw_content_included ?? false)} />
              <InfoRow label="path_like_value_count" value={String(exportPackageSafetyCheck?.safety_check.path_like_value_count ?? 0)} />
              <InfoRow label="api_key_like_value_count" value={String(exportPackageSafetyCheck?.safety_check.api_key_like_value_count ?? 0)} />
              <InfoRow label="personal_identifier_like_value_count" value={String(exportPackageSafetyCheck?.safety_check.personal_identifier_like_value_count ?? 0)} />
              <InfoRow label="unsafe_value_count" value={String(exportPackageSafetyCheck?.safety_check.unsafe_value_count ?? 0)} />
              <InfoRow label="unsafe_items" value={String(exportPackageSafetyCheck?.unsafe_items.length ?? 0)} />
              <InfoRow label="mock_or_redacted_only" value={String(exportPackageSafetyCheck?.mock_or_redacted_only ?? true)} />
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {(exportPackageSafetyCheck?.unsafe_items ?? []).map((item) => (
                <div key={`${item.field_name}-${item.reason}`} className="rounded-md border border-rose-200 bg-rose-50 p-3 text-xs text-rose-800">
                  <div>field_name: {item.field_name}</div>
                  <div>reason: {item.reason}</div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Review State History</h2>
            <div className="mt-4 space-y-3">
              {(reviewStateHistory?.history ?? []).map((item) => (
                <div key={item.state_history_id} className="rounded-md border border-line bg-white p-4">
                  <div className="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
                    <div>
                      <div className="text-sm font-semibold text-ink">
                        {item.from_state} {"->"} {item.to_state}
                      </div>
                      <div className="mt-1 text-xs text-muted">{item.transition}</div>
                    </div>
                    <div className="text-xs text-muted">{item.created_at || "-"}</div>
                  </div>
                  <div className="mt-3 grid gap-2 text-xs text-muted md:grid-cols-4">
                    <span>result: {item.result}</span>
                    <span>stage_id: {item.stage_id}</span>
                    <span>module: {item.module}</span>
                    <span>raw: {String(item.raw_content_included)}</span>
                  </div>
                </div>
              ))}
              {!(reviewStateHistory?.history ?? []).length ? (
                <div className="rounded-md border border-dashed border-line p-5 text-sm text-muted">
                  暂无 review state history metadata。
                </div>
              ) : null}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Available Transitions</h2>
            <div className="mt-4 space-y-3">
              {[...(reviewStateTransitions?.available_transitions ?? []), ...(reviewStateTransitions?.blocked_transitions ?? [])].map((transition) => (
                <div key={transition.transition} className="rounded-md border border-line bg-white p-4">
                  <div className="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
                    <div>
                      <div className="text-sm font-semibold text-ink">
                        {transition.from_state} {"->"} {transition.to_state}
                      </div>
                      <div className="mt-1 text-xs text-muted">{transition.reason}</div>
                    </div>
                    <div className="text-xs text-muted">allowed: {String(transition.allowed)}</div>
                  </div>
                  <div className="mt-3 grid gap-2 text-xs text-muted md:grid-cols-4">
                    <span>target_action: {transition.target_action ?? "-"}</span>
                    <span>target_route: {transition.target_route ?? "-"}</span>
                    <span>confirmations: {transition.required_confirmations.length}</span>
                    <span>raw: {String(transition.raw_content_included)}</span>
                  </div>
                  <LabelList label="required_confirmations" values={transition.required_confirmations} />
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Transition Validation Panel</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <FilterSelect label="from_state" value={transitionFromState} options={REVIEW_STATE_OPTIONS} onChange={setTransitionFromState} />
              <FilterSelect label="to_state" value={transitionToState} options={REVIEW_STATE_OPTIONS} onChange={setTransitionToState} />
              <InfoRow label="would_execute_action" value={String(transitionValidation?.would_execute_action ?? false)} />
              <InfoRow label="valid_transition" value={String(transitionValidation?.valid_transition ?? false)} />
            </div>
            <div className="mt-4 flex flex-wrap gap-3">
              <Button type="button" onClick={() => void validateTransition()} disabled={loading}>
                Validate Transition
              </Button>
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="allowed" value={String(transitionValidation?.allowed ?? false)} />
              <InfoRow label="transition" value={transitionValidation?.transition ?? "-"} />
              <InfoRow label="target_action" value={transitionValidation?.target_action ?? "-"} />
              <InfoRow label="target_route" value={transitionValidation?.target_route ?? "-"} />
              <InfoRow label="raw_content_included" value={String(transitionValidation?.raw_content_included ?? false)} />
              <InfoRow label="mock_or_redacted_only" value={String(transitionValidation?.mock_or_redacted_only ?? true)} />
            </div>
            <ReasonList reasons={transitionValidation?.blocked_reasons ?? []} tone="danger" />
            <LabelList label="required_confirmations" values={transitionValidation?.required_confirmations ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Stage Progress</h2>
            <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
              {stageCards.map((stage) => (
                <div key={stage.stage_id} className="rounded-md border border-line bg-white p-4">
                  <div className="text-xs uppercase tracking-wide text-muted">{stage.stage_id}</div>
                  <div className="mt-2 text-base font-semibold text-ink">{stage.label}</div>
                  <div className={`mt-3 rounded-md border px-3 py-2 text-sm ${stage.blocked ? "border-rose-200 bg-rose-50 text-rose-800" : stage.ready ? "border-emerald-200 bg-emerald-50 text-emerald-800" : "border-line bg-paper text-muted"}`}>
                    {stage.status}
                  </div>
                  <div className="mt-3 space-y-2 text-xs text-muted">
                    <div>ready: {String(stage.ready)}</div>
                    <div>required: {String(stage.required)}</div>
                    <div>blocked: {String(stage.blocked)}</div>
                    <div>next_action: {stage.next_action ?? "-"}</div>
                    <div>target_route: {stage.target_route ?? "-"}</div>
                  </div>
                  {stage.target_route ? (
                    <div className="mt-4">
                      <Link href={buildActionHref(stage.target_route, stage.target_id)}>
                        <Button type="button" variant="secondary">Go to Stage</Button>
                      </Link>
                    </div>
                  ) : null}
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Stage Summary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              {Object.entries(detail?.stage_summary ?? {}).map(([key, value]) => (
                <div key={key} className="rounded-md border border-line bg-paper p-3">
                  <div className="text-xs uppercase tracking-wide text-muted">{key}</div>
                  <pre className="mt-2 max-h-32 overflow-auto text-xs leading-5 text-ink">
                    {JSON.stringify(value, null, 2)}
                  </pre>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Action Eligibility</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {(actionEligibility?.actions ?? []).map((item) => (
                <div key={item.action} className="rounded-md border border-line bg-white p-4">
                  <div className="text-sm font-semibold text-ink">{item.label}</div>
                  <div className="mt-1 text-xs text-muted">{item.action}</div>
                  <div className="mt-3 grid gap-2 text-xs text-muted">
                    <span>eligible: {String(item.eligible)}</span>
                    <span>target_route: {item.target_route}</span>
                    <span>raw_content_included: {String(item.raw_content_included)}</span>
                  </div>
                  <LabelList label="required_confirmations" values={item.required_confirmations} />
                  <LabelList label="blocked_reasons" values={item.blocked_reasons} tone="danger" />
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Blockers</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="blocked" value={String(blockers?.blocked ?? false)} />
              <InfoRow label="raw_content_included" value={String(blockers?.raw_content_included ?? false)} />
              <InfoRow label="mock_or_redacted_only" value={String(blockers?.mock_or_redacted_only ?? true)} />
              <InfoRow label="stage_blockers" value={String(blockers?.stage_blockers?.length ?? 0)} />
            </div>
            <ReasonList reasons={blockers?.blocked_reasons ?? []} tone="danger" />
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              {(blockers?.stage_blockers ?? []).map((item) => (
                <div key={item.stage_id} className="rounded-md border border-line bg-paper p-3">
                  <div className="text-sm font-semibold text-ink">{item.stage_id}</div>
                  <div className="mt-2 text-xs text-muted">blocked: {String(item.blocked)}</div>
                  <ReasonList reasons={item.blocked_reasons} tone="danger" />
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Stage Transitions</h2>
            <div className="mt-4 space-y-3">
              {(stageTransitions?.transitions ?? []).map((transition) => (
                <div key={`${transition.from_stage}-${transition.to_stage}`} className="rounded-md border border-line bg-white p-4">
                  <div className="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
                    <div>
                      <div className="text-sm font-semibold text-ink">
                        {transition.from_stage} {"->"} {transition.to_stage}
                      </div>
                      <div className="mt-1 text-xs text-muted">{transition.reason}</div>
                    </div>
                    <div className="text-xs text-muted">allowed: {String(transition.allowed)}</div>
                  </div>
                  <div className="mt-3 grid gap-2 text-xs text-muted md:grid-cols-3">
                    <span>transition_status: {transition.transition_status}</span>
                    <span>metadata: {String(transition.mock_or_redacted_only)}</span>
                    <span>raw: {String(transition.raw_content_included)}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Checklist</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              {Object.entries(detail?.safety_checklist ?? {}).map(([key, value]) => (
                <InfoRow key={key} label={key} value={String(value)} />
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Audit Filters</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <FilterSelect
                label="stage_id"
                value={String(auditFilters.stage_id ?? "")}
                options={availableFilters?.available_filters.stage_id ?? []}
                onChange={(value) => updateAuditFilter("stage_id", value)}
              />
              <FilterSelect
                label="event_type"
                value={String(auditFilters.event_type ?? "")}
                options={availableFilters?.available_filters.event_type ?? []}
                onChange={(value) => updateAuditFilter("event_type", value)}
              />
              <FilterSelect
                label="result"
                value={String(auditFilters.result ?? "")}
                options={availableFilters?.available_filters.result ?? []}
                onChange={(value) => updateAuditFilter("result", value)}
              />
              <FilterSelect
                label="safety_status"
                value={String(auditFilters.safety_status ?? "")}
                options={availableFilters?.available_filters.safety_status ?? []}
                onChange={(value) => updateAuditFilter("safety_status", value)}
              />
            </div>
            <div className="mt-4 flex flex-wrap gap-3">
              <Button type="button" onClick={() => void loadFilteredAuditTimeline(auditFilters)} disabled={loading}>
                Apply Filters
              </Button>
              <Button type="button" variant="secondary" onClick={resetAuditFilters} disabled={loading}>
                Reset Filters
              </Button>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Audit Summary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="total_events" value={String(auditSummary?.summary.total_events ?? 0)} />
              <InfoRow label="blocked_event_count" value={String(auditSummary?.summary.blocked_event_count ?? 0)} />
              <InfoRow label="warning_event_count" value={String(auditSummary?.summary.warning_event_count ?? 0)} />
              <InfoRow label="redacted_event_count" value={String(auditSummary?.summary.redacted_event_count ?? 0)} />
              <InfoRow label="unsafe_event_count" value={String(auditSummary?.summary.unsafe_event_count ?? 0)} />
              <InfoRow label="raw_content_event_count" value={String(auditSummary?.summary.raw_content_event_count ?? 0)} />
              <InfoRow label="latest_event_at" value={auditSummary?.summary.latest_event_at ?? "-"} />
              <InfoRow label="stage_count" value={String(auditSummary?.summary.stage_count ?? 0)} />
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              {(auditSummary?.summary.stages ?? []).map((stage) => (
                <div key={stage.stage_id} className="rounded-md border border-line bg-paper p-3">
                  <div className="text-sm font-semibold text-ink">{stage.stage_id}</div>
                  <div className="mt-2 text-xs text-muted">events: {stage.event_count}</div>
                  <div className="mt-1 text-xs text-muted">latest_result: {stage.latest_result ?? "-"}</div>
                  <div className="mt-1 text-xs text-muted">blocked: {String(stage.blocked)}</div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Redaction Check</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="passed" value={String(redactionCheck?.redaction_check.passed ?? true)} />
              <InfoRow label="unsafe_event_count" value={String(redactionCheck?.redaction_check.unsafe_event_count ?? 0)} />
              <InfoRow label="path_like_value_count" value={String(redactionCheck?.redaction_check.path_like_value_count ?? 0)} />
              <InfoRow label="api_key_like_value_count" value={String(redactionCheck?.redaction_check.api_key_like_value_count ?? 0)} />
              <InfoRow label="personal_identifier_like_value_count" value={String(redactionCheck?.redaction_check.personal_identifier_like_value_count ?? 0)} />
              <InfoRow label="redacted_event_count" value={String(redactionCheck?.redaction_check.redacted_event_count ?? 0)} />
              <InfoRow label="raw_content_event_count" value={String(redactionCheck?.redaction_check.raw_content_event_count ?? 0)} />
              <InfoRow label="checked_fields" value={String(redactionCheck?.redaction_check.checked_fields.length ?? 0)} />
            </div>
            <LabelList label="checked_fields" values={redactionCheck?.redaction_check.checked_fields ?? []} />
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {(redactionCheck?.unsafe_events ?? []).map((event) => (
                <div key={`${event.timeline_event_id}-${event.field_name}`} className="rounded-md border border-rose-200 bg-rose-50 p-3 text-xs text-rose-800">
                  <div className="font-semibold">{event.timeline_event_id}</div>
                  <div className="mt-1">field: {event.field_name}</div>
                  <div className="mt-1">reason: {event.reason}</div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Unified Audit Timeline</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="event_count" value={String(unifiedAuditTimeline?.event_count ?? 0)} />
              <InfoRow label="returned_count" value={String(unifiedAuditTimeline?.returned_count ?? 0)} />
              <InfoRow label="raw_content_included" value={String(unifiedAuditTimeline?.raw_content_included ?? false)} />
              <InfoRow label="mock_or_redacted_only" value={String(unifiedAuditTimeline?.mock_or_redacted_only ?? true)} />
            </div>
            <div className="mt-4 space-y-3">
              {(unifiedAuditTimeline?.timeline ?? []).map((event) => (
                <div key={event.timeline_event_id} className="rounded-md border border-line bg-white p-4">
                  <div className="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
                    <div>
                      <div className="text-sm font-semibold text-ink">{event.stage_id}</div>
                      <div className="mt-1 text-xs text-muted">{event.timeline_event_id}</div>
                    </div>
                    <div className="text-xs text-muted">{event.created_at || "-"}</div>
                  </div>
                  <div className="mt-3 grid gap-2 text-xs text-muted md:grid-cols-4">
                    <span>event_type: {event.event_type}</span>
                    <span>result: {event.result}</span>
                    <span>safety_status: {event.safety_status}</span>
                    <span>redacted: {String(event.redacted)}</span>
                  </div>
                  <div className="mt-3 rounded-md border border-line bg-paper p-3 text-xs text-muted">
                    {event.message || "-"}
                  </div>
                </div>
              ))}
              {!(unifiedAuditTimeline?.timeline ?? []).length ? (
                <div className="rounded-md border border-dashed border-line p-5 text-sm text-muted">
                  当前过滤条件下暂无 unified audit metadata events。
                </div>
              ) : null}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Audit Timeline</h2>
            <div className="mt-4 space-y-3">
              {(timeline?.timeline ?? detail?.audit_timeline ?? []).map((event) => (
                <div key={event.timeline_event_id} className="rounded-md border border-line bg-white p-4">
                  <div className="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
                    <div>
                      <div className="text-sm font-semibold text-ink">{event.stage_id}</div>
                      <div className="mt-1 text-xs text-muted">{event.timeline_event_id}</div>
                    </div>
                    <div className="text-xs text-muted">{event.created_at || "-"}</div>
                  </div>
                  <div className="mt-3 grid gap-2 text-xs text-muted md:grid-cols-4">
                    <span>event: {event.event_type}</span>
                    <span>result: {event.result}</span>
                    <span>metadata: {String(event.mock_or_redacted_only)}</span>
                    <span>raw: {String(event.raw_content_included)}</span>
                  </div>
                </div>
              ))}
              {!(timeline?.timeline ?? detail?.audit_timeline ?? []).length ? (
                <div className="rounded-md border border-dashed border-line p-5 text-sm text-muted">
                  暂无审计事件。Case OS 不会读取真实材料来补齐时间线。
                </div>
              ) : null}
            </div>
          </CardBody>
        </Card>

        <div className="grid gap-4 xl:grid-cols-2">
          <JsonPanel title="quality_status" value={qualityStatus} />
          <JsonPanel title="quality_checklist" value={qualityChecklist} />
          <JsonPanel title="quality_score" value={qualityScore} />
          <JsonPanel title="quality_findings" value={qualityFindings} />
          <JsonPanel title="quality_recommendations" value={qualityRecommendations} />
          <JsonPanel title="quality_report_preview" value={qualityReportPreview} />
          <JsonPanel title="quality_summary" value={qualitySummary} />
          <JsonPanel title="final_lock_consolidation" value={finalLockConsolidation} />
          <JsonPanel title="metadata_closure" value={metadataClosure} />
          <JsonPanel title="metadata_closure_checklist" value={metadataClosureChecklist} />
          <JsonPanel title="metadata_closure_blockers" value={metadataClosureBlockers} />
          <JsonPanel title="metadata_closure_export_preview" value={metadataClosureExportPreview} />
          <JsonPanel title="export_package_status" value={exportPackageStatus} />
          <JsonPanel title="export_package_summary" value={exportPackageSummary} />
          <JsonPanel title="export_package_list" value={exportPackageList} />
          <JsonPanel title="export_package_detail" value={exportPackageDetail} />
          <JsonPanel title="export_package_content" value={exportPackageContent} />
          <JsonPanel title="export_package_safety_check" value={exportPackageSafetyCheck} />
          <JsonPanel title="export_package_create_result" value={exportPackageCreateResult} />
          <JsonPanel title="review_state" value={reviewState} />
          <JsonPanel title="review_state_summary" value={reviewStateSummary} />
          <JsonPanel title="review_state_history" value={reviewStateHistory} />
          <JsonPanel title="review_state_transitions" value={reviewStateTransitions} />
          <JsonPanel title="transition_validation" value={transitionValidation} />
          <JsonPanel title="unified_audit_timeline" value={unifiedAuditTimeline} />
          <JsonPanel title="audit_summary" value={auditSummary} />
          <JsonPanel title="redaction_check" value={redactionCheck} />
          <JsonPanel title="available_filters" value={availableFilters} />
          <JsonPanel title="stage_orchestration" value={stageOrchestration} />
          <JsonPanel title="action_eligibility" value={actionEligibility} />
          <JsonPanel title="blockers" value={blockers} />
          <JsonPanel title="stage_transitions" value={stageTransitions} />
          <JsonPanel title="case_os_detail" value={{ detail, timeline, nextAction, safetyResponse }} />
        </div>
      </div>
    </AppShell>
  );
}

function buildActionHref(targetRoute?: string | null, targetId?: string | null) {
  if (!targetRoute) {
    return "";
  }
  if (!targetId) {
    return targetRoute;
  }
  const encoded = encodeURIComponent(targetId);
  if (targetRoute.includes("final-lock") || targetRoute.includes("lawyer-final-review")) {
    return `${targetRoute}?packet_id=${encoded}`;
  }
  if (targetRoute.includes("workspace")) {
    return targetRoute;
  }
  return `${targetRoute}?workspace_run_id=${encoded}`;
}

function FilterSelect({
  label,
  value,
  options,
  onChange
}: {
  label: string;
  value: string;
  options: string[];
  onChange: (value: string) => void;
}) {
  return (
    <label className="grid gap-2 text-xs text-muted">
      <span className="uppercase tracking-wide">{label}</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="h-10 rounded-md border border-line bg-white px-3 text-sm text-ink"
      >
        <option value="">All</option>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}

function ReasonList({ reasons, tone = "default" }: { reasons: string[]; tone?: "default" | "danger" }) {
  if (!reasons.length) {
    return null;
  }
  const toneClass = tone === "danger" ? "border-rose-200 bg-rose-50 text-rose-800" : "border-line bg-paper text-muted";
  return (
    <div className={`mt-4 rounded-md border p-3 text-sm ${toneClass}`}>
      {reasons.join(" / ")}
    </div>
  );
}

function LabelList({ label, values, tone = "default" }: { label: string; values: string[]; tone?: "default" | "danger" }) {
  if (!values.length) {
    return null;
  }
  const toneClass = tone === "danger" ? "text-rose-800" : "text-muted";
  return (
    <div className={`mt-3 text-xs ${toneClass}`}>
      <div className="font-semibold text-ink">{label}</div>
      <div className="mt-1 leading-5">{values.join(" / ")}</div>
    </div>
  );
}

function ConfirmBox({ label, checked, onChange }: { label: string; checked: boolean; onChange: (value: boolean) => void }) {
  return (
    <label className="flex items-center gap-3 rounded-md border border-line bg-paper px-3 py-2 text-xs text-muted">
      <input
        type="checkbox"
        checked={checked}
        onChange={(event) => onChange(event.target.checked)}
        className="h-4 w-4 rounded border-line"
      />
      <span>{label}</span>
    </label>
  );
}

function JsonPanel({ title, value }: { title: string; value: unknown }) {
  return (
    <Card>
      <CardBody>
        <h2 className="text-base font-semibold text-ink">{title}</h2>
        <pre className="mt-4 max-h-96 overflow-auto rounded-md bg-slate-950 p-4 text-xs leading-5 text-slate-100">
          {JSON.stringify(value, null, 2)}
        </pre>
      </CardBody>
    </Card>
  );
}

function InlineJsonBlock({ title, value }: { title: string; value: unknown }) {
  return (
    <div className="rounded-md border border-line bg-paper p-3">
      <h3 className="text-sm font-semibold text-ink">{title}</h3>
      <pre className="mt-3 max-h-64 overflow-auto rounded-md bg-slate-950 p-3 text-xs leading-5 text-slate-100">
        {JSON.stringify(value, null, 2)}
      </pre>
    </div>
  );
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800">{message}</div>;
}
