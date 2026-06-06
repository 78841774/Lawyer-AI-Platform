"use client";

import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DarkSafetyBadge,
  DiagnosticsPanel,
  InfoRows,
  RuntimeCard,
  SafeErrorNotice,
  StatusCard,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  buildPersonalExperienceCandidates,
  buildPersonalCodexSkillDraft,
  buildPersonalExperiencePackage,
  buildPersonalSkillPackage,
  buildPersonalTrainingTask,
  approvePersonalPracticeLoadPackage,
  createPersonalLegalRetrievalJob,
  editPersonalPracticeLoadPackage,
  createPersonalCodexTrainingRun,
  createPersonalCodexTrainingRunLoadDryRun,
  createPersonalOcrJob,
  createPersonalSkillExperienceBinding,
  createPersonalRealClosedCaseClassification,
  createPersonalRealClosedCaseIntake,
  createPersonalRealClosedCaseRedaction,
  createPersonalRealClosedCaseSegments,
  createPersonalTrainingArtifactLoadDryRun,
  getPersonalRealClosedCaseAudit,
  getPersonalRealClosedCaseClassification,
  getPersonalRealClosedCaseIntakeStatus,
  getPersonalRealClosedCaseRedactionReport,
  getPersonalRealClosedCaseReviewQueue,
  getPersonalRealClosedCaseSafety,
  getPersonalRealClosedCaseSegments,
  getPersonalRealClosedCaseSourceTraces,
  getPersonalCodexSkillDraftAudit,
  getPersonalExperienceCandidateAudit,
  getPersonalRawWorkProductBoundaryStatus,
  getPersonalSkillExperiencePoolStatus,
  getPersonalV731bTrainingExperiencePipelineStatus,
  getPersonalV731cSkillExperiencePipelineStatus,
  getPersonalV731dPipelineStatus,
  getPersonalV731ePipelineStatus,
  getPersonalV731fPipelineStatus,
  getPersonalExperiencePackageAudit,
  getPersonalExperiencePackageSourceTrace,
  getPersonalPracticeLoadPackageAudit,
  getPersonalPracticeLoadPackageSourceTrace,
  getPersonalExperienceLifecycle,
  getPersonalExperienceLifecycleAuditTimeline,
  getPersonalExperienceLifecycleGraph,
  getPersonalExperienceLifecycleIntegrityCheck,
  getPersonalExperienceLifecycleSafetySummary,
  getPersonalExperienceLifecycleSourceTraceView,
  getPersonalExperienceLifecycleState,
  getPersonalV732ExperienceLifecycleStatus,
  listPersonalExperienceLifecycles,
  recomputePersonalExperienceLifecycle,
  getPersonalCaseAnalysisWorkbenchSchema,
  getPersonalCaseAnalysisWorkbenchStatus,
  getPersonalCaseAnalysisWorkbenchView,
  getPersonalCaseAnalysisWorkbenchOutputs,
  getPersonalCaseAnalysisOutputAudit,
  getPersonalCaseAnalysisOutputSourceTrace,
  getPersonalCaseAnalysisRuntimeOutput,
  getPersonalV733CaseAnalysisWorkbenchStatus,
  listPersonalCaseAnalysisOutputFeedback,
  listPersonalCaseAnalysisOutputRiskEvents,
  listPersonalCaseAnalysisWorkbenchViews,
  markPersonalCaseAnalysisOutputReviewed,
  submitPersonalCaseAnalysisOutputFeedback,
  submitPersonalCaseAnalysisOutputRiskEvent,
  getPersonalSkillPackageAudit,
  getPersonalSkillPackageManifest,
  getPersonalSkillPackageSourceTrace,
  importPersonalApprovedSkillExperience,
  listPersonalExperienceCandidates,
  listPersonalLegalRetrievalJobs,
  listPersonalOcrJobs,
  listPersonalCodexTrainingRuns,
  listPersonalCodexSkillDrafts,
  listPersonalTrainingPackages,
  listPersonalTrainingTasks,
  listPersonalPracticeLoadPackages,
  listPersonalSkillPackages,
  listPersonalSkillExperienceBindings,
  listPersonalSkillExperiencePool,
  listPersonalRealClosedCaseIntakes,
  getPersonalTrainingArtifactAudit,
  getPersonalTrainingArtifactCaseCauseTaxonomy,
  getPersonalTrainingArtifactSafety,
  getPersonalTrainingArtifactScheme,
  getPersonalTrainingArtifactStatus,
  listPersonalTrainingArtifactEvaluations,
  listPersonalTrainingArtifactGates,
  listPersonalTrainingArtifactLoadingManifests,
  listPersonalTrainingArtifactLoadDryRuns,
  listPersonalTrainingArtifactPackages,
  listPersonalTrainingArtifactSkillContexts,
  listPersonalTrainingArtifactSkills,
  listPersonalTrainingArtifactTestCases,
  matchPersonalTrainingArtifactCaseCause,
  redactPersonalExperienceCandidate,
  revalidatePersonalPracticeLoadPackage,
  rejectPersonalPracticeLoadPackage,
  reviewPersonalExperienceCandidate,
  reviewPersonalCodexSkillDraft,
  savePersonalPracticeLoadPackage,
  validatePersonalSkillPackage
} from "@/services/api";
import type {
  CaseCauseNode,
  CodexSkillDraftBuildRequest,
  ExperiencePackageBuildRequest,
  PracticeLoadReviewDecisionRequest,
  PracticeLoadReviewEditRequest,
  PracticeLoadReviewSaveRequest,
  CaseAnalysisRuntimeOutput,
  ExperienceCandidateBuildRequest,
  ExperienceCandidateReviewRequest,
  LegalRetrievalJobRequest,
  OcrJobRequest,
  RealClosedCaseTrainingIntakeRequest,
  SkillPackageBuildRequest,
  TrainingTaskBuildRequest,
  SkillExperienceBindingRequest,
  SkillExperienceImportRequest,
  TrainingArtifactCaseCauseMatchRequest,
  TrainingArtifactLoadDryRunRequest
} from "@/types";

const defaultRequest: TrainingArtifactCaseCauseMatchRequest = {
  case_domain: "civil",
  case_cause_level_1: "contract_dispute",
  case_cause_level_2: "sales_contract_dispute",
  case_cause_level_3: "",
  case_cause_name: "买卖合同纠纷",
  case_cause_code: "civil.contract.sales",
  case_cause_path: ["civil", "contract_dispute", "sales_contract_dispute"],
  evidence_types: ["contract", "invoice", "delivery_record"]
};

export default function PersonalTrainingArtifactsPage() {
  const [data, setData] = useState<Record<string, any>>({});
  const [error, setError] = useState("");
  const [matchResult, setMatchResult] = useState<Record<string, any> | null>(null);
  const [dryRun, setDryRun] = useState<Record<string, any> | null>(null);
  const [trainingRunResult, setTrainingRunResult] = useState<Record<string, any> | null>(null);
  const [trainingRunLoadDryRun, setTrainingRunLoadDryRun] = useState<Record<string, any> | null>(null);
  const [realIntakeResult, setRealIntakeResult] = useState<Record<string, any> | null>(null);
  const [realIntakeArtifacts, setRealIntakeArtifacts] = useState<Record<string, any>>({});
  const [experiencePipelineResult, setExperiencePipelineResult] = useState<Record<string, any>>({});
  const [skillExperienceResult, setSkillExperienceResult] = useState<Record<string, any>>({});
  const [skillDraftResult, setSkillDraftResult] = useState<Record<string, any> | null>(null);
  const [skillDraftArtifacts, setSkillDraftArtifacts] = useState<Record<string, any>>({});
  const [skillPackageResult, setSkillPackageResult] = useState<Record<string, any> | null>(null);
  const [skillPackageArtifacts, setSkillPackageArtifacts] = useState<Record<string, any>>({});
  const [trainingTaskResult, setTrainingTaskResult] = useState<Record<string, any> | null>(null);
  const [trainingPackageResult, setTrainingPackageResult] = useState<Record<string, any> | null>(null);
  const [trainingPackageArtifacts, setTrainingPackageArtifacts] = useState<Record<string, any>>({});
  const [practiceLoadResult, setPracticeLoadResult] = useState<Record<string, any> | null>(null);
  const [practiceLoadArtifacts, setPracticeLoadArtifacts] = useState<Record<string, any>>({});
  const [experienceLifecycleArtifacts, setExperienceLifecycleArtifacts] = useState<Record<string, any>>({});
  const [caseWorkbenchArtifacts, setCaseWorkbenchArtifacts] = useState<Record<string, any>>({});
  const [selectedWorkbenchOutputId, setSelectedWorkbenchOutputId] = useState("");
  const [workbenchFilter, setWorkbenchFilter] = useState({ group: "all", type: "all", risk: "all", status: "all", feedback: "all", keyword: "" });
  const [pathText, setPathText] = useState(defaultRequest.case_cause_path.join(" / "));
  const [evidenceText, setEvidenceText] = useState(defaultRequest.evidence_types.join(" / "));

  const requestPayload = useMemo(
    () => ({
      ...defaultRequest,
      case_cause_path: splitTokens(pathText),
      evidence_types: splitTokens(evidenceText),
      case_cause_level_1: splitTokens(pathText)[1] ?? defaultRequest.case_cause_level_1,
      case_cause_level_2: splitTokens(pathText)[2] ?? defaultRequest.case_cause_level_2
    }),
    [pathText, evidenceText]
  );

  async function loadArtifacts() {
    setError("");
    try {
      const [
        status,
        scheme,
        taxonomy,
        packages,
        skills,
        evaluations,
        gates,
        testCases,
        loadingManifests,
        dryRuns,
        skillContexts,
        audit,
        safety,
        trainingRuns,
        realIntakeStatus,
        realIntakes,
        rawBoundaryStatus,
        v731bStatus,
        ocrJobs,
        legalRetrievalJobs,
        experienceCandidates,
        skillExperiencePoolStatus,
        skillExperiencePool,
        skillExperienceBindings,
        v731cStatus,
        skillDrafts,
        v731dStatus,
        skillPackages,
        v731eStatus,
        trainingTasks,
        trainingPackages,
        v731fStatus,
        practiceLoadPackages,
        v732Status,
        experienceLifecycles,
        v733Status,
        caseWorkbenchStatus,
        caseWorkbenchViews
      ] = await Promise.all([
        getPersonalTrainingArtifactStatus(),
        getPersonalTrainingArtifactScheme(),
        getPersonalTrainingArtifactCaseCauseTaxonomy(),
        listPersonalTrainingArtifactPackages(),
        listPersonalTrainingArtifactSkills(),
        listPersonalTrainingArtifactEvaluations(),
        listPersonalTrainingArtifactGates(),
        listPersonalTrainingArtifactTestCases(),
        listPersonalTrainingArtifactLoadingManifests(),
        listPersonalTrainingArtifactLoadDryRuns(),
        listPersonalTrainingArtifactSkillContexts(),
        getPersonalTrainingArtifactAudit(),
        getPersonalTrainingArtifactSafety(),
        listPersonalCodexTrainingRuns(),
        getPersonalRealClosedCaseIntakeStatus(),
        listPersonalRealClosedCaseIntakes(),
        getPersonalRawWorkProductBoundaryStatus(),
        getPersonalV731bTrainingExperiencePipelineStatus(),
        listPersonalOcrJobs(),
        listPersonalLegalRetrievalJobs(),
        listPersonalExperienceCandidates(),
        getPersonalSkillExperiencePoolStatus(),
        listPersonalSkillExperiencePool(),
        listPersonalSkillExperienceBindings(),
        getPersonalV731cSkillExperiencePipelineStatus(),
        listPersonalCodexSkillDrafts(),
        getPersonalV731dPipelineStatus(),
        listPersonalSkillPackages(),
        getPersonalV731ePipelineStatus(),
        listPersonalTrainingTasks(),
        listPersonalTrainingPackages(),
        getPersonalV731fPipelineStatus(),
        listPersonalPracticeLoadPackages(),
        getPersonalV732ExperienceLifecycleStatus(),
        listPersonalExperienceLifecycles(),
        getPersonalV733CaseAnalysisWorkbenchStatus(),
        getPersonalCaseAnalysisWorkbenchStatus(),
        listPersonalCaseAnalysisWorkbenchViews()
      ]);
      setData({
        status,
        scheme,
        taxonomy,
        packages,
        skills,
        evaluations,
        gates,
        testCases,
        loadingManifests,
        dryRuns,
        skillContexts,
        audit,
        safety,
        trainingRuns,
        realIntakeStatus,
        realIntakes,
        rawBoundaryStatus,
        v731bStatus,
        ocrJobs,
        legalRetrievalJobs,
        experienceCandidates,
        skillExperiencePoolStatus,
        skillExperiencePool,
        skillExperienceBindings,
        v731cStatus,
        skillDrafts,
        v731dStatus,
        skillPackages,
        v731eStatus,
        trainingTasks,
        trainingPackages,
        v731fStatus,
        practiceLoadPackages,
        v732Status,
        experienceLifecycles,
        v733Status,
        caseWorkbenchStatus,
        caseWorkbenchViews
      });
      const lifecycleId = experienceLifecycles.lifecycles?.[0]?.lifecycle_id;
      if (lifecycleId) {
        await refreshExperienceLifecycle(lifecycleId);
      }
      const viewId = caseWorkbenchViews.views?.[0]?.view_id;
      if (viewId) {
        await refreshCaseWorkbench(viewId);
      }
    } catch {
      setError("训练产物加载器 API 暂不可用。页面保持安全 fallback，不读取案件原文、不调用 provider、不展示密钥值。");
    }
  }

  useEffect(() => {
    void loadArtifacts();
  }, []);

  async function runMatch() {
    const result = await matchPersonalTrainingArtifactCaseCause(requestPayload);
    setMatchResult(result);
  }

  async function runDryRun() {
    const payload: TrainingArtifactLoadDryRunRequest = {
      ...requestPayload,
      target_skill_ids: ["case_fact_extraction_skill", "case_legal_analysis_skill"],
      explicit_dry_run_confirmation: true,
      explicit_no_training_confirmation: true,
      explicit_no_open_case_training_confirmation: true,
      explicit_no_auto_publish_confirmation: true
    };
    const result = await createPersonalTrainingArtifactLoadDryRun(payload);
    setDryRun(result);
    await loadArtifacts();
  }

  async function runCodexTraining() {
    const result = await createPersonalCodexTrainingRun({
      source_case_mode: "synthetic_closed_case",
      target_case_cause_paths: [
        ["civil", "contract_dispute", "sales_contract_dispute"],
        ["civil", "contract_dispute", "loan_contract_dispute"],
        ["civil", "tort_dispute", "traffic_accident_dispute"],
        ["civil", "marriage_inheritance", "divorce_dispute"],
        ["civil", "labor_dispute", "labor_contract_dispute"]
      ],
      target_skill_ids: ["case_fact_extraction_skill", "case_legal_analysis_skill"],
      explicit_closed_case_only_confirmation: true,
      explicit_redaction_confirmation: true,
      explicit_no_raw_content_confirmation: true,
      explicit_no_open_case_training_confirmation: true,
      explicit_no_auto_publish_confirmation: true
    });
    setTrainingRunResult(result);
    await loadArtifacts();
  }

  async function runTrainingLoadDryRun() {
    const runId = trainingRunResult?.training_run_id ?? data.trainingRuns?.training_runs?.[0]?.training_run_id;
    if (!runId) return;
    const result = await createPersonalCodexTrainingRunLoadDryRun(runId);
    setTrainingRunLoadDryRun(result);
    await loadArtifacts();
  }

  async function createRealIntake() {
    const payload: RealClosedCaseTrainingIntakeRequest = {
      case_reference_label: "authorized_closed_case_training_metadata_001",
      owner_user_id: "owner_local_demo",
      authorization_confirmed: true,
      case_closed_confirmed: true,
      target_case_cause_path: splitTokens(pathText),
      target_skill_ids: ["case_fact_extraction_skill", "case_legal_analysis_skill"],
      explicit_no_raw_content_confirmation: true,
      explicit_no_open_case_confirmation: true,
      explicit_no_provider_confirmation: true
    };
    const result = await createPersonalRealClosedCaseIntake(payload);
    setRealIntakeResult(result);
    setRealIntakeArtifacts({});
    await loadArtifacts();
  }

  async function runRealIntakePipeline() {
    const intakeId = realIntakeResult?.intake?.intake_id ?? data.realIntakes?.intakes?.[0]?.intake_id;
    if (!intakeId) return;
    const redaction = await createPersonalRealClosedCaseRedaction(intakeId);
    const classification = await createPersonalRealClosedCaseClassification(intakeId);
    const segments = await createPersonalRealClosedCaseSegments(intakeId);
    const reviewQueue = await getPersonalRealClosedCaseReviewQueue(intakeId);
    const sourceTraces = await getPersonalRealClosedCaseSourceTraces(intakeId);
    const audit = await getPersonalRealClosedCaseAudit(intakeId);
    const safety = await getPersonalRealClosedCaseSafety(intakeId);
    setRealIntakeArtifacts({ redaction, classification, segments, reviewQueue, sourceTraces, audit, safety });
    await loadArtifacts();
  }

  async function refreshRealIntakePipeline() {
    const intakeId = realIntakeResult?.intake?.intake_id ?? data.realIntakes?.intakes?.[0]?.intake_id;
    if (!intakeId) return;
    const [redaction, classification, segments, reviewQueue, sourceTraces, audit, safety] = await Promise.all([
      getPersonalRealClosedCaseRedactionReport(intakeId),
      getPersonalRealClosedCaseClassification(intakeId),
      getPersonalRealClosedCaseSegments(intakeId),
      getPersonalRealClosedCaseReviewQueue(intakeId),
      getPersonalRealClosedCaseSourceTraces(intakeId),
      getPersonalRealClosedCaseAudit(intakeId),
      getPersonalRealClosedCaseSafety(intakeId)
    ]);
    setRealIntakeArtifacts({ redaction, classification, segments, reviewQueue, sourceTraces, audit, safety });
  }

  async function runExperiencePipeline() {
    const ocrPayload: OcrJobRequest = {
      material_label: "authorized_lawyer_work_product_metadata_001",
      owner_user_id: "owner_local_demo",
      document_type: "case_work_product",
      page_count: 8,
      explicit_authorized_case_confirmation: true,
      explicit_internal_processing_confirmation: true,
      explicit_no_provider_confirmation: true,
      explicit_no_raw_return_confirmation: true
    };
    const ocrJob = await createPersonalOcrJob(ocrPayload);
    const legalPayload: LegalRetrievalJobRequest = {
      source_ocr_job_id: String(ocrJob.job_id ?? ""),
      query_label: "contract_dispute_experience_basis",
      owner_user_id: "owner_local_demo",
      explicit_no_provider_confirmation: true,
      explicit_no_key_value_confirmation: true,
      explicit_demo_safe_confirmation: true
    };
    const legalRetrievalJob = await createPersonalLegalRetrievalJob(legalPayload);
    const candidatePayload: ExperienceCandidateBuildRequest = {
      source_ocr_job_id: String(ocrJob.job_id ?? ""),
      source_legal_retrieval_job_id: String(legalRetrievalJob.retrieval_job_id ?? ""),
      owner_user_id: "owner_local_demo",
      explicit_redaction_required_confirmation: true,
      explicit_manual_review_required_confirmation: true,
      explicit_no_skill_publish_confirmation: true
    };
    const candidates = await buildPersonalExperienceCandidates(candidatePayload);
    setExperiencePipelineResult({ ocrJob, legalRetrievalJob, candidates });
    await loadArtifacts();
  }

  async function approveFirstExperienceCandidate() {
    const candidateId = experiencePipelineResult.candidates?.candidates?.[0]?.candidate_id ?? data.experienceCandidates?.candidates?.[0]?.candidate_id;
    if (!candidateId) return;
    const redaction = await redactPersonalExperienceCandidate(candidateId);
    const reviewPayload: ExperienceCandidateReviewRequest = {
      action: "approve",
      reviewer_id: "local_demo_lawyer",
      reviewer_note: "仅复核脱敏经验 metadata",
      explicit_manual_review_confirmation: true,
      explicit_no_raw_return_confirmation: true,
      explicit_no_skill_publish_confirmation: true
    };
    const review = await reviewPersonalExperienceCandidate(candidateId, reviewPayload);
    const audit = await getPersonalExperienceCandidateAudit(candidateId);
    setExperiencePipelineResult((current) => ({ ...current, redaction, review, audit }));
    await loadArtifacts();
  }

  async function importAndBindExperience() {
    const candidates = data.experienceCandidates?.candidates ?? [];
    const approvedIds = candidates.filter((candidate: any) => candidate.review_status === "approved_for_skill_experience").map((candidate: any) => candidate.candidate_id);
    const importPayload: SkillExperienceImportRequest = {
      source_candidate_ids: approvedIds,
      owner_user_id: "owner_local_demo",
      explicit_approved_experience_only_confirmation: true,
      explicit_redacted_output_only_confirmation: true,
      explicit_no_skill_publish_confirmation: true
    };
    const imported = await importPersonalApprovedSkillExperience(importPayload);
    const experienceIds = (imported.imported_experiences ?? []).map((entry: any) => entry.experience_id);
    const bindingPayload: SkillExperienceBindingRequest = {
      experience_ids: experienceIds,
      skill_domain: "case_analysis",
      skill_name_candidate: "案件经验提炼 Skill 草案",
      case_cause_scope: "demo_safe_case_cause_scope",
      experience_types: [],
      draft_target_id: "codex_skill_draft_target_v731c"
    };
    const binding = await createPersonalSkillExperienceBinding(bindingPayload);
    setSkillExperienceResult({ imported, binding });
    await loadArtifacts();
  }

  async function buildSkillDraft() {
    const bindingId = skillExperienceResult.binding?.binding_id ?? data.skillExperienceBindings?.bindings?.[0]?.binding_id;
    const experienceIds = skillExperienceResult.imported?.imported_experiences?.map((entry: any) => entry.experience_id) ?? data.skillExperiencePool?.experiences?.map((entry: any) => entry.experience_id) ?? [];
    const payload: CodexSkillDraftBuildRequest = {
      experience_ids: experienceIds,
      binding_id: bindingId ?? null,
      draft_name: "Codex Skill 草案 v7.31c",
      draft_target_id: "codex_skill_draft_target_v731c",
      explicit_approved_experience_only_confirmation: true,
      explicit_no_provider_confirmation: true,
      explicit_no_real_training_confirmation: true,
      explicit_no_skill_publish_confirmation: true
    };
    const result = await buildPersonalCodexSkillDraft(payload);
    setSkillDraftResult(result);
    const draftId = result.draft?.draft_id;
    if (draftId) {
      const audit = await getPersonalCodexSkillDraftAudit(draftId);
      setSkillDraftArtifacts({ audit });
    }
    await loadArtifacts();
  }

  async function reviewSkillDraft(action: string) {
    const draftId = skillDraftResult?.draft?.draft_id ?? data.skillDrafts?.drafts?.[0]?.draft_id;
    if (!draftId) return;
    const review = await reviewPersonalCodexSkillDraft(draftId, {
      action,
      reviewer_id: "local_demo_lawyer",
      reviewer_note: "仅复核 v7.31c Skill 草案结构 metadata",
      explicit_manual_confirmation: true,
      explicit_no_skill_publish_confirmation: true,
      explicit_no_real_training_confirmation: true
    });
    const audit = await getPersonalCodexSkillDraftAudit(draftId);
    setSkillDraftArtifacts({ review, audit });
    await loadArtifacts();
  }

  async function buildSkillPackage() {
    const draftId = skillDraftResult?.draft?.draft_id ?? data.skillDrafts?.drafts?.[0]?.draft_id;
    if (!draftId) return;
    const payload: SkillPackageBuildRequest = {
      source_draft_id: draftId,
      package_name: "案件经验提炼 Skill Package v7.31d",
      package_version: "v7.31d.0",
      supersedes_package_id: null,
      explicit_system_validation_gate_confirmation: true,
      explicit_no_manual_training_output_review_confirmation: true,
      explicit_no_provider_confirmation: true,
      explicit_no_real_training_confirmation: true,
      explicit_no_skill_publish_confirmation: true
    };
    const result = await buildPersonalSkillPackage(payload);
    setSkillPackageResult(result);
    const packageId = result.skill_package?.package_id;
    if (packageId) {
      const [manifest, audit, sourceTrace] = await Promise.all([
        getPersonalSkillPackageManifest(packageId),
        getPersonalSkillPackageAudit(packageId),
        getPersonalSkillPackageSourceTrace(packageId)
      ]);
      setSkillPackageArtifacts({ manifest, audit, sourceTrace });
    }
    await loadArtifacts();
  }

  async function validateSkillPackage() {
    const packageId = skillPackageResult?.skill_package?.package_id ?? data.skillPackages?.skill_packages?.[0]?.package_id;
    if (!packageId) return;
    const validation = await validatePersonalSkillPackage(packageId);
    const [manifest, audit, sourceTrace] = await Promise.all([
      getPersonalSkillPackageManifest(packageId),
      getPersonalSkillPackageAudit(packageId),
      getPersonalSkillPackageSourceTrace(packageId)
    ]);
    setSkillPackageArtifacts({ validation, manifest, audit, sourceTrace });
    await loadArtifacts();
  }

  async function buildTrainingTask() {
    const packageId =
      skillPackageResult?.skill_package?.package_id ??
      data.skillPackages?.skill_packages?.find((item: any) => item.pre_publish_gate_status === "system_validated")?.package_id ??
      data.skillPackages?.skill_packages?.[0]?.package_id;
    if (!packageId) return;
    const payload: TrainingTaskBuildRequest = {
      source_skill_package_id: packageId,
      task_name: "内部训练任务 v7.31e",
      explicit_system_validated_package_confirmation: true,
      explicit_no_manual_training_output_review_confirmation: true,
      explicit_no_provider_confirmation: true,
      explicit_no_real_training_confirmation: true,
      explicit_no_skill_publish_confirmation: true
    };
    const result = await buildPersonalTrainingTask(payload);
    setTrainingTaskResult(result);
    await loadArtifacts();
  }

  async function buildTrainingPackage() {
    const taskId =
      trainingTaskResult?.training_task?.training_task_id ??
      data.trainingTasks?.training_tasks?.[0]?.training_task_id;
    const packageId =
      trainingTaskResult?.training_task?.source_skill_package_id ??
      data.skillPackages?.skill_packages?.find((item: any) => item.pre_publish_gate_status === "system_validated")?.package_id ??
      data.skillPackages?.skill_packages?.[0]?.package_id;
    if (!taskId && !packageId) return;
    const payload: ExperiencePackageBuildRequest = {
      source_training_task_id: taskId ?? null,
      source_skill_package_id: packageId ?? null,
      package_name: "内部训练经验包 v7.31e",
      package_version: "v7.31e.0",
      explicit_pending_practice_load_review_confirmation: true,
      explicit_no_provider_confirmation: true,
      explicit_no_real_training_confirmation: true,
      explicit_no_skill_publish_confirmation: true
    };
    const result = await buildPersonalExperiencePackage(payload);
    setTrainingPackageResult(result);
    const packageIdBuilt = result.training_package?.package_id;
    if (packageIdBuilt) {
      const [audit, sourceTrace] = await Promise.all([
        getPersonalExperiencePackageAudit(packageIdBuilt),
        getPersonalExperiencePackageSourceTrace(packageIdBuilt)
      ]);
      setTrainingPackageArtifacts({ audit, sourceTrace });
    }
    await loadArtifacts();
  }

  function selectedPracticeLoadPackageId() {
    return (
      practiceLoadResult?.package_id ??
      data.practiceLoadPackages?.packages?.[0]?.package_id ??
      trainingPackageResult?.training_package?.package_id ??
      data.trainingPackages?.training_packages?.[0]?.package_id
    );
  }

  async function editPracticeLoadPackage() {
    const packageId = selectedPracticeLoadPackageId();
    if (!packageId) return;
    const payload: PracticeLoadReviewEditRequest = {
      reviewer_id: "local_demo_lawyer",
      reviewer_note: "实战加载前律师编辑开始",
      explicit_lawyer_review_confirmation: true,
      explicit_no_provider_confirmation: true,
      explicit_no_raw_content_confirmation: true,
      explicit_no_skill_publish_confirmation: true
    };
    const result = await editPersonalPracticeLoadPackage(packageId, payload);
    setPracticeLoadResult(result);
    await refreshPracticeLoadArtifacts(result.package_id);
    await loadArtifacts();
  }

  async function savePracticeLoadEdits() {
    const currentPackage = practiceLoadResult ?? data.practiceLoadPackages?.packages?.[0];
    const packageId = currentPackage?.package_id ?? selectedPracticeLoadPackageId();
    if (!packageId) return;
    const payload: PracticeLoadReviewSaveRequest = {
      reviewer_id: "local_demo_lawyer",
      reviewer_note: "律师编辑后的经验包 metadata 保存",
      edited_cards: (currentPackage?.experience_cards ?? []).map((card: any) => ({
        card_id: card.card_id,
        title: card.title,
        lawyer_experience_text: card.lawyer_experience_text,
        applicable_scenarios: card.applicable_scenarios ?? [],
        not_applicable_scenarios: card.not_applicable_scenarios ?? [],
        risk_warnings: card.risk_warnings ?? [],
        usage_boundaries: [...(card.usage_boundaries ?? []), "灰度加载前需保留 audit 与 source trace"],
        gray_load_enabled: true
      })),
      gray_load_enabled: true,
      explicit_lawyer_review_confirmation: true,
      explicit_no_provider_confirmation: true,
      explicit_no_raw_content_confirmation: true,
      explicit_no_skill_publish_confirmation: true
    };
    const result = await savePersonalPracticeLoadPackage(packageId, payload);
    setPracticeLoadResult(result);
    await refreshPracticeLoadArtifacts(result.package_id);
    await loadArtifacts();
  }

  async function revalidatePracticeLoad() {
    const packageId = selectedPracticeLoadPackageId();
    if (!packageId) return;
    const result = await revalidatePersonalPracticeLoadPackage(packageId);
    setPracticeLoadResult(result);
    await refreshPracticeLoadArtifacts(result.package_id);
    await loadArtifacts();
  }

  async function approvePracticeLoad() {
    const packageId = selectedPracticeLoadPackageId();
    if (!packageId) return;
    const payload: PracticeLoadReviewDecisionRequest = {
      reviewer_id: "local_demo_lawyer",
      reviewer_note: "允许进入后续实战加载候选 metadata",
      gray_load_enabled: true,
      explicit_lawyer_review_confirmation: true,
      explicit_system_revalidated_confirmation: true,
      explicit_no_provider_confirmation: true,
      explicit_no_real_training_confirmation: true,
      explicit_no_skill_publish_confirmation: true
    };
    const result = await approvePersonalPracticeLoadPackage(packageId, payload);
    setPracticeLoadResult(result);
    await refreshPracticeLoadArtifacts(result.package_id);
    await loadArtifacts();
  }

  async function rejectPracticeLoad() {
    const packageId = selectedPracticeLoadPackageId();
    if (!packageId) return;
    const payload: PracticeLoadReviewDecisionRequest = {
      reviewer_id: "local_demo_lawyer",
      reviewer_note: "拒绝本轮实战加载 metadata",
      gray_load_enabled: false,
      explicit_lawyer_review_confirmation: true,
      explicit_system_revalidated_confirmation: true,
      explicit_no_provider_confirmation: true,
      explicit_no_real_training_confirmation: true,
      explicit_no_skill_publish_confirmation: true
    };
    const result = await rejectPersonalPracticeLoadPackage(packageId, payload);
    setPracticeLoadResult(result);
    await refreshPracticeLoadArtifacts(result.package_id);
    await loadArtifacts();
  }

  async function refreshPracticeLoadArtifacts(packageId: string) {
    const [audit, sourceTrace] = await Promise.all([
      getPersonalPracticeLoadPackageAudit(packageId),
      getPersonalPracticeLoadPackageSourceTrace(packageId)
    ]);
    setPracticeLoadArtifacts({ audit, sourceTrace });
  }

  function selectedLifecycleId() {
    return experienceLifecycleArtifacts.lifecycle?.lifecycle_id ?? data.experienceLifecycles?.lifecycles?.[0]?.lifecycle_id;
  }

  async function refreshExperienceLifecycle(lifecycleId?: string) {
    const id = lifecycleId ?? selectedLifecycleId();
    if (!id) return;
    const [lifecycle, state, graph, auditTimeline, sourceTraceView, integrityCheck, safetySummary] = await Promise.all([
      getPersonalExperienceLifecycle(id),
      getPersonalExperienceLifecycleState(id),
      getPersonalExperienceLifecycleGraph(id),
      getPersonalExperienceLifecycleAuditTimeline(id),
      getPersonalExperienceLifecycleSourceTraceView(id),
      getPersonalExperienceLifecycleIntegrityCheck(id),
      getPersonalExperienceLifecycleSafetySummary(id)
    ]);
    setExperienceLifecycleArtifacts({ lifecycle, state, graph, auditTimeline, sourceTraceView, integrityCheck, safetySummary });
  }

  async function recomputeExperienceLifecycleView() {
    const id = selectedLifecycleId();
    if (!id) return;
    const lifecycle = await recomputePersonalExperienceLifecycle(id);
    const [state, graph, auditTimeline, sourceTraceView, integrityCheck, safetySummary] = await Promise.all([
      getPersonalExperienceLifecycleState(lifecycle.lifecycle_id),
      getPersonalExperienceLifecycleGraph(lifecycle.lifecycle_id),
      getPersonalExperienceLifecycleAuditTimeline(lifecycle.lifecycle_id),
      getPersonalExperienceLifecycleSourceTraceView(lifecycle.lifecycle_id),
      getPersonalExperienceLifecycleIntegrityCheck(lifecycle.lifecycle_id),
      getPersonalExperienceLifecycleSafetySummary(lifecycle.lifecycle_id)
    ]);
    setExperienceLifecycleArtifacts({ lifecycle, state, graph, auditTimeline, sourceTraceView, integrityCheck, safetySummary });
    await loadArtifacts();
  }

  function selectedWorkbenchViewId() {
    return caseWorkbenchArtifacts.view?.view_id ?? data.caseWorkbenchViews?.views?.[0]?.view_id;
  }

  async function refreshCaseWorkbench(viewId?: string, outputId?: string) {
    const id = viewId ?? selectedWorkbenchViewId();
    if (!id) return;
    const [view, schema, outputs] = await Promise.all([
      getPersonalCaseAnalysisWorkbenchView(id),
      getPersonalCaseAnalysisWorkbenchSchema(id),
      getPersonalCaseAnalysisWorkbenchOutputs(id)
    ]);
    const selectedOutputId = outputId ?? selectedWorkbenchOutputId ?? outputs.outputs?.[0]?.output_id;
    const selectedOutput = selectedOutputId ? await getPersonalCaseAnalysisRuntimeOutput(selectedOutputId) : outputs.outputs?.[0] ?? null;
    const [feedback, riskEvents, audit, sourceTrace] = selectedOutput?.output_id
      ? await Promise.all([
          listPersonalCaseAnalysisOutputFeedback(selectedOutput.output_id),
          listPersonalCaseAnalysisOutputRiskEvents(selectedOutput.output_id),
          getPersonalCaseAnalysisOutputAudit(selectedOutput.output_id),
          getPersonalCaseAnalysisOutputSourceTrace(selectedOutput.output_id)
        ])
      : [null, null, null, null];
    setSelectedWorkbenchOutputId(selectedOutput?.output_id ?? "");
    setCaseWorkbenchArtifacts({ view, schema, outputs, selectedOutput, feedback, riskEvents, audit, sourceTrace });
  }

  async function selectWorkbenchOutput(outputId: string) {
    setSelectedWorkbenchOutputId(outputId);
    const [selectedOutput, feedback, riskEvents, audit, sourceTrace] = await Promise.all([
      getPersonalCaseAnalysisRuntimeOutput(outputId),
      listPersonalCaseAnalysisOutputFeedback(outputId),
      listPersonalCaseAnalysisOutputRiskEvents(outputId),
      getPersonalCaseAnalysisOutputAudit(outputId),
      getPersonalCaseAnalysisOutputSourceTrace(outputId)
    ]);
    setCaseWorkbenchArtifacts((current) => ({ ...current, selectedOutput, feedback, riskEvents, audit, sourceTrace }));
  }

  async function markWorkbenchOutputReviewed() {
    const outputId = selectedWorkbenchOutputId;
    if (!outputId) return;
    const selectedOutput = await markPersonalCaseAnalysisOutputReviewed(outputId);
    await refreshCaseWorkbench(selectedWorkbenchViewId(), selectedOutput.output_id);
    await loadArtifacts();
  }

  async function submitWorkbenchFeedback() {
    const outputId = selectedWorkbenchOutputId;
    if (!outputId) return;
    await submitPersonalCaseAnalysisOutputFeedback(outputId, {
      reviewer_id: "owner_lawyer",
      feedback_type: "schema_output_feedback",
      feedback_summary: "建议补充该项输出的适用边界与律师复核提示。",
      severity: "low",
      explicit_metadata_only_confirmation: true,
      explicit_no_training_confirmation: true
    });
    await refreshCaseWorkbench(selectedWorkbenchViewId(), outputId);
    await loadArtifacts();
  }

  async function submitWorkbenchRiskEvent() {
    const outputId = selectedWorkbenchOutputId;
    if (!outputId) return;
    await submitPersonalCaseAnalysisOutputRiskEvent(outputId, {
      reporter_id: "owner_lawyer",
      risk_level: "medium",
      risk_summary: "该项辅助输出需律师复核适用边界。",
      mitigation_note: "保留为辅助线索，不作为最终法律意见或正式报告。",
      explicit_metadata_only_confirmation: true,
      explicit_no_external_delivery_confirmation: true
    });
    await refreshCaseWorkbench(selectedWorkbenchViewId(), outputId);
    await loadArtifacts();
  }

  const taxonomyNodes = (data.taxonomy?.nodes ?? []) as CaseCauseNode[];
  const lifecycle = experienceLifecycleArtifacts.lifecycle ?? data.experienceLifecycles?.lifecycles?.[0];
  const lifecycleEvents = (experienceLifecycleArtifacts.state?.stage_events ?? lifecycle?.stage_events ?? []) as Record<string, any>[];
  const workbenchView = caseWorkbenchArtifacts.view ?? data.caseWorkbenchViews?.views?.[0];
  const workbenchSchema = caseWorkbenchArtifacts.schema ?? workbenchView;
  const schemaGroups = (workbenchSchema?.output_groups ?? []) as Record<string, any>[];
  const allWorkbenchOutputs = schemaGroups.flatMap((group: any) => (group.outputs ?? []).map((output: any) => ({ ...output, group_title: group.group_title, group_type: group.group_type }))) as CaseAnalysisRuntimeOutput[];
  const outputTypes = Array.from(new Set(allWorkbenchOutputs.map((output: any) => output.output_type)));
  const filteredWorkbenchOutputs = allWorkbenchOutputs.filter((output: any) => {
    const keyword = workbenchFilter.keyword.trim().toLowerCase();
    const feedbackMatched =
      workbenchFilter.feedback === "all" ||
      (workbenchFilter.feedback === "has_feedback" ? Number(output.feedback_count ?? 0) > 0 : Number(output.feedback_count ?? 0) === 0);
    return (
      (workbenchFilter.group === "all" || output.group_id === workbenchFilter.group) &&
      (workbenchFilter.type === "all" || output.output_type === workbenchFilter.type) &&
      (workbenchFilter.risk === "all" || output.risk_level === workbenchFilter.risk) &&
      (workbenchFilter.status === "all" || output.output_status === workbenchFilter.status) &&
      feedbackMatched &&
      (!keyword || String(output.output_summary_redacted ?? "").toLowerCase().includes(keyword) || String(output.output_title ?? "").toLowerCase().includes(keyword))
    );
  });

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}

        <section className="rounded-md border border-slate-800 bg-[#172026] p-8 text-white">
          <div className="text-sm font-medium text-cyan-200">v7.30 Codex Training Scheme & Multi-Level Case-Cause Artifact Loader</div>
          <h1 className="mt-3 text-4xl font-semibold">Codex 训练产物加载器</h1>
          <p className="mt-4 max-w-4xl text-sm leading-6 text-slate-300">
            读取合成闭案训练产物 metadata，按多层级案由匹配 exact / ancestor / common / evidence overlay 包，并生成 Skill Context dry-run。当前不执行模型微调、不读取真实案件、不写训练集、不自动发布 Skill。
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            {["Codex 训练不是微调", "闭案样本 metadata", "案由层级匹配", "fallback dry-run", "不训练未结案件", "不自动发布 Skill"].map((badge) => (
              <DarkSafetyBadge key={badge} label={badge} />
            ))}
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-4">
          <StatusCard label="Loader" value={String(data.status?.training_artifact_loader_ready ?? true)} detail="metadata loader ready" tone="safe" />
          <StatusCard label="Taxonomy" value={data.status?.taxonomy_node_count ?? taxonomyNodes.length} detail="multi-level case cause" tone="info" />
          <StatusCard label="Packages" value={data.status?.package_count ?? data.packages?.artifact_count ?? 0} detail="common / exact / overlay" tone="info" />
          <StatusCard label="Load Executed" value={String(data.status?.load_executed ?? false)} detail="only dry-run" tone="safe" />
        </section>

        <Panel title="v7.31 Training Run / 已结案件 Codex 训练执行">
          <div className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Training Runs" value={data.trainingRuns?.run_count ?? 0} detail="synthetic closed-case samples" tone="info" />
            <StatusCard label="Closed Case Only" value={String(data.trainingRuns?.closed_case_only ?? true)} detail="未结案件不参与训练" tone="safe" />
            <StatusCard label="Fine Tune" value={String(data.trainingRuns?.fine_tune_model_training ?? false)} detail="Codex 训练不是微调" tone="safe" />
            <StatusCard label="Skill Publish" value={String(data.trainingRuns?.skill_published ?? false)} detail="skill_published=false" tone="safe" />
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void runCodexTraining()}>
              执行 synthetic closed-case 训练
            </button>
            <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void runTrainingLoadDryRun()}>
              通过 v7.30 loader 做 dry-run
            </button>
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <Info title="Training Run" items={[trainingRunResult?.training_run_id ?? data.trainingRuns?.training_runs?.[0]?.training_run_id ?? "暂无 run"]} />
            <Info title="Source Case Mode" items={[trainingRunResult?.manifest?.source_case_mode ?? data.trainingRuns?.training_runs?.[0]?.manifest?.source_case_mode ?? "synthetic_closed_case"]} />
            <Info title="Generated Artifacts" items={(trainingRunResult?.manifest?.generated_artifact_ids ?? data.trainingRuns?.training_runs?.[0]?.manifest?.generated_artifact_ids ?? []).slice(0, 8)} />
          </div>
        </Panel>

        <Panel title="v7.31a Real Closed Case Intake / 真实已结案件训练材料导入与脱敏管线">
          <div className="grid gap-4 md:grid-cols-5">
            <StatusCard label="Intake" value={String(data.realIntakeStatus?.intake_pipeline_ready ?? true)} detail="real_closed_case_intake=true" tone="safe" />
            <StatusCard label="Mode" value="real_closed_case" detail="metadata intake only" tone="info" />
            <StatusCard label="Authorization" value={String(realIntakeResult?.intake?.authorization_confirmed ?? true)} detail="owner authorized metadata" tone="safe" />
            <StatusCard label="Closed Case" value={String(realIntakeResult?.intake?.case_closed_confirmed ?? true)} detail="closed_case_only=true" tone="safe" />
            <StatusCard label="Open Case Used" value={String(data.realIntakeStatus?.open_case_data_used ?? false)} detail="open_case_data_used=false" tone="safe" />
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void createRealIntake()}>
              创建已结案件 intake metadata
            </button>
            <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void runRealIntakePipeline()}>
              运行脱敏/归类/切分 mock
            </button>
            <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void refreshRealIntakePipeline()}>
              刷新 intake metadata
            </button>
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <Info title="Intake ID" items={[realIntakeResult?.intake?.intake_id ?? data.realIntakes?.intakes?.[0]?.intake_id ?? "暂无 intake"]} />
            <Info title="Target Skills" items={realIntakeResult?.intake?.target_skill_ids ?? data.realIntakes?.intakes?.[0]?.target_skill_ids ?? ["case_fact_extraction_skill", "case_legal_analysis_skill"]} />
            <Info title="Case Cause Path" items={[joinList(realIntakeResult?.intake?.target_case_cause_path ?? data.realIntakes?.intakes?.[0]?.target_case_cause_path ?? ["civil", "contract_dispute", "sales_contract_dispute"])]} />
          </div>
        </Panel>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="v7.31a Redaction Panel">
            <InfoRows
              rows={[
                ["redaction_required", realIntakeArtifacts.redaction?.redaction_required ?? true],
                ["redaction_completed", realIntakeArtifacts.redaction?.redaction_completed ?? false],
                ["personal_identifiers_removed", realIntakeArtifacts.redaction?.personal_identifiers_removed ?? false],
                ["legal_relevance_preserved", realIntakeArtifacts.redaction?.legal_relevance_preserved ?? false],
                ["jurisdiction_context_preserved", realIntakeArtifacts.redaction?.jurisdiction_context_preserved ?? false],
                ["age_capacity_context_preserved", realIntakeArtifacts.redaction?.age_capacity_context_preserved ?? false],
                ["raw_content_included", realIntakeArtifacts.redaction?.raw_content_included ?? false]
              ]}
            />
          </Panel>
          <Panel title="v7.31a Case Cause Classification">
            <InfoRows
              rows={[
                ["case_cause_name", realIntakeArtifacts.classification?.case_cause_name ?? "待运行"],
                ["case_cause_code", realIntakeArtifacts.classification?.case_cause_code ?? "pending"],
                ["case_cause_path", joinList(realIntakeArtifacts.classification?.case_cause_path)],
                ["confidence_score", realIntakeArtifacts.classification?.confidence_score ?? "pending"],
                ["manual_review_required", realIntakeArtifacts.classification?.manual_review_required ?? true]
              ]}
            />
          </Panel>
          <Panel title="v7.31a Training Sample Segments">
            <InfoRows
              rows={[
                ["segment_count", realIntakeArtifacts.segments?.segment_summary?.segment_count ?? 0],
                ["fact_segment_count", realIntakeArtifacts.segments?.segment_summary?.fact_segment_count ?? 0],
                ["legal_segment_count", realIntakeArtifacts.segments?.segment_summary?.legal_segment_count ?? 0],
                ["metadata_only", realIntakeArtifacts.segments?.metadata_only ?? true],
                ["raw_content_included", realIntakeArtifacts.segments?.raw_content_included ?? false]
              ]}
            />
          </Panel>
        </section>

        <Panel title="v7.31a Review / Source Trace / Audit / Safety">
          <div className="grid gap-4 lg:grid-cols-4">
            <Info title="Review Items" items={(realIntakeArtifacts.reviewQueue?.review_items ?? []).map((item: any) => item.review_type)} />
            <Info title="Source Traces" items={(realIntakeArtifacts.sourceTraces?.source_traces ?? []).map((item: any) => item.source_type)} />
            <Info title="Audit Events" items={(realIntakeArtifacts.audit?.events ?? []).map((item: any) => item.action)} />
            <Info title="Safety" items={realIntakeArtifacts.safety?.safety_checklist ?? ["不读取原文", "不调用 provider", "不写训练集"]} />
          </div>
        </Panel>

        <Panel title="v7.31b 受控解析 / OCR 文档解析 / 法律检索 / 经验候选">
          <div className="grid gap-4 md:grid-cols-5">
            <StatusCard label="Boundary" value={String(data.rawBoundaryStatus?.boundary_runtime_ready ?? true)} detail="受控内部处理" tone="safe" />
            <StatusCard label="OCR Jobs" value={data.ocrJobs?.job_count ?? data.v731bStatus?.ocr_job_count ?? 0} detail="demo-safe metadata" tone="info" />
            <StatusCard label="Legal Retrieval" value={data.legalRetrievalJobs?.job_count ?? data.v731bStatus?.legal_retrieval_job_count ?? 0} detail="reference metadata" tone="info" />
            <StatusCard label="Candidates" value={data.experienceCandidates?.candidate_count ?? data.v731bStatus?.experience_candidate_count ?? 0} detail="requires redaction/review" tone="info" />
            <StatusCard label="Approved" value={data.experienceCandidates?.approved_for_skill_experience_count ?? 0} detail="only later pool-ready" tone="safe" />
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void runExperiencePipeline()}>
              创建 OCR/检索/经验候选
            </button>
            <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void approveFirstExperienceCandidate()}>
              脱敏并复核首个候选
            </button>
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <Info title="OCR Job" items={[
              experiencePipelineResult.ocrJob?.job_id ?? data.ocrJobs?.ocr_jobs?.[0]?.job_id ?? "暂无 OCR job",
              experiencePipelineResult.ocrJob?.parse_status ?? data.ocrJobs?.ocr_jobs?.[0]?.parse_status ?? "pending"
            ]} />
            <Info title="Legal Retrieval" items={[
              experiencePipelineResult.legalRetrievalJob?.retrieval_job_id ?? data.legalRetrievalJobs?.legal_retrieval_jobs?.[0]?.retrieval_job_id ?? "暂无 retrieval job",
              experiencePipelineResult.legalRetrievalJob?.retrieval_status ?? data.legalRetrievalJobs?.legal_retrieval_jobs?.[0]?.retrieval_status ?? "pending"
            ]} />
            <Info title="Experience Candidates" items={(experiencePipelineResult.candidates?.candidates ?? data.experienceCandidates?.candidates ?? []).slice(0, 8).map((item: any) => `${item.candidate_type}: ${item.review_status}`)} />
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <InfoRows
              rows={[
                ["redaction_status", experiencePipelineResult.redaction?.redaction_status ?? "pending"],
                ["review_status", experiencePipelineResult.review?.review?.review_status ?? "pending_review"],
                ["approved_for_skill_experience", experiencePipelineResult.review?.review?.approved_for_skill_experience ?? false],
                ["audit_event_count", experiencePipelineResult.audit?.event_count ?? 0],
                ["provider_call_executed", data.v731bStatus?.provider_call_executed ?? false],
                ["skill_published", data.v731bStatus?.skill_published ?? false]
              ]}
            />
            <Info title="Source Trace Summary" items={(data.experienceCandidates?.candidates ?? []).slice(0, 8).map((item: any) => item.source_trace_id)} />
            <Info title="Audit Summary" items={(experiencePipelineResult.audit?.events ?? []).map((item: any) => item.action)} />
          </div>
        </Panel>

        <Panel title="v7.31c Skill Experience Pool / Codex Skill 草案生成">
          <div className="grid gap-4 md:grid-cols-5">
            <StatusCard label="Pool" value={data.skillExperiencePoolStatus?.experience_count ?? data.v731cStatus?.experience_count ?? 0} detail="approved experience only" tone="safe" />
            <StatusCard label="Unbound" value={data.skillExperiencePoolStatus?.unbound_experience_count ?? 0} detail="等待绑定" tone="info" />
            <StatusCard label="Bindings" value={data.skillExperienceBindings?.binding_count ?? data.v731cStatus?.binding_count ?? 0} detail="draft target" tone="info" />
            <StatusCard label="Drafts" value={data.skillDrafts?.draft_count ?? data.v731cStatus?.draft_count ?? 0} detail="manual confirmation" tone="info" />
            <StatusCard label="Publish" value={String(skillDraftResult?.draft?.skill_published ?? false)} detail="not publishable" tone="safe" />
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void importAndBindExperience()}>
              导入已批准经验并绑定
            </button>
            <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void buildSkillDraft()}>
              生成待确认 Skill 草案
            </button>
            <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void reviewSkillDraft("approve_draft_structure")}>
              确认草案结构
            </button>
            <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void reviewSkillDraft("request_changes")}>
              请求修改草案
            </button>
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <Info title="Pool Entries" items={(skillExperienceResult.imported?.imported_experiences ?? data.skillExperiencePool?.experiences ?? []).slice(0, 8).map((entry: any) => `${entry.experience_id}: ${entry.skill_binding_status}`)} />
            <Info title="Binding" items={[
              skillExperienceResult.binding?.binding_id ?? data.skillExperienceBindings?.bindings?.[0]?.binding_id ?? "暂无 binding",
              skillExperienceResult.binding?.binding_status ?? data.skillExperienceBindings?.bindings?.[0]?.binding_status ?? "pending"
            ]} />
            <Info title="Draft Detail" items={[
              skillDraftResult?.draft?.draft_id ?? data.skillDrafts?.drafts?.[0]?.draft_id ?? "暂无 draft",
              skillDraftResult?.draft?.confirmation_status ?? data.skillDrafts?.drafts?.[0]?.confirmation_status ?? "pending_confirmation",
              skillDraftResult?.draft?.publish_status ?? data.skillDrafts?.drafts?.[0]?.publish_status ?? "not_publishable"
            ]} />
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <InfoRows
              rows={[
                ["included_experience_count", skillDraftResult?.included_experience_count ?? 0],
                ["source_trace_count", skillDraftResult?.draft?.source_trace_ids?.length ?? 0],
                ["audit_event_count", skillDraftArtifacts.audit?.event_count ?? skillDraftResult?.draft?.audit_events?.length ?? 0],
                ["confirmation_status", skillDraftArtifacts.review?.review?.confirmation_status ?? skillDraftResult?.draft?.confirmation_status ?? "pending_confirmation"],
                ["skill_publishable", skillDraftResult?.draft?.skill_publishable ?? false],
                ["real_codex_training_triggered", skillDraftResult?.draft?.real_codex_training_triggered ?? false]
              ]}
            />
            <Info title="Draft Sections" items={(skillDraftResult?.draft?.sections ?? data.skillDrafts?.drafts?.[0]?.sections ?? []).map((item: any) => item.section_type)} />
            <Info title="Audit Summary" items={(skillDraftArtifacts.audit?.events ?? skillDraftResult?.draft?.audit_events ?? []).map((item: any) => item.action)} />
          </div>
        </Panel>

        <Panel title="v7.31d Skill Package 版本化封装 / System Validation Gate">
          <div className="grid gap-4 md:grid-cols-5">
            <StatusCard label="Packages" value={data.skillPackages?.package_count ?? data.v731dStatus?.package_count ?? 0} detail="versioned metadata" tone="info" />
            <StatusCard label="Validated" value={data.skillPackages?.system_validated_count ?? data.v731dStatus?.system_validated_count ?? 0} detail="system gate only" tone="safe" />
            <StatusCard label="Gate" value={skillPackageArtifacts.validation?.pre_publish_gate_status ?? skillPackageResult?.skill_package?.pre_publish_gate_status ?? data.skillPackages?.skill_packages?.[0]?.pre_publish_gate_status ?? "draft_package"} detail="pre-publish validation" tone="info" />
            <StatusCard label="Final Review" value={skillPackageResult?.skill_package?.final_review_status ?? data.v731dStatus?.final_review_status ?? "not_applicable"} detail="v7.31f 前才人工复核加载" tone="safe" />
            <StatusCard label="Skill Publish" value={String(data.v731dStatus?.skill_published ?? false)} detail="not publishable" tone="safe" />
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void buildSkillPackage()}>
              封装 v7.31d Skill Package
            </button>
            <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void validateSkillPackage()}>
              执行 System Validation Gate
            </button>
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <Info title="Package Detail" items={[
              skillPackageResult?.skill_package?.package_id ?? data.skillPackages?.skill_packages?.[0]?.package_id ?? "暂无 package",
              skillPackageResult?.skill_package?.package_version ?? data.skillPackages?.skill_packages?.[0]?.package_version ?? "pending",
              skillPackageArtifacts.validation?.package_status ?? skillPackageResult?.skill_package?.package_status ?? data.skillPackages?.skill_packages?.[0]?.package_status ?? "draft_package"
            ]} />
            <Info title="Manifest" items={[
              skillPackageArtifacts.manifest?.manifest_id ?? skillPackageResult?.skill_package?.manifest_id ?? data.skillPackages?.skill_packages?.[0]?.manifest_id ?? "暂无 manifest",
              `section_count=${skillPackageArtifacts.manifest?.section_count ?? skillPackageResult?.skill_package?.manifest?.section_count ?? 0}`,
              `experience_count=${skillPackageArtifacts.manifest?.experience_count ?? skillPackageResult?.skill_package?.experience_count ?? 0}`
            ]} />
            <Info title="Source Trace / Audit" items={[
              `source_trace_count=${skillPackageArtifacts.sourceTrace?.source_trace_ids?.length ?? skillPackageResult?.skill_package?.source_trace_bundle?.source_trace_ids?.length ?? 0}`,
              `audit_event_count=${skillPackageArtifacts.audit?.event_count ?? skillPackageResult?.skill_package?.audit_events?.length ?? 0}`,
              skillPackageArtifacts.sourceTrace?.trace_status ?? skillPackageResult?.skill_package?.source_trace_bundle?.trace_status ?? "pending"
            ]} />
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <InfoRows
              rows={[
                ["all_experiences_redacted", skillPackageArtifacts.validation?.validation_result?.all_experiences_redacted ?? "pending"],
                ["all_experiences_approved", skillPackageArtifacts.validation?.validation_result?.all_experiences_approved ?? "pending"],
                ["all_source_traces_present", skillPackageArtifacts.validation?.validation_result?.all_source_traces_present ?? "pending"],
                ["audit_complete", skillPackageArtifacts.validation?.validation_result?.audit_complete ?? "pending"],
                ["draft_structure_confirmed", skillPackageArtifacts.validation?.validation_result?.draft_structure_confirmed ?? "pending"],
                ["sensitive_field_scan_passed", skillPackageArtifacts.validation?.validation_result?.sensitive_field_scan_passed ?? "pending"],
                ["ready_for_training_package_build", skillPackageArtifacts.validation?.validation_result?.ready_for_training_package_build ?? false],
                ["real_codex_training_triggered", data.v731dStatus?.real_codex_training_triggered ?? false],
                ["provider_call_executed", data.v731dStatus?.provider_call_executed ?? false]
              ]}
            />
            <Info title="Package List" items={(data.skillPackages?.skill_packages ?? []).slice(0, 8).map((item: any) => `${item.package_id}: ${item.pre_publish_gate_status}`)} />
            <Info title="Validation Warnings" items={skillPackageArtifacts.validation?.warnings ?? data.v731dStatus?.warnings ?? ["系统校验仅处理 metadata，不触发人工加载复核"]} />
          </div>
        </Panel>

        <Panel title="v7.31e Internal Training / Experience Package Builder">
          <div className="grid gap-4 md:grid-cols-5">
            <StatusCard label="Training Tasks" value={data.trainingTasks?.task_count ?? data.v731eStatus?.training_task_count ?? 0} detail="system_validated package only" tone="info" />
            <StatusCard label="Training Packages" value={data.trainingPackages?.package_count ?? data.v731eStatus?.training_package_count ?? 0} detail="structured metadata" tone="info" />
            <StatusCard label="Practice Review" value={data.trainingPackages?.pending_practice_load_review_count ?? data.v731eStatus?.pending_practice_load_review_count ?? 0} detail="pending v7.31f load review" tone="safe" />
            <StatusCard label="Provider Call" value={String(data.v731eStatus?.provider_call_executed ?? false)} detail="provider_call_executed=false" tone="safe" />
            <StatusCard label="Skill Publish" value={String(data.v731eStatus?.skill_published ?? false)} detail="skill_published=false" tone="safe" />
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void buildTrainingTask()}>
              构建内部训练任务
            </button>
            <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void buildTrainingPackage()}>
              构建内部训练经验包
            </button>
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <Info title="Training Task" items={[
              trainingTaskResult?.training_task?.training_task_id ?? data.trainingTasks?.training_tasks?.[0]?.training_task_id ?? "暂无 training task",
              trainingTaskResult?.training_task?.training_task_status ?? data.trainingTasks?.training_tasks?.[0]?.training_task_status ?? "pending",
              `sample_count=${trainingTaskResult?.training_task?.sample_count ?? data.trainingTasks?.training_tasks?.[0]?.sample_count ?? 0}`
            ]} />
            <Info title="Experience Package" items={[
              trainingPackageResult?.training_package?.package_id ?? data.trainingPackages?.training_packages?.[0]?.package_id ?? "暂无 training package",
              trainingPackageResult?.training_package?.package_status ?? data.trainingPackages?.training_packages?.[0]?.package_status ?? "pending_practice_load_review",
              trainingPackageResult?.training_package?.build_status ?? data.trainingPackages?.training_packages?.[0]?.build_status ?? "pending"
            ]} />
            <Info title="Prompt / IO Pair" items={[
              trainingTaskResult?.training_task?.samples?.[0]?.prompt_template ?? data.trainingTasks?.training_tasks?.[0]?.samples?.[0]?.prompt_template ?? "暂无 prompt metadata",
              trainingTaskResult?.training_task?.samples?.[0]?.input_output_pair_id ?? data.trainingTasks?.training_tasks?.[0]?.samples?.[0]?.input_output_pair_id ?? "暂无 pair",
              `source_experience=${trainingTaskResult?.training_task?.samples?.[0]?.source_experience_id ?? data.trainingTasks?.training_tasks?.[0]?.samples?.[0]?.source_experience_id ?? "pending"}`
            ]} />
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <InfoRows
              rows={[
                ["training_task_status", trainingTaskResult?.training_task?.training_task_status ?? data.trainingTasks?.training_tasks?.[0]?.training_task_status ?? "pending"],
                ["build_status", trainingPackageResult?.training_package?.build_status ?? data.trainingPackages?.training_packages?.[0]?.build_status ?? "pending"],
                ["package_status", trainingPackageResult?.training_package?.package_status ?? data.trainingPackages?.training_packages?.[0]?.package_status ?? "pending_practice_load_review"],
                ["practice_load_review_status", data.v731eStatus?.practice_load_review_status ?? "pending_practice_load_review"],
                ["training_output_manual_review_status", data.v731eStatus?.training_output_manual_review_status ?? "not_applicable"],
                ["provider_call_executed", data.v731eStatus?.provider_call_executed ?? false],
                ["real_codex_training_triggered", data.v731eStatus?.real_codex_training_triggered ?? false],
                ["formal_training_set_written", data.v731eStatus?.formal_training_set_written ?? false],
                ["skill_published", data.v731eStatus?.skill_published ?? false],
                ["final_report_generated", data.v731eStatus?.final_report_generated ?? false],
                ["external_delivery_triggered", data.v731eStatus?.external_delivery_triggered ?? false]
              ]}
            />
            <Info title="Audit Summary" items={(trainingPackageArtifacts.audit?.events ?? trainingPackageResult?.training_package?.audit_events ?? data.trainingPackages?.training_packages?.[0]?.audit_events ?? []).map((item: any) => item.action)} />
            <Info title="Source Trace" items={[
              trainingPackageArtifacts.sourceTrace?.source_trace_bundle_id ?? trainingPackageResult?.training_package?.source_trace_bundle_id ?? data.trainingPackages?.training_packages?.[0]?.source_trace_bundle_id ?? "暂无 source trace bundle",
              `trace_count=${trainingPackageArtifacts.sourceTrace?.trace_count ?? trainingPackageResult?.training_package?.source_trace_bundle?.trace_count ?? data.trainingPackages?.training_packages?.[0]?.source_trace_bundle?.trace_count ?? 0}`,
              trainingPackageArtifacts.sourceTrace?.trace_status ?? trainingPackageResult?.training_package?.source_trace_bundle?.trace_status ?? "pending"
            ]} />
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-2">
            <Info title="Training Task List" items={(data.trainingTasks?.training_tasks ?? []).slice(0, 8).map((item: any) => `${item.training_task_id}: ${item.training_task_status}`)} />
            <Info title="Training Package List" items={(data.trainingPackages?.training_packages ?? []).slice(0, 8).map((item: any) => `${item.package_id}: ${item.package_status}`)} />
          </div>
        </Panel>

        <Panel title="v7.31f Practice Runtime Load Review Gate / 律师经验编辑器">
          <div className="grid gap-4 md:grid-cols-5">
            <StatusCard label="Review Packages" value={data.practiceLoadPackages?.package_count ?? data.v731fStatus?.package_count ?? 0} detail="pending practice load review" tone="info" />
            <StatusCard label="Pending Review" value={data.practiceLoadPackages?.pending_practice_load_review_count ?? data.v731fStatus?.pending_practice_load_review_count ?? 0} detail="lawyer review gate" tone="warning" />
            <StatusCard label="Revalidated" value={data.v731fStatus?.system_revalidated_count ?? 0} detail="system revalidation" tone="safe" />
            <StatusCard label="Approved" value={data.v731fStatus?.approved_for_practice_load_count ?? 0} detail="load candidate only" tone="safe" />
            <StatusCard label="Runtime Loaded" value={String(false)} detail="v7.31f 不执行加载" tone="safe" />
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void editPracticeLoadPackage()}>
              进入律师编辑
            </button>
            <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void savePracticeLoadEdits()}>
              保存律师修改
            </button>
            <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void revalidatePracticeLoad()}>
              系统重新校验
            </button>
            <button type="button" className="rounded-md border border-emerald-300 px-4 py-2 text-sm font-semibold text-emerald-800" onClick={() => void approvePracticeLoad()}>
              批准加载候选
            </button>
            <button type="button" className="rounded-md border border-rose-300 px-4 py-2 text-sm font-semibold text-rose-800" onClick={() => void rejectPracticeLoad()}>
              拒绝加载
            </button>
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <Info title="Review Package" items={[
              practiceLoadResult?.package_id ?? data.practiceLoadPackages?.packages?.[0]?.package_id ?? "暂无 practice load review package",
              practiceLoadResult?.review_status ?? data.practiceLoadPackages?.packages?.[0]?.review_status ?? "pending_practice_load_review",
              practiceLoadResult?.validation_status ?? data.practiceLoadPackages?.packages?.[0]?.validation_status ?? "system_revalidation_required"
            ]} />
            <Info title="Generated Experience Package" items={[
              `source_training_package=${practiceLoadResult?.generated_experience_package?.source_training_package_id ?? data.practiceLoadPackages?.packages?.[0]?.generated_experience_package?.source_training_package_id ?? "pending"}`,
              `generated_package_preserved=${String(practiceLoadResult?.generated_experience_package?.generated_package_preserved ?? data.practiceLoadPackages?.packages?.[0]?.generated_experience_package?.generated_package_preserved ?? true)}`,
              `metadata_only=${String(practiceLoadResult?.generated_experience_package?.metadata_only ?? data.practiceLoadPackages?.packages?.[0]?.generated_experience_package?.metadata_only ?? true)}`
            ]} />
            <Info title="Lawyer Approved Package" items={[
              `approved_card_count=${practiceLoadResult?.lawyer_approved_experience_package?.approved_card_count ?? data.practiceLoadPackages?.packages?.[0]?.lawyer_approved_experience_package?.approved_card_count ?? 0}`,
              `gray_load_enabled=${String(practiceLoadResult?.gray_load_enabled ?? data.practiceLoadPackages?.packages?.[0]?.gray_load_enabled ?? false)}`,
              `can_load_to_practice_runtime=${String(practiceLoadResult?.can_load_to_practice_runtime ?? data.practiceLoadPackages?.packages?.[0]?.can_load_to_practice_runtime ?? false)}`
            ]} />
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-2">
            <Info
              title="AI 生成经验"
              items={(practiceLoadResult?.experience_cards ?? data.practiceLoadPackages?.packages?.[0]?.experience_cards ?? []).slice(0, 3).map((card: any) => `${card.title}: ${card.generated_experience_text}`)}
            />
            <Info
              title="律师编辑经验"
              items={(practiceLoadResult?.experience_cards ?? data.practiceLoadPackages?.packages?.[0]?.experience_cards ?? []).slice(0, 3).map((card: any) => `${card.title}: ${card.lawyer_experience_text}`)}
            />
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <InfoRows
              rows={[
                ["review_status", practiceLoadResult?.review_status ?? data.practiceLoadPackages?.packages?.[0]?.review_status ?? "pending_practice_load_review"],
                ["load_gate_status", practiceLoadResult?.load_gate_status ?? data.practiceLoadPackages?.packages?.[0]?.load_gate_status ?? "pending_practice_load_review"],
                ["validation_status", practiceLoadResult?.validation_status ?? data.practiceLoadPackages?.packages?.[0]?.validation_status ?? "system_revalidation_required"],
                ["revalidation_passed", practiceLoadResult?.revalidation_result?.revalidation_passed ?? false],
                ["sensitive_field_scan_passed", practiceLoadResult?.revalidation_result?.sensitive_field_scan_passed ?? false],
                ["source_trace_complete", practiceLoadResult?.revalidation_result?.source_trace_complete ?? false],
                ["audit_complete", practiceLoadResult?.revalidation_result?.audit_complete ?? false],
                ["provider_call_executed", data.v731fStatus?.provider_call_executed ?? false],
                ["real_codex_training_triggered", data.v731fStatus?.real_codex_training_triggered ?? false],
                ["skill_published", data.v731fStatus?.skill_published ?? false],
                ["external_delivery_triggered", data.v731fStatus?.external_delivery_triggered ?? false]
              ]}
            />
            <Info title="Risk / Boundary" items={(practiceLoadResult?.experience_cards ?? data.practiceLoadPackages?.packages?.[0]?.experience_cards ?? []).flatMap((card: any) => [...(card.risk_warnings ?? []), ...(card.usage_boundaries ?? [])]).slice(0, 8)} />
            <Info title="Audit / Source Trace" items={[
              `audit_event_count=${practiceLoadArtifacts.audit?.event_count ?? practiceLoadResult?.audit_events?.length ?? data.practiceLoadPackages?.packages?.[0]?.audit_events?.length ?? 0}`,
              `trace_count=${practiceLoadArtifacts.sourceTrace?.trace_count ?? practiceLoadResult?.source_trace_bundle?.trace_count ?? data.practiceLoadPackages?.packages?.[0]?.source_trace_bundle?.trace_count ?? 0}`,
              practiceLoadArtifacts.sourceTrace?.trace_status ?? practiceLoadResult?.source_trace_bundle?.trace_status ?? "pending"
            ]} />
          </div>
          <div className="mt-4 rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-xs leading-5 text-amber-900">
            v7.31f 只完成实战加载前的律师复核与编辑，不执行真实加载；v7.31g 才进入受控加载与监控。
          </div>
        </Panel>

        <Panel title="v7.32 Experience Lifecycle OS / 实战经验包全生命周期总览">
          <div className="grid gap-4 md:grid-cols-6">
            <StatusCard label="Lifecycles" value={data.v732Status?.lifecycle_count ?? data.experienceLifecycles?.lifecycle_count ?? 0} detail="consolidated metadata" tone="info" />
            <StatusCard label="Stage Events" value={data.v732Status?.stage_event_count ?? lifecycleEvents.length} detail="v7.31b-v7.31j" tone="info" />
            <StatusCard label="Current Stage" value={lifecycle?.current_stage ?? "pending"} detail={lifecycle?.current_status ?? "not_started"} tone="safe" />
            <StatusCard label="Integrity" value={experienceLifecycleArtifacts.integrityCheck?.status ?? "pending"} detail="reference check" tone="safe" />
            <StatusCard label="Next Draft" value={lifecycle?.latest_next_package_draft_id ?? "暂无"} detail="not auto-loaded" tone="warning" />
            <StatusCard label="Runtime Loads" value={lifecycle?.runtime_load_ids?.length ?? 0} detail="lawyer-approved only" tone="safe" />
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void recomputeExperienceLifecycleView()}>
              重新计算生命周期
            </button>
            <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void refreshExperienceLifecycle()}>
              刷新生命周期视图
            </button>
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
            <div className="rounded-md border border-line bg-white">
              <div className="grid grid-cols-[1fr_0.8fr_0.8fr] gap-2 border-b border-line px-3 py-2 text-xs font-semibold text-muted">
                <span>Stage</span>
                <span>Status</span>
                <span>Linked Object</span>
              </div>
              <div className="max-h-72 overflow-auto">
                {lifecycleEvents.slice(0, 12).map((event: any) => (
                  <div key={event.stage_event_id} className="grid grid-cols-[1fr_0.8fr_0.8fr] gap-2 border-b border-slate-100 px-3 py-2 text-xs">
                    <span className="font-medium text-ink">{event.stage_name}</span>
                    <span className="text-muted">{event.stage_status}</span>
                    <span className="truncate text-muted">{event.linked_object_type}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="grid gap-4">
              <Info title="Graph / Lineage" items={[
                `nodes=${experienceLifecycleArtifacts.graph?.nodes?.length ?? 0}`,
                `edges=${experienceLifecycleArtifacts.graph?.edges?.length ?? 0}`,
                `lineage=${experienceLifecycleArtifacts.graph?.lineage?.length ?? 0}`
              ]} />
              <Info title="Audit / Trace / Safety" items={[
                `audit_events=${experienceLifecycleArtifacts.auditTimeline?.events_count ?? 0}`,
                `trace_warnings=${experienceLifecycleArtifacts.sourceTraceView?.missing_trace_warnings?.length ?? 0}`,
                `safety=${experienceLifecycleArtifacts.safetySummary?.overall_safety_status ?? "pending"}`
              ]} />
            </div>
          </div>
          <div className="mt-4 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
            v7.32 只汇总生命周期 metadata，不处理来源材料、不自动修改已加载包、不自动加载下一版、不触发训练、不调用 provider、不读取 key value；实战经验仅辅助律师判断，不替代律师判断。
          </div>
        </Panel>

        <Panel title="v7.33 Case Analysis Skill Output Schema Driven Workbench / 案件分析实战工作台">
          <div className="grid gap-4 md:grid-cols-6">
            <StatusCard label="Case" value={workbenchView?.case_id ?? "pending"} detail={workbenchView?.case_cause_name ?? "schema view"} tone="info" />
            <StatusCard label="Skill" value={workbenchView?.skill_name ?? "pending"} detail={workbenchView?.skill_version ?? "v7.33"} tone="info" />
            <StatusCard label="Package" value={workbenchView?.package_version ?? "pending"} detail={workbenchView?.runtime_load_status ?? "runtime"} tone="safe" />
            <StatusCard label="Outputs" value={workbenchView?.summary_metrics?.total_outputs ?? data.v733Status?.output_count ?? 0} detail="schema-defined" tone="info" />
            <StatusCard label="Feedback" value={workbenchView?.summary_metrics?.feedback_count ?? data.v733Status?.feedback_count ?? 0} detail="metadata only" tone="warning" />
            <StatusCard label="Risk" value={workbenchView?.summary_metrics?.risk_flagged_count ?? 0} detail="lawyer review" tone="warning" />
          </div>

          <div className="mt-4 grid gap-3 rounded-md border border-line bg-slate-50 p-3 md:grid-cols-6">
            <Select label="output_group" value={workbenchFilter.group} onChange={(value) => setWorkbenchFilter((current) => ({ ...current, group: value }))} options={["all", ...schemaGroups.map((group: any) => group.group_id)]} />
            <Select label="output_type" value={workbenchFilter.type} onChange={(value) => setWorkbenchFilter((current) => ({ ...current, type: value }))} options={["all", ...outputTypes]} />
            <Select label="risk_level" value={workbenchFilter.risk} onChange={(value) => setWorkbenchFilter((current) => ({ ...current, risk: value }))} options={["all", "none", "low", "medium", "high"]} />
            <Select label="status" value={workbenchFilter.status} onChange={(value) => setWorkbenchFilter((current) => ({ ...current, status: value }))} options={["all", "generated", "visible", "reviewed", "feedback_submitted", "risk_flagged", "blocked"]} />
            <Select label="feedback" value={workbenchFilter.feedback} onChange={(value) => setWorkbenchFilter((current) => ({ ...current, feedback: value }))} options={["all", "has_feedback", "no_feedback"]} />
            <Text label="keyword" value={workbenchFilter.keyword} onChange={(value) => setWorkbenchFilter((current) => ({ ...current, keyword: value }))} />
          </div>

          <div className="mt-4 grid gap-4 xl:grid-cols-[1.25fr_0.75fr]">
            <div className="space-y-4">
              {schemaGroups.map((group: any) => {
                const groupOutputs = filteredWorkbenchOutputs.filter((output: any) => output.group_id === group.group_id);
                return (
                  <div key={group.group_id} className="rounded-md border border-line bg-white p-4">
                    <div className="flex flex-wrap items-start justify-between gap-3">
                      <div>
                        <div className="text-base font-semibold text-ink">{group.group_title}</div>
                        <div className="mt-1 text-xs text-muted">{group.description}</div>
                      </div>
                      <span className="rounded-md border border-slate-200 bg-slate-50 px-2 py-1 text-xs text-muted">
                        {group.actual_count} / {group.expected_count}
                      </span>
                    </div>
                    <div className="mt-3 grid gap-3">
                      {groupOutputs.map((output: any) => (
                        <button
                          key={output.output_id}
                          type="button"
                          className={`rounded-md border p-3 text-left transition ${selectedWorkbenchOutputId === output.output_id ? "border-cyan-400 bg-cyan-50" : "border-line bg-slate-50 hover:border-slate-300"}`}
                          onClick={() => void selectWorkbenchOutput(output.output_id)}
                        >
                          <div className="flex flex-wrap items-start justify-between gap-3">
                            <div>
                              <div className="text-sm font-semibold text-ink">{output.output_order}. {output.output_title}</div>
                              <div className="mt-1 text-xs text-muted">{output.output_type}</div>
                            </div>
                            <div className="flex flex-wrap gap-1">
                              <span className="rounded-md border border-line bg-white px-2 py-1 text-xs text-muted">{output.risk_level}</span>
                              <span className="rounded-md border border-line bg-white px-2 py-1 text-xs text-muted">{output.output_status}</span>
                            </div>
                          </div>
                          <div className="mt-2 text-xs leading-5 text-muted">{output.output_summary_redacted}</div>
                          <div className="mt-2 text-xs text-muted">feedback={output.feedback_count} · risk={output.risk_event_count} · actions={joinList(output.allowed_actions)}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="rounded-md border border-line bg-white p-4">
              <div className="text-sm font-semibold text-ink">{caseWorkbenchArtifacts.selectedOutput?.output_title ?? "选择一条 schema output"}</div>
              <div className="mt-1 text-xs text-muted">{caseWorkbenchArtifacts.selectedOutput?.output_type ?? "output detail panel"}</div>
              <div className="mt-4 rounded-md bg-slate-50 p-3 text-xs leading-5 text-muted">
                {caseWorkbenchArtifacts.selectedOutput?.output_detail_redacted ?? "详情面板只展示后端 schema output 的脱敏摘要。"}
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                <button type="button" className="rounded-md bg-slate-900 px-3 py-2 text-xs font-semibold text-white" onClick={() => void markWorkbenchOutputReviewed()}>
                  标记已复核
                </button>
                <button type="button" className="rounded-md border border-line px-3 py-2 text-xs font-semibold text-ink" onClick={() => void submitWorkbenchFeedback()}>
                  提交反馈
                </button>
                <button type="button" className="rounded-md border border-amber-300 px-3 py-2 text-xs font-semibold text-amber-800" onClick={() => void submitWorkbenchRiskEvent()}>
                  创建风险事件
                </button>
                <button type="button" className="rounded-md border border-line px-3 py-2 text-xs font-semibold text-ink" onClick={() => void refreshCaseWorkbench()}>
                  刷新工作台
                </button>
              </div>
              <div className="mt-4 grid gap-3">
                <Info title="Source / Runtime" items={[
                  `runtime_load=${caseWorkbenchArtifacts.selectedOutput?.source_runtime_load_id ?? "pending"}`,
                  `source_experience=${joinList(caseWorkbenchArtifacts.selectedOutput?.source_experience_ids)}`,
                  `confidence=${caseWorkbenchArtifacts.selectedOutput?.confidence_label ?? "schema"}`
                ]} />
                <Info title="Feedback / Risk" items={[
                  `feedback_count=${caseWorkbenchArtifacts.feedback?.feedback_count ?? caseWorkbenchArtifacts.selectedOutput?.feedback_count ?? 0}`,
                  `risk_event_count=${caseWorkbenchArtifacts.riskEvents?.risk_event_count ?? caseWorkbenchArtifacts.selectedOutput?.risk_event_count ?? 0}`,
                  `latest_feedback=${caseWorkbenchArtifacts.feedback?.feedback?.[0]?.feedback_summary ?? "暂无反馈"}`
                ]} />
                <Info title="Audit / Source Trace" items={[
                  `audit_events=${caseWorkbenchArtifacts.audit?.event_count ?? 0}`,
                  `trace_status=${caseWorkbenchArtifacts.sourceTrace?.trace_status ?? "pending"}`,
                  ...(caseWorkbenchArtifacts.sourceTrace?.trace_summary ?? []).slice(0, 2)
                ]} />
              </div>
            </div>
          </div>

          <div className="mt-4 rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-xs leading-5 text-amber-900">
            v7.33 前端只把后端 Skill Output Schema 可视化，不自行定义产出名称、类型、数量或分组；本阶段不处理原始案件材料、不调用 provider、不读取 key value、不生成最终法律意见或正式报告。
          </div>
        </Panel>

        <Panel title="Training Scheme / 训练方案">
          <div className="grid gap-4 lg:grid-cols-3">
            <Info title="目标 Skill" items={data.scheme?.target_skill_ids ?? []} />
            <Info title="训练步骤" items={data.scheme?.training_steps ?? []} />
            <Info title="输出产物" items={data.scheme?.output_artifacts ?? []} />
          </div>
          <div className="mt-4">
            <InfoRows
              rows={[
                ["scheme_id", data.scheme?.scheme_id ?? "codex_training_scheme_v7_30"],
                ["fine_tune_model_training", data.scheme?.fine_tune_model_training ?? false],
                ["closed_case_only", data.scheme?.closed_case_only ?? true],
                ["open_case_data_used", data.scheme?.open_case_data_used ?? false],
                ["raw_content_included", data.scheme?.raw_content_included ?? false]
              ]}
            />
          </div>
        </Panel>

        <section className="grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
          <Panel title="Case Cause Taxonomy / 多层级案由">
            <div className="grid gap-3">
              {taxonomyNodes.slice(0, 10).map((node) => (
                <div key={node.case_cause_id} className="rounded-md border border-line bg-slate-50 p-3">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <div className="text-sm font-semibold text-ink">{node.case_cause_name}</div>
                      <div className="mt-1 text-xs text-muted">{node.case_cause_id} · level {node.level}</div>
                    </div>
                    <span className="rounded-md border border-cyan-200 bg-cyan-50 px-2 py-1 text-xs text-cyan-800">{node.case_cause_code}</span>
                  </div>
                  <div className="mt-2 text-xs text-muted">{node.case_cause_path.join(" / ")}</div>
                </div>
              ))}
            </div>
          </Panel>

          <Panel title="Case Cause Match Mock / 案由匹配 dry-run">
            <div className="grid gap-3">
              <Text label="case_cause_path" value={pathText} onChange={setPathText} />
              <Text label="evidence_types" value={evidenceText} onChange={setEvidenceText} />
              <div className="flex flex-wrap gap-2">
                <button type="button" className="rounded-md border border-line px-4 py-2 text-sm font-semibold text-ink" onClick={() => void runMatch()}>
                  匹配案由包
                </button>
                <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void runDryRun()}>
                  生成 Skill Context dry-run
                </button>
              </div>
              <InfoRows
                rows={[
                  ["matched_case_cause_id", matchResult?.matched_case_cause_id ?? dryRun?.match_result?.matched_case_cause_id ?? "pending"],
                  ["selected_package_ids", joinList(matchResult?.selected_package_ids ?? dryRun?.match_result?.selected_package_ids)],
                  ["fallback_chain", joinList(matchResult?.fallback_chain ?? dryRun?.match_result?.fallback_chain)],
                  ["merge_order", joinList(matchResult?.merge_order ?? dryRun?.match_result?.merge_order)]
                ]}
              />
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Experience Package Manifest">
            <ArtifactCards artifacts={data.packages?.artifacts ?? []} fields={["package_type", "load_strategy", "case_cause_scope", "priority"]} />
          </Panel>
          <Panel title="Skill Manifest">
            <ArtifactCards artifacts={data.skills?.artifacts ?? []} titleField="skill_name" fields={["skill_id", "skill_type", "loading_status", "gate_id"]} />
          </Panel>
          <Panel title="Evaluation / Gate / Test Cases">
            <Info title="Evaluations" items={(data.evaluations?.artifacts ?? []).map((item: any) => item.evaluation_id)} />
            <div className="mt-3">
              <Info title="Gates" items={(data.gates?.artifacts ?? []).map((item: any) => item.gate_id)} />
            </div>
            <div className="mt-3">
              <Info title="Test Cases" items={(data.testCases?.artifacts ?? []).map((item: any) => item.test_case_id)} />
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="v7.31 Case Cause Packages">
            <ArtifactCards artifacts={trainingRunResult?.experience_packages ?? data.trainingRuns?.training_runs?.[0]?.experience_packages ?? []} titleField="package_name" fields={["case_cause_scope", "load_strategy", "priority", "source_case_mode"]} />
          </Panel>
          <Panel title="v7.31 Generated Skill Artifacts">
            <ArtifactCards artifacts={trainingRunResult?.generated_skills ?? data.trainingRuns?.training_runs?.[0]?.generated_skills ?? []} titleField="skill_name" fields={["skill_id", "baseline_complete", "loading_status", "skill_published"]} />
          </Panel>
          <Panel title="v7.31 Evaluation / Gate / Tests">
            <Info title="Evaluations" items={(trainingRunResult?.evaluations ?? data.trainingRuns?.training_runs?.[0]?.evaluations ?? []).map((item: any) => item.evaluation_id)} />
            <div className="mt-3">
              <Info title="Gates" items={(trainingRunResult?.gates ?? data.trainingRuns?.training_runs?.[0]?.gates ?? []).map((item: any) => item.gate_id)} />
            </div>
            <div className="mt-3">
              <Info title="Test Cases" items={(trainingRunResult?.test_cases ?? data.trainingRuns?.training_runs?.[0]?.test_cases ?? []).map((item: any) => item.test_case_id)} />
            </div>
          </Panel>
        </section>

        <Panel title="v7.31 Loading Manifest / Dry-run">
          <InfoRows
            rows={[
              ["loading_manifest_id", trainingRunResult?.loading_manifest?.loading_manifest_id ?? data.trainingRuns?.training_runs?.[0]?.loading_manifest?.loading_manifest_id ?? "pending"],
              ["case_cause_match_strategy", trainingRunResult?.loading_manifest?.case_cause_match_strategy ?? data.trainingRuns?.training_runs?.[0]?.loading_manifest?.case_cause_match_strategy ?? "pending"],
              ["fallback_order", joinList(trainingRunResult?.loading_manifest?.fallback_order ?? data.trainingRuns?.training_runs?.[0]?.loading_manifest?.fallback_order)],
              ["conflict_resolution_policy", joinList(trainingRunResult?.loading_manifest?.conflict_resolution_policy ?? data.trainingRuns?.training_runs?.[0]?.loading_manifest?.conflict_resolution_policy)],
              ["load_executed", trainingRunLoadDryRun?.load_dry_run_result?.load_executed ?? false],
              ["skill_published", trainingRunResult?.skill_published ?? false]
            ]}
          />
        </Panel>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="Loading Manifest / Package Merge">
            <InfoRows
              rows={[
                ["supported_load_strategies", joinList(data.loadingManifests?.artifacts?.[0]?.supported_load_strategies)],
                ["merge_order", joinList(data.loadingManifests?.artifacts?.[0]?.merge_order)],
                ["conflict_resolution", joinList(data.loadingManifests?.artifacts?.[0]?.conflict_resolution)],
                ["dry_run_required", data.loadingManifests?.artifacts?.[0]?.dry_run_required ?? true]
              ]}
            />
          </Panel>
          <Panel title="Skill Context">
            <RuntimeCard
              title={dryRun?.skill_context?.skill_context_id ?? data.skillContexts?.skill_contexts?.[0]?.skill_context_id ?? "skill_context_preview"}
              category="case_fact_extraction_skill + case_legal_analysis_skill"
              status="dry-run metadata"
              items={[
                ["selected_skill_ids", joinList(dryRun?.skill_context?.selected_skill_ids ?? data.skillContexts?.skill_contexts?.[0]?.selected_skill_ids)],
                ["selected_package_ids", joinList(dryRun?.skill_context?.selected_package_ids ?? data.skillContexts?.skill_contexts?.[0]?.selected_package_ids)],
                ["fallback_chain", joinList(dryRun?.skill_context?.fallback_chain ?? data.skillContexts?.skill_contexts?.[0]?.fallback_chain)],
                ["load_executed", dryRun?.skill_context?.load_executed ?? false]
              ]}
            />
          </Panel>
        </section>

        <TrustSafetyPanel
          title="训练产物安全边界"
          note="v7.30-v7.31e 只处理合成或脱敏 metadata；不读取真实案件原文、不读取密钥、不调用 provider、不训练未结案件、不自动发布 Skill。"
          items={data.safety?.safety_checklist ?? []}
        />
        <DiagnosticsPanel data={{ matchResult, dryRun, trainingTaskResult, trainingPackageResult, practiceLoadResult, experienceLifecycleArtifacts, caseWorkbenchArtifacts, ...data }} />
      </div>
    </AppShell>
  );
}

function Panel({ title, children }: { title: string; children: ReactNode }) {
  return <section className="rounded-md border border-line bg-white p-5 shadow-sm"><h2 className="text-base font-semibold text-ink">{title}</h2><div className="mt-4">{children}</div></section>;
}

function Info({ title, items }: { title: string; items: unknown[] }) {
  const display = items.length ? items.slice(0, 8) : ["暂无 metadata"];
  return <div className="rounded-md border border-line bg-slate-50 p-4"><div className="text-sm font-semibold text-ink">{title}</div><div className="mt-3 grid gap-2 text-xs text-muted">{display.map((item, index) => <span key={`${String(item)}-${index}`}>{String(item)}</span>)}</div></div>;
}

function ArtifactCards({ artifacts, titleField = "package_name", fields }: { artifacts: Array<Record<string, any>>; titleField?: string; fields: string[] }) {
  return <div className="grid gap-3">{artifacts.slice(0, 5).map((artifact) => (
    <RuntimeCard
      key={String(artifact.package_id ?? artifact.skill_id ?? artifact.evaluation_id)}
      title={String(artifact[titleField] ?? artifact.package_id ?? artifact.skill_id)}
      category={String(artifact.package_id ?? artifact.skill_id ?? "manifest")}
      status={String(artifact.load_strategy ?? artifact.loading_status ?? "metadata")}
      items={fields.map((field) => [field, Array.isArray(artifact[field]) ? artifact[field].join(" / ") : artifact[field]])}
    />
  ))}</div>;
}

function Text({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return <label className="grid gap-2 text-sm"><span>{label}</span><input className="rounded-md border border-line px-3 py-2" value={value} onChange={(event) => onChange(event.target.value)} /></label>;
}

function Select({ label, value, onChange, options }: { label: string; value: string; onChange: (value: string) => void; options: string[] }) {
  return (
    <label className="grid gap-2 text-sm">
      <span>{label}</span>
      <select className="rounded-md border border-line bg-white px-3 py-2" value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => (
          <option key={option} value={option}>{option}</option>
        ))}
      </select>
    </label>
  );
}

function splitTokens(value: string) {
  return value.split("/").map((item) => item.trim()).filter(Boolean);
}

function joinList(value: unknown) {
  return Array.isArray(value) && value.length ? value.join(" / ") : "暂无";
}
