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

export type OCRProviderStatus = {
  provider: string;
  connected: boolean;
  mock_only: boolean;
  supports_pdf: boolean;
  supports_images: boolean;
  notes: string;
};

export type OCRRequest = {
  material_id: string;
  filename: string;
  relative_path?: string | null;
  provider?: string;
  mode?: string;
  mock_only?: boolean;
};

export type OCRSourceRef = {
  source_ref_id: string;
  source_type: string;
  material_id: string;
  filename: string;
  relative_path?: string | null;
  page_number: number;
  char_start: number;
  char_end: number;
  bbox?: Record<string, unknown> | null;
  quote: string;
  provider: string;
  provider_mode: string;
  mock_only: boolean;
};

export type OCRPageResult = {
  page_number: number;
  text: string;
  confidence: number;
  source_ref: OCRSourceRef;
};

export type OCRResult = {
  ocr_run_id: string;
  material_id: string;
  filename: string;
  relative_path?: string | null;
  provider: string;
  provider_mode: string;
  status: string;
  text_available: boolean;
  pages: OCRPageResult[];
  source_refs: OCRSourceRef[];
  warnings: string[];
  created_at: string;
};

export type LegalSearchProviderStatus = {
  provider: string;
  connected: boolean;
  mock_only: boolean;
  supports_case_law: boolean;
  supports_statutes: boolean;
  notes: string;
};

export type LegalSearchRequest = {
  query: string;
  case_cause_code?: string | null;
  jurisdiction?: string | null;
  provider?: string;
  mode?: string;
  mock_only?: boolean;
};

export type LegalSearchSourceRef = {
  source_ref_id: string;
  source_type: string;
  provider: string;
  provider_mode: string;
  source_id: string;
  citation: string;
  url?: string | null;
  quote: string;
  retrieved_at: string;
  mock_only: boolean;
};

export type LegalSearchHit = {
  hit_id: string;
  title: string;
  source_type: string;
  court: string;
  date: string;
  summary: string;
  relevance_score: number;
  source_ref: LegalSearchSourceRef;
};

export type LegalSearchResult = {
  search_run_id: string;
  query: string;
  case_cause_code?: string | null;
  jurisdiction?: string | null;
  provider: string;
  provider_mode: string;
  status: string;
  hits: LegalSearchHit[];
  warnings: string[];
  created_at: string;
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

export type RuntimeRun = {
  run_id: string;
  run_type: "fact_extraction" | "legal_analysis" | "report_generation";
  case_id: string;
  status: string;
  is_latest: boolean;
  llm_provider?: string | null;
  llm_status?: string | null;
  skill_id?: string | null;
  package_id?: string | null;
  counts: Record<string, number>;
  materials_count?: number;
  facts_created_count?: number;
  facts_reused_count?: number;
  facts_skipped_count?: number;
  facts_count?: number;
  analysis_id?: string | null;
  report_id?: string | null;
  source_material_ids?: string[];
  source_fact_ids?: string[];
  source_refs?: unknown;
  error_message?: string | null;
  created_at: string;
  completed_at?: string | null;
};

export type RuntimeRunsResponse = {
  case_id: string;
  extraction_runs: RuntimeRun[];
  analysis_runs: RuntimeRun[];
  report_runs: RuntimeRun[];
};

export type LatestRuntimeRunsResponse = {
  case_id: string;
  latest_extraction_run: RuntimeRun | null;
  latest_analysis_run: RuntimeRun | null;
  latest_report_run: RuntimeRun | null;
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
  latest_extraction_run_id?: string | null;
  latest_analysis_run_id?: string | null;
  latest_report_run_id?: string | null;
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
  run_id?: string;
  run_type?: string;
  facts_count?: number;
  source_fact_ids?: string[];
  source_refs?: unknown;
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
  source_refs?: unknown[];
  citations?: unknown[];
  trace?: Record<string, unknown>;
  citation_summary?: Record<string, unknown>;
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
  citations?: unknown[];
  trace?: Record<string, unknown>;
  citation_summary?: Record<string, unknown>;
  llm_provider?: string | null;
  llm_status?: string | null;
  skill_used?: string | null;
  package_used?: string | null;
  created_at: string;
  updated_at?: string | null;
  run_id?: string;
  run_type?: string;
  analysis_id?: string | null;
};

export type SourceRefsStatus = {
  source_refs_enabled: boolean;
  citation_resolver_enabled: boolean;
  source_trace_enabled: boolean;
  mock_only: boolean;
  real_material_reading_enabled: boolean;
  real_ocr_connected: boolean;
  real_legal_search_connected: boolean;
  notes: string;
};

export type SourceTraceNode = {
  node_id: string;
  node_type: string;
  label: string;
  source_ref_id?: string | null;
  metadata: Record<string, unknown>;
};

export type SourceTraceEdge = {
  edge_id: string;
  from_node_id: string;
  to_node_id: string;
  relation: string;
  metadata: Record<string, unknown>;
};

export type SourceTrace = {
  trace_id: string;
  report_id: string;
  case_id?: string | null;
  nodes: SourceTraceNode[];
  edges: SourceTraceEdge[];
  warnings: string[];
  created_at: string;
  mock_only: boolean;
};

export type CitationResolutionResult = {
  citation_id: string;
  resolved: boolean;
  source_ref?: Record<string, unknown> | null;
  warnings: string[];
  mock_only: boolean;
};

export type LocalSandboxStatus = {
  enabled: boolean;
  mode: string;
  real_case_processing_enabled: boolean;
  live_provider_enabled: boolean;
  deepseek_live_enabled: boolean;
  real_ocr_enabled: boolean;
  real_legal_search_enabled: boolean;
  workspace_runtime_auto_enable: boolean;
  skill_aware_case_processing_auto_enable: boolean;
  requires_manual_review: boolean;
  mock_only: boolean;
  warnings: string[];
};

export type LocalSandboxGuardStatus = {
  provider_mode_guard: Record<string, unknown>;
  material_safety_guard: Record<string, unknown>;
  git_safety_guard: Record<string, unknown>;
};

export type LocalSandboxDryRunRequest = {
  case_id: string;
  workspace_id: string;
  local_case_root?: string | null;
  provider_mode: string;
  ocr_mode: string;
  legal_search_mode: string;
  dry_run_only: boolean;
};

export type LocalSandboxDryRunResult = {
  dry_run_id: string;
  case_id: string;
  workspace_id: string;
  status: string;
  allowed_to_continue: boolean;
  guard_results: Record<string, unknown>;
  audit_log_id: string;
  warnings: string[];
  dry_run_only: boolean;
  created_at: string;
};

export type LocalSandboxAuditLog = {
  audit_log_id: string;
  event_type: string;
  case_id: string;
  workspace_id: string;
  dry_run_id: string;
  provider_mode: string;
  ocr_mode: string;
  legal_search_mode: string;
  result: string;
  warnings: string[];
  local_case_root_redacted: string;
  created_at: string;
};

export type DeploymentReadinessItem = {
  item_id: string;
  label: string;
  status: string;
  required: boolean;
  passed: boolean;
  notes: string;
};

export type InternalAlphaReadinessChecklist = {
  items: DeploymentReadinessItem[];
  required_passed: boolean;
  manual_verification_required: boolean;
  warnings: string[];
};

export type InternalAlphaSubsystemStatus = {
  name: string;
  enabled: boolean;
  status: string;
  mock_only: boolean;
  notes: string;
};

export type InternalAlphaStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  team_mode_enabled: boolean;
  real_case_processing_enabled: boolean;
  workspace_runtime_auto_enable: boolean;
  skill_aware_case_processing_auto_enable: boolean;
  requires_manual_review: boolean;
  local_only: boolean;
  mock_only: boolean;
  warnings: string[];
  subsystems: InternalAlphaSubsystemStatus[];
  readiness: InternalAlphaReadinessChecklist;
};

export type SecretManagementChecklist = {
  env_file_not_committed: boolean;
  api_key_not_committed: boolean;
  jwt_secret_not_default_for_production: boolean;
  deepseek_key_not_committed: boolean;
  ocr_legal_search_keys_not_committed: boolean;
  external_secret_management_required_for_production: boolean;
  notes: string[];
};

export type DatabaseReadinessStatus = {
  sqlite_local_ready: boolean;
  local_db_ignored: boolean;
  database_url_supported: boolean;
  postgresql_ready: boolean;
  alembic_ready: boolean;
  production_migration_out_of_scope: boolean;
  notes: string[];
};

export type InternalAlphaDryRunRequest = {
  case_id: string;
  workspace_id: string;
  local_case_root?: string | null;
  provider_mode: string;
  ocr_mode: string;
  legal_search_mode: string;
  dry_run_only: boolean;
  manual_review_confirmed: boolean;
};

export type InternalAlphaDryRunResult = {
  alpha_dry_run_id: string;
  local_sandbox_dry_run_result: Record<string, unknown>;
  readiness_summary: Record<string, unknown>;
  allowed_to_continue: boolean;
  manual_review_required: boolean;
  audit_log_id: string;
  warnings: string[];
  created_at: string;
};

export type InternalAlphaAuditLog = {
  audit_log_id: string;
  event_type: string;
  case_id: string;
  workspace_id: string;
  alpha_dry_run_id: string;
  local_sandbox_dry_run_id?: string | null;
  provider_mode: string;
  ocr_mode: string;
  legal_search_mode: string;
  result: string;
  warnings: string[];
  local_case_root_redacted: string;
  created_at: string;
};

export type PersonalAlphaStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  team_mode_enabled: boolean;
  real_case_processing_enabled: boolean;
  material_content_reading_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  requires_manual_review: boolean;
  local_only: boolean;
  dry_run_only: boolean;
  warnings: string[];
};

export type RedactionChecklist = {
  client_name_removed: boolean;
  id_numbers_removed: boolean;
  phone_numbers_removed: boolean;
  addresses_removed: boolean;
  bank_info_removed: boolean;
  case_number_removed_or_masked: boolean;
  file_names_redacted: boolean;
  material_content_not_committed: boolean;
  api_keys_not_committed: boolean;
  local_only_confirmed: boolean;
  manual_review_required: boolean;
};

export type PersonalCaseManifestPreviewRequest = {
  case_id: string;
  workspace_id: string;
  case_title_redacted: string;
  local_case_root?: string | null;
  case_cause_code: string;
  jurisdiction: string;
  dry_run_only: boolean;
  manual_review_confirmed: boolean;
};

export type PersonalCaseManifestPreview = {
  manifest_id: string;
  case_id: string;
  workspace_id: string;
  case_title_redacted: string;
  case_cause_code: string;
  jurisdiction: string;
  local_case_root_redacted: string;
  dry_run_only: boolean;
  manual_review_confirmed: boolean;
  allowed_to_continue: boolean;
  redaction_checklist: RedactionChecklist;
  warnings: string[];
  created_at: string;
};

export type MaterialInventoryRequest = {
  case_id: string;
  workspace_id: string;
  local_case_root?: string | null;
  include_file_names: boolean;
  dry_run_only: boolean;
};

export type MaterialInventoryItem = {
  item_id: string;
  filename_redacted: string;
  extension?: string | null;
  relative_path_redacted: string;
  size_bytes?: number | null;
  content_read: boolean;
  mock_only: boolean;
};

export type MaterialInventoryResult = {
  inventory_id: string;
  case_id: string;
  workspace_id: string;
  local_case_root_redacted: string;
  item_count: number;
  items: MaterialInventoryItem[];
  content_read: boolean;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaDryRunRequest = {
  case_id: string;
  workspace_id: string;
  local_case_root?: string | null;
  case_cause_code: string;
  jurisdiction: string;
  provider_mode: string;
  ocr_mode: string;
  legal_search_mode: string;
  llm_mode: string;
  dry_run_only: boolean;
  manual_review_confirmed: boolean;
};

export type PersonalAlphaDryRunResult = {
  personal_alpha_dry_run_id: string;
  manifest_preview: Record<string, unknown>;
  material_inventory: Record<string, unknown>;
  internal_alpha_dry_run_result: Record<string, unknown>;
  local_sandbox_dry_run_result: Record<string, unknown>;
  mock_ocr_preview: Record<string, unknown>;
  mock_legal_search_preview: Record<string, unknown>;
  mock_source_trace_preview: Record<string, unknown>;
  mock_report_draft_preview: Record<string, unknown>;
  allowed_to_continue: boolean;
  manual_review_required: boolean;
  audit_log_id: string;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaAuditLog = {
  audit_log_id: string;
  event_type: string;
  case_id: string;
  workspace_id: string;
  personal_alpha_dry_run_id: string;
  result: string;
  warnings: string[];
  local_case_root_redacted: string;
  created_at: string;
};

export type ControlledMaterialStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  real_material_reading_enabled: boolean;
  real_material_reading_default: boolean;
  requires_explicit_read_confirmation: boolean;
  requires_manual_review: boolean;
  allowed_file_extensions: string[];
  max_file_size_bytes: number;
  read_pdf_enabled: boolean;
  read_docx_enabled: boolean;
  read_image_enabled: boolean;
  ocr_live_enabled: boolean;
  llm_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  store_raw_content_in_git: boolean;
  store_redacted_preview_in_git: boolean;
  store_extracted_text_in_git: boolean;
  store_material_content_in_git: boolean;
  runtime_storage_enabled: boolean;
  runtime_storage_path: string;
  source_trace_enabled: boolean;
  report_draft_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  warnings: string[];
};

export type ControlledMaterialReadRequest = {
  case_id: string;
  workspace_id: string;
  local_case_root?: string | null;
  material_id: string;
  filename_redacted: string;
  read_mode: string;
  explicit_read_confirmation: boolean;
  manual_review_confirmed: boolean;
  provider_mode: string;
  ocr_mode: string;
  llm_mode: string;
  legal_search_mode: string;
};

export type ControlledMaterialReadResult = {
  controlled_read_id: string;
  case_id: string;
  workspace_id: string;
  material_id: string;
  filename_redacted: string;
  local_case_root_redacted: string;
  content_read: boolean;
  controlled_read_ready: boolean;
  requires_next_stage_real_read: boolean;
  extracted_text_stored: boolean;
  git_storage_allowed: boolean;
  allowed_to_continue: boolean;
  guard_results: Record<string, unknown>[];
  source_refs: Record<string, unknown>[];
  warnings: string[];
  audit_log_id: string;
  created_at: string;
};

export type ControlledLocalReadPreviewRequest = {
  case_id: string;
  workspace_id: string;
  local_file_path: string;
  filename_redacted: string;
  material_id: string;
  explicit_read_confirmation: boolean;
  manual_review_confirmed: boolean;
  provider_mode: string;
  ocr_mode: string;
  llm_mode: string;
  legal_search_mode: string;
  preview_only: boolean;
};

export type ControlledLocalReadPreviewResult = {
  preview_id: string;
  case_id: string;
  workspace_id: string;
  material_id: string;
  filename_redacted: string;
  local_file_path_redacted: string;
  file_extension: string;
  file_size_bytes: number;
  content_read: boolean;
  raw_content_stored: boolean;
  redacted_preview_created: boolean;
  redacted_preview: string;
  redacted_preview_storage_path: string;
  source_refs: Record<string, unknown>[];
  guard_results: Record<string, unknown>[];
  audit_log_id: string;
  allowed_to_continue: boolean;
  warnings: string[];
  created_at: string;
};

export type ControlledReadPreviewRecord = {
  preview_id: string;
  case_id: string;
  workspace_id: string;
  material_id: string;
  filename_redacted: string;
  local_file_path_redacted: string;
  redacted_preview: string;
  source_refs: Record<string, unknown>[];
  warnings: string[];
  created_at: string;
};

export type ControlledReportDraftRequest = {
  case_id: string;
  workspace_id: string;
  controlled_read_id: string;
  report_mode: string;
  manual_review_confirmed: boolean;
  llm_mode: string;
};

export type ControlledReportDraftResult = {
  report_draft_id: string;
  case_id: string;
  workspace_id: string;
  controlled_read_id: string;
  status: string;
  legal_opinion_finalized: boolean;
  requires_human_review: boolean;
  final_legal_opinion_enabled: boolean;
  llm_called: boolean;
  content_read: boolean;
  mock_only: boolean;
  source_refs: Record<string, unknown>[];
  warnings: string[];
  audit_log_id: string;
  created_at: string;
};

export type ControlledMaterialAuditLog = {
  audit_log_id: string;
  event_type: string;
  case_id: string;
  workspace_id: string;
  controlled_read_id?: string | null;
  preview_id?: string | null;
  material_id?: string | null;
  filename_redacted?: string | null;
  result: string;
  warnings: string[];
  local_case_root_redacted: string;
  created_at: string;
};

export type ControlledOCRStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  ocr_live_enabled: boolean;
  ocr_live_default: boolean;
  mock_ocr_enabled: boolean;
  requires_explicit_ocr_confirmation: boolean;
  requires_manual_review: boolean;
  allowed_file_extensions: string[];
  max_file_size_bytes: number;
  read_pdf_binary_enabled: boolean;
  read_image_binary_enabled: boolean;
  extract_real_ocr_text_enabled: boolean;
  store_raw_ocr_text_in_git: boolean;
  store_redacted_ocr_preview_in_git: boolean;
  runtime_storage_enabled: boolean;
  runtime_storage_path: string;
  source_trace_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  warnings: string[];
};

export type ControlledOCRPreviewRequest = {
  case_id: string;
  workspace_id: string;
  local_file_path: string;
  filename_redacted: string;
  material_id: string;
  explicit_ocr_confirmation: boolean;
  manual_review_confirmed: boolean;
  ocr_mode: string;
  provider_mode: string;
  preview_only: boolean;
};

export type ControlledOCRPreviewResult = {
  ocr_preview_id: string;
  case_id: string;
  workspace_id: string;
  material_id: string;
  filename_redacted: string;
  local_file_path_redacted: string;
  file_extension: string;
  file_size_bytes: number;
  ocr_called: boolean;
  real_ocr_called: boolean;
  mock_ocr_used: boolean;
  raw_ocr_text_stored: boolean;
  redacted_ocr_preview_created: boolean;
  redacted_ocr_preview: string;
  redacted_ocr_preview_storage_path: string;
  source_refs: Record<string, unknown>[];
  guard_results: Record<string, unknown>[];
  audit_log_id: string;
  allowed_to_continue: boolean;
  warnings: string[];
  created_at: string;
};

export type ControlledOCRPreviewRecord = {
  ocr_preview_id: string;
  case_id: string;
  workspace_id: string;
  material_id: string;
  filename_redacted: string;
  local_file_path_redacted: string;
  redacted_ocr_preview: string;
  source_refs: Record<string, unknown>[];
  warnings: string[];
  created_at: string;
};

export type ControlledOCRAuditLog = {
  audit_log_id: string;
  event_type: string;
  case_id: string;
  workspace_id: string;
  ocr_preview_id?: string | null;
  material_id?: string | null;
  filename_redacted?: string | null;
  result: string;
  warnings: string[];
  created_at: string;
};

export type ControlledLegalSearchStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  legal_search_live_enabled: boolean;
  legal_search_live_default: boolean;
  mock_legal_search_enabled: boolean;
  requires_explicit_legal_search_confirmation: boolean;
  requires_manual_review: boolean;
  query_redaction_enabled: boolean;
  source_trace_enabled: boolean;
  citation_resolver_enabled: boolean;
  store_raw_query_in_git: boolean;
  store_raw_legal_search_results_in_git: boolean;
  store_redacted_search_preview_in_git: boolean;
  runtime_storage_enabled: boolean;
  runtime_storage_path: string;
  final_legal_opinion_enabled: boolean;
  warnings: string[];
};

export type ControlledLegalSearchPreviewRequest = {
  case_id: string;
  workspace_id: string;
  query_text: string;
  query_text_redacted: string;
  case_cause_code: string;
  jurisdiction: string;
  explicit_legal_search_confirmation: boolean;
  manual_review_confirmed: boolean;
  legal_search_mode: string;
  provider_mode: string;
  preview_only: boolean;
};

export type ControlledLegalSearchPreviewResult = {
  search_preview_id: string;
  case_id: string;
  workspace_id: string;
  query_text_redacted: string;
  case_cause_code: string;
  jurisdiction: string;
  legal_search_called: boolean;
  real_legal_search_called: boolean;
  mock_legal_search_used: boolean;
  raw_query_stored: boolean;
  raw_results_stored: boolean;
  redacted_search_preview_created: boolean;
  redacted_search_preview: string;
  redacted_search_preview_storage_path: string;
  citations: Record<string, unknown>[];
  source_refs: Record<string, unknown>[];
  guard_results: Record<string, unknown>[];
  audit_log_id: string;
  allowed_to_continue: boolean;
  warnings: string[];
  created_at: string;
};

export type ControlledLegalSearchPreviewRecord = {
  search_preview_id: string;
  case_id: string;
  workspace_id: string;
  query_text_redacted: string;
  case_cause_code: string;
  jurisdiction: string;
  redacted_search_preview: string;
  citations: Record<string, unknown>[];
  source_refs: Record<string, unknown>[];
  warnings: string[];
  created_at: string;
};

export type ControlledLegalCitationResolutionRequest = {
  citation_id: string;
  search_preview_id: string;
  manual_review_confirmed: boolean;
  legal_search_mode: string;
  provider_mode: string;
};

export type ControlledLegalCitationResolutionResult = {
  citation_id: string;
  search_preview_id: string;
  resolved: boolean;
  real_legal_database_called: boolean;
  mock_resolution_used: boolean;
  source_ref: Record<string, unknown>;
  warnings: string[];
  audit_log_id: string;
  created_at: string;
};

export type ControlledLegalSearchAuditLog = {
  audit_log_id: string;
  event_type: string;
  case_id: string;
  workspace_id: string;
  search_preview_id?: string | null;
  citation_id?: string | null;
  result: string;
  warnings: string[];
  created_at: string;
};

export type ControlledReportDraftStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  mock_report_assembly_enabled: boolean;
  requires_manual_review: boolean;
  requires_explicit_assembly_confirmation: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  runtime_storage_enabled: boolean;
  runtime_storage_path: string;
  source_trace_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  store_raw_material_text_in_git: boolean;
  store_raw_ocr_text_in_git: boolean;
  store_raw_legal_search_results_in_git: boolean;
  store_report_draft_in_git: boolean;
  warnings: string[];
};

export type ControlledReportDraftAssembleRequest = {
  case_id: string;
  workspace_id: string;
  material_preview_ids: string[];
  ocr_preview_ids: string[];
  legal_search_preview_ids: string[];
  citation_ids: string[];
  explicit_assembly_confirmation: boolean;
  manual_review_confirmed: boolean;
  report_mode: string;
  llm_mode: string;
  provider_mode: string;
  preview_only: boolean;
};

export type ControlledReportDraftAssembleResult = {
  draft_id: string;
  case_id: string;
  workspace_id: string;
  status: string;
  mock_report_assembled: boolean;
  final_legal_opinion_generated: boolean;
  llm_called: boolean;
  deepseek_live_called: boolean;
  real_ocr_called: boolean;
  real_legal_database_called: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  report_draft_storage_path: string;
  mock_assembled_report: Record<string, unknown>;
  source_refs: Record<string, unknown>[];
  citations: Record<string, unknown>[];
  guard_results: Record<string, unknown>[];
  audit_log_id: string;
  allowed_to_continue: boolean;
  warnings: string[];
  created_at: string;
};

export type ControlledReportDraftRecord = {
  draft_id: string;
  case_id: string;
  workspace_id: string;
  mock_assembled_report: Record<string, unknown>;
  source_refs: Record<string, unknown>[];
  citations: Record<string, unknown>[];
  warnings: string[];
  created_at: string;
};

export type ControlledReportDraftAuditLog = {
  audit_log_id: string;
  event_type: string;
  case_id: string;
  workspace_id: string;
  draft_id: string;
  result: string;
  warnings: string[];
  created_at: string;
};

export type ControlledLawyerReviewStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  mock_review_enabled: boolean;
  requires_explicit_review_confirmation: boolean;
  requires_explicit_assembly_confirmation: boolean;
  requires_manual_review: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  skill_publish_enabled: boolean;
  workspace_runtime_auto_enable: boolean;
  runtime_storage_enabled: boolean;
  runtime_storage_path: string;
  source_trace_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  store_raw_material_text_in_git: boolean;
  store_raw_ocr_text_in_git: boolean;
  store_raw_legal_search_results_in_git: boolean;
  store_review_record_in_git: boolean;
  warnings: string[];
};

export type ControlledLawyerReviewSubmitRequest = {
  draft_id: string;
  case_id: string;
  workspace_id: string;
  submitted_by: string;
  explicit_review_confirmation: boolean;
  explicit_assembly_confirmation: boolean;
  manual_review_confirmed: boolean;
  review_mode: string;
  draft_status: string;
  llm_mode: string;
  provider_mode: string;
  preview_only: boolean;
};

export type ControlledLawyerReviewActionRequest = {
  reviewer_id: string;
  review_notes: string;
  explicit_review_confirmation: boolean;
  manual_review_confirmed: boolean;
  llm_mode: string;
  provider_mode: string;
};

export type ControlledLawyerReviewResult = {
  review_id: string;
  draft_id: string;
  case_id: string;
  workspace_id: string;
  status: string;
  action: string;
  submitted: boolean;
  approved: boolean;
  rejected: boolean;
  revision_requested: boolean;
  final_legal_opinion_generated: boolean;
  llm_called: boolean;
  deepseek_live_called: boolean;
  real_ocr_called: boolean;
  real_legal_database_called: boolean;
  skill_published: boolean;
  workspace_runtime_enabled: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  review_record_storage_path: string;
  review_record: Record<string, unknown>;
  history: Record<string, unknown>[];
  guard_results: Record<string, unknown>[];
  audit_log_id: string;
  allowed_to_continue: boolean;
  warnings: string[];
  created_at: string;
};

export type ControlledLawyerReviewRecord = {
  review_id: string;
  draft_id: string;
  case_id: string;
  workspace_id: string;
  status: string;
  submitted_by: string;
  reviewer_id: string;
  review_notes: string;
  final_legal_opinion_generated: boolean;
  history: Record<string, unknown>[];
  warnings: string[];
  created_at: string;
  updated_at: string;
};

export type ControlledLawyerReviewAuditLog = {
  audit_log_id: string;
  event_type: string;
  review_id: string;
  draft_id: string;
  case_id: string;
  workspace_id: string;
  action: string;
  result: string;
  warnings: string[];
  created_at: string;
};

export type ControlledRevisionStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  mock_revision_enabled: boolean;
  requires_review_id: boolean;
  requires_manual_review: boolean;
  requires_explicit_revision_confirmation: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  runtime_storage_enabled: boolean;
  runtime_storage_path: string;
  source_trace_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  store_raw_material_text_in_git: boolean;
  store_raw_ocr_text_in_git: boolean;
  store_raw_legal_search_results_in_git: boolean;
  store_revision_output_in_git: boolean;
  warnings: string[];
};

export type ControlledRevisionRequest = {
  case_id: string;
  workspace_id: string;
  review_id: string;
  draft_id: string;
  revision_reason: string;
  revision_instructions: string;
  requested_action: string;
  explicit_revision_confirmation: boolean;
  manual_review_confirmed: boolean;
  llm_mode: string;
  provider_mode: string;
  preview_only: boolean;
};

export type ControlledRevisionResult = {
  revision_id: string;
  case_id: string;
  workspace_id: string;
  review_id: string;
  draft_id: string;
  status: string;
  requested_action: string;
  mock_revision_created: boolean;
  final_legal_opinion_generated: boolean;
  llm_called: boolean;
  deepseek_live_called: boolean;
  real_ocr_called: boolean;
  real_legal_database_called: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  revision_storage_path: string;
  mock_revision_plan: Record<string, unknown>;
  revision_checklist: Record<string, unknown>[];
  source_refs: Record<string, unknown>[];
  guard_results: Record<string, unknown>[];
  audit_log_id: string;
  allowed_to_continue: boolean;
  warnings: string[];
  created_at: string;
};

export type ControlledRevisionRecord = {
  revision_id: string;
  case_id: string;
  workspace_id: string;
  review_id: string;
  draft_id: string;
  requested_action: string;
  mock_revision_plan: Record<string, unknown>;
  revision_checklist: Record<string, unknown>[];
  source_refs: Record<string, unknown>[];
  warnings: string[];
  created_at: string;
};

export type ControlledRevisionAuditLog = {
  audit_log_id: string;
  event_type: string;
  case_id: string;
  workspace_id: string;
  review_id: string;
  draft_id: string;
  revision_id: string;
  result: string;
  warnings: string[];
  created_at: string;
};

export type ControlledFinalReviewLockStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  mock_final_lock_enabled: boolean;
  requires_revision_id: boolean;
  requires_review_id: boolean;
  requires_draft_id: boolean;
  requires_manual_final_confirmation: boolean;
  requires_explicit_final_lock_confirmation: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  runtime_storage_enabled: boolean;
  runtime_storage_path: string;
  source_trace_enabled: boolean;
  immutable_snapshot_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  store_raw_material_text_in_git: boolean;
  store_raw_ocr_text_in_git: boolean;
  store_raw_legal_search_results_in_git: boolean;
  store_final_lock_snapshot_in_git: boolean;
  warnings: string[];
};

export type ControlledFinalReviewLockRequest = {
  case_id: string;
  workspace_id: string;
  draft_id: string;
  review_id: string;
  revision_id: string;
  final_review_notes: string;
  final_checklist_confirmed: boolean;
  explicit_final_lock_confirmation: boolean;
  manual_final_review_confirmed: boolean;
  lock_mode: string;
  llm_mode: string;
  provider_mode: string;
  preview_only: boolean;
};

export type ControlledFinalReviewLockResult = {
  final_lock_id: string;
  case_id: string;
  workspace_id: string;
  draft_id: string;
  review_id: string;
  revision_id: string;
  status: string;
  lock_mode: string;
  mock_final_lock_created: boolean;
  immutable_snapshot_created: boolean;
  final_legal_opinion_generated: boolean;
  llm_called: boolean;
  deepseek_live_called: boolean;
  real_ocr_called: boolean;
  real_legal_database_called: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  final_lock_storage_path: string;
  mock_final_review_snapshot: Record<string, unknown>;
  final_review_checklist: Record<string, unknown>[];
  source_refs: Record<string, unknown>[];
  guard_results: Record<string, unknown>[];
  audit_log_id: string;
  allowed_to_continue: boolean;
  warnings: string[];
  created_at: string;
};

export type ControlledFinalReviewLockRecord = {
  final_lock_id: string;
  case_id: string;
  workspace_id: string;
  draft_id: string;
  review_id: string;
  revision_id: string;
  lock_mode: string;
  mock_final_review_snapshot: Record<string, unknown>;
  final_review_checklist: Record<string, unknown>[];
  source_refs: Record<string, unknown>[];
  warnings: string[];
  created_at: string;
  immutable_snapshot: boolean;
};

export type ControlledFinalReviewLockAuditLog = {
  audit_log_id: string;
  event_type: string;
  case_id: string;
  workspace_id: string;
  draft_id: string;
  review_id: string;
  revision_id: string;
  final_lock_id: string;
  result: string;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaWorkspaceStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  end_to_end_workflow_enabled: boolean;
  mock_first_enabled: boolean;
  requires_manual_review: boolean;
  requires_explicit_workspace_confirmation: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  runtime_storage_enabled: boolean;
  runtime_storage_path: string;
  unified_audit_timeline_enabled: boolean;
  source_trace_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  store_raw_material_text_in_git: boolean;
  store_raw_ocr_text_in_git: boolean;
  store_raw_legal_search_results_in_git: boolean;
  store_workspace_snapshot_in_git: boolean;
  warnings: string[];
};

export type PersonalAlphaWorkspaceRequest = {
  case_id: string;
  workspace_id: string;
  workflow_mode: string;
  material_preview_id: string;
  ocr_preview_id: string;
  legal_search_preview_id: string;
  draft_id: string;
  review_id: string;
  revision_id: string;
  final_lock_id: string;
  explicit_workspace_confirmation: boolean;
  manual_review_confirmed: boolean;
  provider_mode: string;
  llm_mode: string;
  preview_only: boolean;
};

export type PersonalAlphaWorkspaceRunResult = {
  workspace_run_id: string;
  case_id: string;
  workspace_id: string;
  workflow_mode: string;
  status: string;
  end_to_end_mock_run_created: boolean;
  final_legal_opinion_generated: boolean;
  llm_called: boolean;
  deepseek_live_called: boolean;
  real_ocr_called: boolean;
  real_legal_database_called: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  stage_statuses: Record<string, unknown>[];
  workspace_snapshot: Record<string, unknown>;
  unified_audit_timeline: Record<string, unknown>[];
  source_refs: Record<string, unknown>[];
  guard_results: Record<string, unknown>[];
  audit_log_id: string;
  allowed_to_continue: boolean;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaWorkspaceRunRecord = {
  workspace_run_id: string;
  case_id: string;
  workspace_id: string;
  workflow_mode: string;
  stage_statuses: Record<string, unknown>[];
  workspace_snapshot: Record<string, unknown>;
  unified_audit_timeline: Record<string, unknown>[];
  source_refs: Record<string, unknown>[];
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaWorkspaceAuditLog = {
  audit_log_id: string;
  event_type: string;
  case_id: string;
  workspace_id: string;
  workspace_run_id: string;
  workflow_mode: string;
  result: string;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaDashboardStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  requires_manual_review: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  source_runtime_path: string;
  warnings: string[];
};

export type PersonalAlphaDashboardSummary = {
  total_workspace_runs: number;
  ready_stage_count: number;
  pending_stage_count: number;
  blocked_stage_count: number;
  audit_event_count: number;
  source_trace_count: number;
  mock_or_redacted_only: boolean;
  warnings: string[];
};

export type PersonalAlphaDashboardStageHealth = {
  stage_id: string;
  label: string;
  status: string;
  required: boolean;
  mock_only: boolean;
  source_ref_id: string;
  notes: string;
};

export type PersonalAlphaDashboardAuditTimeline = {
  timeline: Record<string, unknown>[];
  mock_or_redacted_only: boolean;
  warnings: string[];
};

export type PersonalAlphaDashboardSourceTraceSummary = {
  source_refs: Record<string, unknown>[];
  source_trace_count: number;
  mock_or_redacted_only: boolean;
  warnings: string[];
};

export type PersonalAlphaRunStageDetail = {
  stage_id: string;
  label: string;
  status: string;
  required: boolean;
  mock_only: boolean;
  source_ref_id: string;
  notes: string;
};

export type PersonalAlphaRunGuardSummary = {
  guard_count: number;
  blocked_count: number;
  passed_count: number;
  warnings: string[];
};

export type PersonalAlphaRunSafetyChecklist = {
  local_only: boolean;
  mock_first: boolean;
  controlled_first: boolean;
  metadata_only: boolean;
  manual_review_required: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  final_legal_opinion_generated: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
};

export type PersonalAlphaRunDetail = {
  workspace_run_id: string;
  case_id: string;
  workspace_id: string;
  workflow_mode: string;
  status: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  llm_called: boolean;
  deepseek_live_called: boolean;
  real_ocr_called: boolean;
  real_legal_database_called: boolean;
  stage_details: PersonalAlphaRunStageDetail[];
  audit_timeline: Record<string, unknown>[];
  source_refs: Record<string, unknown>[];
  guard_summary: PersonalAlphaRunGuardSummary;
  safety_checklist: PersonalAlphaRunSafetyChecklist;
  warnings: string[];
  created_at: string;
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
  package_id?: string;
  skill_id?: string;
  name?: string;
  domain?: string;
  version?: string;
  status: string;
  package_path?: string;
  created_at: string;
  experience_package_id?: string;
  source_run_id?: string;
  source_package_id?: string;
  case_cause_code?: string;
  build_mode?: string;
  llm_called?: boolean;
  real_case_material_used?: boolean;
  skill_registry_published?: boolean;
  published_skill_id?: string | null;
  inheritance_chain?: string[];
  taxonomy_path?: string[];
  package_contents?: Record<string, boolean>;
  review?: {
    requires_human_review: boolean;
    review_status: string;
    reviewed_by: string | null;
    reviewed_at: string | null;
  };
  safety?: {
    auto_publish_enabled: boolean;
    can_publish_to_skill_registry?: boolean;
    child_package_cannot_disable_safety_rules?: boolean;
  };
  manifest?: Record<string, unknown>;
};

export type ExperiencePackageDetail = ExperiencePackage & {
  manifest: Record<string, unknown>;
};

export type SkillRegistryEntry = {
  skill_id: string;
  skill_name?: string;
  domain?: string;
  version: string;
  status: string;
  validation_status?: string | null;
  evaluation_score?: number | null;
  package_id?: string | null;
  package_status?: string | null;
  source_experience_package_id?: string;
  source_run_id?: string;
  source_package_id?: string;
  case_cause_code?: string;
  publish_mode?: string;
  workspace_scope?: string;
  llm_called?: boolean;
  real_case_material_used?: boolean;
  published_at?: string;
  review?: {
    requires_human_review: boolean;
    review_status: string;
    reviewed_by: string | null;
  };
  inheritance_chain?: string[];
  taxonomy_path?: string[];
  safety?: {
    auto_publish_enabled: boolean;
    controlled_publish?: boolean;
    rollback_supported?: boolean;
    deprecate_supported?: boolean;
    child_package_cannot_disable_safety_rules?: boolean;
  };
  runtime?: {
    workspace_runtime_enabled: boolean;
    skill_aware_case_processing_enabled: boolean;
    requires_manual_enablement: boolean;
  };
  events?: Array<{
    event: string;
    reason: string;
    created_at: string;
  }>;
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
} & Partial<SkillRegistryEntry>;

export type CaseSkillBinding = {
  binding_id?: string;
  case_id: string;
  skill_id: string;
  package_id: string;
  status: string;
  message?: string;
  created_at?: string;
};

export type VersionedSkillTrainingPackage = {
  training_package_id: string;
  legacy_skill_id?: string;
  domain?: string;
  display_name?: string;
  version: string;
  status: string;
  registry_status?: string;
  case_cause_code?: string;
  case_cause_path?: string[];
  case_cause_display_path?: string;
  parent_package_ids?: string[];
  inheritance_order?: string[];
  path: string;
};

export type VersionedSkillTrainingPackageMetadata = {
  training_package_id: string;
  legacy_skill_id?: string;
  display_name: string;
  version: string;
  status: string;
  registry_status?: string;
  source?: string;
  source_packages?: string[];
  domain?: string;
  case_cause_level_1?: string | null;
  case_cause_level_2?: string | null;
  case_cause_level_3?: string | null;
  case_cause_level_4?: string | null;
  case_cause_code?: string;
  case_cause_path?: string[];
  case_cause_display_path?: string;
  parent_package_ids?: string[];
  inheritance_order?: string[];
  rule_override_policy?: {
    more_specific_overrides_general?: boolean;
    safety_rules_cannot_be_disabled?: boolean;
    human_review_required?: boolean;
  };
  training_scope: string[];
  asset_types?: string[];
  source_assets?: string[];
  requires_human_review: boolean;
  auto_train_enabled: boolean;
  auto_publish_enabled: boolean;
  next_stage?: string;
  a10_validation?: {
    required_title?: string;
    required_modules?: string[];
  };
};

export type VersionedSkillTrainingPackageDetail = {
  package: VersionedSkillTrainingPackage;
  metadata: VersionedSkillTrainingPackageMetadata;
  readme: string;
};

export type VersionedSkillTrainingPackageFile = {
  path: string;
  size: number;
};

export type CaseCauseTaxonomyEntry = {
  case_cause_code: string;
  display_name: string;
  level: number;
  parent_case_cause_code: string | null;
  path: string[];
  display_path: string;
  aliases: string[];
  status: string;
};

export type VersionedSkillTrainingRun = {
  run_id: string;
  package_id: string;
  case_cause_code: string;
  status: string;
  runner: string;
  llm_provider: string;
  llm_called: boolean;
  inheritance_chain: string[];
  taxonomy_path: string[];
  inputs: {
    source: string;
    real_case_material_used: boolean;
    legacy_asset_modified: boolean;
  };
  outputs: {
    skill_candidate_created: boolean;
    experience_package_created: boolean;
    skill_registry_published: boolean;
  };
  mock_evaluation: {
    accuracy: number;
    consistency: number;
    completeness: number;
    legal_relevance: number;
    report_quality: number;
    notes: string;
  };
  safety: {
    requires_human_review: boolean;
    auto_train_enabled: boolean;
    auto_publish_enabled: boolean;
    child_package_cannot_disable_safety_rules: boolean;
  };
  started_at?: string;
  completed_at?: string;
};
