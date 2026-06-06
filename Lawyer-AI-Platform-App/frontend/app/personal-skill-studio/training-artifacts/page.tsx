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
  createPersonalLegalRetrievalJob,
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
  importPersonalApprovedSkillExperience,
  listPersonalExperienceCandidates,
  listPersonalLegalRetrievalJobs,
  listPersonalOcrJobs,
  listPersonalCodexTrainingRuns,
  listPersonalCodexSkillDrafts,
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
  reviewPersonalExperienceCandidate,
  reviewPersonalCodexSkillDraft
} from "@/services/api";
import type {
  CaseCauseNode,
  CodexSkillDraftBuildRequest,
  ExperienceCandidateBuildRequest,
  ExperienceCandidateReviewRequest,
  LegalRetrievalJobRequest,
  OcrJobRequest,
  RealClosedCaseTrainingIntakeRequest,
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
        skillDrafts
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
        listPersonalCodexSkillDrafts()
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
        skillDrafts
      });
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

  const taxonomyNodes = (data.taxonomy?.nodes ?? []) as CaseCauseNode[];

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
          note="v7.30 只加载合成 metadata；不读取真实案件、不读取密钥、不调用 provider、不训练未结案件、不自动发布 Skill。"
          items={data.safety?.safety_checklist ?? []}
        />
        <DiagnosticsPanel data={{ matchResult, dryRun, ...data }} />
      </div>
    </AppShell>
  );
}

function Panel({ title, children }: { title: string; children: ReactNode }) {
  return <section className="rounded-md border border-line bg-white p-5 shadow-sm"><h2 className="text-base font-semibold text-ink">{title}</h2><div className="mt-4">{children}</div></section>;
}

function Info({ title, items }: { title: string; items: unknown[] }) {
  const display = items.length ? items.slice(0, 8) : ["暂无 metadata"];
  return <div className="rounded-md border border-line bg-slate-50 p-4"><div className="text-sm font-semibold text-ink">{title}</div><div className="mt-3 grid gap-2 text-xs text-muted">{display.map((item) => <span key={String(item)}>{String(item)}</span>)}</div></div>;
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

function splitTokens(value: string) {
  return value.split("/").map((item) => item.trim()).filter(Boolean);
}

function joinList(value: unknown) {
  return Array.isArray(value) && value.length ? value.join(" / ") : "暂无";
}
