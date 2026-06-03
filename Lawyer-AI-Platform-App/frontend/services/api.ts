import type {
  AuthStatus,
  Case,
  CaseSkillBinding,
  DashboardStats,
  Fact,
  LegalAnalysis,
  Material,
  Report,
  RuntimeStatus,
  Skill,
  ExperiencePackage,
  ExperiencePackageDetail,
  SkillRegistryDetail,
  SkillRegistryEntry,
  User,
  Workspace
} from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8001";
const TOKEN_STORAGE_KEY = "lawyer_ai_access_token";
const DEFAULT_LOCAL_DEV_TOKEN = "dev-local-token";

export type {
  AuthStatus,
  Case as CaseRecord,
  CaseSkillBinding,
  DashboardStats,
  Fact as FactRecord,
  LegalAnalysis as LegalAnalysisRecord,
  Material as MaterialRecord,
  Report as ReportRecord,
  RuntimeStatus as LLMStatus,
  ExperiencePackage as ExperiencePackageRecord,
  SkillRegistryEntry as SkillRegistryRecord,
  Skill as WorkspaceSkillRecord,
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
  materials: Material[];
  facts: Fact[];
  analyses: LegalAnalysis[];
  reports: Report[];
};

export type CaseCreatePayload = {
  title: string;
  client_name?: string | null;
  counterparty_name?: string | null;
  case_type?: string | null;
  contract_type?: string | null;
  dispute_amount?: string | null;
  objective?: string | null;
  jurisdiction?: string | null;
  intake_notes?: string | null;
};

export type ExtractFactsResponse = {
  case_id: string;
  facts: Fact[];
  skill_used?: string;
  package_used?: string;
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
  get: (caseId: string) => request<Case>(`/cases/${caseId}`)
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
  buildForSkill: (skillId: string) => postJson<ExperiencePackage>(`/skills/${skillId}/packages/build`)
};

export const skillRegistryApi = {
  list: async () => {
    const response = await request<{ skills: SkillRegistryEntry[] }>("/skill-registry");
    return response.skills;
  },
  get: (skillId: string) => request<SkillRegistryDetail>(`/skill-registry/${skillId}`),
  publish: (skillId: string) => postJson<Record<string, unknown>>(`/skill-registry/${skillId}/publish`),
  deprecate: (skillId: string) => postJson<Record<string, unknown>>(`/skill-registry/${skillId}/deprecate`)
};

export const runtimeApi = {
  health: () => request<{ status: string }>("/health"),
  llmStatus: () => request<RuntimeStatus>("/llm/status"),
  dashboardStats: () => request<DashboardStats>("/dashboard/stats")
};

// Future resource groups: experiencePackageApi, auditApi, settingsApi.

export const getHealth = runtimeApi.health;
export const getDashboardStats = runtimeApi.dashboardStats;
export const getLLMStatus = runtimeApi.llmStatus;
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
export const getSkillRegistry = skillRegistryApi.list;
export const getSkillRegistryDetail = skillRegistryApi.get;
export const publishSkillToRegistry = skillRegistryApi.publish;
export const deprecateSkillInRegistry = skillRegistryApi.deprecate;

export async function getCaseDetail(caseId: string): Promise<CaseDetail> {
  const [caseRecord, materials, facts, analyses, reports] = await Promise.all([
    caseApi.get(caseId),
    materialApi.listByCase(caseId),
    factApi.listByCase(caseId),
    analysisApi.listByCase(caseId),
    reportApi.listByCase(caseId)
  ]);

  return {
    case: caseRecord,
    materials,
    facts,
    analyses,
    reports
  };
}

function getFileRelativePath(file: File) {
  const fileWithFolderPath = file as File & { webkitRelativePath?: string };
  return fileWithFolderPath.webkitRelativePath || file.name;
}
