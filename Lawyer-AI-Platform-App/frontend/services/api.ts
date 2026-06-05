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
  PersonalAlphaCaseOSFinalLockConsolidation,
  PersonalAlphaCaseOSMetadataClosure,
  PersonalAlphaCaseOSMetadataClosureBlockers,
  PersonalAlphaCaseOSMetadataClosureChecklist,
  PersonalAlphaCaseOSMetadataClosureExportPreview,
  PersonalAlphaCaseOSNextAction,
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
  PersonalAlphaCaseOSFinalLockConsolidation,
  PersonalAlphaCaseOSMetadataClosure,
  PersonalAlphaCaseOSMetadataClosureBlockers,
  PersonalAlphaCaseOSMetadataClosureChecklist,
  PersonalAlphaCaseOSMetadataClosureExportPreview,
  PersonalAlphaCaseOSNextAction,
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
    const payload = await response.json();
    if (typeof payload.detail === "string") {
      return payload.detail;
    }
  } catch {
    // Fall through to the generic message.
  }
  return `API request failed: ${path}`;
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
export const getPersonalAlphaCaseOSNextAction = personalAlphaCaseOSApi.getNextAction;
export const getPersonalAlphaCaseOSStageOrchestration = personalAlphaCaseOSApi.getStageOrchestration;
export const getPersonalAlphaCaseOSStageTransitions = personalAlphaCaseOSApi.getStageTransitions;
export const getPersonalAlphaCaseOSActionEligibility = personalAlphaCaseOSApi.getActionEligibility;
export const getPersonalAlphaCaseOSBlockers = personalAlphaCaseOSApi.getBlockers;
export const getPersonalAlphaCaseOSSafetyChecklist = personalAlphaCaseOSApi.getSafetyChecklist;
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
