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
  User,
  Workspace
} from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8001";
const TOKEN_STORAGE_KEY = "lawyer_ai_access_token";

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
  return token ? { Authorization: `Bearer ${token}` } : {};
}

function getStoredAccessToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  return window.localStorage.getItem(TOKEN_STORAGE_KEY);
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
  create: (title: string) => postJson<Case>("/cases", { title }),
  get: (caseId: string) => request<Case>(`/cases/${caseId}`)
};

export const materialApi = {
  listByCase: (caseId: string) => request<Material[]>(`/cases/${caseId}/materials`),
  upload: (caseId: string, file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("material_type", "document");
    return postForm<Material>(`/cases/${caseId}/materials`, formData);
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
export const getCases = caseApi.list;
export const createCase = caseApi.create;
export const getCase = caseApi.get;
export const getCaseMaterials = materialApi.listByCase;
export const uploadMaterial = materialApi.upload;
export const getCaseFacts = factApi.listByCase;
export const extractFacts = factApi.extract;
export const getCaseAnalyses = analysisApi.listByCase;
export const runLegalAnalysis = analysisApi.run;
export const getCaseReports = reportApi.listByCase;
export const getReports = reportApi.list;
export const getReport = reportApi.get;
export const generateReport = reportApi.generate;
export const getWorkspaceSkills = skillApi.listPublished;
export const getWorkspaceSkill = skillApi.getPublished;
export const applySkillToCase = skillApi.applyToCase;
export const getCaseSkills = skillApi.listForCase;

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
