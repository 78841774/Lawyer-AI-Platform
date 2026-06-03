export type DashboardStats = {
  cases: number;
  materials: number;
  facts: number;
  analyses: number;
  reports: number;
};

export type RuntimeStatus = {
  provider: string;
  model: string;
  configured: boolean;
  base_url_configured: boolean;
};

export type AuthStatus = {
  authenticated: boolean;
  user_id: string;
  auth_mode: "jwt" | "dev_token" | "local_fallback";
  expires_at: string | null;
};

export type User = {
  user_id: string;
  email: string;
  display_name: string;
  role: string;
  status: string;
  created_at: string;
  updated_at: string;
};

export type Workspace = {
  workspace_id: string;
  name: string;
  owner_user_id: string;
  status: string;
  created_at: string;
  updated_at: string;
};

export type Case = {
  case_id: string;
  title: string;
  description?: string | null;
  client_name?: string | null;
  counterparty_name?: string | null;
  opposing_party?: string | null;
  case_type?: string | null;
  contract_type?: string | null;
  dispute_amount?: string | null;
  status: string;
  objective?: string | null;
  jurisdiction?: string | null;
  intake_notes?: string | null;
  intake_status?: string | null;
  priority?: string | null;
  tags?: string[] | null;
  workspace_id: string;
  owner_user_id: string;
  created_at: string;
  updated_at: string;
};

export type Material = {
  material_id: string;
  case_id: string;
  filename: string;
  original_filename?: string | null;
  relative_path?: string | null;
  folder_path?: string | null;
  file_ext?: string | null;
  material_type: string;
  upload_batch_id?: string | null;
  display_order?: number | null;
  storage_path: string;
  status: string;
  created_at: string;
};

export type Fact = {
  fact_id: string;
  case_id: string;
  material_id: string;
  content: string;
  fact_type: string;
  confidence: number;
  source_text: string | null;
  source_refs?: {
    material_id?: string | null;
    filename?: string | null;
    relative_path?: string | null;
  };
  status: string;
  created_at: string;
};

export type IntakeStatus = {
  case_id: string;
  intake_status: string;
  has_materials: boolean;
  materials_count: number;
  facts_count: number;
  analyses_count: number;
  reports_count: number;
  ready_for_fact_extraction: boolean;
  ready_for_analysis: boolean;
  ready_for_report: boolean;
  next_recommended_action: string | null;
};

export type LegalAnalysis = {
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
  llm_provider?: string | null;
  llm_status?: string | null;
  skill_used?: string;
  package_used?: string;
};

export type ReportSourceRefs = {
  fact_ids?: string[];
  analysis_id?: string;
  skill_id?: string;
  package_id?: string;
  llm_provider?: string | null;
  llm_status?: string | null;
  material_refs?: Array<{
    material_id?: string | null;
    filename?: string | null;
    relative_path?: string | null;
  }>;
} & Record<string, unknown>;

export type Report = {
  report_id: string;
  case_id: string;
  report_type: string;
  title: string;
  content: string;
  status: string;
  version: number;
  storage_path: string;
  source_refs: ReportSourceRefs;
  llm_provider?: string | null;
  llm_status?: string | null;
  skill_used?: string | null;
  package_used?: string | null;
  created_at: string;
  updated_at?: string | null;
};

export type Skill = {
  skill_id: string;
  case_id?: string | null;
  skill_name: string;
  domain: string;
  version: string;
  package_id?: string | null;
  package_path?: string | null;
  status: string;
  evaluation_score?: number | null;
  validation_status?: string | null;
  created_at?: string | null;
  validated_at?: string | null;
};

export type ExperiencePackage = {
  package_id: string;
  skill_id: string;
  name: string;
  domain: string;
  version: string;
  status: string;
  package_path: string;
  created_at: string;
};

export type ExperiencePackageDetail = ExperiencePackage & {
  manifest: Record<string, unknown>;
};

export type SkillRegistryEntry = {
  skill_id: string;
  skill_name: string;
  domain: string;
  version: string;
  status: string;
  validation_status: string;
  evaluation_score: number;
  package_id: string | null;
  package_status: string | null;
};

export type SkillRegistryDetail = {
  skill: Pick<
    Skill,
    "skill_id" | "skill_name" | "domain" | "version" | "status" | "validation_status" | "evaluation_score"
  >;
  evaluation: Record<string, unknown>;
  package: ExperiencePackage | null;
  lifecycle_status: {
    skill_status: string;
    validation_status: string;
    package_status: string | null;
  };
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
