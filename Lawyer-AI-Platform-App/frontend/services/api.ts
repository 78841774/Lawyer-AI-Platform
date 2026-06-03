const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8001";

export type DashboardStats = {
  cases: number;
  materials: number;
  facts: number;
  analyses: number;
  reports: number;
};

export type CaseRecord = {
  case_id: string;
  title: string;
  case_type: string;
  status: string;
  objective: string | null;
  workspace_id: string;
  owner_user_id: string;
  created_at: string;
  updated_at: string;
};

export type UserRecord = {
  user_id: string;
  email: string;
  display_name: string;
  role: string;
  status: string;
  created_at: string;
  updated_at: string;
};

export type WorkspaceRecord = {
  workspace_id: string;
  name: string;
  owner_user_id: string;
  status: string;
  created_at: string;
  updated_at: string;
};

export type AuthStatus = {
  authenticated: boolean;
  user_id: string;
  auth_mode: "jwt" | "dev_token" | "local_fallback";
  expires_at: string | null;
};

export type LoginResponse = {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
  user_id: string;
  expires_at: string;
};

export type MaterialRecord = {
  material_id: string;
  case_id: string;
  filename: string;
  material_type: string;
  storage_path: string;
  status: string;
  created_at: string;
};

export type FactRecord = {
  fact_id: string;
  case_id: string;
  material_id: string;
  content: string;
  fact_type: string;
  confidence: number;
  source_text: string | null;
  status: string;
  created_at: string;
};

export type LegalAnalysisRecord = {
  analysis_id: string;
  case_id: string;
  issues: Array<{ issue: string; confidence: number }>;
  rules: Array<{
    source: string;
    rule?: string;
    skill_id?: string;
    package_id?: string;
  }>;
  reasoning: string[];
  conclusion: string;
  risk_level: string;
  confidence: number;
  status: string;
  created_at: string;
  skill_used?: string;
  package_used?: string;
};

export type ReportRecord = {
  report_id: string;
  case_id: string;
  report_type: string;
  title: string;
  content: string;
  status: string;
  version: number;
  storage_path: string;
  source_refs: {
    fact_ids?: string[];
    analysis_id?: string;
    skill_id?: string;
    package_id?: string;
  };
  created_at: string;
};

export type WorkspaceSkillRecord = {
  skill_id: string;
  skill_name: string;
  domain: string;
  version: string;
  package_id: string;
  package_path: string;
  status: string;
};

export type WorkspaceSkillDetail = {
  skill: WorkspaceSkillRecord;
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

export type CaseSkillBinding = {
  binding_id?: string;
  case_id: string;
  skill_id: string;
  package_id: string;
  status: string;
  message?: string;
  created_at?: string;
};

export type CaseDetail = {
  case: CaseRecord;
  materials: MaterialRecord[];
  facts: FactRecord[];
  analyses: LegalAnalysisRecord[];
  reports: ReportRecord[];
};

export type ExtractFactsResponse = {
  case_id: string;
  facts: FactRecord[];
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
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: buildAuthHeaders(),
    cache: "no-store"
  });

  if (!response.ok) {
    throw new ApiError(await buildErrorMessage(response, path), response.status);
  }

  return response.json();
}

async function postJson<T>(path: string, payload?: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
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
  const response = await fetch(`${API_BASE_URL}${path}`, {
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
  return window.localStorage.getItem("lawyer_ai_access_token");
}

export function storeAccessToken(token: string) {
  if (typeof window !== "undefined") {
    window.localStorage.setItem("lawyer_ai_access_token", token);
  }
}

export function clearAccessToken() {
  if (typeof window !== "undefined") {
    window.localStorage.removeItem("lawyer_ai_access_token");
  }
}

export async function getHealth(): Promise<{ status: string }> {
  return request<{ status: string }>("/health");
}

export async function getDashboardStats(): Promise<DashboardStats> {
  return request<DashboardStats>("/dashboard/stats");
}

export async function getCurrentUser(): Promise<UserRecord> {
  return request<UserRecord>("/users/me");
}

export async function getAuthStatus(): Promise<AuthStatus> {
  return request<AuthStatus>("/auth/status");
}

export async function loginWithDevToken(
  userId = "user_local_001",
  devToken = "dev-local-token"
): Promise<LoginResponse> {
  return postJson<LoginResponse>("/auth/login", {
    user_id: userId,
    dev_token: devToken
  });
}

export async function getWorkspaces(): Promise<WorkspaceRecord[]> {
  return request<WorkspaceRecord[]>("/workspaces");
}

export async function getWorkspace(workspaceId: string): Promise<WorkspaceRecord> {
  return request<WorkspaceRecord>(`/workspaces/${workspaceId}`);
}

export async function getWorkspaceCases(workspaceId: string): Promise<CaseRecord[]> {
  return request<CaseRecord[]>(`/workspaces/${workspaceId}/cases`);
}

export async function getCases(): Promise<CaseRecord[]> {
  return request<CaseRecord[]>("/cases");
}

export async function createCase(title: string): Promise<CaseRecord> {
  return postJson<CaseRecord>("/cases", { title });
}

export async function getCase(caseId: string): Promise<CaseRecord> {
  return request<CaseRecord>(`/cases/${caseId}`);
}

export async function getCaseMaterials(caseId: string): Promise<MaterialRecord[]> {
  return request<MaterialRecord[]>(`/cases/${caseId}/materials`);
}

export async function uploadMaterial(caseId: string, file: File): Promise<MaterialRecord> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("material_type", "document");
  return postForm<MaterialRecord>(`/cases/${caseId}/materials`, formData);
}

export async function getCaseFacts(caseId: string): Promise<FactRecord[]> {
  const response = await request<{ facts: FactRecord[] }>(`/cases/${caseId}/facts`);
  return response.facts;
}

export async function extractFacts(caseId: string): Promise<ExtractFactsResponse> {
  return postJson<ExtractFactsResponse>(`/cases/${caseId}/facts/extract`);
}

export async function getCaseAnalyses(caseId: string): Promise<LegalAnalysisRecord[]> {
  const response = await request<{ analyses: LegalAnalysisRecord[] }>(`/cases/${caseId}/analysis`);
  return response.analyses;
}

export async function runLegalAnalysis(caseId: string): Promise<LegalAnalysisRecord> {
  return postJson<LegalAnalysisRecord>(`/cases/${caseId}/analysis/run`);
}

export async function getCaseReports(caseId: string): Promise<ReportRecord[]> {
  const response = await request<{ reports: ReportRecord[] }>(`/cases/${caseId}/reports`);
  return response.reports;
}

export async function getReports(): Promise<ReportRecord[]> {
  return request<ReportRecord[]>("/reports");
}

export async function getReport(reportId: string): Promise<ReportRecord> {
  return request<ReportRecord>(`/reports/${reportId}`);
}

export async function generateReport(caseId: string): Promise<ReportRecord> {
  return postJson<ReportRecord>(`/cases/${caseId}/reports/generate`);
}

export async function getWorkspaceSkills(): Promise<WorkspaceSkillRecord[]> {
  const response = await request<{ skills: WorkspaceSkillRecord[] }>("/workspace/skills");
  return response.skills;
}

export async function getWorkspaceSkill(skillId: string): Promise<WorkspaceSkillDetail> {
  return request<WorkspaceSkillDetail>(`/workspace/skills/${skillId}`);
}

export async function applySkillToCase(
  caseId: string,
  skillId: string
): Promise<CaseSkillBinding> {
  return postJson<CaseSkillBinding>(`/cases/${caseId}/skills/${skillId}/apply`);
}

export async function getCaseSkills(caseId: string): Promise<CaseSkillBinding[]> {
  const response = await request<{ skills: CaseSkillBinding[] }>(`/cases/${caseId}/skills`);
  return response.skills;
}

export async function getCaseDetail(caseId: string): Promise<CaseDetail> {
  const [caseRecord, materials, facts, analyses, reports] = await Promise.all([
    getCase(caseId),
    getCaseMaterials(caseId),
    getCaseFacts(caseId),
    getCaseAnalyses(caseId),
    getCaseReports(caseId)
  ]);

  return {
    case: caseRecord,
    materials,
    facts,
    analyses,
    reports
  };
}
