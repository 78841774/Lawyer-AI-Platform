import type {
  AuthStatus,
  Case,
  CaseSkillBinding,
  CaseCauseTaxonomyEntry,
  CitationResolutionResult,
  ControlledLawyerReviewActionRequest,
  ControlledLawyerReviewAuditLog,
  ControlledLawyerReviewRecord,
  ControlledLawyerReviewResult,
  ControlledLawyerReviewStatus,
  ControlledLawyerReviewSubmitRequest,
  ControlledLegalCitationResolutionRequest,
  ControlledLegalCitationResolutionResult,
  ControlledLegalSearchAuditLog,
  ControlledLegalSearchPreviewRecord,
  ControlledLegalSearchPreviewRequest,
  ControlledLegalSearchPreviewResult,
  ControlledLegalSearchStatus,
  ControlledReportDraftAssembleRequest,
  ControlledReportDraftAssembleResult,
  ControlledReportDraftAuditLog,
  ControlledReportDraftRecord,
  ControlledReportDraftStatus,
  ControlledLocalReadPreviewRequest,
  ControlledLocalReadPreviewResult,
  ControlledMaterialAuditLog,
  ControlledMaterialReadRequest,
  ControlledMaterialReadResult,
  ControlledMaterialStatus,
  ControlledOCRAuditLog,
  ControlledOCRPreviewRecord,
  ControlledOCRPreviewRequest,
  ControlledOCRPreviewResult,
  ControlledOCRStatus,
  ControlledReadPreviewRecord,
  ControlledFinalReviewLockAuditLog,
  ControlledFinalReviewLockRecord,
  ControlledFinalReviewLockRequest,
  ControlledFinalReviewLockResult,
  ControlledFinalReviewLockStatus,
  ControlledRevisionAuditLog,
  ControlledRevisionRecord,
  ControlledRevisionRequest,
  ControlledRevisionResult,
  ControlledRevisionStatus,
  ControlledReportDraftRequest,
  ControlledReportDraftResult,
  DashboardStats,
  Fact,
  IntakeStatus,
  DatabaseReadinessStatus,
  LegalAnalysis,
  MaterialInventoryRequest,
  MaterialInventoryResult,
  InternalAlphaAuditLog,
  InternalAlphaDryRunRequest,
  InternalAlphaDryRunResult,
  InternalAlphaReadinessChecklist,
  InternalAlphaStatus,
  PersonalAlphaAuditLog,
  PersonalAlphaCaseOSActionEligibility,
  PersonalAlphaCaseOSAuditTimeline,
  PersonalAlphaCaseOSAuditTimelineAvailableFilters,
  PersonalAlphaCaseOSAuditTimelineFilters,
  PersonalAlphaCaseOSAuditTimelineRedactionCheck,
  PersonalAlphaCaseOSAuditTimelineSummary,
  PersonalAlphaCaseOSBlockers,
  PersonalAlphaCaseOSCaseDetail,
  PersonalAlphaCaseOSCaseListItem,
  PersonalAlphaCaseOSExportPackageContent,
  PersonalAlphaCaseOSExportPackageCreateRequest,
  PersonalAlphaCaseOSExportPackageCreateResult,
  PersonalAlphaCaseOSExportPackageDetail,
  PersonalAlphaCaseOSExportPackageList,
  PersonalAlphaCaseOSExportPackageSafetyCheck,
  PersonalAlphaCaseOSExportPackageStatus,
  PersonalAlphaCaseOSExportPackageSummary,
  PersonalAlphaCaseOSFinalLockConsolidation,
  PersonalAlphaCaseOSHardeningSafetyCheck,
  PersonalAlphaCaseOSHardeningStatus,
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
  PersonalAlphaCaseOSReleaseCandidateAudit,
  PersonalAlphaCaseOSReleaseCandidateCaseReadiness,
  PersonalAlphaCaseOSReleaseCandidateChecklist,
  PersonalAlphaCaseOSReleaseCandidateReadiness,
  PersonalAlphaCaseOSReleaseCandidateStatus,
  PersonalAlphaCaseOSReleaseCandidateSummary,
  PersonalAlphaCaseOSReleaseNotesPreview,
  PersonalAlphaCaseOSResponseConsistency,
  PersonalAlphaCaseOSReviewState,
  PersonalAlphaCaseOSReviewStateHistory,
  PersonalAlphaCaseOSReviewStateSummary,
  PersonalAlphaCaseOSReviewStateTransitionValidation,
  PersonalAlphaCaseOSReviewStateTransitions,
  PersonalAlphaCaseOSSafetyChecklist,
  PersonalAlphaCaseOSStageOrchestration,
  PersonalAlphaCaseOSStageState,
  PersonalAlphaCaseOSStageTransitions,
  PersonalAlphaCaseOSStatus,
  PersonalAlphaCaseOSRuntimeStorageCheck,
  PersonalAlphaCaseOSUnifiedAuditTimeline,
  PersonalAlphaDashboardAuditTimeline,
  PersonalAlphaDashboardSourceTraceSummary,
  PersonalAlphaDashboardStageHealth,
  PersonalAlphaDashboardStatus,
  PersonalAlphaDashboardSummary,
  PersonalAlphaDryRunRequest,
  PersonalAlphaDryRunResult,
  PersonalAlphaFinalGateDecisionList,
  PersonalAlphaFinalGateDecisionRequest,
  PersonalAlphaFinalGateDecisionResult,
  PersonalAlphaFinalGateRunDetail,
  PersonalAlphaFinalGateStatus,
  PersonalAlphaFinalGateSummaryResponse,
  PersonalAlphaFinalLockCreateRequest,
  PersonalAlphaFinalLockCreateResult,
  PersonalAlphaFinalLockList,
  PersonalAlphaFinalLockReadiness,
  PersonalAlphaFinalLockRecord,
  PersonalAlphaFinalLockStatus,
  PersonalAlphaFinalPacketCreateRequest,
  PersonalAlphaFinalPacketCreateResult,
  PersonalAlphaFinalPacketList,
  PersonalAlphaFinalPacketPreview,
  PersonalAlphaFinalPacketRecord,
  PersonalAlphaFinalPacketStatus,
  PersonalAlphaLawyerFinalReviewActionList,
  PersonalAlphaLawyerFinalReviewActionRecord,
  PersonalAlphaLawyerFinalReviewActionRequest,
  PersonalAlphaLawyerFinalReviewActionResult,
  PersonalAlphaLawyerFinalReviewPacketDetail,
  PersonalAlphaLawyerFinalReviewStatus,
  PersonalAlphaLawyerFinalReviewSummary,
  PersonalAlphaFinalReadinessRunDetail,
  PersonalAlphaFinalReadinessStatus,
  PersonalAlphaFinalReadinessSummaryResponse,
  PersonalAlphaRunDetail,
  PersonalAlphaEvidenceSummaryResponse,
  PersonalAlphaSourceReviewDecisionList,
  PersonalAlphaSourceReviewDecisionRequest,
  PersonalAlphaSourceReviewDecisionResult,
  PersonalAlphaSourceReviewDecisionSummaryResponse,
  PersonalAlphaSourceReviewRunDetail,
  PersonalAlphaSourceReviewStatus,
  PersonalAlphaSourceTraceResponse,
  PersonalAlphaStatus,
  PersonalAlphaWorkspaceAuditLog,
  PersonalAlphaWorkspaceRequest,
  PersonalAlphaWorkspaceRunRecord,
  PersonalAlphaWorkspaceRunResult,
  PersonalAlphaWorkspaceStatus,
  PersonalAIAuditTimeline,
  PersonalAIGatewayStatus,
  PersonalAILiveAuditTimeline,
  PersonalAILiveGatewayStatus,
  PersonalAILiveProviderConfig,
  PersonalAILiveProviderConfigList,
  PersonalAILiveRunList,
  PersonalAILiveRunRecord,
  PersonalAILiveRunRequest,
  PersonalAILiveSafetyStatus,
  PersonalAIMockRunRequest,
  PersonalAIMockRunResult,
  PersonalAIProvider,
  PersonalAIProviderList,
  PersonalAIPromptRenderPreviewRequest,
  PersonalAIPromptRenderPreviewResult,
  PersonalAIPromptTemplate,
  PersonalAIPromptTemplateList,
  PersonalAIRunList,
  PersonalAIRunRecord,
  PersonalAISafetyStatus,
  PersonalAITokenUsageSummary,
  PersonalMaterialAuditTimeline,
  PersonalMaterialLiveAuditTimeline,
  PersonalMaterialLiveGatewayStatus,
  PersonalMaterialLiveGateList,
  PersonalMaterialLiveGateMockRequest,
  PersonalMaterialLiveGateStatus,
  PersonalMaterialLiveHealthDryRun,
  PersonalMaterialLiveProviderConfig,
  PersonalMaterialLiveProviderConfigList,
  PersonalMaterialLiveProviderReadiness,
  PersonalMaterialLiveProviderReadinessList,
  PersonalMaterialLiveReviewActionRequest,
  PersonalMaterialLiveReviewActionResult,
  PersonalMaterialLiveReviewQueue,
  PersonalMaterialLiveRunList,
  PersonalMaterialLiveRunRecord,
  PersonalMaterialLiveRunRequest,
  PersonalMaterialLiveSafetyStatus,
  PersonalMaterialLiveSecretBoundary,
  PersonalMaterialLiveSourceTraceList,
  PersonalMaterialParseJobList,
  PersonalMaterialParseJobRecord,
  PersonalMaterialParseJobRequest,
  PersonalMaterialParseJobResult,
  PersonalMaterialProvider,
  PersonalMaterialProviderList,
  PersonalMaterialRuntimeStatus,
  PersonalMaterialSafetyStatus,
  PersonalMaterialSourceTraceList,
  PersonalEnterpriseQueryList,
  PersonalEnterpriseQueryMockRequest,
  PersonalEnterpriseQueryResult,
  CaseAnalysisAuditTimeline,
  CaseAnalysisEvaluation,
  CaseAnalysisEvaluationList,
  CaseAnalysisGate,
  CaseAnalysisGateList,
  CaseAnalysisReviewActionRequest,
  CaseAnalysisReviewActionResult,
  CaseAnalysisReviewQueue,
  CaseAnalysisRuntime,
  CaseAnalysisRuntimeList,
  CaseAnalysisRunList,
  CaseAnalysisRunMockRequest,
  CaseAnalysisRunRecord,
  CaseAnalysisSafetyStatus,
  CaseAnalysisSourceTrace,
  CaseAnalysisSourceTraceList,
  FactAnalysisDraft,
  FactAnalysisDraftList,
  FactDraftMockRequest,
  LegalAnalysisDraft,
  LegalAnalysisDraftList,
  LegalDraftMockRequest,
  PersonalCaseAnalysisStatus,
  SkillBaselineReport,
  ExportBoundary,
  OwnerDownloadList,
  OwnerDownloadMockRequest,
  OwnerDownloadRecord,
  OwnerOutputAuditTimeline,
  OwnerOutputDownloadList,
  OwnerOutputDownloadRecord,
  OwnerOutputDownloadRequest,
  OwnerOutputGate,
  OwnerOutputList,
  OwnerOutputOptimization,
  OwnerOutputQuality,
  OwnerOutputRecord,
  OwnerOutputSafetyStatus,
  OwnerOutputSourceTraceList,
  OwnerOutputStatus,
  IssueLogItem,
  IssueLogList,
  IssueLogMockRequest,
  OptimizationBacklogItem,
  OptimizationBacklogList,
  OptimizationBacklogMockRequest,
  QualityReview,
  SafetyConfirmation,
  StageObservation,
  StageObservationList,
  StageObservationMockRequest,
  TrialAuditTimeline,
  TrialChecklist,
  TrialReadinessStatus,
  TrialSafetyStatus,
  TrialSession,
  TrialSessionList,
  TrialSessionMockRequest,
  CategorySummaryList,
  LiveGateList,
  LiveGateMockRequest,
  LiveGateStatus,
  LiveConnectionAuditTimeline,
  LiveConnectionHealthDryRun,
  LiveConnectionLiveGate,
  LiveConnectionProvider,
  LiveConnectionProviderList,
  LiveConnectionRunList,
  LiveConnectionRunRecord,
  LiveConnectionRunRequest,
  LiveConnectionRuntimeList,
  LiveConnectionSafetyStatus,
  LiveConnectionSecretBoundary,
  LiveConnectionStatus,
  LiveConnectionUsagePolicy,
  LegalEnterpriseCategorySummaryList,
  LegalEnterpriseGenericResponse,
  LegalEnterpriseProvider,
  LegalEnterpriseProviderList,
  LegalEnterpriseStatus,
  ProviderAuditTimeline,
  ProviderHealthDryRun,
  ProviderList,
  ProviderMetadata,
  ProviderSafetyStatus,
  ProviderStatus,
  SecretBoundaryStatus,
  UsagePolicy,
  PilotAuditTimeline,
  PilotOutputList,
  PilotOutputMockRequest,
  PilotOutputRecord,
  PilotReadiness,
  PilotReviewActionRequest,
  PilotReviewActionResult,
  PilotReviewQueue,
  PilotRunList,
  PilotRunMockRequest,
  PilotRunRecord,
  PilotRuntimeList,
  PilotSafetyStatus,
  PilotSourceTraceList,
  PilotStatus,
  PilotWorkflow,
  ProviderGateSummary,
  SkillFinalDraft,
  SkillFinalDraftList,
  PersonalIntelligenceAuditTimeline,
  PersonalIntelligenceConfirmationActionRequest,
  PersonalIntelligenceConfirmationActionResult,
  PersonalIntelligenceLiveAuditTimeline,
  PersonalIntelligenceLiveGatewayStatus,
  PersonalIntelligenceLiveProviderConfig,
  PersonalIntelligenceLiveProviderConfigList,
  PersonalIntelligenceLiveReviewActionRequest,
  PersonalIntelligenceLiveReviewActionResult,
  PersonalIntelligenceLiveReviewQueue,
  PersonalIntelligenceLiveRunList,
  PersonalIntelligenceLiveRunRecord,
  PersonalIntelligenceLiveRunRequest,
  PersonalIntelligenceLiveSafetyStatus,
  PersonalIntelligenceLiveSourceTrace,
  PersonalIntelligenceLiveSourceTraceList,
  PersonalIntelligenceProvider,
  PersonalIntelligenceProviderList,
  PersonalIntelligenceSafetyStatus,
  PersonalIntelligenceSourceTrace,
  PersonalIntelligenceSourceTraceList,
  PersonalIntelligenceStatus,
  PersonalLegalSearchList,
  PersonalLegalSearchMockRequest,
  PersonalLegalSearchResult,
  CaseProductionAuditTimeline,
  CaseProductionSafetyStatus,
  CaseProductionSourceTrace,
  CaseProductionSourceTraceList,
  DeliveryPacketAuditTimeline,
  DeliveryPacketList,
  DeliveryPacketMockRequest,
  DeliveryPacketRecord,
  DeliveryPacketRuntime,
  DeliveryPacketRuntimeList,
  DeliveryPacketSafetyStatus,
  ExportReadiness,
  ExportReadinessList,
  EvaluationMockRequest,
  ExperiencePackageDraft,
  ExperiencePackageDraftList,
  ExperiencePackageMockRequest,
  FinalLockActionRequest,
  FinalLockList,
  FinalLockRecord,
  PacketItemList,
  PacketItemMockRequest,
  PacketItemRecord,
  PersonalCaseProductionStatus,
  PersonalDeliveryPacketStatus,
  PersonalShowcasePackStatus,
  PersonalSkillStudioRuntime,
  PersonalSkillStudioRuntimeList,
  PersonalSkillStudioStatus,
  ProductionCaseList,
  ProductionCaseMockRequest,
  ProductionCaseRecord,
  ProductionReadiness,
  ProductionReadinessList,
  PromotionActionRequest,
  PromotionActionResult,
  ReviewGateActionRequest,
  ReviewGateActionResult,
  ReviewSummary,
  ReviewSummaryList,
  PilotSampleList,
  PilotSampleMockRequest,
  PilotSampleRecord,
  SkillCandidateDraft,
  SkillCandidateDraftList,
  SkillCandidateMockRequest,
  SkillEvaluationDraft,
  SkillEvaluationDraftList,
  SkillSampleRegistry,
  SkillTrainingRuntimeStatus,
  SkillStudioAuditTimeline,
  SkillStudioBaselineDiscovery,
  SkillStudioFinalDraft,
  SkillStudioFinalDraftList,
  SkillStudioFinalGate,
  SkillStudioFinalOptimization,
  SkillStudioFinalOwnerDownload,
  SkillStudioFinalOwnerDownloadList,
  SkillStudioFinalOwnerDownloadRequest,
  SkillStudioFinalQuality,
  SkillStudioSafetyStatus,
  SkillStudioSourceTrace,
  SkillStudioSourceTraceList,
  TrainingArtifactCaseCauseMatchRequest,
  TrainingArtifactCaseCauseMatchResult,
  TrainingArtifactLoadDryRun,
  TrainingArtifactLoadDryRunList,
  TrainingArtifactLoadDryRunRequest,
  TrainingArtifactManifestList,
  TrainingArtifactSafetyStatus,
  TrainingArtifactSkillContext,
  TrainingArtifactSkillContextList,
  TrainingArtifactStatus,
  CodexSkillDraft,
  CodexSkillDraftBuildRequest,
  CodexSkillDraftBuildResponse,
  CodexSkillDraftList,
  ExperienceCandidateBuildRequest,
  ExperienceCandidateList,
  ExperienceCandidateReviewRequest,
  InternalExperiencePackage,
  ExperiencePackageBuildRequest,
  ExperiencePackageBuildResponse,
  ExperiencePackageList,
  LegalRetrievalJobList,
  LegalRetrievalJobRequest,
  OcrJobList,
  OcrJobRequest,
  PracticeLoadReviewDecisionRequest,
  PracticeLoadReviewEditRequest,
  PracticeLoadReviewPackage,
  PracticeLoadReviewPackageAudit,
  PracticeLoadReviewPackageList,
  PracticeLoadReviewSaveRequest,
  PracticeLoadReviewSourceTraceBundle,
  RawWorkProductBoundaryStatus,
  SkillExperienceBinding,
  SkillExperienceBindingList,
  SkillExperienceBindingRequest,
  SkillExperienceImportRequest,
  SkillExperienceImportResponse,
  SkillExperiencePoolEntry,
  SkillExperiencePoolList,
  SkillExperiencePoolStatus,
  SkillPackage,
  SkillPackageAudit,
  SkillPackageBuildRequest,
  SkillPackageBuildResponse,
  SkillPackageList,
  SkillPackageManifest,
  SkillPackageSourceTraceBundle,
  SkillPackageValidationResult,
  TrainingPackageAudit,
  TrainingPackageSourceTraceBundle,
  TrainingTaskBuildRequest,
  TrainingTaskBuildResponse,
  TrainingTaskList,
  V731bTrainingExperiencePipelineStatus,
  V731cSkillExperiencePipelineStatus,
  V731dSkillPackagePipelineStatus,
  V731eTrainingPipelineStatus,
  V731fPracticeLoadPipelineStatus,
  V732ExperienceLifecycleStatus,
  ExperienceLifecycleList,
  ExperienceLifecycleRecord,
  ExperienceLifecycleGraph,
  ExperienceLifecycleAuditTimeline,
  ExperienceLifecycleSourceTraceView,
  ExperienceLifecycleIntegrityCheck,
  ExperienceLifecycleSafetySummary,
  CaseAnalysisSkillOutputSchema,
  CaseAnalysisWorkbenchView,
  CaseAnalysisWorkbenchViewList,
  CaseAnalysisRuntimeOutput,
  CaseAnalysisRuntimeOutputList,
  CaseAnalysisOutputFeedback,
  CaseAnalysisOutputFeedbackList,
  CaseAnalysisOutputFeedbackRequest,
  CaseAnalysisOutputRiskEvent,
  CaseAnalysisOutputRiskEventList,
  CaseAnalysisOutputRiskEventRequest,
  CaseAnalysisOutputAudit,
  CaseAnalysisOutputSourceTrace,
  V733CaseAnalysisWorkbenchStatus,
  CodexTrainingRun,
  CodexTrainingRunList,
  CodexTrainingRunLoadDryRunResult,
  CodexTrainingRunRequest,
  CaseCauseClassification,
  CodexTrainingScheme,
  CaseCauseNode,
  CaseCauseTaxonomyManifest,
  RealClosedCaseIntakeStatus,
  RealClosedCaseTrainingIntakeList,
  RealClosedCaseTrainingIntakeRecord,
  RealClosedCaseTrainingIntakeRequest,
  RedactionReport,
  TrainingSampleSegment,
  SkillTestCaseDraft,
  SkillTestCaseDraftList,
  SourceBundleList,
  SourceBundleMockRequest,
  SourceBundleRecord,
  ShowcaseAuditTimeline,
  ShowcaseMetrics,
  ShowcaseRuntime,
  ShowcaseRuntimeList,
  ShowcaseSafetyStatus,
  StoryFlowList,
  StoryFlowMockRequest,
  StoryFlowRecord,
  TrustPanel,
  StageRunList,
  StageRunMockRequest,
  StageRunRecord,
  TestCaseMockRequest,
  WorkflowRunList,
  WorkflowRunMockRequest,
  WorkflowRunRecord,
  WorkflowStage,
  WorkflowStageList,
  PersonalOCRJobList,
  PersonalOCRJobRecord,
  PersonalOCRJobRequest,
  PersonalOCRJobResult,
  PersonalOCRPreview,
  PersonalOCRReviewActionRequest,
  PersonalOCRReviewActionResult,
  PersonalOCRReviewQueue,
  PersonalProductionConsoleSummary,
  PersonalProductionMode,
  PersonalProductionProviderCapabilities,
  PersonalProductionReadiness,
  PersonalProductionRuntimeRegistry,
  PersonalProductionSafety,
  PersonalProductionShowcase,
  PersonalProductionStatus,
  PersonalCaseManifestPreview,
  PersonalCaseManifestPreviewRequest,
  LocalSandboxAuditLog,
  LocalSandboxDryRunRequest,
  LocalSandboxDryRunResult,
  LocalSandboxGuardStatus,
  LocalSandboxStatus,
  Material,
  Report,
  SecretManagementChecklist,
  LatestRuntimeRunsResponse,
  LegalSearchProviderStatus,
  LegalSearchRequest,
  LegalSearchResult,
  RuntimeRun,
  RuntimeRunsResponse,
  RuntimeStatus,
  OCRProviderStatus,
  OCRRequest,
  OCRResult,
  Skill,
  ExperiencePackage,
  ExperiencePackageDetail,
  SkillRegistryDetail,
  SkillRegistryEntry,
  SourceRefsStatus,
  SourceTrace,
  User,
  VersionedSkillTrainingPackage,
  VersionedSkillTrainingPackageDetail,
  VersionedSkillTrainingPackageFile,
  VersionedSkillTrainingRun,
  Workspace
} from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8001";
const TOKEN_STORAGE_KEY = "lawyer_ai_access_token";
const DEFAULT_LOCAL_DEV_TOKEN = "dev-local-token";
const SAFE_API_ERROR_MESSAGE = "请求未完成。请确认本地后端 8001 已启动，并保持 mock-first、provider-gated、律师复核必需。";

export type {
  AuthStatus,
  Case as CaseRecord,
  CaseSkillBinding,
  CaseCauseTaxonomyEntry,
  ControlledLawyerReviewActionRequest,
  ControlledLawyerReviewAuditLog,
  ControlledLawyerReviewRecord,
  ControlledLawyerReviewResult,
  ControlledLawyerReviewStatus,
  ControlledLawyerReviewSubmitRequest,
  ControlledLegalCitationResolutionRequest,
  ControlledLegalCitationResolutionResult,
  ControlledLegalSearchAuditLog,
  ControlledLegalSearchPreviewRecord,
  ControlledLegalSearchPreviewRequest,
  ControlledLegalSearchPreviewResult,
  ControlledLegalSearchStatus,
  ControlledReportDraftAssembleRequest,
  ControlledReportDraftAssembleResult,
  ControlledReportDraftAuditLog,
  ControlledReportDraftRecord,
  ControlledReportDraftStatus,
  ControlledLocalReadPreviewRequest,
  ControlledLocalReadPreviewResult,
  ControlledMaterialAuditLog,
  ControlledMaterialReadRequest,
  ControlledMaterialReadResult,
  ControlledMaterialStatus,
  ControlledOCRAuditLog,
  ControlledOCRPreviewRecord,
  ControlledOCRPreviewRequest,
  ControlledOCRPreviewResult,
  ControlledOCRStatus,
  ControlledReadPreviewRecord,
  ControlledFinalReviewLockAuditLog,
  ControlledFinalReviewLockRecord,
  ControlledFinalReviewLockRequest,
  ControlledFinalReviewLockResult,
  ControlledFinalReviewLockStatus,
  ControlledRevisionAuditLog,
  ControlledRevisionRecord,
  ControlledRevisionRequest,
  ControlledRevisionResult,
  ControlledRevisionStatus,
  ControlledReportDraftRequest,
  ControlledReportDraftResult,
  DashboardStats,
  Fact as FactRecord,
  IntakeStatus as IntakeStatusRecord,
  DatabaseReadinessStatus,
  LegalAnalysis as LegalAnalysisRecord,
  MaterialInventoryRequest,
  MaterialInventoryResult,
  InternalAlphaAuditLog,
  InternalAlphaDryRunRequest,
  InternalAlphaDryRunResult,
  InternalAlphaReadinessChecklist,
  InternalAlphaStatus,
  PersonalAlphaAuditLog,
  PersonalAlphaCaseOSActionEligibility,
  PersonalAlphaCaseOSAuditTimeline,
  PersonalAlphaCaseOSAuditTimelineAvailableFilters,
  PersonalAlphaCaseOSAuditTimelineFilters,
  PersonalAlphaCaseOSAuditTimelineRedactionCheck,
  PersonalAlphaCaseOSAuditTimelineSummary,
  PersonalAlphaCaseOSBlockers,
  PersonalAlphaCaseOSCaseDetail,
  PersonalAlphaCaseOSCaseListItem,
  PersonalAlphaCaseOSExportPackageContent,
  PersonalAlphaCaseOSExportPackageCreateRequest,
  PersonalAlphaCaseOSExportPackageCreateResult,
  PersonalAlphaCaseOSExportPackageDetail,
  PersonalAlphaCaseOSExportPackageList,
  PersonalAlphaCaseOSExportPackageSafetyCheck,
  PersonalAlphaCaseOSExportPackageStatus,
  PersonalAlphaCaseOSExportPackageSummary,
  PersonalAlphaCaseOSFinalLockConsolidation,
  PersonalAlphaCaseOSHardeningSafetyCheck,
  PersonalAlphaCaseOSHardeningStatus,
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
  PersonalAlphaCaseOSReleaseCandidateAudit,
  PersonalAlphaCaseOSReleaseCandidateCaseReadiness,
  PersonalAlphaCaseOSReleaseCandidateChecklist,
  PersonalAlphaCaseOSReleaseCandidateReadiness,
  PersonalAlphaCaseOSReleaseCandidateStatus,
  PersonalAlphaCaseOSReleaseCandidateSummary,
  PersonalAlphaCaseOSReleaseNotesPreview,
  PersonalAlphaCaseOSResponseConsistency,
  PersonalAlphaCaseOSReviewState,
  PersonalAlphaCaseOSReviewStateHistory,
  PersonalAlphaCaseOSReviewStateSummary,
  PersonalAlphaCaseOSReviewStateTransitionValidation,
  PersonalAlphaCaseOSReviewStateTransitions,
  PersonalAlphaCaseOSSafetyChecklist,
  PersonalAlphaCaseOSStageOrchestration,
  PersonalAlphaCaseOSStageState,
  PersonalAlphaCaseOSStageTransitions,
  PersonalAlphaCaseOSStatus,
  PersonalAlphaCaseOSRuntimeStorageCheck,
  PersonalAlphaCaseOSUnifiedAuditTimeline,
  PersonalAlphaDashboardAuditTimeline,
  PersonalAlphaDashboardSourceTraceSummary,
  PersonalAlphaDashboardStageHealth,
  PersonalAlphaDashboardStatus,
  PersonalAlphaDashboardSummary,
  PersonalAlphaDryRunRequest,
  PersonalAlphaDryRunResult,
  PersonalAlphaFinalGateDecisionList,
  PersonalAlphaFinalGateDecisionRequest,
  PersonalAlphaFinalGateDecisionResult,
  PersonalAlphaFinalGateRunDetail,
  PersonalAlphaFinalGateStatus,
  PersonalAlphaFinalGateSummaryResponse,
  PersonalAlphaFinalLockCreateRequest,
  PersonalAlphaFinalLockCreateResult,
  PersonalAlphaFinalLockList,
  PersonalAlphaFinalLockReadiness,
  PersonalAlphaFinalLockRecord,
  PersonalAlphaFinalLockStatus,
  PersonalAlphaFinalPacketCreateRequest,
  PersonalAlphaFinalPacketCreateResult,
  PersonalAlphaFinalPacketList,
  PersonalAlphaFinalPacketPreview,
  PersonalAlphaFinalPacketRecord,
  PersonalAlphaFinalPacketStatus,
  PersonalAlphaLawyerFinalReviewActionList,
  PersonalAlphaLawyerFinalReviewActionRecord,
  PersonalAlphaLawyerFinalReviewActionRequest,
  PersonalAlphaLawyerFinalReviewActionResult,
  PersonalAlphaLawyerFinalReviewPacketDetail,
  PersonalAlphaLawyerFinalReviewStatus,
  PersonalAlphaLawyerFinalReviewSummary,
  PersonalAlphaFinalReadinessRunDetail,
  PersonalAlphaFinalReadinessStatus,
  PersonalAlphaFinalReadinessSummaryResponse,
  PersonalAlphaRunDetail,
  PersonalAlphaEvidenceSummaryResponse,
  PersonalAlphaSourceReviewDecisionList,
  PersonalAlphaSourceReviewDecisionRequest,
  PersonalAlphaSourceReviewDecisionResult,
  PersonalAlphaSourceReviewDecisionSummaryResponse,
  PersonalAlphaSourceReviewRunDetail,
  PersonalAlphaSourceReviewStatus,
  PersonalAlphaSourceTraceResponse,
  PersonalAlphaStatus,
  PersonalAlphaWorkspaceAuditLog,
  PersonalAlphaWorkspaceRequest,
  PersonalAlphaWorkspaceRunRecord,
  PersonalAlphaWorkspaceRunResult,
  PersonalAlphaWorkspaceStatus,
  PersonalAIAuditTimeline,
  PersonalAIGatewayStatus,
  PersonalAILiveAuditTimeline,
  PersonalAILiveGatewayStatus,
  PersonalAILiveProviderConfig,
  PersonalAILiveProviderConfigList,
  PersonalAILiveRunList,
  PersonalAILiveRunRecord,
  PersonalAILiveRunRequest,
  PersonalAILiveSafetyStatus,
  PersonalAIMockRunRequest,
  PersonalAIMockRunResult,
  PersonalAIProvider,
  PersonalAIProviderList,
  PersonalAIPromptRenderPreviewRequest,
  PersonalAIPromptRenderPreviewResult,
  PersonalAIPromptTemplate,
  PersonalAIPromptTemplateList,
  PersonalAIRunList,
  PersonalAIRunRecord,
  PersonalAISafetyStatus,
  PersonalAITokenUsageSummary,
  PersonalMaterialAuditTimeline,
  PersonalMaterialLiveAuditTimeline,
  PersonalMaterialLiveGatewayStatus,
  PersonalMaterialLiveGateList,
  PersonalMaterialLiveGateMockRequest,
  PersonalMaterialLiveGateStatus,
  PersonalMaterialLiveHealthDryRun,
  PersonalMaterialLiveProviderConfig,
  PersonalMaterialLiveProviderConfigList,
  PersonalMaterialLiveProviderReadiness,
  PersonalMaterialLiveProviderReadinessList,
  PersonalMaterialLiveReviewActionRequest,
  PersonalMaterialLiveReviewActionResult,
  PersonalMaterialLiveReviewQueue,
  PersonalMaterialLiveRunList,
  PersonalMaterialLiveRunRecord,
  PersonalMaterialLiveRunRequest,
  PersonalMaterialLiveSafetyStatus,
  PersonalMaterialLiveSecretBoundary,
  PersonalMaterialLiveSourceTraceList,
  PersonalMaterialParseJobList,
  PersonalMaterialParseJobRecord,
  PersonalMaterialParseJobRequest,
  PersonalMaterialParseJobResult,
  PersonalMaterialProvider,
  PersonalMaterialProviderList,
  PersonalMaterialRuntimeStatus,
  PersonalMaterialSafetyStatus,
  PersonalMaterialSourceTraceList,
  LiveConnectionAuditTimeline,
  LiveConnectionHealthDryRun,
  LiveConnectionLiveGate,
  LiveConnectionProvider,
  LiveConnectionProviderList,
  LiveConnectionRunList,
  LiveConnectionRunRecord,
  LiveConnectionRunRequest,
  LiveConnectionRuntimeList,
  LiveConnectionSafetyStatus,
  LiveConnectionSecretBoundary,
  LiveConnectionStatus,
  LiveConnectionUsagePolicy,
  LegalEnterpriseCategorySummaryList,
  LegalEnterpriseGenericResponse,
  LegalEnterpriseProvider,
  LegalEnterpriseProviderList,
  LegalEnterpriseStatus,
  PersonalEnterpriseQueryList,
  PersonalEnterpriseQueryMockRequest,
  PersonalEnterpriseQueryResult,
  PersonalIntelligenceAuditTimeline,
  PersonalIntelligenceConfirmationActionRequest,
  PersonalIntelligenceConfirmationActionResult,
  PersonalIntelligenceLiveAuditTimeline,
  PersonalIntelligenceLiveGatewayStatus,
  PersonalIntelligenceLiveProviderConfig,
  PersonalIntelligenceLiveProviderConfigList,
  PersonalIntelligenceLiveReviewActionRequest,
  PersonalIntelligenceLiveReviewActionResult,
  PersonalIntelligenceLiveReviewQueue,
  PersonalIntelligenceLiveRunList,
  PersonalIntelligenceLiveRunRecord,
  PersonalIntelligenceLiveRunRequest,
  PersonalIntelligenceLiveSafetyStatus,
  PersonalIntelligenceLiveSourceTrace,
  PersonalIntelligenceLiveSourceTraceList,
  PersonalIntelligenceProvider,
  PersonalIntelligenceProviderList,
  PersonalIntelligenceSafetyStatus,
  PersonalIntelligenceSourceTrace,
  PersonalIntelligenceSourceTraceList,
  PersonalIntelligenceStatus,
  PersonalLegalSearchList,
  PersonalLegalSearchMockRequest,
  PersonalLegalSearchResult,
  CaseProductionAuditTimeline,
  CaseProductionSafetyStatus,
  CaseProductionSourceTrace,
  CaseProductionSourceTraceList,
  DeliveryPacketAuditTimeline,
  DeliveryPacketList,
  DeliveryPacketMockRequest,
  DeliveryPacketRecord,
  DeliveryPacketRuntime,
  DeliveryPacketRuntimeList,
  DeliveryPacketSafetyStatus,
  ExportReadiness,
  ExportReadinessList,
  EvaluationMockRequest,
  ExperiencePackageDraft,
  ExperiencePackageDraftList,
  ExperiencePackageMockRequest,
  FinalLockActionRequest,
  FinalLockList,
  FinalLockRecord,
  PacketItemList,
  PacketItemMockRequest,
  PacketItemRecord,
  PersonalCaseProductionStatus,
  PersonalDeliveryPacketStatus,
  PersonalShowcasePackStatus,
  PersonalSkillStudioRuntime,
  PersonalSkillStudioRuntimeList,
  PersonalSkillStudioStatus,
  ProductionCaseList,
  ProductionCaseMockRequest,
  ProductionCaseRecord,
  ProductionReadiness,
  ProductionReadinessList,
  PromotionActionRequest,
  PromotionActionResult,
  ReviewGateActionRequest,
  ReviewGateActionResult,
  ReviewSummary,
  ReviewSummaryList,
  PilotSampleList,
  PilotSampleMockRequest,
  PilotSampleRecord,
  SkillCandidateDraft,
  SkillCandidateDraftList,
  SkillCandidateMockRequest,
  SkillEvaluationDraft,
  SkillEvaluationDraftList,
  SkillSampleRegistry,
  SkillTrainingRuntimeStatus,
  SkillStudioAuditTimeline,
  SkillStudioSafetyStatus,
  SkillStudioSourceTrace,
  SkillStudioSourceTraceList,
  TrainingArtifactCaseCauseMatchRequest,
  TrainingArtifactCaseCauseMatchResult,
  TrainingArtifactLoadDryRun,
  TrainingArtifactLoadDryRunList,
  TrainingArtifactLoadDryRunRequest,
  TrainingArtifactManifestList,
  TrainingArtifactSafetyStatus,
  TrainingArtifactSkillContext,
  TrainingArtifactSkillContextList,
  TrainingArtifactStatus,
  CodexSkillDraft,
  CodexSkillDraftBuildRequest,
  CodexSkillDraftBuildResponse,
  CodexSkillDraftList,
  ExperienceCandidateBuildRequest,
  ExperienceCandidateList,
  ExperienceCandidateReviewRequest,
  InternalExperiencePackage,
  ExperiencePackageBuildRequest,
  ExperiencePackageBuildResponse,
  ExperiencePackageList,
  LegalRetrievalJobList,
  LegalRetrievalJobRequest,
  OcrJobList,
  OcrJobRequest,
  PracticeLoadReviewDecisionRequest,
  PracticeLoadReviewEditRequest,
  PracticeLoadReviewPackage,
  PracticeLoadReviewPackageAudit,
  PracticeLoadReviewPackageList,
  PracticeLoadReviewSaveRequest,
  PracticeLoadReviewSourceTraceBundle,
  RawWorkProductBoundaryStatus,
  SkillExperienceBinding,
  SkillExperienceBindingList,
  SkillExperienceBindingRequest,
  SkillExperienceImportRequest,
  SkillExperienceImportResponse,
  SkillExperiencePoolEntry,
  SkillExperiencePoolList,
  SkillExperiencePoolStatus,
  SkillPackage,
  SkillPackageAudit,
  SkillPackageBuildRequest,
  SkillPackageBuildResponse,
  SkillPackageList,
  SkillPackageManifest,
  SkillPackageSourceTraceBundle,
  SkillPackageValidationResult,
  TrainingPackageAudit,
  TrainingPackageSourceTraceBundle,
  TrainingTaskBuildRequest,
  TrainingTaskBuildResponse,
  TrainingTaskList,
  V731bTrainingExperiencePipelineStatus,
  V731cSkillExperiencePipelineStatus,
  V731dSkillPackagePipelineStatus,
  V731eTrainingPipelineStatus,
  V731fPracticeLoadPipelineStatus,
  CodexTrainingRun,
  CodexTrainingRunList,
  CodexTrainingRunLoadDryRunResult,
  CodexTrainingRunRequest,
  CaseCauseClassification,
  CodexTrainingScheme,
  CaseCauseNode,
  CaseCauseTaxonomyManifest,
  RealClosedCaseIntakeStatus,
  RealClosedCaseTrainingIntakeList,
  RealClosedCaseTrainingIntakeRecord,
  RealClosedCaseTrainingIntakeRequest,
  RedactionReport,
  TrainingSampleSegment,
  SkillTestCaseDraft,
  SkillTestCaseDraftList,
  SourceBundleList,
  SourceBundleMockRequest,
  SourceBundleRecord,
  ShowcaseAuditTimeline,
  ShowcaseMetrics,
  ShowcaseRuntime,
  ShowcaseRuntimeList,
  ShowcaseSafetyStatus,
  StoryFlowList,
  StoryFlowMockRequest,
  StoryFlowRecord,
  TrustPanel,
  StageRunList,
  StageRunMockRequest,
  StageRunRecord,
  TestCaseMockRequest,
  WorkflowRunList,
  WorkflowRunMockRequest,
  WorkflowRunRecord,
  WorkflowStage,
  WorkflowStageList,
  PersonalOCRJobList,
  PersonalOCRJobRecord,
  PersonalOCRJobRequest,
  PersonalOCRJobResult,
  PersonalOCRPreview,
  PersonalOCRReviewActionRequest,
  PersonalOCRReviewActionResult,
  PersonalOCRReviewQueue,
  PersonalProductionConsoleSummary,
  PersonalProductionMode,
  PersonalProductionProviderCapabilities,
  PersonalProductionReadiness,
  PersonalProductionRuntimeRegistry,
  PersonalProductionSafety,
  PersonalProductionShowcase,
  PersonalProductionStatus,
  PersonalCaseManifestPreview,
  PersonalCaseManifestPreviewRequest,
  LocalSandboxAuditLog,
  LocalSandboxDryRunRequest,
  LocalSandboxDryRunResult,
  LocalSandboxGuardStatus,
  LocalSandboxStatus,
  Material as MaterialRecord,
  Report as ReportRecord,
  SecretManagementChecklist,
  RuntimeRun,
  RuntimeRunsResponse,
  LatestRuntimeRunsResponse,
  LegalSearchProviderStatus,
  LegalSearchRequest,
  LegalSearchResult,
  RuntimeStatus as LLMStatus,
  OCRProviderStatus,
  OCRRequest,
  OCRResult,
  ExperiencePackage as ExperiencePackageRecord,
  SkillRegistryEntry as SkillRegistryRecord,
  SkillRegistryDetail,
  SourceRefsStatus,
  SourceTrace,
  CitationResolutionResult,
  Skill as WorkspaceSkillRecord,
  VersionedSkillTrainingPackage,
  VersionedSkillTrainingPackageDetail,
  VersionedSkillTrainingPackageFile,
  VersionedSkillTrainingRun,
  User as UserRecord,
  Workspace as WorkspaceRecord
};

export type LoginResponse = {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
  user_id: string;
  expires_at: string;
};

export type WorkspaceSkillDetail = {
  skill: Skill;
  package: {
    package_id: string;
    name: string;
    domain: string;
    version: string;
    status: string;
    package_path: string;
  };
  prompts_summary: Record<string, { length: number; preview: string }>;
  templates_summary: Record<string, { length: number; preview: string }>;
};

export type CaseDetail = {
  case: Case;
  intakeStatus: IntakeStatus | null;
  materials: Material[];
  facts: Fact[];
  analyses: LegalAnalysis[];
  reports: Report[];
  runtimeRuns: RuntimeRunsResponse | null;
};

export type CaseCreatePayload = {
  title: string;
  description?: string | null;
  client_name?: string | null;
  counterparty_name?: string | null;
  opposing_party?: string | null;
  case_type?: string | null;
  contract_type?: string | null;
  dispute_amount?: string | null;
  objective?: string | null;
  jurisdiction?: string | null;
  intake_notes?: string | null;
  priority?: string | null;
  tags?: string[];
};

export type ExtractFactsResponse = {
  case_id: string;
  run_id: string;
  run_type: "fact_extraction";
  status: string;
  facts: Fact[];
  llm_provider?: string | null;
  llm_status?: string | null;
  skill_used?: string | null;
  package_used?: string | null;
  materials_count: number;
  facts_created_count: number;
  facts_reused_count: number;
  facts_skipped_count: number;
  source_refs?: unknown;
};

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

const LOCAL_MOCK_CASES: Case[] = [
  {
    case_id: "case_local_mock_001",
    title: "本地演示案件",
    case_type: "contract_dispute",
    status: "draft",
    objective: "local fallback",
    workspace_id: "workspace_local_001",
    owner_user_id: "user_local_001",
    created_at: "2026-06-03T00:00:00Z",
    updated_at: "2026-06-03T00:00:00Z"
  }
];

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: buildAuthHeaders(),
    cache: "no-store"
  });

  if (!response.ok) {
    throw new ApiError(await buildErrorMessage(response, path), response.status);
  }

  return response.json();
}

async function postJson<T>(path: string, payload?: unknown): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...buildAuthHeaders()
    },
    body: JSON.stringify(payload ?? {}),
    cache: "no-store"
  });

  if (!response.ok) {
    throw new ApiError(await buildErrorMessage(response, path), response.status);
  }

  return response.json();
}

function buildAuditTimelineQuery(filters?: Partial<PersonalAlphaCaseOSAuditTimelineFilters>) {
  if (!filters) {
    return "";
  }
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      params.set(key, String(value));
    }
  });
  const query = params.toString();
  return query ? `?${query}` : "";
}

async function postForm<T>(path: string, formData: FormData): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: buildAuthHeaders(),
    body: formData,
    cache: "no-store"
  });

  if (!response.ok) {
    throw new ApiError(await buildErrorMessage(response, path), response.status);
  }

  return response.json();
}

async function buildErrorMessage(response: Response, path: string) {
  try {
    await response.json();
  } catch {
    // Do not surface backend stack traces, local paths, or provider details in the UI.
  }
  if (response.status >= 400 && response.status < 500) {
    return `${SAFE_API_ERROR_MESSAGE} 当前请求未通过受控校验（HTTP ${response.status}）。`;
  }
  return `${SAFE_API_ERROR_MESSAGE} 服务状态异常（HTTP ${response.status}，endpoint=${path}）。`;
}

function buildAuthHeaders(): Record<string, string> {
  const token = getStoredAccessToken();
  if (token) {
    return { Authorization: `Bearer ${token}` };
  }

  const devToken = getLocalDevToken();
  return devToken ? { "X-Dev-Token": devToken } : {};
}

function getStoredAccessToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  return window.localStorage.getItem(TOKEN_STORAGE_KEY);
}

function getLocalDevToken(): string | null {
  const configuredToken =
    process.env.NEXT_PUBLIC_LOCAL_DEV_TOKEN ||
    (typeof window === "undefined" ? process.env.LOCAL_DEV_TOKEN : undefined);

  if (configuredToken) {
    return configuredToken;
  }

  return isLocalApiBase() ? DEFAULT_LOCAL_DEV_TOKEN : null;
}

function isLocalApiBase() {
  try {
    const parsed = new URL(API_BASE);
    return ["127.0.0.1", "localhost", "::1"].includes(parsed.hostname);
  } catch {
    return false;
  }
}

function shouldUseLocalMockFallback(error: unknown) {
  return isLocalApiBase() && error instanceof ApiError;
}

export function storeAccessToken(token: string) {
  if (typeof window !== "undefined") {
    window.localStorage.setItem(TOKEN_STORAGE_KEY, token);
  }
}

export function clearAccessToken() {
  if (typeof window !== "undefined") {
    window.localStorage.removeItem(TOKEN_STORAGE_KEY);
  }
}

export const authApi = {
  status: () => request<AuthStatus>("/auth/status"),
  loginLocal: () =>
    postJson<LoginResponse>("/auth/login", {
      user_id: "user_local_001",
      dev_token: "dev-local-token"
    }),
  logoutLocal: () => clearAccessToken()
};

export const userApi = {
  me: () => request<User>("/users/me")
};

export const workspaceApi = {
  list: () => request<Workspace[]>("/workspaces"),
  get: (workspaceId: string) => request<Workspace>(`/workspaces/${workspaceId}`),
  cases: (workspaceId: string) => request<Case[]>(`/workspaces/${workspaceId}/cases`)
};

export const caseApi = {
  list: () => request<Case[]>("/cases"),
  listWithLocalFallback: async () => {
    try {
      return await request<Case[]>("/cases");
    } catch (error) {
      if (shouldUseLocalMockFallback(error)) {
        return LOCAL_MOCK_CASES;
      }
      throw error;
    }
  },
  create: (payload: string | CaseCreatePayload) =>
    postJson<Case>("/cases", typeof payload === "string" ? { title: payload } : payload),
  get: (caseId: string) => request<Case>(`/cases/${caseId}`),
  intakeStatus: (caseId: string) => request<IntakeStatus>(`/cases/${caseId}/intake/status`)
};

export const runtimeRunApi = {
  listByCase: (caseId: string) => request<RuntimeRunsResponse>(`/cases/${caseId}/runtime-runs`),
  latestByCase: (caseId: string) => request<LatestRuntimeRunsResponse>(`/cases/${caseId}/runtime-runs/latest`)
};

export const materialApi = {
  listByCase: (caseId: string) => request<Material[]>(`/cases/${caseId}/materials`),
  upload: (caseId: string, file: File, relativePath?: string) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("material_type", "document");
    if (relativePath) {
      formData.append("relative_path", relativePath);
    }
    return postForm<Material>(`/cases/${caseId}/materials`, formData);
  },
  uploadBatch: (caseId: string, files: File[], uploadBatchId?: string) => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
      formData.append("relative_paths", getFileRelativePath(file));
      formData.append("material_types", "document");
    });
    if (uploadBatchId) {
      formData.append("upload_batch_id", uploadBatchId);
    }
    return postForm<Material[]>(`/cases/${caseId}/materials/batch`, formData);
  }
};

export const factApi = {
  listByCase: async (caseId: string) => {
    const response = await request<{ facts: Fact[] }>(`/cases/${caseId}/facts`);
    return response.facts;
  },
  extract: (caseId: string) => postJson<ExtractFactsResponse>(`/cases/${caseId}/facts/extract`)
};

export const analysisApi = {
  listByCase: async (caseId: string) => {
    const response = await request<{ analyses: LegalAnalysis[] }>(`/cases/${caseId}/analysis`);
    return response.analyses;
  },
  run: (caseId: string) => postJson<LegalAnalysis>(`/cases/${caseId}/analysis/run`)
};

export const reportApi = {
  list: () => request<Report[]>("/reports"),
  get: (reportId: string) => request<Report>(`/reports/${reportId}`),
  listByCase: async (caseId: string) => {
    const response = await request<{ reports: Report[] }>(`/cases/${caseId}/reports`);
    return response.reports;
  },
  generate: (caseId: string) => postJson<Report>(`/cases/${caseId}/reports/generate`)
};

export const skillApi = {
  list: async () => {
    const response = await request<{ skills: Skill[] }>("/skills");
    return response.skills;
  },
  get: (skillId: string) => request<Skill>(`/skills/${skillId}`),
  evaluate: (skillId: string) => postJson<Record<string, unknown>>(`/skills/${skillId}/evaluate`),
  listPublished: async () => {
    const response = await request<{ skills: Skill[] }>("/workspace/skills");
    return response.skills;
  },
  getPublished: (skillId: string) => request<WorkspaceSkillDetail>(`/workspace/skills/${skillId}`),
  applyToCase: (caseId: string, skillId: string) =>
    postJson<CaseSkillBinding>(`/cases/${caseId}/skills/${skillId}/apply`),
  listForCase: async (caseId: string) => {
    const response = await request<{ skills: CaseSkillBinding[] }>(`/cases/${caseId}/skills`);
    return response.skills;
  }
};

export const experiencePackageApi = {
  list: async () => {
    const response = await request<{ experience_packages: ExperiencePackage[] }>("/experience-packages");
    return response.experience_packages;
  },
  get: (packageId: string) => request<ExperiencePackageDetail>(`/experience-packages/${packageId}`),
  getManifest: (packageId: string) => request<Record<string, unknown>>(`/experience-packages/${packageId}/manifest`),
  buildForSkill: (skillId: string) => postJson<ExperiencePackage>(`/skills/${skillId}/packages/build`),
  createCandidate: (runId: string) =>
    postJson<ExperiencePackage>("/experience-packages/create", { run_id: runId }),
  review: (experiencePackageId: string, reviewStatus: string, reviewedBy = "local_demo_user") =>
    postJson<ExperiencePackage>(`/experience-packages/${encodeURIComponent(experiencePackageId)}/review`, {
      review_status: reviewStatus,
      reviewed_by: reviewedBy
    })
};

export const skillRegistryApi = {
  list: async () => {
    const response = await request<{ skills: SkillRegistryEntry[] }>("/skill-registry");
    return response.skills;
  },
  get: (skillId: string) => request<SkillRegistryDetail>(`/skill-registry/${skillId}`),
  publish: (skillId: string) => postJson<Record<string, unknown>>(`/skill-registry/${skillId}/publish`),
  publishExperiencePackage: (experiencePackageId: string, workspaceScope = "local_demo_workspace") =>
    postJson<SkillRegistryEntry>("/skill-registry/publish", {
      experience_package_id: experiencePackageId,
      workspace_scope: workspaceScope
    }),
  deprecate: (skillId: string, reason = "local UI action") =>
    postJson<Record<string, unknown>>(`/skill-registry/${skillId}/deprecate`, { reason }),
  rollback: (skillId: string, reason = "local UI action") =>
    postJson<Record<string, unknown>>(`/skill-registry/${skillId}/rollback`, { reason })
};

export const versionedTrainingPackageApi = {
  list: async () => {
    const response = await request<{ packages: VersionedSkillTrainingPackage[] }>("/versioned-skill-training-packages");
    return response.packages;
  },
  get: (packageId: string) =>
    request<VersionedSkillTrainingPackageDetail>(
      `/versioned-skill-training-packages/${encodeURIComponent(packageId)}`
    ),
  files: async (packageId: string) => {
    const response = await request<{ files: VersionedSkillTrainingPackageFile[] }>(
      `/versioned-skill-training-packages/${encodeURIComponent(packageId)}/files`
    );
    return response.files;
  },
  byCaseCause: async (caseCauseCode: string) => {
    const response = await request<{ packages: VersionedSkillTrainingPackage[] }>(
      `/versioned-skill-training-packages/by-case-cause/${encodeURIComponent(caseCauseCode)}`
    );
    return response.packages;
  }
};

export const versionedTrainingRunApi = {
  list: async () => {
    const response = await request<{ runs: VersionedSkillTrainingRun[] }>("/versioned-skill-training-runs");
    return response.runs;
  },
  get: (runId: string) =>
    request<VersionedSkillTrainingRun>(`/versioned-skill-training-runs/${encodeURIComponent(runId)}`),
  createMock: (packageId: string) =>
    postJson<VersionedSkillTrainingRun>("/versioned-skill-training-runs/mock", { package_id: packageId })
};

export const caseCauseTaxonomyApi = {
  list: () => request<{ case_causes: CaseCauseTaxonomyEntry[] }>("/case-cause-taxonomy"),
  get: (caseCauseCode: string) =>
    request<CaseCauseTaxonomyEntry>(`/case-cause-taxonomy/${encodeURIComponent(caseCauseCode)}`),
  ancestors: (caseCauseCode: string) =>
    request<{ ancestors: CaseCauseTaxonomyEntry[] }>(
      `/case-cause-taxonomy/${encodeURIComponent(caseCauseCode)}/ancestors`
    ),
  children: (caseCauseCode: string) =>
    request<{ children: CaseCauseTaxonomyEntry[] }>(
      `/case-cause-taxonomy/${encodeURIComponent(caseCauseCode)}/children`
    )
};

export const runtimeApi = {
  health: () => request<{ status: string }>("/health"),
  llmStatus: () => request<RuntimeStatus>("/llm/status"),
  dashboardStats: () => request<DashboardStats>("/dashboard/stats")
};

export const ocrApi = {
  status: () => request<OCRProviderStatus>("/ocr/status"),
  mockExtract: (payload: OCRRequest) => postJson<OCRResult>("/ocr/mock-extract", {
    provider: "mock_ocr",
    mode: "mock",
    mock_only: true,
    ...payload
  })
};

export const legalSearchApi = {
  status: () => request<LegalSearchProviderStatus>("/legal-search/status"),
  mockSearch: (payload: LegalSearchRequest) => postJson<LegalSearchResult>("/legal-search/mock-search", {
    provider: "mock_legal_search",
    mode: "mock",
    mock_only: true,
    ...payload
  })
};

export const sourceRefsApi = {
  status: () => request<SourceRefsStatus>("/source-refs/status"),
  mockTrace: (reportId: string) =>
    request<SourceTrace>(`/source-refs/mock-trace/${encodeURIComponent(reportId)}`),
  resolve: (citationId: string) =>
    request<CitationResolutionResult>(`/source-refs/resolve/${encodeURIComponent(citationId)}`)
};

export const localSandboxApi = {
  status: () => request<LocalSandboxStatus>("/local-sandbox/status"),
  guards: () => request<LocalSandboxGuardStatus>("/local-sandbox/guards"),
  dryRun: (payload: LocalSandboxDryRunRequest) => postJson<LocalSandboxDryRunResult>("/local-sandbox/dry-run", payload),
  auditLogs: async () => {
    const response = await request<{ audit_logs: LocalSandboxAuditLog[] }>("/local-sandbox/audit-logs");
    return response.audit_logs;
  }
};

export const internalAlphaApi = {
  status: () => request<InternalAlphaStatus>("/internal-alpha/status"),
  readiness: () => request<InternalAlphaReadinessChecklist>("/internal-alpha/readiness"),
  secrets: () => request<SecretManagementChecklist>("/internal-alpha/secrets"),
  database: () => request<DatabaseReadinessStatus>("/internal-alpha/database"),
  dryRun: (payload: InternalAlphaDryRunRequest) =>
    postJson<InternalAlphaDryRunResult>("/internal-alpha/dry-run", payload),
  auditLogs: async () => {
    const response = await request<{ audit_logs: InternalAlphaAuditLog[] }>("/internal-alpha/audit-logs");
    return response.audit_logs;
  }
};

export const personalAlphaApi = {
  status: () => request<PersonalAlphaStatus>("/personal-alpha/status"),
  previewManifest: (payload: PersonalCaseManifestPreviewRequest) =>
    postJson<PersonalCaseManifestPreview>("/personal-alpha/manifest/preview", payload),
  previewMaterialInventory: (payload: MaterialInventoryRequest) =>
    postJson<MaterialInventoryResult>("/personal-alpha/materials/inventory", payload),
  dryRun: (payload: PersonalAlphaDryRunRequest) =>
    postJson<PersonalAlphaDryRunResult>("/personal-alpha/dry-run", payload),
  auditLogs: async () => {
    const response = await request<{ audit_logs: PersonalAlphaAuditLog[] }>("/personal-alpha/audit-logs");
    return response.audit_logs;
  }
};

export const controlledMaterialApi = {
  status: () => request<ControlledMaterialStatus>("/controlled-material/status"),
  readConfirmed: (payload: ControlledMaterialReadRequest) =>
    postJson<ControlledMaterialReadResult>("/controlled-material/read-confirmed", payload),
  localReadPreview: (payload: ControlledLocalReadPreviewRequest) =>
    postJson<ControlledLocalReadPreviewResult>("/controlled-material/local-read-preview", payload),
  readPreview: (previewId: string) =>
    request<ControlledReadPreviewRecord>(`/controlled-material/read-preview/${encodeURIComponent(previewId)}`),
  reportDraft: (payload: ControlledReportDraftRequest) =>
    postJson<ControlledReportDraftResult>("/controlled-material/report-draft", payload),
  auditLogs: async () => {
    const response = await request<{ audit_logs: ControlledMaterialAuditLog[] }>("/controlled-material/audit-logs");
    return response.audit_logs;
  }
};

export const controlledOCRApi = {
  status: () => request<ControlledOCRStatus>("/controlled-ocr/status"),
  preview: (payload: ControlledOCRPreviewRequest) =>
    postJson<ControlledOCRPreviewResult>("/controlled-ocr/preview", payload),
  readPreview: (ocrPreviewId: string) =>
    request<ControlledOCRPreviewRecord>(`/controlled-ocr/preview/${encodeURIComponent(ocrPreviewId)}`),
  auditLogs: async () => {
    const response = await request<{ audit_logs: ControlledOCRAuditLog[] }>("/controlled-ocr/audit-logs");
    return response.audit_logs;
  }
};

export const controlledLegalSearchApi = {
  status: () => request<ControlledLegalSearchStatus>("/controlled-legal-search/status"),
  preview: (payload: ControlledLegalSearchPreviewRequest) =>
    postJson<ControlledLegalSearchPreviewResult>("/controlled-legal-search/preview", payload),
  readPreview: (searchPreviewId: string) =>
    request<ControlledLegalSearchPreviewRecord>(`/controlled-legal-search/preview/${encodeURIComponent(searchPreviewId)}`),
  resolveCitation: (payload: ControlledLegalCitationResolutionRequest) =>
    postJson<ControlledLegalCitationResolutionResult>("/controlled-legal-search/resolve-citation", payload),
  auditLogs: async () => {
    const response = await request<{ audit_logs: ControlledLegalSearchAuditLog[] }>("/controlled-legal-search/audit-logs");
    return response.audit_logs;
  }
};

export const controlledReportDraftApi = {
  status: () => request<ControlledReportDraftStatus>("/controlled-report-draft/status"),
  assemble: (payload: ControlledReportDraftAssembleRequest) =>
    postJson<ControlledReportDraftAssembleResult>("/controlled-report-draft/assemble", payload),
  readDraft: (draftId: string) =>
    request<ControlledReportDraftRecord>(`/controlled-report-draft/${encodeURIComponent(draftId)}`),
  auditLogs: async () => {
    const response = await request<{ audit_logs: ControlledReportDraftAuditLog[] }>("/controlled-report-draft/audit-logs");
    return response.audit_logs;
  }
};

export const controlledLawyerReviewApi = {
  status: () => request<ControlledLawyerReviewStatus>("/controlled-review/status"),
  submit: (payload: ControlledLawyerReviewSubmitRequest) =>
    postJson<ControlledLawyerReviewResult>("/controlled-review/submit", payload),
  readReview: (reviewId: string) =>
    request<ControlledLawyerReviewRecord>(`/controlled-review/${encodeURIComponent(reviewId)}`),
  approve: (reviewId: string, payload: ControlledLawyerReviewActionRequest) =>
    postJson<ControlledLawyerReviewResult>(`/controlled-review/${encodeURIComponent(reviewId)}/approve`, payload),
  reject: (reviewId: string, payload: ControlledLawyerReviewActionRequest) =>
    postJson<ControlledLawyerReviewResult>(`/controlled-review/${encodeURIComponent(reviewId)}/reject`, payload),
  requestRevision: (reviewId: string, payload: ControlledLawyerReviewActionRequest) =>
    postJson<ControlledLawyerReviewResult>(`/controlled-review/${encodeURIComponent(reviewId)}/request-revision`, payload),
  auditLogs: async () => {
    const response = await request<{ audit_logs: ControlledLawyerReviewAuditLog[] }>("/controlled-review/audit-logs");
    return response.audit_logs;
  }
};

export const controlledRevisionApi = {
  status: () => request<ControlledRevisionStatus>("/controlled-revision/status"),
  requestRevision: (payload: ControlledRevisionRequest) =>
    postJson<ControlledRevisionResult>("/controlled-revision/request", payload),
  readRevision: (revisionId: string) =>
    request<ControlledRevisionRecord>(`/controlled-revision/${encodeURIComponent(revisionId)}`),
  auditLogs: async () => {
    const response = await request<{ audit_logs: ControlledRevisionAuditLog[] }>("/controlled-revision/audit-logs");
    return response.audit_logs;
  }
};

export const controlledFinalReviewApi = {
  status: () => request<ControlledFinalReviewLockStatus>("/controlled-final-review/status"),
  lock: (payload: ControlledFinalReviewLockRequest) =>
    postJson<ControlledFinalReviewLockResult>("/controlled-final-review/lock", payload),
  readLock: (finalLockId: string) =>
    request<ControlledFinalReviewLockRecord>(`/controlled-final-review/${encodeURIComponent(finalLockId)}`),
  auditLogs: async () => {
    const response = await request<{ audit_logs: ControlledFinalReviewLockAuditLog[] }>("/controlled-final-review/audit-logs");
    return response.audit_logs;
  }
};

export const personalAlphaWorkspaceApi = {
  status: () => request<PersonalAlphaWorkspaceStatus>("/personal-alpha-workspace/status"),
  run: (payload: PersonalAlphaWorkspaceRequest) =>
    postJson<PersonalAlphaWorkspaceRunResult>("/personal-alpha-workspace/run", payload),
  readRun: (workspaceRunId: string) =>
    request<PersonalAlphaWorkspaceRunRecord>(`/personal-alpha-workspace/${encodeURIComponent(workspaceRunId)}`),
  auditLogs: async () => {
    const response = await request<{ audit_logs: PersonalAlphaWorkspaceAuditLog[] }>("/personal-alpha-workspace/audit-logs");
    return response.audit_logs;
  }
};

export const personalAlphaDashboardApi = {
  status: () => request<PersonalAlphaDashboardStatus>("/personal-alpha-dashboard/status"),
  summary: () => request<PersonalAlphaDashboardSummary>("/personal-alpha-dashboard/summary"),
  stageHealth: async () => {
    const response = await request<{ stage_health: PersonalAlphaDashboardStageHealth[] }>("/personal-alpha-dashboard/stage-health");
    return response.stage_health;
  },
  auditTimeline: () => request<PersonalAlphaDashboardAuditTimeline>("/personal-alpha-dashboard/audit-timeline"),
  sourceTraceSummary: () => request<PersonalAlphaDashboardSourceTraceSummary>("/personal-alpha-dashboard/source-trace-summary"),
  getRunDetail: (workspaceRunId: string) =>
    request<PersonalAlphaRunDetail>(`/personal-alpha-dashboard/runs/${encodeURIComponent(workspaceRunId)}`)
};

export const personalAlphaSourceReviewApi = {
  status: () => request<PersonalAlphaSourceReviewStatus>("/personal-alpha-source-review/status"),
  getRunDetail: (workspaceRunId: string) =>
    request<PersonalAlphaSourceReviewRunDetail>(`/personal-alpha-source-review/run/${encodeURIComponent(workspaceRunId)}`),
  getSourceTraces: (workspaceRunId: string) =>
    request<PersonalAlphaSourceTraceResponse>(`/personal-alpha-source-review/run/${encodeURIComponent(workspaceRunId)}/source-traces`),
  getEvidenceSummary: (workspaceRunId: string) =>
    request<PersonalAlphaEvidenceSummaryResponse>(`/personal-alpha-source-review/run/${encodeURIComponent(workspaceRunId)}/evidence-summary`),
  listDecisions: (workspaceRunId: string) =>
    request<PersonalAlphaSourceReviewDecisionList>(`/personal-alpha-source-review/run/${encodeURIComponent(workspaceRunId)}/decisions`),
  submitDecision: (workspaceRunId: string, payload: PersonalAlphaSourceReviewDecisionRequest) =>
    postJson<PersonalAlphaSourceReviewDecisionResult>(`/personal-alpha-source-review/run/${encodeURIComponent(workspaceRunId)}/decisions`, payload),
  getDecisionSummary: (workspaceRunId: string) =>
    request<PersonalAlphaSourceReviewDecisionSummaryResponse>(`/personal-alpha-source-review/run/${encodeURIComponent(workspaceRunId)}/decision-summary`)
};

export const personalAlphaFinalReadinessApi = {
  getStatus: () => request<PersonalAlphaFinalReadinessStatus>("/personal-alpha-final-readiness/status"),
  getRunDetail: (workspaceRunId: string) =>
    request<PersonalAlphaFinalReadinessRunDetail>(`/personal-alpha-final-readiness/run/${encodeURIComponent(workspaceRunId)}`),
  getRunSummary: (workspaceRunId: string) =>
    request<PersonalAlphaFinalReadinessSummaryResponse>(`/personal-alpha-final-readiness/run/${encodeURIComponent(workspaceRunId)}/summary`)
};

export const personalAlphaFinalGateApi = {
  getStatus: () => request<PersonalAlphaFinalGateStatus>("/personal-alpha-final-gate/status"),
  getRunDetail: (workspaceRunId: string) =>
    request<PersonalAlphaFinalGateRunDetail>(`/personal-alpha-final-gate/run/${encodeURIComponent(workspaceRunId)}`),
  getSummary: (workspaceRunId: string) =>
    request<PersonalAlphaFinalGateSummaryResponse>(`/personal-alpha-final-gate/run/${encodeURIComponent(workspaceRunId)}/summary`),
  listDecisions: (workspaceRunId: string) =>
    request<PersonalAlphaFinalGateDecisionList>(`/personal-alpha-final-gate/run/${encodeURIComponent(workspaceRunId)}/decisions`),
  submitDecision: (workspaceRunId: string, payload: PersonalAlphaFinalGateDecisionRequest) =>
    postJson<PersonalAlphaFinalGateDecisionResult>(`/personal-alpha-final-gate/run/${encodeURIComponent(workspaceRunId)}/decisions`, payload)
};

export const personalAlphaFinalPacketApi = {
  getStatus: () => request<PersonalAlphaFinalPacketStatus>("/personal-alpha-final-packet/status"),
  getPreview: (workspaceRunId: string) =>
    request<PersonalAlphaFinalPacketPreview>(`/personal-alpha-final-packet/run/${encodeURIComponent(workspaceRunId)}/preview`),
  createPacket: (workspaceRunId: string, payload: PersonalAlphaFinalPacketCreateRequest) =>
    postJson<PersonalAlphaFinalPacketCreateResult>(`/personal-alpha-final-packet/run/${encodeURIComponent(workspaceRunId)}/create`, payload),
  listPackets: () => request<PersonalAlphaFinalPacketList>("/personal-alpha-final-packet/packets"),
  getPacket: (packetId: string) =>
    request<PersonalAlphaFinalPacketRecord>(`/personal-alpha-final-packet/packets/${encodeURIComponent(packetId)}`),
  listRunPackets: (workspaceRunId: string) =>
    request<PersonalAlphaFinalPacketList>(`/personal-alpha-final-packet/run/${encodeURIComponent(workspaceRunId)}/packets`)
};

export const personalAlphaLawyerFinalReviewApi = {
  getStatus: () => request<PersonalAlphaLawyerFinalReviewStatus>("/personal-alpha-lawyer-final-review/status"),
  getPacketDetail: (packetId: string) =>
    request<PersonalAlphaLawyerFinalReviewPacketDetail>(`/personal-alpha-lawyer-final-review/packets/${encodeURIComponent(packetId)}`),
  getSummary: (packetId: string) =>
    request<{
      packet_id: string;
      workspace_run_id: string;
      summary: PersonalAlphaLawyerFinalReviewSummary;
      mock_or_redacted_only: boolean;
      raw_content_included: boolean;
      final_legal_opinion_generated: boolean;
      final_report_generated: boolean;
      warnings: string[];
    }>(`/personal-alpha-lawyer-final-review/packets/${encodeURIComponent(packetId)}/summary`),
  listActions: (packetId: string) =>
    request<PersonalAlphaLawyerFinalReviewActionList>(`/personal-alpha-lawyer-final-review/packets/${encodeURIComponent(packetId)}/actions`),
  submitAction: (packetId: string, payload: PersonalAlphaLawyerFinalReviewActionRequest) =>
    postJson<PersonalAlphaLawyerFinalReviewActionResult>(`/personal-alpha-lawyer-final-review/packets/${encodeURIComponent(packetId)}/actions`, payload),
  getAction: (actionId: string) =>
    request<PersonalAlphaLawyerFinalReviewActionRecord>(`/personal-alpha-lawyer-final-review/actions/${encodeURIComponent(actionId)}`)
};

export const personalAlphaFinalLockApi = {
  getStatus: () => request<PersonalAlphaFinalLockStatus>("/personal-alpha-final-lock/status"),
  getReadiness: (packetId: string) =>
    request<PersonalAlphaFinalLockReadiness>(`/personal-alpha-final-lock/packets/${encodeURIComponent(packetId)}/readiness`),
  createLock: (packetId: string, payload: PersonalAlphaFinalLockCreateRequest) =>
    postJson<PersonalAlphaFinalLockCreateResult>(`/personal-alpha-final-lock/packets/${encodeURIComponent(packetId)}/create`, payload),
  listLocks: () => request<PersonalAlphaFinalLockList>("/personal-alpha-final-lock/locks"),
  getLock: (lockId: string) =>
    request<PersonalAlphaFinalLockRecord>(`/personal-alpha-final-lock/locks/${encodeURIComponent(lockId)}`),
  listPacketLocks: (packetId: string) =>
    request<PersonalAlphaFinalLockList>(`/personal-alpha-final-lock/packets/${encodeURIComponent(packetId)}/locks`)
};

export const personalAlphaCaseOSApi = {
  getStatus: () => request<PersonalAlphaCaseOSStatus>("/case-os/status"),
  getHardeningStatus: () => request<PersonalAlphaCaseOSHardeningStatus>("/case-os/hardening/status"),
  getReleaseCandidateStatus: () => request<PersonalAlphaCaseOSReleaseCandidateStatus>("/case-os/release-candidate/status"),
  getReleaseCandidateSummary: () => request<PersonalAlphaCaseOSReleaseCandidateSummary>("/case-os/release-candidate/summary"),
  getReleaseCandidateChecklist: () => request<PersonalAlphaCaseOSReleaseCandidateChecklist>("/case-os/release-candidate/checklist"),
  getReleaseCandidateReadiness: () => request<PersonalAlphaCaseOSReleaseCandidateReadiness>("/case-os/release-candidate/readiness"),
  getReleaseCandidateAudit: () => request<PersonalAlphaCaseOSReleaseCandidateAudit>("/case-os/release-candidate/audit"),
  getReleaseCandidateReleaseNotesPreview: () =>
    request<PersonalAlphaCaseOSReleaseNotesPreview>("/case-os/release-candidate/release-notes-preview"),
  listCases: () => request<PersonalAlphaCaseOSCaseListItem[]>("/case-os"),
  getCaseDetail: (caseId: string) =>
    request<PersonalAlphaCaseOSCaseDetail>(`/case-os/${encodeURIComponent(caseId)}`),
  getAuditTimeline: (caseId: string) =>
    request<PersonalAlphaCaseOSAuditTimeline>(`/case-os/${encodeURIComponent(caseId)}/audit-timeline`),
  getUnifiedAuditTimeline: (caseId: string, filters?: Partial<PersonalAlphaCaseOSAuditTimelineFilters>) =>
    request<PersonalAlphaCaseOSUnifiedAuditTimeline>(
      `/case-os/${encodeURIComponent(caseId)}/audit-timeline/unified${buildAuditTimelineQuery(filters)}`
    ),
  getAuditTimelineSummary: (caseId: string) =>
    request<PersonalAlphaCaseOSAuditTimelineSummary>(`/case-os/${encodeURIComponent(caseId)}/audit-timeline/summary`),
  getAuditTimelineRedactionCheck: (caseId: string) =>
    request<PersonalAlphaCaseOSAuditTimelineRedactionCheck>(`/case-os/${encodeURIComponent(caseId)}/audit-timeline/redaction-check`),
  getAuditTimelineFilters: (caseId: string) =>
    request<PersonalAlphaCaseOSAuditTimelineAvailableFilters>(`/case-os/${encodeURIComponent(caseId)}/audit-timeline/filters`),
  getReviewState: (caseId: string) =>
    request<PersonalAlphaCaseOSReviewState>(`/case-os/${encodeURIComponent(caseId)}/review-state`),
  getReviewStateHistory: (caseId: string) =>
    request<PersonalAlphaCaseOSReviewStateHistory>(`/case-os/${encodeURIComponent(caseId)}/review-state/history`),
  getReviewStateTransitions: (caseId: string) =>
    request<PersonalAlphaCaseOSReviewStateTransitions>(`/case-os/${encodeURIComponent(caseId)}/review-state/transitions`),
  validateReviewStateTransition: (caseId: string, fromState: string, toState: string) =>
    request<PersonalAlphaCaseOSReviewStateTransitionValidation>(
      `/case-os/${encodeURIComponent(caseId)}/review-state/validate-transition?from_state=${encodeURIComponent(fromState)}&to_state=${encodeURIComponent(toState)}`
    ),
  getReviewStateSummary: (caseId: string) =>
    request<PersonalAlphaCaseOSReviewStateSummary>(`/case-os/${encodeURIComponent(caseId)}/review-state/summary`),
  getFinalLockConsolidation: (caseId: string) =>
    request<PersonalAlphaCaseOSFinalLockConsolidation>(`/case-os/${encodeURIComponent(caseId)}/final-lock-consolidation`),
  getMetadataClosure: (caseId: string) =>
    request<PersonalAlphaCaseOSMetadataClosure>(`/case-os/${encodeURIComponent(caseId)}/metadata-closure`),
  getMetadataClosureChecklist: (caseId: string) =>
    request<PersonalAlphaCaseOSMetadataClosureChecklist>(`/case-os/${encodeURIComponent(caseId)}/metadata-closure/checklist`),
  getMetadataClosureBlockers: (caseId: string) =>
    request<PersonalAlphaCaseOSMetadataClosureBlockers>(`/case-os/${encodeURIComponent(caseId)}/metadata-closure/blockers`),
  getMetadataClosureExportPreview: (caseId: string) =>
    request<PersonalAlphaCaseOSMetadataClosureExportPreview>(`/case-os/${encodeURIComponent(caseId)}/metadata-closure/export-preview`),
  getExportPackageStatus: (caseId: string) =>
    request<PersonalAlphaCaseOSExportPackageStatus>(`/case-os/${encodeURIComponent(caseId)}/export-packages/status`),
  createExportPackage: (caseId: string, payload: PersonalAlphaCaseOSExportPackageCreateRequest) =>
    postJson<PersonalAlphaCaseOSExportPackageCreateResult>(`/case-os/${encodeURIComponent(caseId)}/export-packages/create`, payload),
  listExportPackages: (caseId: string) =>
    request<PersonalAlphaCaseOSExportPackageList>(`/case-os/${encodeURIComponent(caseId)}/export-packages`),
  getExportPackage: (caseId: string, packageId: string) =>
    request<PersonalAlphaCaseOSExportPackageDetail>(`/case-os/${encodeURIComponent(caseId)}/export-packages/${encodeURIComponent(packageId)}`),
  getExportPackageContent: (caseId: string, packageId: string) =>
    request<PersonalAlphaCaseOSExportPackageContent>(`/case-os/${encodeURIComponent(caseId)}/export-packages/${encodeURIComponent(packageId)}/content`),
  getExportPackageSafetyCheck: (caseId: string, packageId: string) =>
    request<PersonalAlphaCaseOSExportPackageSafetyCheck>(`/case-os/${encodeURIComponent(caseId)}/export-packages/${encodeURIComponent(packageId)}/safety-check`),
  getExportPackageSummary: (caseId: string) =>
    request<PersonalAlphaCaseOSExportPackageSummary>(`/case-os/${encodeURIComponent(caseId)}/export-packages/summary`),
  getQualityStatus: (caseId: string) =>
    request<PersonalAlphaCaseOSQualityStatus>(`/case-os/${encodeURIComponent(caseId)}/quality/status`),
  getQualityChecklist: (caseId: string) =>
    request<PersonalAlphaCaseOSQualityChecklist>(`/case-os/${encodeURIComponent(caseId)}/quality/checklist`),
  getQualityScore: (caseId: string) =>
    request<PersonalAlphaCaseOSQualityScore>(`/case-os/${encodeURIComponent(caseId)}/quality/score`),
  getQualityFindings: (caseId: string) =>
    request<PersonalAlphaCaseOSQualityFindings>(`/case-os/${encodeURIComponent(caseId)}/quality/findings`),
  getQualityRecommendations: (caseId: string) =>
    request<PersonalAlphaCaseOSQualityRecommendations>(`/case-os/${encodeURIComponent(caseId)}/quality/recommendations`),
  getQualityReportPreview: (caseId: string) =>
    request<PersonalAlphaCaseOSQualityReportPreview>(`/case-os/${encodeURIComponent(caseId)}/quality/report-preview`),
  getQualitySummary: (caseId: string) =>
    request<PersonalAlphaCaseOSQualitySummary>(`/case-os/${encodeURIComponent(caseId)}/quality/summary`),
  getHardeningSafetyCheck: (caseId: string) =>
    request<PersonalAlphaCaseOSHardeningSafetyCheck>(`/case-os/${encodeURIComponent(caseId)}/hardening/safety-check`),
  getHardeningResponseConsistency: (caseId: string) =>
    request<PersonalAlphaCaseOSResponseConsistency>(`/case-os/${encodeURIComponent(caseId)}/hardening/response-consistency`),
  getHardeningRuntimeStorageCheck: (caseId: string) =>
    request<PersonalAlphaCaseOSRuntimeStorageCheck>(`/case-os/${encodeURIComponent(caseId)}/hardening/runtime-storage-check`),
  getReleaseCandidateCaseReadiness: (caseId: string) =>
    request<PersonalAlphaCaseOSReleaseCandidateCaseReadiness>(`/case-os/${encodeURIComponent(caseId)}/release-candidate/case-readiness`),
  getNextAction: (caseId: string) =>
    request<PersonalAlphaCaseOSNextAction>(`/case-os/${encodeURIComponent(caseId)}/next-action`),
  getStageOrchestration: (caseId: string) =>
    request<PersonalAlphaCaseOSStageOrchestration>(`/case-os/${encodeURIComponent(caseId)}/stage-orchestration`),
  getStageTransitions: (caseId: string) =>
    request<PersonalAlphaCaseOSStageTransitions>(`/case-os/${encodeURIComponent(caseId)}/stage-transitions`),
  getActionEligibility: (caseId: string) =>
    request<PersonalAlphaCaseOSActionEligibility>(`/case-os/${encodeURIComponent(caseId)}/action-eligibility`),
  getBlockers: (caseId: string) =>
    request<PersonalAlphaCaseOSBlockers>(`/case-os/${encodeURIComponent(caseId)}/blockers`),
  getSafetyChecklist: (caseId: string) =>
    request<{
      case_id: string;
      safety_checklist: PersonalAlphaCaseOSSafetyChecklist;
      mock_or_redacted_only: boolean;
      raw_content_included: boolean;
      warnings: string[];
    }>(`/case-os/${encodeURIComponent(caseId)}/safety-checklist`)
};

export const personalProductionApi = {
  getStatus: () => request<PersonalProductionStatus>("/personal-production/status"),
  getMode: () => request<PersonalProductionMode>("/personal-production/mode"),
  getShowcase: () => request<PersonalProductionShowcase>("/personal-production/showcase"),
  getRuntimeRegistry: () => request<PersonalProductionRuntimeRegistry>("/personal-production/runtime-registry"),
  getProviderCapabilities: () => request<PersonalProductionProviderCapabilities>("/personal-production/provider-capabilities"),
  getReadiness: () => request<PersonalProductionReadiness>("/personal-production/readiness"),
  getSafety: () => request<PersonalProductionSafety>("/personal-production/safety"),
  getConsoleSummary: () => request<PersonalProductionConsoleSummary>("/personal-production/console-summary")
};

export const personalAIGatewayApi = {
  getStatus: () => request<PersonalAIGatewayStatus>("/personal-ai-gateway/status"),
  getProviders: () => request<PersonalAIProviderList>("/personal-ai-gateway/providers"),
  getProvider: (providerId: string) =>
    request<PersonalAIProvider>(`/personal-ai-gateway/providers/${encodeURIComponent(providerId)}`),
  getPromptTemplates: () => request<PersonalAIPromptTemplateList>("/personal-ai-gateway/prompt-templates"),
  getPromptTemplate: (templateId: string) =>
    request<PersonalAIPromptTemplate>(`/personal-ai-gateway/prompt-templates/${encodeURIComponent(templateId)}`),
  renderPromptPreview: (payload: PersonalAIPromptRenderPreviewRequest) =>
    postJson<PersonalAIPromptRenderPreviewResult>("/personal-ai-gateway/prompt-render-preview", payload),
  createMockRun: (payload: PersonalAIMockRunRequest) =>
    postJson<PersonalAIMockRunResult>("/personal-ai-gateway/runs/mock", payload),
  listRuns: () => request<PersonalAIRunList>("/personal-ai-gateway/runs"),
  getRun: (aiRunId: string) =>
    request<PersonalAIRunRecord>(`/personal-ai-gateway/runs/${encodeURIComponent(aiRunId)}`),
  getAudit: () => request<PersonalAIAuditTimeline>("/personal-ai-gateway/audit"),
  getTokenUsageSummary: () => request<PersonalAITokenUsageSummary>("/personal-ai-gateway/token-usage/summary"),
  getSafety: () => request<PersonalAISafetyStatus>("/personal-ai-gateway/safety"),
  getLiveStatus: () => request<PersonalAILiveGatewayStatus>("/personal-ai-gateway/live/status"),
  getLiveProviders: () => request<PersonalAILiveProviderConfigList>("/personal-ai-gateway/live/providers"),
  getLiveProvider: (providerId: string) =>
    request<PersonalAILiveProviderConfig>(`/personal-ai-gateway/live/providers/${encodeURIComponent(providerId)}`),
  createLiveDryRun: (payload: PersonalAILiveRunRequest) =>
    postJson<PersonalAILiveRunRecord>("/personal-ai-gateway/live/dry-run", payload),
  createLiveRun: (payload: PersonalAILiveRunRequest) =>
    postJson<PersonalAILiveRunRecord>("/personal-ai-gateway/live/runs", payload),
  listLiveRuns: () => request<PersonalAILiveRunList>("/personal-ai-gateway/live/runs"),
  getLiveRun: (runId: string) =>
    request<PersonalAILiveRunRecord>(`/personal-ai-gateway/live/runs/${encodeURIComponent(runId)}`),
  getLiveAudit: () => request<PersonalAILiveAuditTimeline>("/personal-ai-gateway/live/audit"),
  getLiveSafety: () => request<PersonalAILiveSafetyStatus>("/personal-ai-gateway/live/safety")
};

export const personalMaterialRuntimeApi = {
  getStatus: () => request<PersonalMaterialRuntimeStatus>("/personal-material-runtime/status"),
  getProviders: () => request<PersonalMaterialProviderList>("/personal-material-runtime/providers"),
  getProvider: (providerId: string) =>
    request<PersonalMaterialProvider>(`/personal-material-runtime/providers/${encodeURIComponent(providerId)}`),
  createMockParseJob: (payload: PersonalMaterialParseJobRequest) =>
    postJson<PersonalMaterialParseJobResult>("/personal-material-runtime/parse-jobs/mock", payload),
  listParseJobs: () => request<PersonalMaterialParseJobList>("/personal-material-runtime/parse-jobs"),
  getParseJob: (parseJobId: string) =>
    request<PersonalMaterialParseJobRecord>(`/personal-material-runtime/parse-jobs/${encodeURIComponent(parseJobId)}`),
  createMockOCRJob: (payload: PersonalOCRJobRequest) =>
    postJson<PersonalOCRJobResult>("/personal-material-runtime/ocr-jobs/mock", payload),
  listOCRJobs: () => request<PersonalOCRJobList>("/personal-material-runtime/ocr-jobs"),
  getOCRJob: (ocrJobId: string) =>
    request<PersonalOCRJobRecord>(`/personal-material-runtime/ocr-jobs/${encodeURIComponent(ocrJobId)}`),
  getOCRPreview: (ocrJobId: string) =>
    request<PersonalOCRPreview>(`/personal-material-runtime/ocr-jobs/${encodeURIComponent(ocrJobId)}/preview`),
  getOCRReviewQueue: () => request<PersonalOCRReviewQueue>("/personal-material-runtime/ocr-review-queue"),
  submitOCRReviewAction: (ocrJobId: string, payload: PersonalOCRReviewActionRequest) =>
    postJson<PersonalOCRReviewActionResult>(
      `/personal-material-runtime/ocr-review-queue/${encodeURIComponent(ocrJobId)}/actions`,
      payload
    ),
  getSourceTraces: () => request<PersonalMaterialSourceTraceList>("/personal-material-runtime/source-traces"),
  getAudit: () => request<PersonalMaterialAuditTimeline>("/personal-material-runtime/audit"),
  getSafety: () => request<PersonalMaterialSafetyStatus>("/personal-material-runtime/safety"),
  getLiveStatus: () => request<PersonalMaterialLiveGatewayStatus>("/personal-material-runtime/live/status"),
  getLiveProviders: () => request<PersonalMaterialLiveProviderReadinessList>("/personal-material-runtime/live/providers"),
  getLiveProvider: (providerId: string) =>
    request<PersonalMaterialLiveProviderReadiness>(`/personal-material-runtime/live/providers/${encodeURIComponent(providerId)}`),
  getLiveSecretBoundary: (providerId: string) =>
    request<PersonalMaterialLiveSecretBoundary>(
      `/personal-material-runtime/live/providers/${encodeURIComponent(providerId)}/secret-boundary`
    ),
  getLiveGate: (providerId: string) =>
    request<PersonalMaterialLiveGateStatus>(`/personal-material-runtime/live/providers/${encodeURIComponent(providerId)}/live-gate`),
  getLiveHealthDryRun: (providerId: string) =>
    request<PersonalMaterialLiveHealthDryRun>(
      `/personal-material-runtime/live/providers/${encodeURIComponent(providerId)}/health/dry-run`
    ),
  createLiveGateMock: (payload: PersonalMaterialLiveGateMockRequest) =>
    postJson<PersonalMaterialLiveGateStatus>("/personal-material-runtime/live-gates/mock", payload),
  listLiveGates: () => request<PersonalMaterialLiveGateList>("/personal-material-runtime/live-gates"),
  createDocumentLiveDryRun: (payload: PersonalMaterialLiveRunRequest) =>
    postJson<PersonalMaterialLiveRunRecord>("/personal-material-runtime/live/document/dry-run", payload),
  createDocumentLiveRun: (payload: PersonalMaterialLiveRunRequest) =>
    postJson<PersonalMaterialLiveRunRecord>("/personal-material-runtime/live/document/runs", payload),
  listDocumentLiveRuns: () => request<PersonalMaterialLiveRunList>("/personal-material-runtime/live/document/runs"),
  getDocumentLiveRun: (runId: string) =>
    request<PersonalMaterialLiveRunRecord>(`/personal-material-runtime/live/document/runs/${encodeURIComponent(runId)}`),
  createOCRLiveDryRun: (payload: PersonalMaterialLiveRunRequest) =>
    postJson<PersonalMaterialLiveRunRecord>("/personal-material-runtime/live/ocr/dry-run", payload),
  createOCRLiveRun: (payload: PersonalMaterialLiveRunRequest) =>
    postJson<PersonalMaterialLiveRunRecord>("/personal-material-runtime/live/ocr/runs", payload),
  listOCRLiveRuns: () => request<PersonalMaterialLiveRunList>("/personal-material-runtime/live/ocr/runs"),
  getOCRLiveRun: (runId: string) =>
    request<PersonalMaterialLiveRunRecord>(`/personal-material-runtime/live/ocr/runs/${encodeURIComponent(runId)}`),
  getLiveReviewQueue: () => request<PersonalMaterialLiveReviewQueue>("/personal-material-runtime/live/review-queue"),
  submitLiveReviewAction: (reviewItemId: string, payload: PersonalMaterialLiveReviewActionRequest) =>
    postJson<PersonalMaterialLiveReviewActionResult>(
      `/personal-material-runtime/live/review-queue/${encodeURIComponent(reviewItemId)}/actions`,
      payload
    ),
  getLiveSourceTraces: () => request<PersonalMaterialLiveSourceTraceList>("/personal-material-runtime/live/source-traces"),
  getLiveAudit: () => request<PersonalMaterialLiveAuditTimeline>("/personal-material-runtime/live/audit"),
  getLiveSafety: () => request<PersonalMaterialLiveSafetyStatus>("/personal-material-runtime/live/safety")
};

export const personalIntelligenceApi = {
  getStatus: () => request<PersonalIntelligenceStatus>("/personal-intelligence/status"),
  getProviders: () => request<PersonalIntelligenceProviderList>("/personal-intelligence/providers"),
  getProvider: (providerId: string) =>
    request<PersonalIntelligenceProvider>(`/personal-intelligence/providers/${encodeURIComponent(providerId)}`),
  createMockLegalSearch: (payload: PersonalLegalSearchMockRequest) =>
    postJson<PersonalLegalSearchResult>("/personal-intelligence/legal-search/mock", payload),
  listLegalSearch: () => request<PersonalLegalSearchList>("/personal-intelligence/legal-search"),
  getLegalSearch: (legalSearchId: string) =>
    request<PersonalLegalSearchResult>(`/personal-intelligence/legal-search/${encodeURIComponent(legalSearchId)}`),
  createMockEnterpriseQuery: (payload: PersonalEnterpriseQueryMockRequest) =>
    postJson<PersonalEnterpriseQueryResult>("/personal-intelligence/enterprise-query/mock", payload),
  listEnterpriseQuery: () => request<PersonalEnterpriseQueryList>("/personal-intelligence/enterprise-query"),
  getEnterpriseQuery: (enterpriseQueryId: string) =>
    request<PersonalEnterpriseQueryResult>(`/personal-intelligence/enterprise-query/${encodeURIComponent(enterpriseQueryId)}`),
  listSourceTraces: () => request<PersonalIntelligenceSourceTraceList>("/personal-intelligence/source-traces"),
  getSourceTrace: (sourceTraceId: string) =>
    request<PersonalIntelligenceSourceTrace>(`/personal-intelligence/source-traces/${encodeURIComponent(sourceTraceId)}`),
  getConfirmationQueue: () => request<PersonalIntelligenceSourceTraceList>("/personal-intelligence/confirmation-queue"),
  submitConfirmationAction: (sourceTraceId: string, payload: PersonalIntelligenceConfirmationActionRequest) =>
    postJson<PersonalIntelligenceConfirmationActionResult>(
      `/personal-intelligence/confirmation-queue/${encodeURIComponent(sourceTraceId)}/actions`,
      payload
    ),
  getAudit: () => request<PersonalIntelligenceAuditTimeline>("/personal-intelligence/audit"),
  getSafety: () => request<PersonalIntelligenceSafetyStatus>("/personal-intelligence/safety"),
  getLiveStatus: () => request<PersonalIntelligenceLiveGatewayStatus>("/personal-intelligence/live/status"),
  getLiveProviders: () => request<PersonalIntelligenceLiveProviderConfigList>("/personal-intelligence/live/providers"),
  getLiveProvider: (providerId: string) =>
    request<PersonalIntelligenceLiveProviderConfig>(`/personal-intelligence/live/providers/${encodeURIComponent(providerId)}`),
  createLegalLiveDryRun: (payload: PersonalIntelligenceLiveRunRequest) =>
    postJson<PersonalIntelligenceLiveRunRecord>("/personal-intelligence/live/legal-search/dry-run", payload),
  createLegalLiveRun: (payload: PersonalIntelligenceLiveRunRequest) =>
    postJson<PersonalIntelligenceLiveRunRecord>("/personal-intelligence/live/legal-search/runs", payload),
  listLegalLiveRuns: () => request<PersonalIntelligenceLiveRunList>("/personal-intelligence/live/legal-search/runs"),
  getLegalLiveRun: (runId: string) =>
    request<PersonalIntelligenceLiveRunRecord>(`/personal-intelligence/live/legal-search/runs/${encodeURIComponent(runId)}`),
  createEnterpriseLiveDryRun: (payload: PersonalIntelligenceLiveRunRequest) =>
    postJson<PersonalIntelligenceLiveRunRecord>("/personal-intelligence/live/enterprise-query/dry-run", payload),
  createEnterpriseLiveRun: (payload: PersonalIntelligenceLiveRunRequest) =>
    postJson<PersonalIntelligenceLiveRunRecord>("/personal-intelligence/live/enterprise-query/runs", payload),
  listEnterpriseLiveRuns: () => request<PersonalIntelligenceLiveRunList>("/personal-intelligence/live/enterprise-query/runs"),
  getEnterpriseLiveRun: (runId: string) =>
    request<PersonalIntelligenceLiveRunRecord>(`/personal-intelligence/live/enterprise-query/runs/${encodeURIComponent(runId)}`),
  getLiveReviewQueue: () => request<PersonalIntelligenceLiveReviewQueue>("/personal-intelligence/live/review-queue"),
  submitLiveReviewAction: (reviewItemId: string, payload: PersonalIntelligenceLiveReviewActionRequest) =>
    postJson<PersonalIntelligenceLiveReviewActionResult>(
      `/personal-intelligence/live/review-queue/${encodeURIComponent(reviewItemId)}/actions`,
      payload
    ),
  listLiveSourceTraces: () => request<PersonalIntelligenceLiveSourceTraceList>("/personal-intelligence/live/source-traces"),
  getLiveSourceTrace: (sourceTraceId: string) =>
    request<PersonalIntelligenceLiveSourceTrace>(`/personal-intelligence/live/source-traces/${encodeURIComponent(sourceTraceId)}`),
  getLiveAudit: () => request<PersonalIntelligenceLiveAuditTimeline>("/personal-intelligence/live/audit"),
  getLiveSafety: () => request<PersonalIntelligenceLiveSafetyStatus>("/personal-intelligence/live/safety")
};

export const personalSkillStudioApi = {
  getStatus: () => request<PersonalSkillStudioStatus>("/personal-skill-studio/status"),
  getSkillTrainingStatus: () => request<SkillTrainingRuntimeStatus>("/personal-skill-studio/skill-training/status"),
  getSkillSampleRegistry: () => request<SkillSampleRegistry>("/personal-skill-studio/skill-training/sample-registry"),
  listRuntimes: () => request<PersonalSkillStudioRuntimeList>("/personal-skill-studio/runtimes"),
  getRuntime: (runtimeId: string) =>
    request<PersonalSkillStudioRuntime>(`/personal-skill-studio/runtimes/${encodeURIComponent(runtimeId)}`),
  createExperiencePackage: (payload: ExperiencePackageMockRequest) =>
    postJson<ExperiencePackageDraft>("/personal-skill-studio/experience-packages/mock", payload),
  listExperiencePackages: () => request<ExperiencePackageDraftList>("/personal-skill-studio/experience-packages"),
  getExperiencePackage: (id: string) => request<ExperiencePackageDraft>(`/personal-skill-studio/experience-packages/${encodeURIComponent(id)}`),
  createSkillCandidate: (payload: SkillCandidateMockRequest) =>
    postJson<SkillCandidateDraft>("/personal-skill-studio/skill-candidates/mock", payload),
  listSkillCandidates: () => request<SkillCandidateDraftList>("/personal-skill-studio/skill-candidates"),
  getSkillCandidate: (id: string) => request<SkillCandidateDraft>(`/personal-skill-studio/skill-candidates/${encodeURIComponent(id)}`),
  createTestCase: (payload: TestCaseMockRequest) => postJson<SkillTestCaseDraft>("/personal-skill-studio/test-cases/mock", payload),
  listTestCases: () => request<SkillTestCaseDraftList>("/personal-skill-studio/test-cases"),
  getTestCase: (id: string) => request<SkillTestCaseDraft>(`/personal-skill-studio/test-cases/${encodeURIComponent(id)}`),
  createEvaluation: (payload: EvaluationMockRequest) => postJson<SkillEvaluationDraft>("/personal-skill-studio/evaluations/mock", payload),
  listEvaluations: () => request<SkillEvaluationDraftList>("/personal-skill-studio/evaluations"),
  getEvaluation: (id: string) => request<SkillEvaluationDraft>(`/personal-skill-studio/evaluations/${encodeURIComponent(id)}`),
  getPromotionQueue: () => request<SkillCandidateDraftList>("/personal-skill-studio/promotion-queue"),
  submitPromotionAction: (skillCandidateId: string, payload: PromotionActionRequest) =>
    postJson<PromotionActionResult>(`/personal-skill-studio/promotion-queue/${encodeURIComponent(skillCandidateId)}/actions`, payload),
  listFinalDrafts: () => request<SkillStudioFinalDraftList>("/personal-skill-studio/final-drafts"),
  getFinalDraft: (skillId: string) => request<SkillStudioFinalDraft>(`/personal-skill-studio/final-drafts/${encodeURIComponent(skillId)}`),
  getFinalDraftLineage: (skillId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/final-drafts/${encodeURIComponent(skillId)}/lineage`),
  getFinalDraftBaseline: (skillId: string) =>
    request<SkillStudioBaselineDiscovery>(`/personal-skill-studio/final-drafts/${encodeURIComponent(skillId)}/baseline`),
  getFinalDraftQuality: (skillId: string) =>
    request<SkillStudioFinalQuality>(`/personal-skill-studio/final-drafts/${encodeURIComponent(skillId)}/quality`),
  getFinalDraftGate: (skillId: string) =>
    request<SkillStudioFinalGate>(`/personal-skill-studio/final-drafts/${encodeURIComponent(skillId)}/gate`),
  getFinalDraftOptimization: (skillId: string) =>
    request<SkillStudioFinalOptimization>(`/personal-skill-studio/final-drafts/${encodeURIComponent(skillId)}/optimization`),
  getFinalDraftSourceTraces: (skillId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/final-drafts/${encodeURIComponent(skillId)}/source-traces`),
  getFinalDraftAudit: (skillId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/final-drafts/${encodeURIComponent(skillId)}/audit`),
  createFinalDraftOwnerDownload: (skillId: string, payload: SkillStudioFinalOwnerDownloadRequest) =>
    postJson<SkillStudioFinalOwnerDownload>(`/personal-skill-studio/final-drafts/${encodeURIComponent(skillId)}/owner-downloads/mock`, payload),
  listFinalDraftOwnerDownloads: () => request<SkillStudioFinalOwnerDownloadList>("/personal-skill-studio/final-draft-downloads"),
  getFinalDraftOwnerDownload: (downloadId: string) =>
    request<SkillStudioFinalOwnerDownload>(`/personal-skill-studio/final-draft-downloads/${encodeURIComponent(downloadId)}`),
  getFinalDraftSafety: () => request<SkillStudioSafetyStatus>("/personal-skill-studio/final-drafts-safety"),
  getTrainingArtifactStatus: () => request<TrainingArtifactStatus>("/personal-skill-studio/training-artifacts/status"),
  getTrainingArtifactScheme: () => request<CodexTrainingScheme>("/personal-skill-studio/training-artifacts/scheme"),
  getTrainingArtifactCaseCauseTaxonomy: () =>
    request<CaseCauseTaxonomyManifest>("/personal-skill-studio/training-artifacts/case-cause-taxonomy"),
  getTrainingArtifactCaseCauseNode: (caseCauseId: string) =>
    request<CaseCauseNode>(`/personal-skill-studio/training-artifacts/case-cause-taxonomy/${encodeURIComponent(caseCauseId)}`),
  listTrainingArtifactPackages: () => request<TrainingArtifactManifestList>("/personal-skill-studio/training-artifacts/packages"),
  getTrainingArtifactPackage: (packageId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/packages/${encodeURIComponent(packageId)}`),
  listTrainingArtifactSkills: () => request<TrainingArtifactManifestList>("/personal-skill-studio/training-artifacts/skills"),
  getTrainingArtifactSkill: (skillId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/skills/${encodeURIComponent(skillId)}`),
  listTrainingArtifactEvaluations: () => request<TrainingArtifactManifestList>("/personal-skill-studio/training-artifacts/evaluations"),
  listTrainingArtifactGates: () => request<TrainingArtifactManifestList>("/personal-skill-studio/training-artifacts/gates"),
  listTrainingArtifactTestCases: () => request<TrainingArtifactManifestList>("/personal-skill-studio/training-artifacts/test-cases"),
  listTrainingArtifactLoadingManifests: () =>
    request<TrainingArtifactManifestList>("/personal-skill-studio/training-artifacts/loading-manifests"),
  matchTrainingArtifactCaseCause: (payload: TrainingArtifactCaseCauseMatchRequest) =>
    postJson<TrainingArtifactCaseCauseMatchResult>("/personal-skill-studio/training-artifacts/case-cause-match/mock", payload),
  createTrainingArtifactLoadDryRun: (payload: TrainingArtifactLoadDryRunRequest) =>
    postJson<TrainingArtifactLoadDryRun>("/personal-skill-studio/training-artifacts/load-dry-run/mock", payload),
  listTrainingArtifactLoadDryRuns: () => request<TrainingArtifactLoadDryRunList>("/personal-skill-studio/training-artifacts/load-dry-runs"),
  getTrainingArtifactLoadDryRun: (runId: string) =>
    request<TrainingArtifactLoadDryRun>(`/personal-skill-studio/training-artifacts/load-dry-runs/${encodeURIComponent(runId)}`),
  listTrainingArtifactSkillContexts: () =>
    request<TrainingArtifactSkillContextList>("/personal-skill-studio/training-artifacts/skill-contexts"),
  getTrainingArtifactSkillContext: (skillContextId: string) =>
    request<TrainingArtifactSkillContext>(`/personal-skill-studio/training-artifacts/skill-contexts/${encodeURIComponent(skillContextId)}`),
  getTrainingArtifactAudit: () => request<Record<string, unknown>>("/personal-skill-studio/training-artifacts/audit"),
  getTrainingArtifactSafety: () => request<TrainingArtifactSafetyStatus>("/personal-skill-studio/training-artifacts/safety"),
  listCodexTrainingRuns: () => request<CodexTrainingRunList>("/personal-skill-studio/training-artifacts/training-runs"),
  createCodexTrainingRun: (payload: CodexTrainingRunRequest) =>
    postJson<CodexTrainingRun>("/personal-skill-studio/training-artifacts/training-runs/mock", payload),
  getCodexTrainingRun: (runId: string) =>
    request<CodexTrainingRun>(`/personal-skill-studio/training-artifacts/training-runs/${encodeURIComponent(runId)}`),
  getCodexTrainingRunSummary: (runId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/training-runs/${encodeURIComponent(runId)}/summary`),
  getCodexTrainingRunCaseCausePackages: (runId: string) =>
    request<TrainingArtifactManifestList>(`/personal-skill-studio/training-artifacts/training-runs/${encodeURIComponent(runId)}/case-cause-packages`),
  getCodexTrainingRunGeneratedSkills: (runId: string) =>
    request<TrainingArtifactManifestList>(`/personal-skill-studio/training-artifacts/training-runs/${encodeURIComponent(runId)}/generated-skills`),
  getCodexTrainingRunEvaluations: (runId: string) =>
    request<TrainingArtifactManifestList>(`/personal-skill-studio/training-artifacts/training-runs/${encodeURIComponent(runId)}/evaluations`),
  getCodexTrainingRunGates: (runId: string) =>
    request<TrainingArtifactManifestList>(`/personal-skill-studio/training-artifacts/training-runs/${encodeURIComponent(runId)}/gates`),
  getCodexTrainingRunTestCases: (runId: string) =>
    request<TrainingArtifactManifestList>(`/personal-skill-studio/training-artifacts/training-runs/${encodeURIComponent(runId)}/test-cases`),
  getCodexTrainingRunLoadingManifest: (runId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/training-runs/${encodeURIComponent(runId)}/loading-manifest`),
  createCodexTrainingRunLoadDryRun: (runId: string) =>
    postJson<CodexTrainingRunLoadDryRunResult>(`/personal-skill-studio/training-artifacts/training-runs/${encodeURIComponent(runId)}/load-dry-run/mock`, {}),
  getCodexTrainingRunAudit: (runId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/training-runs/${encodeURIComponent(runId)}/audit`),
  getCodexTrainingRunSafety: (runId: string) =>
    request<TrainingArtifactSafetyStatus>(`/personal-skill-studio/training-artifacts/training-runs/${encodeURIComponent(runId)}/safety`),
  getRealClosedCaseIntakeStatus: () =>
    request<RealClosedCaseIntakeStatus>("/personal-skill-studio/training-artifacts/real-closed-case-intake/status"),
  createRealClosedCaseIntake: (payload: RealClosedCaseTrainingIntakeRequest) =>
    postJson<RealClosedCaseTrainingIntakeRecord>("/personal-skill-studio/training-artifacts/real-closed-case-intake/mock", payload),
  listRealClosedCaseIntakes: () =>
    request<RealClosedCaseTrainingIntakeList>("/personal-skill-studio/training-artifacts/real-closed-case-intakes"),
  getRealClosedCaseIntake: (intakeId: string) =>
    request<RealClosedCaseTrainingIntakeRecord>(`/personal-skill-studio/training-artifacts/real-closed-case-intakes/${encodeURIComponent(intakeId)}`),
  getRealClosedCaseRedactionReport: (intakeId: string) =>
    request<RedactionReport>(`/personal-skill-studio/training-artifacts/real-closed-case-intakes/${encodeURIComponent(intakeId)}/redaction-report`),
  createRealClosedCaseRedaction: (intakeId: string) =>
    postJson<RedactionReport>(`/personal-skill-studio/training-artifacts/real-closed-case-intakes/${encodeURIComponent(intakeId)}/redaction/mock`, {}),
  getRealClosedCaseClassification: (intakeId: string) =>
    request<CaseCauseClassification>(`/personal-skill-studio/training-artifacts/real-closed-case-intakes/${encodeURIComponent(intakeId)}/case-cause-classification`),
  createRealClosedCaseClassification: (intakeId: string) =>
    postJson<CaseCauseClassification>(`/personal-skill-studio/training-artifacts/real-closed-case-intakes/${encodeURIComponent(intakeId)}/case-cause-classification/mock`, {}),
  getRealClosedCaseSegments: (intakeId: string) =>
    request<Record<string, unknown> & { segments: TrainingSampleSegment[] }>(`/personal-skill-studio/training-artifacts/real-closed-case-intakes/${encodeURIComponent(intakeId)}/segments`),
  createRealClosedCaseSegments: (intakeId: string) =>
    postJson<Record<string, unknown> & { segments: TrainingSampleSegment[] }>(`/personal-skill-studio/training-artifacts/real-closed-case-intakes/${encodeURIComponent(intakeId)}/segments/mock`, {}),
  getRealClosedCaseReviewQueue: (intakeId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/real-closed-case-intakes/${encodeURIComponent(intakeId)}/review-queue`),
  submitRealClosedCaseReviewAction: (intakeId: string, reviewItemId: string, payload: Record<string, unknown>) =>
    postJson<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/real-closed-case-intakes/${encodeURIComponent(intakeId)}/review-queue/${encodeURIComponent(reviewItemId)}/actions/mock`, payload),
  getRealClosedCaseSourceTraces: (intakeId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/real-closed-case-intakes/${encodeURIComponent(intakeId)}/source-traces`),
  getRealClosedCaseAudit: (intakeId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/real-closed-case-intakes/${encodeURIComponent(intakeId)}/audit`),
  getRealClosedCaseSafety: (intakeId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/real-closed-case-intakes/${encodeURIComponent(intakeId)}/safety`),
  getRawWorkProductBoundaryStatus: () =>
    request<RawWorkProductBoundaryStatus>("/personal-skill-studio/training-artifacts/raw-work-product-boundary/status"),
  createOcrJob: (payload: OcrJobRequest) =>
    postJson<Record<string, unknown>>("/personal-skill-studio/training-artifacts/ocr-jobs", payload),
  listOcrJobs: () =>
    request<OcrJobList>("/personal-skill-studio/training-artifacts/ocr-jobs"),
  getOcrJob: (jobId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/ocr-jobs/${encodeURIComponent(jobId)}`),
  createLegalRetrievalJob: (payload: LegalRetrievalJobRequest) =>
    postJson<Record<string, unknown>>("/personal-skill-studio/training-artifacts/legal-retrieval-jobs", payload),
  listLegalRetrievalJobs: () =>
    request<LegalRetrievalJobList>("/personal-skill-studio/training-artifacts/legal-retrieval-jobs"),
  getLegalRetrievalJob: (jobId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/legal-retrieval-jobs/${encodeURIComponent(jobId)}`),
  buildExperienceCandidates: (payload: ExperienceCandidateBuildRequest) =>
    postJson<ExperienceCandidateList>("/personal-skill-studio/training-artifacts/experience-candidates/build", payload),
  listExperienceCandidates: () =>
    request<ExperienceCandidateList>("/personal-skill-studio/training-artifacts/experience-candidates"),
  getExperienceCandidate: (candidateId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/experience-candidates/${encodeURIComponent(candidateId)}`),
  redactExperienceCandidate: (candidateId: string) =>
    postJson<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/experience-candidates/${encodeURIComponent(candidateId)}/redact`, {}),
  reviewExperienceCandidate: (candidateId: string, payload: ExperienceCandidateReviewRequest) =>
    postJson<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/experience-candidates/${encodeURIComponent(candidateId)}/review`, payload),
  getExperienceCandidateAudit: (candidateId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/experience-candidates/${encodeURIComponent(candidateId)}/audit`),
  getV731bTrainingExperiencePipelineStatus: () =>
    request<V731bTrainingExperiencePipelineStatus>("/personal-skill-studio/training-artifacts/v7-31b/status"),
  getSkillExperiencePoolStatus: () =>
    request<SkillExperiencePoolStatus>("/personal-skill-studio/training-artifacts/skill-experience-pool/status"),
  importApprovedSkillExperience: (payload: SkillExperienceImportRequest) =>
    postJson<SkillExperienceImportResponse>("/personal-skill-studio/training-artifacts/skill-experience-pool/import-approved", payload),
  listSkillExperiencePool: () =>
    request<SkillExperiencePoolList>("/personal-skill-studio/training-artifacts/skill-experience-pool"),
  getSkillExperiencePoolEntry: (experienceId: string) =>
    request<SkillExperiencePoolEntry>(`/personal-skill-studio/training-artifacts/skill-experience-pool/${encodeURIComponent(experienceId)}`),
  createSkillExperienceBinding: (payload: SkillExperienceBindingRequest) =>
    postJson<SkillExperienceBinding>("/personal-skill-studio/training-artifacts/skill-experience-bindings", payload),
  listSkillExperienceBindings: () =>
    request<SkillExperienceBindingList>("/personal-skill-studio/training-artifacts/skill-experience-bindings"),
  getSkillExperienceBinding: (bindingId: string) =>
    request<SkillExperienceBinding>(`/personal-skill-studio/training-artifacts/skill-experience-bindings/${encodeURIComponent(bindingId)}`),
  listCodexSkillDrafts: () =>
    request<CodexSkillDraftList>("/personal-skill-studio/training-artifacts/codex-skill-drafts"),
  buildCodexSkillDraft: (payload: CodexSkillDraftBuildRequest) =>
    postJson<CodexSkillDraftBuildResponse>("/personal-skill-studio/training-artifacts/codex-skill-drafts/build", payload),
  getCodexSkillDraft: (draftId: string) =>
    request<CodexSkillDraft>(`/personal-skill-studio/training-artifacts/codex-skill-drafts/${encodeURIComponent(draftId)}`),
  reviewCodexSkillDraft: (draftId: string, payload: Record<string, unknown>) =>
    postJson<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/codex-skill-drafts/${encodeURIComponent(draftId)}/review`, payload),
  getCodexSkillDraftAudit: (draftId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/codex-skill-drafts/${encodeURIComponent(draftId)}/audit`),
  getV731cSkillExperiencePipelineStatus: () =>
    request<V731cSkillExperiencePipelineStatus>("/personal-skill-studio/training-artifacts/v7-31c/status"),
  listSkillPackages: () =>
    request<SkillPackageList>("/personal-skill-studio/training-artifacts/skill-packages"),
  getSkillPackageDetail: (packageId: string) =>
    request<SkillPackage>(`/personal-skill-studio/training-artifacts/skill-packages/${encodeURIComponent(packageId)}`),
  buildSkillPackage: (payload: SkillPackageBuildRequest) =>
    postJson<SkillPackageBuildResponse>("/personal-skill-studio/training-artifacts/skill-packages/build", payload),
  validateSkillPackage: (packageId: string) =>
    postJson<SkillPackageValidationResult & Record<string, unknown>>(`/personal-skill-studio/training-artifacts/skill-packages/${encodeURIComponent(packageId)}/validate`, {}),
  getSkillPackageManifest: (packageId: string) =>
    request<SkillPackageManifest>(`/personal-skill-studio/training-artifacts/skill-packages/${encodeURIComponent(packageId)}/manifest`),
  getSkillPackageAudit: (packageId: string) =>
    request<SkillPackageAudit>(`/personal-skill-studio/training-artifacts/skill-packages/${encodeURIComponent(packageId)}/audit`),
  getSkillPackageSourceTrace: (packageId: string) =>
    request<SkillPackageSourceTraceBundle>(`/personal-skill-studio/training-artifacts/skill-packages/${encodeURIComponent(packageId)}/source-trace`),
  getV731dPipelineStatus: () =>
    request<V731dSkillPackagePipelineStatus>("/personal-skill-studio/training-artifacts/v7-31d/status"),
  listTrainingTasks: () =>
    request<TrainingTaskList>("/personal-skill-studio/training-artifacts/training-tasks"),
  buildTrainingTask: (payload: TrainingTaskBuildRequest) =>
    postJson<TrainingTaskBuildResponse>("/personal-skill-studio/training-artifacts/training-tasks/build", payload),
  listTrainingPackages: () =>
    request<ExperiencePackageList>("/personal-skill-studio/training-artifacts/training-packages"),
  buildExperiencePackage: (payload: ExperiencePackageBuildRequest) =>
    postJson<ExperiencePackageBuildResponse>("/personal-skill-studio/training-artifacts/training-packages/build", payload),
  getTrainingPackage: (packageId: string) =>
    request<InternalExperiencePackage>(`/personal-skill-studio/training-artifacts/training-packages/${encodeURIComponent(packageId)}`),
  getExperiencePackageAudit: (packageId: string) =>
    request<TrainingPackageAudit>(`/personal-skill-studio/training-artifacts/training-packages/${encodeURIComponent(packageId)}/audit`),
  getExperiencePackageSourceTrace: (packageId: string) =>
    request<TrainingPackageSourceTraceBundle>(`/personal-skill-studio/training-artifacts/training-packages/${encodeURIComponent(packageId)}/source-trace`),
  getV731ePipelineStatus: () =>
    request<V731eTrainingPipelineStatus>("/personal-skill-studio/training-artifacts/v7-31e/status"),
  listPracticeLoadPackages: () =>
    request<PracticeLoadReviewPackageList>("/personal-skill-studio/training-artifacts/practice-load-review/packages"),
  getPracticeLoadPackage: (packageId: string) =>
    request<PracticeLoadReviewPackage>(`/personal-skill-studio/training-artifacts/practice-load-review/packages/${encodeURIComponent(packageId)}`),
  editPracticeLoadPackage: (packageId: string, payload: PracticeLoadReviewEditRequest) =>
    postJson<PracticeLoadReviewPackage>(`/personal-skill-studio/training-artifacts/practice-load-review/packages/${encodeURIComponent(packageId)}/edit`, payload),
  savePracticeLoadPackage: (packageId: string, payload: PracticeLoadReviewSaveRequest) =>
    postJson<PracticeLoadReviewPackage>(`/personal-skill-studio/training-artifacts/practice-load-review/packages/${encodeURIComponent(packageId)}/save`, payload),
  revalidatePracticeLoadPackage: (packageId: string) =>
    postJson<PracticeLoadReviewPackage>(`/personal-skill-studio/training-artifacts/practice-load-review/packages/${encodeURIComponent(packageId)}/revalidate`, {}),
  approvePracticeLoadPackage: (packageId: string, payload: PracticeLoadReviewDecisionRequest) =>
    postJson<PracticeLoadReviewPackage>(`/personal-skill-studio/training-artifacts/practice-load-review/packages/${encodeURIComponent(packageId)}/approve`, payload),
  rejectPracticeLoadPackage: (packageId: string, payload: PracticeLoadReviewDecisionRequest) =>
    postJson<PracticeLoadReviewPackage>(`/personal-skill-studio/training-artifacts/practice-load-review/packages/${encodeURIComponent(packageId)}/reject`, payload),
  getPracticeLoadPackageAudit: (packageId: string) =>
    request<PracticeLoadReviewPackageAudit>(`/personal-skill-studio/training-artifacts/practice-load-review/packages/${encodeURIComponent(packageId)}/audit`),
  getPracticeLoadPackageSourceTrace: (packageId: string) =>
    request<PracticeLoadReviewSourceTraceBundle>(`/personal-skill-studio/training-artifacts/practice-load-review/packages/${encodeURIComponent(packageId)}/source-trace`),
  getV731fPipelineStatus: () =>
    request<V731fPracticeLoadPipelineStatus>("/personal-skill-studio/training-artifacts/v7-31f/status"),
  getExperienceLifecycleStatus: () =>
    request<V732ExperienceLifecycleStatus>("/personal-skill-studio/training-artifacts/experience-lifecycle/status"),
  listExperienceLifecycles: () =>
    request<ExperienceLifecycleList>("/personal-skill-studio/training-artifacts/experience-lifecycles"),
  getExperienceLifecycle: (lifecycleId: string) =>
    request<ExperienceLifecycleRecord>(`/personal-skill-studio/training-artifacts/experience-lifecycles/${encodeURIComponent(lifecycleId)}`),
  getExperienceLifecycleState: (lifecycleId: string) =>
    request<Record<string, unknown>>(`/personal-skill-studio/training-artifacts/experience-lifecycles/${encodeURIComponent(lifecycleId)}/state`),
  getExperienceLifecycleGraph: (lifecycleId: string) =>
    request<ExperienceLifecycleGraph>(`/personal-skill-studio/training-artifacts/experience-lifecycles/${encodeURIComponent(lifecycleId)}/graph`),
  getExperienceLifecycleAuditTimeline: (lifecycleId: string) =>
    request<ExperienceLifecycleAuditTimeline>(`/personal-skill-studio/training-artifacts/experience-lifecycles/${encodeURIComponent(lifecycleId)}/audit-timeline`),
  getExperienceLifecycleSourceTraceView: (lifecycleId: string) =>
    request<ExperienceLifecycleSourceTraceView>(`/personal-skill-studio/training-artifacts/experience-lifecycles/${encodeURIComponent(lifecycleId)}/source-trace-view`),
  getExperienceLifecycleIntegrityCheck: (lifecycleId: string) =>
    request<ExperienceLifecycleIntegrityCheck>(`/personal-skill-studio/training-artifacts/experience-lifecycles/${encodeURIComponent(lifecycleId)}/integrity-check`),
  getExperienceLifecycleSafetySummary: (lifecycleId: string) =>
    request<ExperienceLifecycleSafetySummary>(`/personal-skill-studio/training-artifacts/experience-lifecycles/${encodeURIComponent(lifecycleId)}/safety-summary`),
  recomputeExperienceLifecycle: (lifecycleId: string) =>
    postJson<ExperienceLifecycleRecord>(`/personal-skill-studio/training-artifacts/experience-lifecycles/${encodeURIComponent(lifecycleId)}/recompute`, {}),
  getV732ExperienceLifecycleStatus: () =>
    request<V732ExperienceLifecycleStatus>("/personal-skill-studio/training-artifacts/v7-32/status"),
  getCaseAnalysisWorkbenchStatus: () =>
    request<V733CaseAnalysisWorkbenchStatus>("/personal-skill-studio/training-artifacts/case-analysis-workbench/status"),
  listCaseAnalysisWorkbenchViews: () =>
    request<CaseAnalysisWorkbenchViewList>("/personal-skill-studio/training-artifacts/case-analysis-workbench/views"),
  getCaseAnalysisWorkbenchView: (viewId: string) =>
    request<CaseAnalysisWorkbenchView>(`/personal-skill-studio/training-artifacts/case-analysis-workbench/views/${encodeURIComponent(viewId)}`),
  getCaseAnalysisWorkbenchSchema: (viewId: string) =>
    request<CaseAnalysisSkillOutputSchema>(`/personal-skill-studio/training-artifacts/case-analysis-workbench/views/${encodeURIComponent(viewId)}/schema`),
  getCaseAnalysisWorkbenchOutputs: (viewId: string) =>
    request<CaseAnalysisRuntimeOutputList>(`/personal-skill-studio/training-artifacts/case-analysis-workbench/views/${encodeURIComponent(viewId)}/outputs`),
  getCaseAnalysisRuntimeOutput: (outputId: string) =>
    request<CaseAnalysisRuntimeOutput>(`/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${encodeURIComponent(outputId)}`),
  markCaseAnalysisOutputReviewed: (outputId: string) =>
    postJson<CaseAnalysisRuntimeOutput>(`/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${encodeURIComponent(outputId)}/mark-reviewed`, {}),
  submitCaseAnalysisOutputFeedback: (outputId: string, payload: CaseAnalysisOutputFeedbackRequest) =>
    postJson<CaseAnalysisOutputFeedback>(`/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${encodeURIComponent(outputId)}/feedback`, payload),
  submitCaseAnalysisOutputRiskEvent: (outputId: string, payload: CaseAnalysisOutputRiskEventRequest) =>
    postJson<CaseAnalysisOutputRiskEvent>(`/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${encodeURIComponent(outputId)}/risk-event`, payload),
  listCaseAnalysisOutputFeedback: (outputId: string) =>
    request<CaseAnalysisOutputFeedbackList>(`/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${encodeURIComponent(outputId)}/feedback`),
  listCaseAnalysisOutputRiskEvents: (outputId: string) =>
    request<CaseAnalysisOutputRiskEventList>(`/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${encodeURIComponent(outputId)}/risk-events`),
  getCaseAnalysisOutputAudit: (outputId: string) =>
    request<CaseAnalysisOutputAudit>(`/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${encodeURIComponent(outputId)}/audit`),
  getCaseAnalysisOutputSourceTrace: (outputId: string) =>
    request<CaseAnalysisOutputSourceTrace>(`/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${encodeURIComponent(outputId)}/source-trace`),
  getV733CaseAnalysisWorkbenchStatus: () =>
    request<V733CaseAnalysisWorkbenchStatus>("/personal-skill-studio/training-artifacts/v7-33/status"),
  listSourceTraces: () => request<SkillStudioSourceTraceList>("/personal-skill-studio/source-traces"),
  getSourceTrace: (id: string) => request<SkillStudioSourceTrace>(`/personal-skill-studio/source-traces/${encodeURIComponent(id)}`),
  getAudit: () => request<SkillStudioAuditTimeline>("/personal-skill-studio/audit"),
  getSafety: () => request<SkillStudioSafetyStatus>("/personal-skill-studio/safety")
};

export const personalCaseProductionApi = {
  getStatus: () => request<PersonalCaseProductionStatus>("/personal-case-production/status"),
  listWorkflowStages: () => request<WorkflowStageList>("/personal-case-production/workflow-stages"),
  getWorkflowStage: (stageId: string) =>
    request<WorkflowStage>(`/personal-case-production/workflow-stages/${encodeURIComponent(stageId)}`),
  createProductionCase: (payload: ProductionCaseMockRequest) => postJson<ProductionCaseRecord>("/personal-case-production/cases/mock", payload),
  listProductionCases: () => request<ProductionCaseList>("/personal-case-production/cases"),
  getProductionCase: (id: string) => request<ProductionCaseRecord>(`/personal-case-production/cases/${encodeURIComponent(id)}`),
  createWorkflowRun: (payload: WorkflowRunMockRequest) => postJson<WorkflowRunRecord>("/personal-case-production/workflow-runs/mock", payload),
  listWorkflowRuns: () => request<WorkflowRunList>("/personal-case-production/workflow-runs"),
  getWorkflowRun: (id: string) => request<WorkflowRunRecord>(`/personal-case-production/workflow-runs/${encodeURIComponent(id)}`),
  createStageRun: (payload: StageRunMockRequest) => postJson<StageRunRecord>("/personal-case-production/stage-runs/mock", payload),
  listStageRuns: () => request<StageRunList>("/personal-case-production/stage-runs"),
  getStageRun: (id: string) => request<StageRunRecord>(`/personal-case-production/stage-runs/${encodeURIComponent(id)}`),
  listReadiness: () => request<ProductionReadinessList>("/personal-case-production/readiness"),
  getReadiness: (id: string) => request<ProductionReadiness>(`/personal-case-production/readiness/${encodeURIComponent(id)}`),
  getReviewGates: () => request<ProductionCaseList>("/personal-case-production/review-gates"),
  submitReviewGateAction: (productionCaseId: string, payload: ReviewGateActionRequest) =>
    postJson<ReviewGateActionResult>(`/personal-case-production/review-gates/${encodeURIComponent(productionCaseId)}/actions`, payload),
  listSourceTraces: () => request<CaseProductionSourceTraceList>("/personal-case-production/source-traces"),
  getSourceTrace: (id: string) => request<CaseProductionSourceTrace>(`/personal-case-production/source-traces/${encodeURIComponent(id)}`),
  getAudit: () => request<CaseProductionAuditTimeline>("/personal-case-production/audit"),
  getSafety: () => request<CaseProductionSafetyStatus>("/personal-case-production/safety")
};

export const personalCaseAnalysisApi = {
  getStatus: () => request<PersonalCaseAnalysisStatus>("/personal-case-analysis/status"),
  listRuntimes: () => request<CaseAnalysisRuntimeList>("/personal-case-analysis/runtimes"),
  getRuntime: (runtimeId: string) =>
    request<CaseAnalysisRuntime>(`/personal-case-analysis/runtimes/${encodeURIComponent(runtimeId)}`),
  getSkillBaselines: () => request<SkillBaselineReport>("/personal-case-analysis/skill-baselines"),
  createRun: (payload: CaseAnalysisRunMockRequest) => postJson<CaseAnalysisRunRecord>("/personal-case-analysis/runs/mock", payload),
  createControlledRun: (payload: CaseAnalysisRunMockRequest) => postJson<CaseAnalysisRunRecord>("/personal-case-analysis/runs", payload),
  listRuns: () => request<CaseAnalysisRunList>("/personal-case-analysis/runs"),
  getRun: (runId: string) => request<CaseAnalysisRunRecord>(`/personal-case-analysis/runs/${encodeURIComponent(runId)}`),
  createFactDraft: (payload: FactDraftMockRequest) => postJson<FactAnalysisDraft>("/personal-case-analysis/fact-drafts/mock", payload),
  listFactDrafts: () => request<FactAnalysisDraftList>("/personal-case-analysis/fact-drafts"),
  getFactDraft: (draftId: string) =>
    request<FactAnalysisDraft>(`/personal-case-analysis/fact-drafts/${encodeURIComponent(draftId)}`),
  createLegalDraft: (payload: LegalDraftMockRequest) => postJson<LegalAnalysisDraft>("/personal-case-analysis/legal-drafts/mock", payload),
  listLegalDrafts: () => request<LegalAnalysisDraftList>("/personal-case-analysis/legal-drafts"),
  getLegalDraft: (draftId: string) =>
    request<LegalAnalysisDraft>(`/personal-case-analysis/legal-drafts/${encodeURIComponent(draftId)}`),
  listLegalDraftVersions: (draftId: string) =>
    request<Record<string, unknown>>(`/personal-case-analysis/legal-drafts/${encodeURIComponent(draftId)}/versions`),
  createLegalDraftVersion: (draftId: string, payload: Record<string, unknown>) =>
    postJson<Record<string, unknown>>(`/personal-case-analysis/legal-drafts/${encodeURIComponent(draftId)}/versions/mock`, payload),
  getLegalDraftQuality: (draftId: string) =>
    request<Record<string, unknown>>(`/personal-case-analysis/legal-drafts/${encodeURIComponent(draftId)}/quality`),
  getLegalDraftGate: (draftId: string) =>
    request<Record<string, unknown>>(`/personal-case-analysis/legal-drafts/${encodeURIComponent(draftId)}/gate`),
  confirmLegalDraftForReview: (draftId: string, payload: Record<string, unknown>) =>
    postJson<Record<string, unknown>>(`/personal-case-analysis/legal-drafts/${encodeURIComponent(draftId)}/confirm-for-review/mock`, payload),
  getReviewQueue: () => request<CaseAnalysisReviewQueue>("/personal-case-analysis/review-queue"),
  submitReviewAction: (reviewItemId: string, payload: CaseAnalysisReviewActionRequest) =>
    postJson<CaseAnalysisReviewActionResult>(
      `/personal-case-analysis/review-queue/${encodeURIComponent(reviewItemId)}/actions`,
      payload,
    ),
  listEvaluations: () => request<CaseAnalysisEvaluationList>("/personal-case-analysis/evaluations"),
  getEvaluation: (evaluationId: string) =>
    request<CaseAnalysisEvaluation>(`/personal-case-analysis/evaluations/${encodeURIComponent(evaluationId)}`),
  listGates: () => request<CaseAnalysisGateList>("/personal-case-analysis/gates"),
  getGate: (gateId: string) => request<CaseAnalysisGate>(`/personal-case-analysis/gates/${encodeURIComponent(gateId)}`),
  listSourceTraces: () => request<CaseAnalysisSourceTraceList>("/personal-case-analysis/source-traces"),
  getSourceTrace: (sourceTraceId: string) =>
    request<CaseAnalysisSourceTrace>(`/personal-case-analysis/source-traces/${encodeURIComponent(sourceTraceId)}`),
  getAudit: () => request<CaseAnalysisAuditTimeline>("/personal-case-analysis/audit"),
  getSafety: () => request<CaseAnalysisSafetyStatus>("/personal-case-analysis/safety")
};

export const personalCaseWorkspaceApi = {
  getStatus: () => request<Record<string, unknown>>("/personal-case-workspace/status"),
  listCases: () => request<Record<string, unknown>>("/personal-case-workspace/cases"),
  getCase: (caseId: string) => request<Record<string, unknown>>(`/personal-case-workspace/cases/${encodeURIComponent(caseId)}`),
  listMaterials: (caseId: string) => request<Record<string, unknown>>(`/personal-case-workspace/cases/${encodeURIComponent(caseId)}/materials`),
  getMaterial: (materialId: string) => request<Record<string, unknown>>(`/personal-case-workspace/materials/${encodeURIComponent(materialId)}`),
  createOwnerRawView: (materialId: string, payload: Record<string, unknown>) =>
    postJson<Record<string, unknown>>(`/personal-case-workspace/materials/${encodeURIComponent(materialId)}/owner-raw-view`, payload),
  getOCRStatus: (materialId: string) =>
    request<Record<string, unknown>>(`/personal-case-workspace/materials/${encodeURIComponent(materialId)}/ocr-status`),
  getMaterialSourceTraces: (materialId: string) =>
    request<Record<string, unknown>>(`/personal-case-workspace/materials/${encodeURIComponent(materialId)}/source-traces`),
  getFactInput: (materialId: string) =>
    request<Record<string, unknown>>(`/personal-case-workspace/materials/${encodeURIComponent(materialId)}/fact-input`),
  createFactCorrection: (materialId: string, payload: Record<string, unknown>) =>
    postJson<Record<string, unknown>>(`/personal-case-workspace/materials/${encodeURIComponent(materialId)}/fact-input/corrections/mock`, payload),
  listSourceTraces: () => request<Record<string, unknown>>("/personal-case-workspace/source-traces"),
  getAudit: () => request<Record<string, unknown>>("/personal-case-workspace/audit"),
  getSafety: () => request<Record<string, unknown>>("/personal-case-workspace/safety"),
  listFactPreviews: () => request<Record<string, unknown>>("/personal-case-workspace/fact-previews"),
  createFactPreview: (payload: Record<string, unknown>) =>
    postJson<Record<string, unknown>>("/personal-case-workspace/fact-previews/mock", payload),
  getFactPreview: (factPreviewId: string) =>
    request<Record<string, unknown>>(`/personal-case-workspace/fact-previews/${encodeURIComponent(factPreviewId)}`),
  createFactPreviewCorrection: (factPreviewId: string, payload: Record<string, unknown>) =>
    postJson<Record<string, unknown>>(`/personal-case-workspace/fact-previews/${encodeURIComponent(factPreviewId)}/corrections/mock`, payload),
  listFactPreviewCorrections: (factPreviewId: string) =>
    request<Record<string, unknown>>(`/personal-case-workspace/fact-previews/${encodeURIComponent(factPreviewId)}/corrections`),
  getFactCorrection: (correctionId: string) =>
    request<Record<string, unknown>>(`/personal-case-workspace/fact-corrections/${encodeURIComponent(correctionId)}`),
  listFactPreviewVersions: (factPreviewId: string) =>
    request<Record<string, unknown>>(`/personal-case-workspace/fact-previews/${encodeURIComponent(factPreviewId)}/versions`),
  createFactPreviewVersion: (factPreviewId: string, payload: Record<string, unknown>) =>
    postJson<Record<string, unknown>>(`/personal-case-workspace/fact-previews/${encodeURIComponent(factPreviewId)}/versions/mock`, payload),
  getFactPreviewQuality: (factPreviewId: string) =>
    request<Record<string, unknown>>(`/personal-case-workspace/fact-previews/${encodeURIComponent(factPreviewId)}/quality`),
  getFactPreviewGate: (factPreviewId: string) =>
    request<Record<string, unknown>>(`/personal-case-workspace/fact-previews/${encodeURIComponent(factPreviewId)}/gate`),
  getFactPreviewSourceTraces: (factPreviewId: string) =>
    request<Record<string, unknown>>(`/personal-case-workspace/fact-previews/${encodeURIComponent(factPreviewId)}/source-traces`),
  confirmFactPreviewForLegalAnalysis: (factPreviewId: string, payload: Record<string, unknown>) =>
    postJson<Record<string, unknown>>(`/personal-case-workspace/fact-previews/${encodeURIComponent(factPreviewId)}/confirm-for-legal-analysis/mock`, payload),
  getFactInputReadiness: () => request<Record<string, unknown>>("/personal-case-workspace/fact-input-readiness"),
  getFactAudit: () => request<Record<string, unknown>>("/personal-case-workspace/fact-audit"),
  getFactSafety: () => request<Record<string, unknown>>("/personal-case-workspace/fact-safety")
};

export const personalProductionPilotApi = {
  getStatus: () => request<PilotStatus>("/personal-production-pilot/status"),
  getReadiness: () => request<PilotReadiness>("/personal-production-pilot/readiness"),
  getWorkflow: () => request<PilotWorkflow>("/personal-production-pilot/workflow"),
  listRuntimes: () => request<PilotRuntimeList>("/personal-production-pilot/runtimes"),
  getProviderGates: () => request<ProviderGateSummary>("/personal-production-pilot/provider-gates"),
  getSafety: () => request<PilotSafetyStatus>("/personal-production-pilot/safety"),
  createRun: (payload: PilotRunMockRequest) => postJson<PilotRunRecord>("/personal-production-pilot/runs/mock", payload),
  createControlledRun: (payload: PilotRunMockRequest) => postJson<PilotRunRecord>("/personal-production-pilot/runs", payload),
  listRuns: () => request<PilotRunList>("/personal-production-pilot/runs"),
  getRun: (runId: string) => request<PilotRunRecord>(`/personal-production-pilot/runs/${encodeURIComponent(runId)}`),
  getCaseAnalysisSummary: () => request<Record<string, unknown>>("/personal-production-pilot/case-analysis-summary"),
  listSkillFinalDrafts: () => request<SkillFinalDraftList>("/personal-production-pilot/skill-final-drafts"),
  getSkillFinalDraft: (draftId: string) =>
    request<SkillFinalDraft>(`/personal-production-pilot/skill-final-drafts/${encodeURIComponent(draftId)}`),
  createOutput: (payload: PilotOutputMockRequest) => postJson<PilotOutputRecord>("/personal-production-pilot/outputs/mock", payload),
  listOutputs: () => request<PilotOutputList>("/personal-production-pilot/outputs"),
  getOutput: (outputId: string) => request<PilotOutputRecord>(`/personal-production-pilot/outputs/${encodeURIComponent(outputId)}`),
  createOwnerDownload: (outputId: string, payload: OwnerDownloadMockRequest) =>
    postJson<OwnerDownloadRecord>(`/personal-production-pilot/outputs/${encodeURIComponent(outputId)}/owner-downloads/mock`, payload),
  listOwnerDownloads: () => request<OwnerDownloadList>("/personal-production-pilot/owner-downloads"),
  getOwnerDownload: (downloadId: string) =>
    request<OwnerDownloadRecord>(`/personal-production-pilot/owner-downloads/${encodeURIComponent(downloadId)}`),
  getReviewQueue: () => request<PilotReviewQueue>("/personal-production-pilot/review-queue"),
  submitReviewAction: (reviewItemId: string, payload: PilotReviewActionRequest) =>
    postJson<PilotReviewActionResult>(`/personal-production-pilot/review-queue/${encodeURIComponent(reviewItemId)}/actions`, payload),
  listSourceTraces: () => request<PilotSourceTraceList>("/personal-production-pilot/source-traces"),
  getAudit: () => request<PilotAuditTimeline>("/personal-production-pilot/audit"),
  getExportBoundary: () => request<ExportBoundary>("/personal-production-pilot/export-boundary"),
  getDashboardStatus: () => request<Record<string, unknown>>("/personal-production-pilot/dashboard/status"),
  getDashboardMetrics: () => request<Record<string, unknown>>("/personal-production-pilot/dashboard/metrics"),
  getDashboardQuality: () => request<Record<string, unknown>>("/personal-production-pilot/dashboard/quality"),
  getDashboardSafety: () => request<Record<string, unknown>>("/personal-production-pilot/dashboard/safety")
};

export const personalOwnerOutputCenterApi = {
  getStatus: () => request<OwnerOutputStatus>("/personal-owner-output-center/status"),
  listOutputs: () => request<OwnerOutputList>("/personal-owner-output-center/outputs"),
  getOutput: (outputId: string) =>
    request<OwnerOutputRecord>(`/personal-owner-output-center/outputs/${encodeURIComponent(outputId)}`),
  getOutputQuality: (outputId: string) =>
    request<OwnerOutputQuality>(`/personal-owner-output-center/outputs/${encodeURIComponent(outputId)}/quality`),
  getOutputGate: (outputId: string) =>
    request<OwnerOutputGate>(`/personal-owner-output-center/outputs/${encodeURIComponent(outputId)}/gate`),
  getOutputOptimization: (outputId: string) =>
    request<OwnerOutputOptimization>(`/personal-owner-output-center/outputs/${encodeURIComponent(outputId)}/optimization`),
  getOutputSourceTraces: (outputId: string) =>
    request<OwnerOutputSourceTraceList>(`/personal-owner-output-center/outputs/${encodeURIComponent(outputId)}/source-traces`),
  createDownload: (outputId: string, payload: OwnerOutputDownloadRequest) =>
    postJson<OwnerOutputDownloadRecord>(`/personal-owner-output-center/outputs/${encodeURIComponent(outputId)}/downloads/mock`, payload),
  listDownloads: () => request<OwnerOutputDownloadList>("/personal-owner-output-center/downloads"),
  getDownload: (downloadId: string) =>
    request<OwnerOutputDownloadRecord>(`/personal-owner-output-center/downloads/${encodeURIComponent(downloadId)}`),
  getAudit: () => request<OwnerOutputAuditTimeline>("/personal-owner-output-center/audit"),
  getSafety: () => request<OwnerOutputSafetyStatus>("/personal-owner-output-center/safety")
};

export const personalTrialReadinessApi = {
  getStatus: () => request<TrialReadinessStatus>("/personal-trial-readiness/status"),
  getChecklist: () => request<TrialChecklist>("/personal-trial-readiness/checklist"),
  getSafety: () => request<TrialSafetyStatus>("/personal-trial-readiness/safety"),
  createTrial: (payload: TrialSessionMockRequest) => postJson<TrialSession>("/personal-trial-readiness/trials/mock", payload),
  listTrials: () => request<TrialSessionList>("/personal-trial-readiness/trials"),
  getTrial: (trialId: string) => request<TrialSession>(`/personal-trial-readiness/trials/${encodeURIComponent(trialId)}`),
  getTrialChecklist: (trialId: string) => request<TrialChecklist>(`/personal-trial-readiness/trials/${encodeURIComponent(trialId)}/checklist`),
  createTrialChecklist: (trialId: string) => postJson<TrialChecklist>(`/personal-trial-readiness/trials/${encodeURIComponent(trialId)}/checklist/mock`),
  listObservations: (trialId: string) => request<StageObservationList>(`/personal-trial-readiness/trials/${encodeURIComponent(trialId)}/observations`),
  createObservation: (trialId: string, payload: StageObservationMockRequest) =>
    postJson<StageObservation>(`/personal-trial-readiness/trials/${encodeURIComponent(trialId)}/observations/mock`, payload),
  listTrialIssues: (trialId: string) => request<IssueLogList>(`/personal-trial-readiness/trials/${encodeURIComponent(trialId)}/issues`),
  createIssue: (trialId: string, payload: IssueLogMockRequest) =>
    postJson<IssueLogItem>(`/personal-trial-readiness/trials/${encodeURIComponent(trialId)}/issues/mock`, payload),
  listIssues: () => request<IssueLogList>("/personal-trial-readiness/issues"),
  getIssue: (issueId: string) => request<IssueLogItem>(`/personal-trial-readiness/issues/${encodeURIComponent(issueId)}`),
  getQuality: (trialId: string) => request<QualityReview>(`/personal-trial-readiness/trials/${encodeURIComponent(trialId)}/quality`),
  createQuality: (trialId: string) => postJson<QualityReview>(`/personal-trial-readiness/trials/${encodeURIComponent(trialId)}/quality/mock`),
  getSafetyConfirmation: (trialId: string) =>
    request<SafetyConfirmation>(`/personal-trial-readiness/trials/${encodeURIComponent(trialId)}/safety-confirmation`),
  createSafetyConfirmation: (trialId: string) =>
    postJson<SafetyConfirmation>(`/personal-trial-readiness/trials/${encodeURIComponent(trialId)}/safety-confirmation/mock`),
  listOptimizationBacklog: () => request<OptimizationBacklogList>("/personal-trial-readiness/optimization-backlog"),
  createOptimizationBacklog: (payload: OptimizationBacklogMockRequest) =>
    postJson<OptimizationBacklogItem>("/personal-trial-readiness/optimization-backlog/mock", payload),
  getAudit: () => request<TrialAuditTimeline>("/personal-trial-readiness/audit")
};

export const personalProviderReadinessApi = {
  getStatus: () => request<ProviderStatus>("/personal-provider-readiness/status"),
  listProviders: () => request<ProviderList>("/personal-provider-readiness/providers"),
  getProvider: (providerId: string) =>
    request<ProviderMetadata>(`/personal-provider-readiness/providers/${encodeURIComponent(providerId)}`),
  getSecretBoundary: (providerId: string) =>
    request<SecretBoundaryStatus>(`/personal-provider-readiness/providers/${encodeURIComponent(providerId)}/secret-boundary`),
  getLiveGate: (providerId: string) =>
    request<LiveGateStatus>(`/personal-provider-readiness/providers/${encodeURIComponent(providerId)}/live-gate`),
  getUsagePolicy: (providerId: string) =>
    request<UsagePolicy>(`/personal-provider-readiness/providers/${encodeURIComponent(providerId)}/usage-policy`),
  getHealthDryRun: (providerId: string) =>
    request<ProviderHealthDryRun>(`/personal-provider-readiness/providers/${encodeURIComponent(providerId)}/health/dry-run`),
  listCategories: () => request<CategorySummaryList>("/personal-provider-readiness/categories"),
  listCategoryProviders: (category: string) =>
    request<ProviderList>(`/personal-provider-readiness/categories/${encodeURIComponent(category)}/providers`),
  createLiveGateMock: (payload: LiveGateMockRequest) =>
    postJson<LiveGateStatus>("/personal-provider-readiness/live-gates/mock", payload),
  listLiveGates: () => request<LiveGateList>("/personal-provider-readiness/live-gates"),
  getAudit: () => request<ProviderAuditTimeline>("/personal-provider-readiness/audit"),
  getSafety: () => request<ProviderSafetyStatus>("/personal-provider-readiness/safety")
};

export const personalLiveConnectionApi = {
  getStatus: () => request<LiveConnectionStatus>("/personal-live-connection/status"),
  listRuntimes: () => request<LiveConnectionRuntimeList>("/personal-live-connection/runtimes"),
  listProviders: () => request<LiveConnectionProviderList>("/personal-live-connection/providers"),
  getProvider: (providerId: string) =>
    request<LiveConnectionProvider>(`/personal-live-connection/providers/${encodeURIComponent(providerId)}`),
  getSecretBoundary: (providerId: string) =>
    request<LiveConnectionSecretBoundary>(`/personal-live-connection/providers/${encodeURIComponent(providerId)}/secret-boundary`),
  getLiveGate: (providerId: string) =>
    request<LiveConnectionLiveGate>(`/personal-live-connection/providers/${encodeURIComponent(providerId)}/live-gate`),
  getUsagePolicy: (providerId: string) =>
    request<LiveConnectionUsagePolicy>(`/personal-live-connection/providers/${encodeURIComponent(providerId)}/usage-policy`),
  getHealthDryRun: (providerId: string) =>
    request<LiveConnectionHealthDryRun>(`/personal-live-connection/providers/${encodeURIComponent(providerId)}/health/dry-run`),
  createDryRun: (payload: LiveConnectionRunRequest) =>
    postJson<LiveConnectionRunRecord>("/personal-live-connection/runs/dry-run", payload),
  createRun: (payload: LiveConnectionRunRequest) => postJson<LiveConnectionRunRecord>("/personal-live-connection/runs", payload),
  listRuns: () => request<LiveConnectionRunList>("/personal-live-connection/runs"),
  getRun: (runId: string) => request<LiveConnectionRunRecord>(`/personal-live-connection/runs/${encodeURIComponent(runId)}`),
  getAudit: () => request<LiveConnectionAuditTimeline>("/personal-live-connection/audit"),
  getSafety: () => request<LiveConnectionSafetyStatus>("/personal-live-connection/safety")
};

export const personalLegalEnterpriseApi = {
  getStatus: () => request<LegalEnterpriseStatus>("/personal-legal-enterprise/status"),
  listProviders: () => request<LegalEnterpriseProviderList>("/personal-legal-enterprise/providers"),
  getProvider: (providerId: string) =>
    request<LegalEnterpriseProvider>(`/personal-legal-enterprise/providers/${encodeURIComponent(providerId)}`),
  getSecretBoundary: (providerId: string) =>
    request<LegalEnterpriseGenericResponse>(`/personal-legal-enterprise/providers/${encodeURIComponent(providerId)}/secret-boundary`),
  getLiveGate: (providerId: string) =>
    request<LegalEnterpriseGenericResponse>(`/personal-legal-enterprise/providers/${encodeURIComponent(providerId)}/live-gate`),
  getUsagePolicy: (providerId: string) =>
    request<LegalEnterpriseGenericResponse>(`/personal-legal-enterprise/providers/${encodeURIComponent(providerId)}/usage-policy`),
  getHealthDryRun: (providerId: string) =>
    request<LegalEnterpriseGenericResponse>(`/personal-legal-enterprise/providers/${encodeURIComponent(providerId)}/health/dry-run`),
  listCategories: () => request<LegalEnterpriseCategorySummaryList>("/personal-legal-enterprise/categories"),
  listCategoryProviders: (category: string) =>
    request<LegalEnterpriseProviderList>(`/personal-legal-enterprise/categories/${encodeURIComponent(category)}/providers`),
  createLiveGateMock: (payload: Record<string, unknown>) =>
    postJson<LegalEnterpriseGenericResponse>("/personal-legal-enterprise/live-gates/mock", payload),
  listLiveGates: () => request<LegalEnterpriseGenericResponse>("/personal-legal-enterprise/live-gates"),
  createLegalSearchDryRun: (payload: Record<string, unknown>) =>
    postJson<LegalEnterpriseGenericResponse>("/personal-legal-enterprise/legal-search/dry-run", payload),
  createLegalSearchRun: (payload: Record<string, unknown>) =>
    postJson<LegalEnterpriseGenericResponse>("/personal-legal-enterprise/legal-search/runs", payload),
  listLegalSearchRuns: () => request<LegalEnterpriseGenericResponse>("/personal-legal-enterprise/legal-search/runs"),
  createEnterpriseLookupDryRun: (payload: Record<string, unknown>) =>
    postJson<LegalEnterpriseGenericResponse>("/personal-legal-enterprise/enterprise-lookup/dry-run", payload),
  createEnterpriseLookupRun: (payload: Record<string, unknown>) =>
    postJson<LegalEnterpriseGenericResponse>("/personal-legal-enterprise/enterprise-lookup/runs", payload),
  listEnterpriseLookupRuns: () => request<LegalEnterpriseGenericResponse>("/personal-legal-enterprise/enterprise-lookup/runs"),
  getReviewQueue: () => request<LegalEnterpriseGenericResponse>("/personal-legal-enterprise/review-queue"),
  submitReviewAction: (reviewItemId: string, payload: Record<string, unknown>) =>
    postJson<LegalEnterpriseGenericResponse>(`/personal-legal-enterprise/review-queue/${encodeURIComponent(reviewItemId)}/actions/mock`, payload),
  getSourceTraces: () => request<LegalEnterpriseGenericResponse>("/personal-legal-enterprise/source-traces"),
  getAudit: () => request<LegalEnterpriseGenericResponse>("/personal-legal-enterprise/audit"),
  getSafety: () => request<LegalEnterpriseGenericResponse>("/personal-legal-enterprise/safety")
};

export const personalDeliveryPacketApi = {
  getStatus: () => request<PersonalDeliveryPacketStatus>("/personal-delivery-packet/status"),
  listRuntimes: () => request<DeliveryPacketRuntimeList>("/personal-delivery-packet/runtimes"),
  getRuntime: (runtimeId: string) =>
    request<DeliveryPacketRuntime>(`/personal-delivery-packet/runtimes/${encodeURIComponent(runtimeId)}`),
  createPacket: (payload: DeliveryPacketMockRequest) => postJson<DeliveryPacketRecord>("/personal-delivery-packet/packets/mock", payload),
  listPackets: () => request<DeliveryPacketList>("/personal-delivery-packet/packets"),
  getPacket: (deliveryPacketId: string) =>
    request<DeliveryPacketRecord>(`/personal-delivery-packet/packets/${encodeURIComponent(deliveryPacketId)}`),
  createPacketItem: (payload: PacketItemMockRequest) =>
    postJson<PacketItemRecord>("/personal-delivery-packet/packet-items/mock", payload),
  listPacketItems: () => request<PacketItemList>("/personal-delivery-packet/packet-items"),
  getPacketItem: (packetItemId: string) =>
    request<PacketItemRecord>(`/personal-delivery-packet/packet-items/${encodeURIComponent(packetItemId)}`),
  createSourceBundle: (payload: SourceBundleMockRequest) =>
    postJson<SourceBundleRecord>("/personal-delivery-packet/source-bundles/mock", payload),
  listSourceBundles: () => request<SourceBundleList>("/personal-delivery-packet/source-bundles"),
  getSourceBundle: (sourceBundleId: string) =>
    request<SourceBundleRecord>(`/personal-delivery-packet/source-bundles/${encodeURIComponent(sourceBundleId)}`),
  listExportReadiness: () => request<ExportReadinessList>("/personal-delivery-packet/export-readiness"),
  getExportReadiness: (deliveryPacketId: string) =>
    request<ExportReadiness>(`/personal-delivery-packet/export-readiness/${encodeURIComponent(deliveryPacketId)}`),
  listFinalLocks: () => request<FinalLockList>("/personal-delivery-packet/final-locks"),
  submitFinalLockAction: (deliveryPacketId: string, payload: FinalLockActionRequest) =>
    postJson<FinalLockRecord>(`/personal-delivery-packet/final-locks/${encodeURIComponent(deliveryPacketId)}/actions`, payload),
  listReviewSummaries: () => request<ReviewSummaryList>("/personal-delivery-packet/review-summaries"),
  getReviewSummary: (deliveryPacketId: string) =>
    request<ReviewSummary>(`/personal-delivery-packet/review-summaries/${encodeURIComponent(deliveryPacketId)}`),
  getAudit: () => request<DeliveryPacketAuditTimeline>("/personal-delivery-packet/audit"),
  getSafety: () => request<DeliveryPacketSafetyStatus>("/personal-delivery-packet/safety")
};

export const personalShowcasePackApi = {
  getStatus: () => request<PersonalShowcasePackStatus>("/personal-showcase-pack/status"),
  listRuntimes: () => request<ShowcaseRuntimeList>("/personal-showcase-pack/runtimes"),
  getRuntime: (runtimeId: string) =>
    request<ShowcaseRuntime>(`/personal-showcase-pack/runtimes/${encodeURIComponent(runtimeId)}`),
  createPilotSample: (payload: PilotSampleMockRequest) =>
    postJson<PilotSampleRecord>("/personal-showcase-pack/pilot-samples/mock", payload),
  listPilotSamples: () => request<PilotSampleList>("/personal-showcase-pack/pilot-samples"),
  getPilotSample: (pilotSampleId: string) =>
    request<PilotSampleRecord>(`/personal-showcase-pack/pilot-samples/${encodeURIComponent(pilotSampleId)}`),
  createStoryFlow: (payload: StoryFlowMockRequest) => postJson<StoryFlowRecord>("/personal-showcase-pack/story-flows/mock", payload),
  listStoryFlows: () => request<StoryFlowList>("/personal-showcase-pack/story-flows"),
  getStoryFlow: (storyFlowId: string) =>
    request<StoryFlowRecord>(`/personal-showcase-pack/story-flows/${encodeURIComponent(storyFlowId)}`),
  getMetrics: () => request<ShowcaseMetrics>("/personal-showcase-pack/metrics"),
  getTrustPanel: () => request<TrustPanel>("/personal-showcase-pack/trust-panel"),
  getAudit: () => request<ShowcaseAuditTimeline>("/personal-showcase-pack/audit"),
  getSafety: () => request<ShowcaseSafetyStatus>("/personal-showcase-pack/safety")
};

// Future resource groups: experiencePackageApi, auditApi, settingsApi.

export const getHealth = runtimeApi.health;
export const getDashboardStats = runtimeApi.dashboardStats;
export const getLLMStatus = runtimeApi.llmStatus;
export const getOCRStatus = ocrApi.status;
export const mockOCRExtract = ocrApi.mockExtract;
export const getLegalSearchStatus = legalSearchApi.status;
export const mockLegalSearch = legalSearchApi.mockSearch;
export const getSourceRefsStatus = sourceRefsApi.status;
export const getMockSourceTrace = sourceRefsApi.mockTrace;
export const resolveCitation = sourceRefsApi.resolve;
export const getLocalSandboxStatus = localSandboxApi.status;
export const getLocalSandboxGuards = localSandboxApi.guards;
export const runLocalSandboxDryRun = localSandboxApi.dryRun;
export const getLocalSandboxAuditLogs = localSandboxApi.auditLogs;
export const getInternalAlphaStatus = internalAlphaApi.status;
export const getInternalAlphaReadiness = internalAlphaApi.readiness;
export const getInternalAlphaSecrets = internalAlphaApi.secrets;
export const getInternalAlphaDatabase = internalAlphaApi.database;
export const runInternalAlphaDryRun = internalAlphaApi.dryRun;
export const getInternalAlphaAuditLogs = internalAlphaApi.auditLogs;
export const getPersonalAlphaStatus = personalAlphaApi.status;
export const previewPersonalAlphaManifest = personalAlphaApi.previewManifest;
export const previewPersonalAlphaMaterialInventory = personalAlphaApi.previewMaterialInventory;
export const runPersonalAlphaDryRun = personalAlphaApi.dryRun;
export const getPersonalAlphaAuditLogs = personalAlphaApi.auditLogs;
export const getPersonalAlphaWorkspaceStatus = personalAlphaWorkspaceApi.status;
export const runPersonalAlphaWorkspace = personalAlphaWorkspaceApi.run;
export const getPersonalAlphaWorkspaceRun = personalAlphaWorkspaceApi.readRun;
export const getPersonalAlphaWorkspaceAuditLogs = personalAlphaWorkspaceApi.auditLogs;
export const getPersonalAlphaDashboardStatus = personalAlphaDashboardApi.status;
export const getPersonalAlphaDashboardSummary = personalAlphaDashboardApi.summary;
export const getPersonalAlphaDashboardStageHealth = personalAlphaDashboardApi.stageHealth;
export const getPersonalAlphaDashboardAuditTimeline = personalAlphaDashboardApi.auditTimeline;
export const getPersonalAlphaDashboardSourceTraceSummary = personalAlphaDashboardApi.sourceTraceSummary;
export const getPersonalAlphaDashboardRunDetail = personalAlphaDashboardApi.getRunDetail;
export const getPersonalAlphaSourceReviewStatus = personalAlphaSourceReviewApi.status;
export const getPersonalAlphaSourceReviewRunDetail = personalAlphaSourceReviewApi.getRunDetail;
export const getPersonalAlphaSourceReviewSourceTraces = personalAlphaSourceReviewApi.getSourceTraces;
export const getPersonalAlphaSourceReviewEvidenceSummary = personalAlphaSourceReviewApi.getEvidenceSummary;
export const getPersonalAlphaSourceReviewDecisions = personalAlphaSourceReviewApi.listDecisions;
export const submitPersonalAlphaSourceReviewDecision = personalAlphaSourceReviewApi.submitDecision;
export const getPersonalAlphaSourceReviewDecisionSummary = personalAlphaSourceReviewApi.getDecisionSummary;
export const getPersonalAlphaFinalReadinessStatus = personalAlphaFinalReadinessApi.getStatus;
export const getPersonalAlphaFinalReadinessRunDetail = personalAlphaFinalReadinessApi.getRunDetail;
export const getPersonalAlphaFinalReadinessRunSummary = personalAlphaFinalReadinessApi.getRunSummary;
export const getPersonalAlphaFinalGateStatus = personalAlphaFinalGateApi.getStatus;
export const getPersonalAlphaFinalGateRunDetail = personalAlphaFinalGateApi.getRunDetail;
export const getPersonalAlphaFinalGateSummary = personalAlphaFinalGateApi.getSummary;
export const getPersonalAlphaFinalGateDecisions = personalAlphaFinalGateApi.listDecisions;
export const submitPersonalAlphaFinalGateDecision = personalAlphaFinalGateApi.submitDecision;
export const getPersonalAlphaFinalPacketStatus = personalAlphaFinalPacketApi.getStatus;
export const getPersonalAlphaFinalPacketPreview = personalAlphaFinalPacketApi.getPreview;
export const createPersonalAlphaFinalPacket = personalAlphaFinalPacketApi.createPacket;
export const listPersonalAlphaFinalPackets = personalAlphaFinalPacketApi.listPackets;
export const getPersonalAlphaFinalPacket = personalAlphaFinalPacketApi.getPacket;
export const listPersonalAlphaFinalPacketsByRun = personalAlphaFinalPacketApi.listRunPackets;
export const getPersonalAlphaLawyerFinalReviewStatus = personalAlphaLawyerFinalReviewApi.getStatus;
export const getPersonalAlphaLawyerFinalReviewPacketDetail = personalAlphaLawyerFinalReviewApi.getPacketDetail;
export const getPersonalAlphaLawyerFinalReviewSummary = personalAlphaLawyerFinalReviewApi.getSummary;
export const getPersonalAlphaLawyerFinalReviewActions = personalAlphaLawyerFinalReviewApi.listActions;
export const submitPersonalAlphaLawyerFinalReviewAction = personalAlphaLawyerFinalReviewApi.submitAction;
export const getPersonalAlphaLawyerFinalReviewAction = personalAlphaLawyerFinalReviewApi.getAction;
export const getPersonalAlphaFinalLockStatus = personalAlphaFinalLockApi.getStatus;
export const getPersonalAlphaFinalLockReadiness = personalAlphaFinalLockApi.getReadiness;
export const createPersonalAlphaFinalLock = personalAlphaFinalLockApi.createLock;
export const listPersonalAlphaFinalLocks = personalAlphaFinalLockApi.listLocks;
export const getPersonalAlphaFinalLock = personalAlphaFinalLockApi.getLock;
export const listPersonalAlphaFinalLocksByPacket = personalAlphaFinalLockApi.listPacketLocks;
export const getPersonalAlphaCaseOSStatus = personalAlphaCaseOSApi.getStatus;
export const getPersonalAlphaCaseOSHardeningStatus = personalAlphaCaseOSApi.getHardeningStatus;
export const getPersonalAlphaCaseOSReleaseCandidateStatus = personalAlphaCaseOSApi.getReleaseCandidateStatus;
export const getPersonalAlphaCaseOSReleaseCandidateSummary = personalAlphaCaseOSApi.getReleaseCandidateSummary;
export const getPersonalAlphaCaseOSReleaseCandidateChecklist = personalAlphaCaseOSApi.getReleaseCandidateChecklist;
export const getPersonalAlphaCaseOSReleaseCandidateReadiness = personalAlphaCaseOSApi.getReleaseCandidateReadiness;
export const getPersonalAlphaCaseOSReleaseCandidateAudit = personalAlphaCaseOSApi.getReleaseCandidateAudit;
export const getPersonalAlphaCaseOSReleaseNotesPreview = personalAlphaCaseOSApi.getReleaseCandidateReleaseNotesPreview;
export const listPersonalAlphaCaseOSCases = personalAlphaCaseOSApi.listCases;
export const getPersonalAlphaCaseOSCaseDetail = personalAlphaCaseOSApi.getCaseDetail;
export const getPersonalAlphaCaseOSAuditTimeline = personalAlphaCaseOSApi.getAuditTimeline;
export const getPersonalAlphaCaseOSUnifiedAuditTimeline = personalAlphaCaseOSApi.getUnifiedAuditTimeline;
export const getPersonalAlphaCaseOSAuditTimelineSummary = personalAlphaCaseOSApi.getAuditTimelineSummary;
export const getPersonalAlphaCaseOSAuditTimelineRedactionCheck = personalAlphaCaseOSApi.getAuditTimelineRedactionCheck;
export const getPersonalAlphaCaseOSAuditTimelineFilters = personalAlphaCaseOSApi.getAuditTimelineFilters;
export const getPersonalAlphaCaseOSReviewState = personalAlphaCaseOSApi.getReviewState;
export const getPersonalAlphaCaseOSReviewStateHistory = personalAlphaCaseOSApi.getReviewStateHistory;
export const getPersonalAlphaCaseOSReviewStateTransitions = personalAlphaCaseOSApi.getReviewStateTransitions;
export const validatePersonalAlphaCaseOSReviewStateTransition = personalAlphaCaseOSApi.validateReviewStateTransition;
export const getPersonalAlphaCaseOSReviewStateSummary = personalAlphaCaseOSApi.getReviewStateSummary;
export const getPersonalAlphaCaseOSFinalLockConsolidation = personalAlphaCaseOSApi.getFinalLockConsolidation;
export const getPersonalAlphaCaseOSMetadataClosure = personalAlphaCaseOSApi.getMetadataClosure;
export const getPersonalAlphaCaseOSMetadataClosureChecklist = personalAlphaCaseOSApi.getMetadataClosureChecklist;
export const getPersonalAlphaCaseOSMetadataClosureBlockers = personalAlphaCaseOSApi.getMetadataClosureBlockers;
export const getPersonalAlphaCaseOSMetadataClosureExportPreview = personalAlphaCaseOSApi.getMetadataClosureExportPreview;
export const getPersonalAlphaCaseOSExportPackageStatus = personalAlphaCaseOSApi.getExportPackageStatus;
export const createPersonalAlphaCaseOSExportPackage = personalAlphaCaseOSApi.createExportPackage;
export const listPersonalAlphaCaseOSExportPackages = personalAlphaCaseOSApi.listExportPackages;
export const getPersonalAlphaCaseOSExportPackage = personalAlphaCaseOSApi.getExportPackage;
export const getPersonalAlphaCaseOSExportPackageContent = personalAlphaCaseOSApi.getExportPackageContent;
export const getPersonalAlphaCaseOSExportPackageSafetyCheck = personalAlphaCaseOSApi.getExportPackageSafetyCheck;
export const getPersonalAlphaCaseOSExportPackageSummary = personalAlphaCaseOSApi.getExportPackageSummary;
export const getPersonalAlphaCaseOSQualityStatus = personalAlphaCaseOSApi.getQualityStatus;
export const getPersonalAlphaCaseOSQualityChecklist = personalAlphaCaseOSApi.getQualityChecklist;
export const getPersonalAlphaCaseOSQualityScore = personalAlphaCaseOSApi.getQualityScore;
export const getPersonalAlphaCaseOSQualityFindings = personalAlphaCaseOSApi.getQualityFindings;
export const getPersonalAlphaCaseOSQualityRecommendations = personalAlphaCaseOSApi.getQualityRecommendations;
export const getPersonalAlphaCaseOSQualityReportPreview = personalAlphaCaseOSApi.getQualityReportPreview;
export const getPersonalAlphaCaseOSQualitySummary = personalAlphaCaseOSApi.getQualitySummary;
export const getPersonalAlphaCaseOSHardeningSafetyCheck = personalAlphaCaseOSApi.getHardeningSafetyCheck;
export const getPersonalAlphaCaseOSHardeningResponseConsistency = personalAlphaCaseOSApi.getHardeningResponseConsistency;
export const getPersonalAlphaCaseOSHardeningRuntimeStorageCheck = personalAlphaCaseOSApi.getHardeningRuntimeStorageCheck;
export const getPersonalAlphaCaseOSReleaseCandidateCaseReadiness = personalAlphaCaseOSApi.getReleaseCandidateCaseReadiness;
export const getPersonalAlphaCaseOSNextAction = personalAlphaCaseOSApi.getNextAction;
export const getPersonalAlphaCaseOSStageOrchestration = personalAlphaCaseOSApi.getStageOrchestration;
export const getPersonalAlphaCaseOSStageTransitions = personalAlphaCaseOSApi.getStageTransitions;
export const getPersonalAlphaCaseOSActionEligibility = personalAlphaCaseOSApi.getActionEligibility;
export const getPersonalAlphaCaseOSBlockers = personalAlphaCaseOSApi.getBlockers;
export const getPersonalAlphaCaseOSSafetyChecklist = personalAlphaCaseOSApi.getSafetyChecklist;
export const getPersonalProductionStatus = personalProductionApi.getStatus;
export const getPersonalProductionMode = personalProductionApi.getMode;
export const getPersonalProductionShowcase = personalProductionApi.getShowcase;
export const getPersonalProductionRuntimeRegistry = personalProductionApi.getRuntimeRegistry;
export const getPersonalProductionProviderCapabilities = personalProductionApi.getProviderCapabilities;
export const getPersonalProductionReadiness = personalProductionApi.getReadiness;
export const getPersonalProductionSafety = personalProductionApi.getSafety;
export const getPersonalProductionConsoleSummary = personalProductionApi.getConsoleSummary;
export const getPersonalAIGatewayStatus = personalAIGatewayApi.getStatus;
export const getPersonalAIProviders = personalAIGatewayApi.getProviders;
export const getPersonalAIProvider = personalAIGatewayApi.getProvider;
export const getPersonalAIPromptTemplates = personalAIGatewayApi.getPromptTemplates;
export const getPersonalAIPromptTemplate = personalAIGatewayApi.getPromptTemplate;
export const renderPersonalAIPromptPreview = personalAIGatewayApi.renderPromptPreview;
export const createPersonalAIMockRun = personalAIGatewayApi.createMockRun;
export const listPersonalAIRuns = personalAIGatewayApi.listRuns;
export const getPersonalAIRun = personalAIGatewayApi.getRun;
export const getPersonalAIAudit = personalAIGatewayApi.getAudit;
export const getPersonalAITokenUsageSummary = personalAIGatewayApi.getTokenUsageSummary;
export const getPersonalAISafety = personalAIGatewayApi.getSafety;
export const getPersonalAILiveStatus = personalAIGatewayApi.getLiveStatus;
export const getPersonalAILiveProviders = personalAIGatewayApi.getLiveProviders;
export const getPersonalAILiveProvider = personalAIGatewayApi.getLiveProvider;
export const createPersonalAILiveDryRun = personalAIGatewayApi.createLiveDryRun;
export const createPersonalAILiveRun = personalAIGatewayApi.createLiveRun;
export const listPersonalAILiveRuns = personalAIGatewayApi.listLiveRuns;
export const getPersonalAILiveRun = personalAIGatewayApi.getLiveRun;
export const getPersonalAILiveAudit = personalAIGatewayApi.getLiveAudit;
export const getPersonalAILiveSafety = personalAIGatewayApi.getLiveSafety;
export const getPersonalMaterialRuntimeStatus = personalMaterialRuntimeApi.getStatus;
export const getPersonalMaterialRuntimeProviders = personalMaterialRuntimeApi.getProviders;
export const getPersonalMaterialRuntimeProvider = personalMaterialRuntimeApi.getProvider;
export const createPersonalMaterialParseJob = personalMaterialRuntimeApi.createMockParseJob;
export const listPersonalMaterialParseJobs = personalMaterialRuntimeApi.listParseJobs;
export const getPersonalMaterialParseJob = personalMaterialRuntimeApi.getParseJob;
export const createPersonalOCRJob = personalMaterialRuntimeApi.createMockOCRJob;
export const listPersonalOCRJobs = personalMaterialRuntimeApi.listOCRJobs;
export const getPersonalOCRJob = personalMaterialRuntimeApi.getOCRJob;
export const getPersonalOCRPreview = personalMaterialRuntimeApi.getOCRPreview;
export const getPersonalOCRReviewQueue = personalMaterialRuntimeApi.getOCRReviewQueue;
export const submitPersonalOCRReviewAction = personalMaterialRuntimeApi.submitOCRReviewAction;
export const getPersonalMaterialSourceTraces = personalMaterialRuntimeApi.getSourceTraces;
export const getPersonalMaterialAudit = personalMaterialRuntimeApi.getAudit;
export const getPersonalMaterialSafety = personalMaterialRuntimeApi.getSafety;
export const getPersonalMaterialLiveStatus = personalMaterialRuntimeApi.getLiveStatus;
export const getPersonalMaterialLiveProviders = personalMaterialRuntimeApi.getLiveProviders;
export const getPersonalMaterialLiveProvider = personalMaterialRuntimeApi.getLiveProvider;
export const getPersonalMaterialLiveSecretBoundary = personalMaterialRuntimeApi.getLiveSecretBoundary;
export const getPersonalMaterialLiveGate = personalMaterialRuntimeApi.getLiveGate;
export const getPersonalMaterialLiveHealthDryRun = personalMaterialRuntimeApi.getLiveHealthDryRun;
export const createPersonalMaterialLiveGateMock = personalMaterialRuntimeApi.createLiveGateMock;
export const listPersonalMaterialLiveGates = personalMaterialRuntimeApi.listLiveGates;
export const createPersonalMaterialDocumentLiveDryRun = personalMaterialRuntimeApi.createDocumentLiveDryRun;
export const createPersonalMaterialDocumentLiveRun = personalMaterialRuntimeApi.createDocumentLiveRun;
export const listPersonalMaterialDocumentLiveRuns = personalMaterialRuntimeApi.listDocumentLiveRuns;
export const getPersonalMaterialDocumentLiveRun = personalMaterialRuntimeApi.getDocumentLiveRun;
export const createPersonalMaterialOCRLiveDryRun = personalMaterialRuntimeApi.createOCRLiveDryRun;
export const createPersonalMaterialOCRLiveRun = personalMaterialRuntimeApi.createOCRLiveRun;
export const listPersonalMaterialOCRLiveRuns = personalMaterialRuntimeApi.listOCRLiveRuns;
export const getPersonalMaterialOCRLiveRun = personalMaterialRuntimeApi.getOCRLiveRun;
export const getPersonalMaterialLiveReviewQueue = personalMaterialRuntimeApi.getLiveReviewQueue;
export const submitPersonalMaterialLiveReviewAction = personalMaterialRuntimeApi.submitLiveReviewAction;
export const getPersonalMaterialLiveSourceTraces = personalMaterialRuntimeApi.getLiveSourceTraces;
export const getPersonalMaterialLiveAudit = personalMaterialRuntimeApi.getLiveAudit;
export const getPersonalMaterialLiveSafety = personalMaterialRuntimeApi.getLiveSafety;
export const getPersonalIntelligenceStatus = personalIntelligenceApi.getStatus;
export const getPersonalIntelligenceProviders = personalIntelligenceApi.getProviders;
export const getPersonalIntelligenceProvider = personalIntelligenceApi.getProvider;
export const createPersonalLegalSearchMock = personalIntelligenceApi.createMockLegalSearch;
export const listPersonalLegalSearch = personalIntelligenceApi.listLegalSearch;
export const getPersonalLegalSearch = personalIntelligenceApi.getLegalSearch;
export const createPersonalEnterpriseQueryMock = personalIntelligenceApi.createMockEnterpriseQuery;
export const listPersonalEnterpriseQuery = personalIntelligenceApi.listEnterpriseQuery;
export const getPersonalEnterpriseQuery = personalIntelligenceApi.getEnterpriseQuery;
export const listPersonalIntelligenceSourceTraces = personalIntelligenceApi.listSourceTraces;
export const getPersonalIntelligenceSourceTrace = personalIntelligenceApi.getSourceTrace;
export const getPersonalIntelligenceConfirmationQueue = personalIntelligenceApi.getConfirmationQueue;
export const submitPersonalIntelligenceConfirmationAction = personalIntelligenceApi.submitConfirmationAction;
export const getPersonalIntelligenceAudit = personalIntelligenceApi.getAudit;
export const getPersonalIntelligenceSafety = personalIntelligenceApi.getSafety;
export const getPersonalIntelligenceLiveStatus = personalIntelligenceApi.getLiveStatus;
export const getPersonalIntelligenceLiveProviders = personalIntelligenceApi.getLiveProviders;
export const getPersonalIntelligenceLiveProvider = personalIntelligenceApi.getLiveProvider;
export const createPersonalIntelligenceLegalLiveDryRun = personalIntelligenceApi.createLegalLiveDryRun;
export const createPersonalIntelligenceLegalLiveRun = personalIntelligenceApi.createLegalLiveRun;
export const listPersonalIntelligenceLegalLiveRuns = personalIntelligenceApi.listLegalLiveRuns;
export const getPersonalIntelligenceLegalLiveRun = personalIntelligenceApi.getLegalLiveRun;
export const createPersonalIntelligenceEnterpriseLiveDryRun = personalIntelligenceApi.createEnterpriseLiveDryRun;
export const createPersonalIntelligenceEnterpriseLiveRun = personalIntelligenceApi.createEnterpriseLiveRun;
export const listPersonalIntelligenceEnterpriseLiveRuns = personalIntelligenceApi.listEnterpriseLiveRuns;
export const getPersonalIntelligenceEnterpriseLiveRun = personalIntelligenceApi.getEnterpriseLiveRun;
export const getPersonalIntelligenceLiveReviewQueue = personalIntelligenceApi.getLiveReviewQueue;
export const submitPersonalIntelligenceLiveReviewAction = personalIntelligenceApi.submitLiveReviewAction;
export const listPersonalIntelligenceLiveSourceTraces = personalIntelligenceApi.listLiveSourceTraces;
export const getPersonalIntelligenceLiveSourceTrace = personalIntelligenceApi.getLiveSourceTrace;
export const getPersonalIntelligenceLiveAudit = personalIntelligenceApi.getLiveAudit;
export const getPersonalIntelligenceLiveSafety = personalIntelligenceApi.getLiveSafety;
export const getPersonalSkillStudioStatus = personalSkillStudioApi.getStatus;
export const getPersonalSkillTrainingStatus = personalSkillStudioApi.getSkillTrainingStatus;
export const getPersonalSkillSampleRegistry = personalSkillStudioApi.getSkillSampleRegistry;
export const listPersonalSkillStudioRuntimes = personalSkillStudioApi.listRuntimes;
export const createPersonalExperiencePackage = personalSkillStudioApi.createExperiencePackage;
export const listPersonalExperiencePackages = personalSkillStudioApi.listExperiencePackages;
export const createPersonalSkillCandidate = personalSkillStudioApi.createSkillCandidate;
export const listPersonalSkillCandidates = personalSkillStudioApi.listSkillCandidates;
export const createPersonalSkillTestCase = personalSkillStudioApi.createTestCase;
export const listPersonalSkillTestCases = personalSkillStudioApi.listTestCases;
export const createPersonalSkillEvaluation = personalSkillStudioApi.createEvaluation;
export const listPersonalSkillEvaluations = personalSkillStudioApi.listEvaluations;
export const getPersonalSkillStudioPromotionQueue = personalSkillStudioApi.getPromotionQueue;
export const submitPersonalSkillStudioPromotionAction = personalSkillStudioApi.submitPromotionAction;
export const listPersonalSkillFinalDrafts = personalSkillStudioApi.listFinalDrafts;
export const getPersonalSkillFinalDraft = personalSkillStudioApi.getFinalDraft;
export const getPersonalSkillFinalDraftLineage = personalSkillStudioApi.getFinalDraftLineage;
export const getPersonalSkillFinalDraftBaseline = personalSkillStudioApi.getFinalDraftBaseline;
export const getPersonalSkillFinalDraftQuality = personalSkillStudioApi.getFinalDraftQuality;
export const getPersonalSkillFinalDraftGate = personalSkillStudioApi.getFinalDraftGate;
export const getPersonalSkillFinalDraftOptimization = personalSkillStudioApi.getFinalDraftOptimization;
export const getPersonalSkillFinalDraftSourceTraces = personalSkillStudioApi.getFinalDraftSourceTraces;
export const getPersonalSkillFinalDraftAudit = personalSkillStudioApi.getFinalDraftAudit;
export const createPersonalSkillFinalDraftOwnerDownload = personalSkillStudioApi.createFinalDraftOwnerDownload;
export const listPersonalSkillFinalDraftOwnerDownloads = personalSkillStudioApi.listFinalDraftOwnerDownloads;
export const getPersonalSkillFinalDraftOwnerDownload = personalSkillStudioApi.getFinalDraftOwnerDownload;
export const getPersonalSkillFinalDraftSafety = personalSkillStudioApi.getFinalDraftSafety;
export const getPersonalTrainingArtifactStatus = personalSkillStudioApi.getTrainingArtifactStatus;
export const getPersonalTrainingArtifactScheme = personalSkillStudioApi.getTrainingArtifactScheme;
export const getPersonalTrainingArtifactCaseCauseTaxonomy = personalSkillStudioApi.getTrainingArtifactCaseCauseTaxonomy;
export const getPersonalTrainingArtifactCaseCauseNode = personalSkillStudioApi.getTrainingArtifactCaseCauseNode;
export const listPersonalTrainingArtifactPackages = personalSkillStudioApi.listTrainingArtifactPackages;
export const getPersonalTrainingArtifactPackage = personalSkillStudioApi.getTrainingArtifactPackage;
export const listPersonalTrainingArtifactSkills = personalSkillStudioApi.listTrainingArtifactSkills;
export const getPersonalTrainingArtifactSkill = personalSkillStudioApi.getTrainingArtifactSkill;
export const listPersonalTrainingArtifactEvaluations = personalSkillStudioApi.listTrainingArtifactEvaluations;
export const listPersonalTrainingArtifactGates = personalSkillStudioApi.listTrainingArtifactGates;
export const listPersonalTrainingArtifactTestCases = personalSkillStudioApi.listTrainingArtifactTestCases;
export const listPersonalTrainingArtifactLoadingManifests = personalSkillStudioApi.listTrainingArtifactLoadingManifests;
export const matchPersonalTrainingArtifactCaseCause = personalSkillStudioApi.matchTrainingArtifactCaseCause;
export const createPersonalTrainingArtifactLoadDryRun = personalSkillStudioApi.createTrainingArtifactLoadDryRun;
export const listPersonalTrainingArtifactLoadDryRuns = personalSkillStudioApi.listTrainingArtifactLoadDryRuns;
export const getPersonalTrainingArtifactLoadDryRun = personalSkillStudioApi.getTrainingArtifactLoadDryRun;
export const listPersonalTrainingArtifactSkillContexts = personalSkillStudioApi.listTrainingArtifactSkillContexts;
export const getPersonalTrainingArtifactSkillContext = personalSkillStudioApi.getTrainingArtifactSkillContext;
export const getPersonalTrainingArtifactAudit = personalSkillStudioApi.getTrainingArtifactAudit;
export const getPersonalTrainingArtifactSafety = personalSkillStudioApi.getTrainingArtifactSafety;
export const listPersonalCodexTrainingRuns = personalSkillStudioApi.listCodexTrainingRuns;
export const createPersonalCodexTrainingRun = personalSkillStudioApi.createCodexTrainingRun;
export const getPersonalCodexTrainingRun = personalSkillStudioApi.getCodexTrainingRun;
export const getPersonalCodexTrainingRunSummary = personalSkillStudioApi.getCodexTrainingRunSummary;
export const getPersonalCodexTrainingRunCaseCausePackages = personalSkillStudioApi.getCodexTrainingRunCaseCausePackages;
export const getPersonalCodexTrainingRunGeneratedSkills = personalSkillStudioApi.getCodexTrainingRunGeneratedSkills;
export const getPersonalCodexTrainingRunEvaluations = personalSkillStudioApi.getCodexTrainingRunEvaluations;
export const getPersonalCodexTrainingRunGates = personalSkillStudioApi.getCodexTrainingRunGates;
export const getPersonalCodexTrainingRunTestCases = personalSkillStudioApi.getCodexTrainingRunTestCases;
export const getPersonalCodexTrainingRunLoadingManifest = personalSkillStudioApi.getCodexTrainingRunLoadingManifest;
export const createPersonalCodexTrainingRunLoadDryRun = personalSkillStudioApi.createCodexTrainingRunLoadDryRun;
export const getPersonalCodexTrainingRunAudit = personalSkillStudioApi.getCodexTrainingRunAudit;
export const getPersonalCodexTrainingRunSafety = personalSkillStudioApi.getCodexTrainingRunSafety;
export const getPersonalRealClosedCaseIntakeStatus = personalSkillStudioApi.getRealClosedCaseIntakeStatus;
export const createPersonalRealClosedCaseIntake = personalSkillStudioApi.createRealClosedCaseIntake;
export const listPersonalRealClosedCaseIntakes = personalSkillStudioApi.listRealClosedCaseIntakes;
export const getPersonalRealClosedCaseIntake = personalSkillStudioApi.getRealClosedCaseIntake;
export const getPersonalRealClosedCaseRedactionReport = personalSkillStudioApi.getRealClosedCaseRedactionReport;
export const createPersonalRealClosedCaseRedaction = personalSkillStudioApi.createRealClosedCaseRedaction;
export const getPersonalRealClosedCaseClassification = personalSkillStudioApi.getRealClosedCaseClassification;
export const createPersonalRealClosedCaseClassification = personalSkillStudioApi.createRealClosedCaseClassification;
export const getPersonalRealClosedCaseSegments = personalSkillStudioApi.getRealClosedCaseSegments;
export const createPersonalRealClosedCaseSegments = personalSkillStudioApi.createRealClosedCaseSegments;
export const getPersonalRealClosedCaseReviewQueue = personalSkillStudioApi.getRealClosedCaseReviewQueue;
export const submitPersonalRealClosedCaseReviewAction = personalSkillStudioApi.submitRealClosedCaseReviewAction;
export const getPersonalRealClosedCaseSourceTraces = personalSkillStudioApi.getRealClosedCaseSourceTraces;
export const getPersonalRealClosedCaseAudit = personalSkillStudioApi.getRealClosedCaseAudit;
export const getPersonalRealClosedCaseSafety = personalSkillStudioApi.getRealClosedCaseSafety;
export const getPersonalRawWorkProductBoundaryStatus = personalSkillStudioApi.getRawWorkProductBoundaryStatus;
export const createPersonalOcrJob = personalSkillStudioApi.createOcrJob;
export const listPersonalOcrJobs = personalSkillStudioApi.listOcrJobs;
export const getPersonalOcrJob = personalSkillStudioApi.getOcrJob;
export const createPersonalLegalRetrievalJob = personalSkillStudioApi.createLegalRetrievalJob;
export const listPersonalLegalRetrievalJobs = personalSkillStudioApi.listLegalRetrievalJobs;
export const getPersonalLegalRetrievalJob = personalSkillStudioApi.getLegalRetrievalJob;
export const buildPersonalExperienceCandidates = personalSkillStudioApi.buildExperienceCandidates;
export const listPersonalExperienceCandidates = personalSkillStudioApi.listExperienceCandidates;
export const getPersonalExperienceCandidate = personalSkillStudioApi.getExperienceCandidate;
export const redactPersonalExperienceCandidate = personalSkillStudioApi.redactExperienceCandidate;
export const reviewPersonalExperienceCandidate = personalSkillStudioApi.reviewExperienceCandidate;
export const getPersonalExperienceCandidateAudit = personalSkillStudioApi.getExperienceCandidateAudit;
export const getPersonalV731bTrainingExperiencePipelineStatus = personalSkillStudioApi.getV731bTrainingExperiencePipelineStatus;
export const getPersonalSkillExperiencePoolStatus = personalSkillStudioApi.getSkillExperiencePoolStatus;
export const importPersonalApprovedSkillExperience = personalSkillStudioApi.importApprovedSkillExperience;
export const listPersonalSkillExperiencePool = personalSkillStudioApi.listSkillExperiencePool;
export const getPersonalSkillExperiencePoolEntry = personalSkillStudioApi.getSkillExperiencePoolEntry;
export const createPersonalSkillExperienceBinding = personalSkillStudioApi.createSkillExperienceBinding;
export const listPersonalSkillExperienceBindings = personalSkillStudioApi.listSkillExperienceBindings;
export const getPersonalSkillExperienceBinding = personalSkillStudioApi.getSkillExperienceBinding;
export const listPersonalCodexSkillDrafts = personalSkillStudioApi.listCodexSkillDrafts;
export const buildPersonalCodexSkillDraft = personalSkillStudioApi.buildCodexSkillDraft;
export const getPersonalCodexSkillDraft = personalSkillStudioApi.getCodexSkillDraft;
export const reviewPersonalCodexSkillDraft = personalSkillStudioApi.reviewCodexSkillDraft;
export const getPersonalCodexSkillDraftAudit = personalSkillStudioApi.getCodexSkillDraftAudit;
export const getPersonalV731cSkillExperiencePipelineStatus = personalSkillStudioApi.getV731cSkillExperiencePipelineStatus;
export const listPersonalSkillPackages = personalSkillStudioApi.listSkillPackages;
export const getPersonalSkillPackageDetail = personalSkillStudioApi.getSkillPackageDetail;
export const buildPersonalSkillPackage = personalSkillStudioApi.buildSkillPackage;
export const validatePersonalSkillPackage = personalSkillStudioApi.validateSkillPackage;
export const getPersonalSkillPackageManifest = personalSkillStudioApi.getSkillPackageManifest;
export const getPersonalSkillPackageAudit = personalSkillStudioApi.getSkillPackageAudit;
export const getPersonalSkillPackageSourceTrace = personalSkillStudioApi.getSkillPackageSourceTrace;
export const getPersonalV731dPipelineStatus = personalSkillStudioApi.getV731dPipelineStatus;
export const listPersonalTrainingTasks = personalSkillStudioApi.listTrainingTasks;
export const buildPersonalTrainingTask = personalSkillStudioApi.buildTrainingTask;
export const listPersonalTrainingPackages = personalSkillStudioApi.listTrainingPackages;
export const buildPersonalExperiencePackage = personalSkillStudioApi.buildExperiencePackage;
export const getPersonalTrainingPackage = personalSkillStudioApi.getTrainingPackage;
export const getPersonalExperiencePackageAudit = personalSkillStudioApi.getExperiencePackageAudit;
export const getPersonalExperiencePackageSourceTrace = personalSkillStudioApi.getExperiencePackageSourceTrace;
export const getPersonalV731ePipelineStatus = personalSkillStudioApi.getV731ePipelineStatus;
export const listPersonalPracticeLoadPackages = personalSkillStudioApi.listPracticeLoadPackages;
export const getPersonalPracticeLoadPackage = personalSkillStudioApi.getPracticeLoadPackage;
export const editPersonalPracticeLoadPackage = personalSkillStudioApi.editPracticeLoadPackage;
export const savePersonalPracticeLoadPackage = personalSkillStudioApi.savePracticeLoadPackage;
export const revalidatePersonalPracticeLoadPackage = personalSkillStudioApi.revalidatePracticeLoadPackage;
export const approvePersonalPracticeLoadPackage = personalSkillStudioApi.approvePracticeLoadPackage;
export const rejectPersonalPracticeLoadPackage = personalSkillStudioApi.rejectPracticeLoadPackage;
export const getPersonalPracticeLoadPackageAudit = personalSkillStudioApi.getPracticeLoadPackageAudit;
export const getPersonalPracticeLoadPackageSourceTrace = personalSkillStudioApi.getPracticeLoadPackageSourceTrace;
export const getPersonalV731fPipelineStatus = personalSkillStudioApi.getV731fPipelineStatus;
export const getPersonalExperienceLifecycleStatus = personalSkillStudioApi.getExperienceLifecycleStatus;
export const listPersonalExperienceLifecycles = personalSkillStudioApi.listExperienceLifecycles;
export const getPersonalExperienceLifecycle = personalSkillStudioApi.getExperienceLifecycle;
export const getPersonalExperienceLifecycleState = personalSkillStudioApi.getExperienceLifecycleState;
export const getPersonalExperienceLifecycleGraph = personalSkillStudioApi.getExperienceLifecycleGraph;
export const getPersonalExperienceLifecycleAuditTimeline = personalSkillStudioApi.getExperienceLifecycleAuditTimeline;
export const getPersonalExperienceLifecycleSourceTraceView = personalSkillStudioApi.getExperienceLifecycleSourceTraceView;
export const getPersonalExperienceLifecycleIntegrityCheck = personalSkillStudioApi.getExperienceLifecycleIntegrityCheck;
export const getPersonalExperienceLifecycleSafetySummary = personalSkillStudioApi.getExperienceLifecycleSafetySummary;
export const recomputePersonalExperienceLifecycle = personalSkillStudioApi.recomputeExperienceLifecycle;
export const getPersonalV732ExperienceLifecycleStatus = personalSkillStudioApi.getV732ExperienceLifecycleStatus;
export const getPersonalCaseAnalysisWorkbenchStatus = personalSkillStudioApi.getCaseAnalysisWorkbenchStatus;
export const listPersonalCaseAnalysisWorkbenchViews = personalSkillStudioApi.listCaseAnalysisWorkbenchViews;
export const getPersonalCaseAnalysisWorkbenchView = personalSkillStudioApi.getCaseAnalysisWorkbenchView;
export const getPersonalCaseAnalysisWorkbenchSchema = personalSkillStudioApi.getCaseAnalysisWorkbenchSchema;
export const getPersonalCaseAnalysisWorkbenchOutputs = personalSkillStudioApi.getCaseAnalysisWorkbenchOutputs;
export const getPersonalCaseAnalysisRuntimeOutput = personalSkillStudioApi.getCaseAnalysisRuntimeOutput;
export const markPersonalCaseAnalysisOutputReviewed = personalSkillStudioApi.markCaseAnalysisOutputReviewed;
export const submitPersonalCaseAnalysisOutputFeedback = personalSkillStudioApi.submitCaseAnalysisOutputFeedback;
export const submitPersonalCaseAnalysisOutputRiskEvent = personalSkillStudioApi.submitCaseAnalysisOutputRiskEvent;
export const listPersonalCaseAnalysisOutputFeedback = personalSkillStudioApi.listCaseAnalysisOutputFeedback;
export const listPersonalCaseAnalysisOutputRiskEvents = personalSkillStudioApi.listCaseAnalysisOutputRiskEvents;
export const getPersonalCaseAnalysisOutputAudit = personalSkillStudioApi.getCaseAnalysisOutputAudit;
export const getPersonalCaseAnalysisOutputSourceTrace = personalSkillStudioApi.getCaseAnalysisOutputSourceTrace;
export const getPersonalV733CaseAnalysisWorkbenchStatus = personalSkillStudioApi.getV733CaseAnalysisWorkbenchStatus;
export const listPersonalSkillStudioSourceTraces = personalSkillStudioApi.listSourceTraces;
export const getPersonalSkillStudioAudit = personalSkillStudioApi.getAudit;
export const getPersonalSkillStudioSafety = personalSkillStudioApi.getSafety;
export const getPersonalCaseProductionStatus = personalCaseProductionApi.getStatus;
export const listPersonalCaseProductionWorkflowStages = personalCaseProductionApi.listWorkflowStages;
export const createPersonalProductionCase = personalCaseProductionApi.createProductionCase;
export const listPersonalProductionCases = personalCaseProductionApi.listProductionCases;
export const createPersonalWorkflowRun = personalCaseProductionApi.createWorkflowRun;
export const listPersonalWorkflowRuns = personalCaseProductionApi.listWorkflowRuns;
export const createPersonalStageRun = personalCaseProductionApi.createStageRun;
export const listPersonalStageRuns = personalCaseProductionApi.listStageRuns;
export const listPersonalCaseProductionReadiness = personalCaseProductionApi.listReadiness;
export const getPersonalCaseProductionReadiness = personalCaseProductionApi.getReadiness;
export const getPersonalCaseProductionReviewGates = personalCaseProductionApi.getReviewGates;
export const submitPersonalCaseProductionReviewGateAction = personalCaseProductionApi.submitReviewGateAction;
export const listPersonalCaseProductionSourceTraces = personalCaseProductionApi.listSourceTraces;
export const getPersonalCaseProductionAudit = personalCaseProductionApi.getAudit;
export const getPersonalCaseProductionSafety = personalCaseProductionApi.getSafety;
export const getPersonalCaseAnalysisStatus = personalCaseAnalysisApi.getStatus;
export const listPersonalCaseAnalysisRuntimes = personalCaseAnalysisApi.listRuntimes;
export const getPersonalCaseAnalysisRuntime = personalCaseAnalysisApi.getRuntime;
export const getPersonalCaseAnalysisSkillBaselines = personalCaseAnalysisApi.getSkillBaselines;
export const createPersonalCaseAnalysisRun = personalCaseAnalysisApi.createRun;
export const createPersonalCaseAnalysisControlledRun = personalCaseAnalysisApi.createControlledRun;
export const listPersonalCaseAnalysisRuns = personalCaseAnalysisApi.listRuns;
export const getPersonalCaseAnalysisRun = personalCaseAnalysisApi.getRun;
export const createPersonalCaseAnalysisFactDraft = personalCaseAnalysisApi.createFactDraft;
export const listPersonalCaseAnalysisFactDrafts = personalCaseAnalysisApi.listFactDrafts;
export const getPersonalCaseAnalysisFactDraft = personalCaseAnalysisApi.getFactDraft;
export const createPersonalCaseAnalysisLegalDraft = personalCaseAnalysisApi.createLegalDraft;
export const listPersonalCaseAnalysisLegalDrafts = personalCaseAnalysisApi.listLegalDrafts;
export const getPersonalCaseAnalysisLegalDraft = personalCaseAnalysisApi.getLegalDraft;
export const listPersonalCaseAnalysisLegalDraftVersions = personalCaseAnalysisApi.listLegalDraftVersions;
export const createPersonalCaseAnalysisLegalDraftVersion = personalCaseAnalysisApi.createLegalDraftVersion;
export const getPersonalCaseAnalysisLegalDraftQuality = personalCaseAnalysisApi.getLegalDraftQuality;
export const getPersonalCaseAnalysisLegalDraftGate = personalCaseAnalysisApi.getLegalDraftGate;
export const confirmPersonalCaseAnalysisLegalDraftForReview = personalCaseAnalysisApi.confirmLegalDraftForReview;
export const getPersonalCaseAnalysisReviewQueue = personalCaseAnalysisApi.getReviewQueue;
export const submitPersonalCaseAnalysisReviewAction = personalCaseAnalysisApi.submitReviewAction;
export const listPersonalCaseAnalysisEvaluations = personalCaseAnalysisApi.listEvaluations;
export const getPersonalCaseAnalysisEvaluation = personalCaseAnalysisApi.getEvaluation;
export const listPersonalCaseAnalysisGates = personalCaseAnalysisApi.listGates;
export const getPersonalCaseAnalysisGate = personalCaseAnalysisApi.getGate;
export const listPersonalCaseAnalysisSourceTraces = personalCaseAnalysisApi.listSourceTraces;
export const getPersonalCaseAnalysisSourceTrace = personalCaseAnalysisApi.getSourceTrace;
export const getPersonalCaseAnalysisAudit = personalCaseAnalysisApi.getAudit;
export const getPersonalCaseAnalysisSafety = personalCaseAnalysisApi.getSafety;
export const getPersonalCaseWorkspaceStatus = personalCaseWorkspaceApi.getStatus;
export const listPersonalCaseWorkspaceCases = personalCaseWorkspaceApi.listCases;
export const getPersonalCaseWorkspaceCase = personalCaseWorkspaceApi.getCase;
export const listPersonalCaseWorkspaceMaterials = personalCaseWorkspaceApi.listMaterials;
export const getPersonalCaseWorkspaceMaterial = personalCaseWorkspaceApi.getMaterial;
export const createPersonalCaseWorkspaceOwnerRawView = personalCaseWorkspaceApi.createOwnerRawView;
export const getPersonalCaseWorkspaceOCRStatus = personalCaseWorkspaceApi.getOCRStatus;
export const getPersonalCaseWorkspaceMaterialSourceTraces = personalCaseWorkspaceApi.getMaterialSourceTraces;
export const getPersonalCaseWorkspaceFactInput = personalCaseWorkspaceApi.getFactInput;
export const createPersonalCaseWorkspaceFactCorrection = personalCaseWorkspaceApi.createFactCorrection;
export const listPersonalCaseWorkspaceSourceTraces = personalCaseWorkspaceApi.listSourceTraces;
export const getPersonalCaseWorkspaceAudit = personalCaseWorkspaceApi.getAudit;
export const getPersonalCaseWorkspaceSafety = personalCaseWorkspaceApi.getSafety;
export const listPersonalCaseWorkspaceFactPreviews = personalCaseWorkspaceApi.listFactPreviews;
export const createPersonalCaseWorkspaceFactPreview = personalCaseWorkspaceApi.createFactPreview;
export const getPersonalCaseWorkspaceFactPreview = personalCaseWorkspaceApi.getFactPreview;
export const createPersonalCaseWorkspaceFactPreviewCorrection = personalCaseWorkspaceApi.createFactPreviewCorrection;
export const listPersonalCaseWorkspaceFactPreviewCorrections = personalCaseWorkspaceApi.listFactPreviewCorrections;
export const getPersonalCaseWorkspaceFactCorrection = personalCaseWorkspaceApi.getFactCorrection;
export const listPersonalCaseWorkspaceFactPreviewVersions = personalCaseWorkspaceApi.listFactPreviewVersions;
export const createPersonalCaseWorkspaceFactPreviewVersion = personalCaseWorkspaceApi.createFactPreviewVersion;
export const getPersonalCaseWorkspaceFactPreviewQuality = personalCaseWorkspaceApi.getFactPreviewQuality;
export const getPersonalCaseWorkspaceFactPreviewGate = personalCaseWorkspaceApi.getFactPreviewGate;
export const getPersonalCaseWorkspaceFactPreviewSourceTraces = personalCaseWorkspaceApi.getFactPreviewSourceTraces;
export const confirmPersonalCaseWorkspaceFactPreviewForLegalAnalysis = personalCaseWorkspaceApi.confirmFactPreviewForLegalAnalysis;
export const getPersonalCaseWorkspaceFactInputReadiness = personalCaseWorkspaceApi.getFactInputReadiness;
export const getPersonalCaseWorkspaceFactAudit = personalCaseWorkspaceApi.getFactAudit;
export const getPersonalCaseWorkspaceFactSafety = personalCaseWorkspaceApi.getFactSafety;
export const getPersonalProductionPilotStatus = personalProductionPilotApi.getStatus;
export const getPersonalProductionPilotReadiness = personalProductionPilotApi.getReadiness;
export const getPersonalProductionPilotWorkflow = personalProductionPilotApi.getWorkflow;
export const listPersonalProductionPilotRuntimes = personalProductionPilotApi.listRuntimes;
export const getPersonalProductionPilotProviderGates = personalProductionPilotApi.getProviderGates;
export const getPersonalProductionPilotSafety = personalProductionPilotApi.getSafety;
export const createPersonalProductionPilotRun = personalProductionPilotApi.createRun;
export const createPersonalProductionPilotControlledRun = personalProductionPilotApi.createControlledRun;
export const listPersonalProductionPilotRuns = personalProductionPilotApi.listRuns;
export const getPersonalProductionPilotRun = personalProductionPilotApi.getRun;
export const getPersonalProductionPilotCaseAnalysisSummary = personalProductionPilotApi.getCaseAnalysisSummary;
export const listPersonalProductionPilotSkillFinalDrafts = personalProductionPilotApi.listSkillFinalDrafts;
export const getPersonalProductionPilotSkillFinalDraft = personalProductionPilotApi.getSkillFinalDraft;
export const createPersonalProductionPilotOutput = personalProductionPilotApi.createOutput;
export const listPersonalProductionPilotOutputs = personalProductionPilotApi.listOutputs;
export const getPersonalProductionPilotOutput = personalProductionPilotApi.getOutput;
export const createPersonalProductionPilotOwnerDownload = personalProductionPilotApi.createOwnerDownload;
export const listPersonalProductionPilotOwnerDownloads = personalProductionPilotApi.listOwnerDownloads;
export const getPersonalProductionPilotOwnerDownload = personalProductionPilotApi.getOwnerDownload;
export const getPersonalProductionPilotReviewQueue = personalProductionPilotApi.getReviewQueue;
export const submitPersonalProductionPilotReviewAction = personalProductionPilotApi.submitReviewAction;
export const listPersonalProductionPilotSourceTraces = personalProductionPilotApi.listSourceTraces;
export const getPersonalProductionPilotAudit = personalProductionPilotApi.getAudit;
export const getPersonalProductionPilotExportBoundary = personalProductionPilotApi.getExportBoundary;
export const getPersonalProductionPilotDashboardStatus = personalProductionPilotApi.getDashboardStatus;
export const getPersonalProductionPilotDashboardMetrics = personalProductionPilotApi.getDashboardMetrics;
export const getPersonalProductionPilotDashboardQuality = personalProductionPilotApi.getDashboardQuality;
export const getPersonalProductionPilotDashboardSafety = personalProductionPilotApi.getDashboardSafety;
export const getPersonalOwnerOutputCenterStatus = personalOwnerOutputCenterApi.getStatus;
export const listPersonalOwnerOutputCenterOutputs = personalOwnerOutputCenterApi.listOutputs;
export const getPersonalOwnerOutputCenterOutput = personalOwnerOutputCenterApi.getOutput;
export const getPersonalOwnerOutputCenterOutputQuality = personalOwnerOutputCenterApi.getOutputQuality;
export const getPersonalOwnerOutputCenterOutputGate = personalOwnerOutputCenterApi.getOutputGate;
export const getPersonalOwnerOutputCenterOutputOptimization = personalOwnerOutputCenterApi.getOutputOptimization;
export const getPersonalOwnerOutputCenterOutputSourceTraces = personalOwnerOutputCenterApi.getOutputSourceTraces;
export const createPersonalOwnerOutputCenterDownload = personalOwnerOutputCenterApi.createDownload;
export const listPersonalOwnerOutputCenterDownloads = personalOwnerOutputCenterApi.listDownloads;
export const getPersonalOwnerOutputCenterDownload = personalOwnerOutputCenterApi.getDownload;
export const getPersonalOwnerOutputCenterAudit = personalOwnerOutputCenterApi.getAudit;
export const getPersonalOwnerOutputCenterSafety = personalOwnerOutputCenterApi.getSafety;
export const getPersonalTrialReadinessStatus = personalTrialReadinessApi.getStatus;
export const getPersonalTrialReadinessChecklist = personalTrialReadinessApi.getChecklist;
export const getPersonalTrialReadinessSafety = personalTrialReadinessApi.getSafety;
export const createPersonalTrialReadinessTrial = personalTrialReadinessApi.createTrial;
export const listPersonalTrialReadinessTrials = personalTrialReadinessApi.listTrials;
export const getPersonalTrialReadinessTrial = personalTrialReadinessApi.getTrial;
export const getPersonalTrialReadinessTrialChecklist = personalTrialReadinessApi.getTrialChecklist;
export const createPersonalTrialReadinessTrialChecklist = personalTrialReadinessApi.createTrialChecklist;
export const listPersonalTrialReadinessObservations = personalTrialReadinessApi.listObservations;
export const createPersonalTrialReadinessObservation = personalTrialReadinessApi.createObservation;
export const listPersonalTrialReadinessTrialIssues = personalTrialReadinessApi.listTrialIssues;
export const createPersonalTrialReadinessIssue = personalTrialReadinessApi.createIssue;
export const listPersonalTrialReadinessIssues = personalTrialReadinessApi.listIssues;
export const getPersonalTrialReadinessIssue = personalTrialReadinessApi.getIssue;
export const getPersonalTrialReadinessQuality = personalTrialReadinessApi.getQuality;
export const createPersonalTrialReadinessQuality = personalTrialReadinessApi.createQuality;
export const getPersonalTrialReadinessSafetyConfirmation = personalTrialReadinessApi.getSafetyConfirmation;
export const createPersonalTrialReadinessSafetyConfirmation = personalTrialReadinessApi.createSafetyConfirmation;
export const listPersonalTrialReadinessOptimizationBacklog = personalTrialReadinessApi.listOptimizationBacklog;
export const createPersonalTrialReadinessOptimizationBacklog = personalTrialReadinessApi.createOptimizationBacklog;
export const getPersonalTrialReadinessAudit = personalTrialReadinessApi.getAudit;
export const getPersonalProviderReadinessStatus = personalProviderReadinessApi.getStatus;
export const listPersonalProviderReadinessProviders = personalProviderReadinessApi.listProviders;
export const getPersonalProviderReadinessProvider = personalProviderReadinessApi.getProvider;
export const getPersonalProviderReadinessSecretBoundary = personalProviderReadinessApi.getSecretBoundary;
export const getPersonalProviderReadinessLiveGate = personalProviderReadinessApi.getLiveGate;
export const getPersonalProviderReadinessUsagePolicy = personalProviderReadinessApi.getUsagePolicy;
export const getPersonalProviderReadinessHealthDryRun = personalProviderReadinessApi.getHealthDryRun;
export const listPersonalProviderReadinessCategories = personalProviderReadinessApi.listCategories;
export const listPersonalProviderReadinessCategoryProviders = personalProviderReadinessApi.listCategoryProviders;
export const createPersonalProviderReadinessLiveGateMock = personalProviderReadinessApi.createLiveGateMock;
export const listPersonalProviderReadinessLiveGates = personalProviderReadinessApi.listLiveGates;
export const getPersonalProviderReadinessAudit = personalProviderReadinessApi.getAudit;
export const getPersonalProviderReadinessSafety = personalProviderReadinessApi.getSafety;
export const getPersonalLiveConnectionStatus = personalLiveConnectionApi.getStatus;
export const listPersonalLiveConnectionRuntimes = personalLiveConnectionApi.listRuntimes;
export const listPersonalLiveConnectionProviders = personalLiveConnectionApi.listProviders;
export const getPersonalLiveConnectionProvider = personalLiveConnectionApi.getProvider;
export const getPersonalLiveConnectionSecretBoundary = personalLiveConnectionApi.getSecretBoundary;
export const getPersonalLiveConnectionLiveGate = personalLiveConnectionApi.getLiveGate;
export const getPersonalLiveConnectionUsagePolicy = personalLiveConnectionApi.getUsagePolicy;
export const getPersonalLiveConnectionHealthDryRun = personalLiveConnectionApi.getHealthDryRun;
export const createPersonalLiveConnectionDryRun = personalLiveConnectionApi.createDryRun;
export const createPersonalLiveConnectionRun = personalLiveConnectionApi.createRun;
export const listPersonalLiveConnectionRuns = personalLiveConnectionApi.listRuns;
export const getPersonalLiveConnectionRun = personalLiveConnectionApi.getRun;
export const getPersonalLiveConnectionAudit = personalLiveConnectionApi.getAudit;
export const getPersonalLiveConnectionSafety = personalLiveConnectionApi.getSafety;
export const getPersonalLegalEnterpriseStatus = personalLegalEnterpriseApi.getStatus;
export const listPersonalLegalEnterpriseProviders = personalLegalEnterpriseApi.listProviders;
export const getPersonalLegalEnterpriseProvider = personalLegalEnterpriseApi.getProvider;
export const getPersonalLegalEnterpriseSecretBoundary = personalLegalEnterpriseApi.getSecretBoundary;
export const getPersonalLegalEnterpriseLiveGate = personalLegalEnterpriseApi.getLiveGate;
export const getPersonalLegalEnterpriseUsagePolicy = personalLegalEnterpriseApi.getUsagePolicy;
export const getPersonalLegalEnterpriseHealthDryRun = personalLegalEnterpriseApi.getHealthDryRun;
export const listPersonalLegalEnterpriseCategories = personalLegalEnterpriseApi.listCategories;
export const listPersonalLegalEnterpriseCategoryProviders = personalLegalEnterpriseApi.listCategoryProviders;
export const createPersonalLegalEnterpriseLiveGateMock = personalLegalEnterpriseApi.createLiveGateMock;
export const listPersonalLegalEnterpriseLiveGates = personalLegalEnterpriseApi.listLiveGates;
export const createPersonalLegalSearchDryRun = personalLegalEnterpriseApi.createLegalSearchDryRun;
export const createPersonalLegalSearchRun = personalLegalEnterpriseApi.createLegalSearchRun;
export const listPersonalLegalSearchRuns = personalLegalEnterpriseApi.listLegalSearchRuns;
export const createPersonalEnterpriseLookupDryRun = personalLegalEnterpriseApi.createEnterpriseLookupDryRun;
export const createPersonalEnterpriseLookupRun = personalLegalEnterpriseApi.createEnterpriseLookupRun;
export const listPersonalEnterpriseLookupRuns = personalLegalEnterpriseApi.listEnterpriseLookupRuns;
export const getPersonalLegalEnterpriseReviewQueue = personalLegalEnterpriseApi.getReviewQueue;
export const submitPersonalLegalEnterpriseReviewAction = personalLegalEnterpriseApi.submitReviewAction;
export const getPersonalLegalEnterpriseSourceTraces = personalLegalEnterpriseApi.getSourceTraces;
export const getPersonalLegalEnterpriseAudit = personalLegalEnterpriseApi.getAudit;
export const getPersonalLegalEnterpriseSafety = personalLegalEnterpriseApi.getSafety;
export const getControlledMaterialStatus = controlledMaterialApi.status;
export const runControlledMaterialReadConfirmed = controlledMaterialApi.readConfirmed;
export const runControlledLocalReadPreview = controlledMaterialApi.localReadPreview;
export const getControlledReadPreview = controlledMaterialApi.readPreview;
export const generateControlledReportDraft = controlledMaterialApi.reportDraft;
export const getControlledMaterialAuditLogs = controlledMaterialApi.auditLogs;
export const getControlledOCRStatus = controlledOCRApi.status;
export const runControlledOCRPreview = controlledOCRApi.preview;
export const getControlledOCRPreview = controlledOCRApi.readPreview;
export const getControlledOCRAuditLogs = controlledOCRApi.auditLogs;
export const getControlledLegalSearchStatus = controlledLegalSearchApi.status;
export const runControlledLegalSearchPreview = controlledLegalSearchApi.preview;
export const getControlledLegalSearchPreview = controlledLegalSearchApi.readPreview;
export const resolveControlledLegalCitation = controlledLegalSearchApi.resolveCitation;
export const getControlledLegalSearchAuditLogs = controlledLegalSearchApi.auditLogs;
export const getControlledReportDraftStatus = controlledReportDraftApi.status;
export const assembleControlledReportDraft = controlledReportDraftApi.assemble;
export const getControlledReportDraft = controlledReportDraftApi.readDraft;
export const getControlledReportDraftAuditLogs = controlledReportDraftApi.auditLogs;
export const getControlledLawyerReviewStatus = controlledLawyerReviewApi.status;
export const submitControlledLawyerReview = controlledLawyerReviewApi.submit;
export const getControlledLawyerReview = controlledLawyerReviewApi.readReview;
export const approveControlledLawyerReview = controlledLawyerReviewApi.approve;
export const rejectControlledLawyerReview = controlledLawyerReviewApi.reject;
export const requestRevisionControlledLawyerReview = controlledLawyerReviewApi.requestRevision;
export const getControlledLawyerReviewAuditLogs = controlledLawyerReviewApi.auditLogs;
export const getControlledRevisionStatus = controlledRevisionApi.status;
export const requestControlledRevision = controlledRevisionApi.requestRevision;
export const getControlledRevision = controlledRevisionApi.readRevision;
export const getControlledRevisionAuditLogs = controlledRevisionApi.auditLogs;
export const getControlledFinalReviewStatus = controlledFinalReviewApi.status;
export const lockControlledFinalReview = controlledFinalReviewApi.lock;
export const getControlledFinalReviewLock = controlledFinalReviewApi.readLock;
export const getControlledFinalReviewAuditLogs = controlledFinalReviewApi.auditLogs;
export const getCurrentUser = userApi.me;
export const getAuthStatus = authApi.status;
export const loginLocal = authApi.loginLocal;
export const logoutLocal = authApi.logoutLocal;
export const loginWithDevToken = authApi.loginLocal;
export const getWorkspaces = workspaceApi.list;
export const getWorkspace = workspaceApi.get;
export const getWorkspaceCases = workspaceApi.cases;
export const getCases = caseApi.listWithLocalFallback;
export const createCase = caseApi.create;
export const getCase = caseApi.get;
export const getCaseIntakeStatus = caseApi.intakeStatus;
export const getCaseRuntimeRuns = runtimeRunApi.listByCase;
export const getCaseLatestRuntimeRuns = runtimeRunApi.latestByCase;
export const getCaseMaterials = materialApi.listByCase;
export const uploadMaterial = materialApi.upload;
export const uploadMaterialsBatch = materialApi.uploadBatch;
export const uploadFolderMaterials = materialApi.uploadBatch;
export const getCaseFacts = factApi.listByCase;
export const extractFacts = factApi.extract;
export const getCaseAnalyses = analysisApi.listByCase;
export const getCaseAnalysis = analysisApi.listByCase;
export const runLegalAnalysis = analysisApi.run;
export const getCaseReports = reportApi.listByCase;
export const getReports = reportApi.list;
export const getReport = reportApi.get;
export const generateReport = reportApi.generate;
export const getSkills = skillApi.list;
export const getSkill = skillApi.get;
export const evaluateSkill = skillApi.evaluate;
export const getWorkspaceSkills = skillApi.listPublished;
export const getWorkspaceSkill = skillApi.getPublished;
export const applySkillToCase = skillApi.applyToCase;
export const getCaseSkills = skillApi.listForCase;
export const getLlmStatus = runtimeApi.llmStatus;
export const getExperiencePackages = experiencePackageApi.list;
export const getExperiencePackage = experiencePackageApi.get;
export const getExperiencePackageManifest = experiencePackageApi.getManifest;
export const buildExperiencePackage = experiencePackageApi.buildForSkill;
export const createExperiencePackageCandidate = experiencePackageApi.createCandidate;
export const reviewExperiencePackage = experiencePackageApi.review;
export const getSkillRegistry = skillRegistryApi.list;
export const getSkillRegistryDetail = skillRegistryApi.get;
export const publishSkillToRegistry = skillRegistryApi.publish;
export const publishExperiencePackageToSkillRegistry = skillRegistryApi.publishExperiencePackage;
export const deprecateSkillInRegistry = skillRegistryApi.deprecate;
export const rollbackSkillInRegistry = skillRegistryApi.rollback;
export const getVersionedTrainingPackages = versionedTrainingPackageApi.list;
export const getVersionedTrainingPackage = versionedTrainingPackageApi.get;
export const getVersionedTrainingPackageFiles = versionedTrainingPackageApi.files;
export const getVersionedTrainingPackagesByCaseCause = versionedTrainingPackageApi.byCaseCause;
export const getVersionedTrainingRuns = versionedTrainingRunApi.list;
export const getVersionedTrainingRun = versionedTrainingRunApi.get;
export const createMockVersionedTrainingRun = versionedTrainingRunApi.createMock;
export const getCaseCauseTaxonomy = caseCauseTaxonomyApi.list;
export const getCaseCause = caseCauseTaxonomyApi.get;
export const getCaseCauseAncestors = caseCauseTaxonomyApi.ancestors;
export const getCaseCauseChildren = caseCauseTaxonomyApi.children;

export async function getCaseDetail(caseId: string): Promise<CaseDetail> {
  const [caseRecord, intakeStatus, materials, facts, analyses, reports, runtimeRuns] = await Promise.all([
    caseApi.get(caseId),
    caseApi.intakeStatus(caseId).catch(() => null),
    materialApi.listByCase(caseId),
    factApi.listByCase(caseId),
    analysisApi.listByCase(caseId),
    reportApi.listByCase(caseId),
    runtimeRunApi.listByCase(caseId).catch(() => null)
  ]);

  return {
    case: caseRecord,
    intakeStatus,
    materials,
    facts,
    analyses,
    reports,
    runtimeRuns
  };
}

function getFileRelativePath(file: File) {
  const fileWithFolderPath = file as File & { webkitRelativePath?: string };
  return fileWithFolderPath.webkitRelativePath || file.name;
}
