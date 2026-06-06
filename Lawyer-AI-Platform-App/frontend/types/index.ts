export type DashboardStats = {
  cases: number;
  materials: number;
  facts: number;
  analyses: number;
  reports: number;
};

export type OwnerOutputFormatOptions = {
  markdown_available: boolean;
  json_available: boolean;
  pdf_draft_metadata_available: boolean;
  docx_draft_metadata_available: boolean;
};

export type OwnerOutputSafetyBase = {
  owner_only: boolean;
  owner_access_required: boolean;
  downloadable_by_owner_only: boolean;
  draft_or_metadata: boolean;
  metadata_only: boolean;
  draft_only: boolean;
  public_link_created: boolean;
  email_sent: boolean;
  external_delivery_triggered: boolean;
  third_party_share_enabled: boolean;
  client_auto_delivery: boolean;
  final_legal_opinion_auto_generated: boolean;
  final_report_auto_generated: boolean;
  final_skill_published: boolean;
  skill_auto_published: boolean;
  training_data_generated: boolean;
  writes_to_training_set: boolean;
  gate_reference_only: boolean;
  blocks_next_stage: boolean;
  quality_reference_only: boolean;
  source_trace_required: boolean;
  audit_required: boolean;
  api_key_exposed: boolean;
};

export type OwnerOutputRecord = OwnerOutputSafetyBase & {
  output_id: string;
  output_type: string;
  output_title: string;
  source_runtime: string;
  source_module: string;
  source_id: string;
  case_id?: string | null;
  skill_id?: string | null;
  owner_user_id: string;
  format_options: OwnerOutputFormatOptions;
  quality_score: number;
  gate_status: string;
  dimension_scores: Record<string, number>;
  optimization_suggestions: string[];
  source_trace_count: number;
  review_status: string;
  created_at: string;
  updated_at: string;
  warnings: string[];
};

export type OwnerOutputList = OwnerOutputSafetyBase & {
  outputs: OwnerOutputRecord[];
  output_count: number;
  skill_final_draft_count: number;
  fact_output_count: number;
  legal_draft_count: number;
  pilot_delivery_count: number;
  owner_download_ready: boolean;
  external_delivery_disabled: boolean;
  warnings: string[];
};

export type OwnerOutputStatus = OwnerOutputSafetyBase & {
  enabled: boolean;
  mode: string;
  version: string;
  runtime_label: string;
  output_center_ready: boolean;
  skill_final_drafts_aggregated: boolean;
  fact_outputs_aggregated: boolean;
  legal_drafts_aggregated: boolean;
  pilot_delivery_outputs_aggregated: boolean;
  owner_only_download_ready: boolean;
  public_link_disabled: boolean;
  email_sending_disabled: boolean;
  external_delivery_disabled: boolean;
  warnings: string[];
};

export type OwnerOutputQuality = OwnerOutputSafetyBase & {
  output_id: string;
  quality_score: number;
  dimension_scores: Record<string, number>;
  optimization_suggestions: string[];
  warnings: string[];
};

export type OwnerOutputGate = OwnerOutputSafetyBase & {
  output_id: string;
  gate_status: string;
  gate_score: number;
  low_confidence_flags: string[];
  warnings: string[];
};

export type OwnerOutputOptimization = OwnerOutputSafetyBase & {
  output_id: string;
  optimization_suggestions: string[];
  warnings: string[];
};

export type OwnerOutputSourceTrace = OwnerOutputSafetyBase & {
  source_trace_id: string;
  output_id: string;
  source_type: string;
  source_label: string;
  source_module: string;
  linked_source_id: string;
  trace_status: string;
  warnings: string[];
};

export type OwnerOutputSourceTraceList = OwnerOutputSafetyBase & {
  output_id?: string | null;
  source_traces: OwnerOutputSourceTrace[];
  source_trace_count: number;
  warnings: string[];
};

export type OwnerOutputDownloadRequest = {
  owner_user_id?: string;
  requested_format: string;
  explicit_owner_confirmation: boolean;
  explicit_no_public_link_confirmation: boolean;
  explicit_no_email_confirmation: boolean;
  explicit_no_external_delivery_confirmation: boolean;
};

export type OwnerOutputDownloadRecord = OwnerOutputSafetyBase & {
  download_id: string;
  output_id: string;
  owner_user_id: string;
  requested_format: string;
  download_status: string;
  file_generated: boolean;
  file_path_visible: boolean;
  created_at: string;
  warnings: string[];
};

export type OwnerOutputDownloadList = OwnerOutputSafetyBase & {
  owner_downloads: OwnerOutputDownloadRecord[];
  download_count: number;
  warnings: string[];
};

export type OwnerOutputAuditTimeline = OwnerOutputSafetyBase & {
  events: Array<Record<string, unknown>>;
  event_count: number;
  warnings: string[];
};

export type OwnerOutputSafetyStatus = OwnerOutputSafetyBase & {
  safety_checklist: string[];
  safety_item_count: number;
  all_safety_checks_passed: boolean;
  warnings: string[];
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

export type PersonalAlphaSourceReviewStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  requires_manual_review: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  warnings: string[];
};

export type PersonalAlphaSourceTrace = {
  source_ref_id: string;
  source_type: string;
  workspace_run_id: string;
  case_id: string;
  workspace_id: string;
  stage_id: string;
  evidence_item_id: string;
  evidence_status: string;
  provider: string;
  provider_mode: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  notes: string;
};

export type PersonalAlphaEvidenceSummary = {
  total_sources: number;
  total_evidence_items: number;
  blocked_sources: number;
  ready_sources: number;
  pending_sources: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaSourceReviewSafetyChecklist = {
  local_only: boolean;
  mock_first: boolean;
  controlled_first: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  manual_review_required: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  final_legal_opinion_generated: boolean;
  llm_called: boolean;
  deepseek_live_called: boolean;
  real_ocr_called: boolean;
  real_legal_database_called: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
};

export type PersonalAlphaSourceReviewRunDetail = {
  workspace_run_id: string;
  case_id: string;
  workspace_id: string;
  workflow_mode: string;
  status: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  source_traces: PersonalAlphaSourceTrace[];
  evidence_summary: PersonalAlphaEvidenceSummary;
  audit_timeline: Record<string, unknown>[];
  safety_checklist: PersonalAlphaSourceReviewSafetyChecklist;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaSourceTraceResponse = {
  workspace_run_id: string;
  source_traces: PersonalAlphaSourceTrace[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaEvidenceSummaryResponse = {
  workspace_run_id: string;
  evidence_summary: PersonalAlphaEvidenceSummary;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
};

export type PersonalAlphaSourceReviewDecisionRequest = {
  source_ref_id: string;
  decision: string;
  reviewer_id: string;
  reason: string;
  manual_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
};

export type PersonalAlphaSourceReviewDecisionRecord = {
  decision_id: string;
  workspace_run_id: string;
  source_ref_id: string;
  decision: string;
  reviewer_id: string;
  reason: string;
  status: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  manual_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaSourceReviewDecisionResult = PersonalAlphaSourceReviewDecisionRecord;

export type PersonalAlphaSourceReviewDecisionList = {
  workspace_run_id: string;
  decisions: PersonalAlphaSourceReviewDecisionRecord[];
  decision_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaSourceReviewDecisionSummary = {
  total_decisions: number;
  approved_count: number;
  rejected_count: number;
  revision_requested_count: number;
  unclear_count: number;
  latest_decision_at: string | null;
  ready_for_next_stage: boolean;
  requires_additional_review: boolean;
};

export type PersonalAlphaSourceReviewDecisionSummaryResponse = {
  workspace_run_id: string;
  summary: PersonalAlphaSourceReviewDecisionSummary;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaFinalReadinessStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  advisory_only: boolean;
  requires_manual_review: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  runtime_storage_enabled: boolean;
  runtime_storage_path: string;
  warnings: string[];
};

export type PersonalAlphaFinalReadinessSafetyChecklist = {
  local_only: boolean;
  mock_first: boolean;
  controlled_first: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  advisory_only: boolean;
  manual_review_required: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  final_legal_opinion_generated: boolean;
  llm_called: boolean;
  deepseek_live_called: boolean;
  real_ocr_called: boolean;
  real_legal_database_called: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  runtime_storage_ignored: boolean;
};

export type PersonalAlphaFinalReadinessStage = {
  stage_id: string;
  label: string;
  required: boolean;
  source_ref_id: string;
  workspace_stage_status: string;
  latest_decision: string;
  decision_count: number;
  stage_ready: boolean;
  blocked: boolean;
  requires_additional_review: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  notes: string;
};

export type PersonalAlphaFinalReadinessSummary = {
  workspace_run_id: string;
  total_stages: number;
  mandatory_stage_count: number;
  ready_stage_count: number;
  blocked_stage_count: number;
  pending_stage_count: number;
  decision_count: number;
  approved_decision_count: number;
  rejected_decision_count: number;
  revision_requested_count: number;
  unclear_decision_count: number;
  stage_ready: boolean;
  requires_additional_review: boolean;
  final_review_ready: boolean;
  final_legal_opinion_generated: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaFinalReadinessRunDetail = {
  workspace_run_id: string;
  case_id: string;
  workspace_id: string;
  workflow_mode: string;
  status: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  advisory_only: boolean;
  summary: PersonalAlphaFinalReadinessSummary;
  stages: PersonalAlphaFinalReadinessStage[];
  blocked_stages: PersonalAlphaFinalReadinessStage[];
  safety_checklist: PersonalAlphaFinalReadinessSafetyChecklist;
  decision_metadata: Record<string, unknown>;
  run_metadata: Record<string, unknown>;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaFinalReadinessSummaryResponse = {
  workspace_run_id: string;
  summary: PersonalAlphaFinalReadinessSummary;
  blocked_stages: PersonalAlphaFinalReadinessStage[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  advisory_only: boolean;
  warnings: string[];
};

export type PersonalAlphaFinalGateStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  metadata_only: boolean;
  advisory_only: boolean;
  requires_final_readiness: boolean;
  requires_manual_review: boolean;
  final_report_generation_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  warnings: string[];
};

export type PersonalAlphaFinalGateRequirements = {
  requires_final_review_ready: boolean;
  requires_no_blocked_stages: boolean;
  requires_manual_gate_decision: boolean;
  requires_metadata_only: boolean;
  requires_no_raw_content: boolean;
};

export type PersonalAlphaFinalGateSafetyChecklist = {
  local_only: boolean;
  mock_first: boolean;
  controlled_first: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  advisory_only: boolean;
  manual_review_required: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
};

export type PersonalAlphaFinalGateSummary = {
  gate_open: boolean;
  final_review_ready: boolean;
  requires_additional_review: boolean;
  latest_gate_decision: string | null;
  gate_decision_count: number;
  approved_gate_count: number;
  blocked_gate_count: number;
  more_review_requested_count: number;
  can_proceed_to_controlled_final_review: boolean;
};

export type PersonalAlphaFinalGateRunDetail = {
  workspace_run_id: string;
  status: string;
  final_review_ready: boolean;
  gate_open: boolean;
  requires_additional_review: boolean;
  blocked: boolean;
  can_proceed_to_controlled_final_review: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  readiness_summary: Record<string, unknown>;
  gate_requirements: PersonalAlphaFinalGateRequirements;
  safety_checklist: PersonalAlphaFinalGateSafetyChecklist;
  gate_summary: PersonalAlphaFinalGateSummary;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaFinalGateDecisionRequest = {
  decision: string;
  reviewer_id: string;
  reason: string;
  manual_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
};

export type PersonalAlphaFinalGateDecisionRecord = {
  gate_decision_id: string;
  workspace_run_id: string;
  decision: string;
  reviewer_id: string;
  reason: string;
  status: string;
  can_proceed_to_controlled_final_review: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  manual_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaFinalGateDecisionResult = PersonalAlphaFinalGateDecisionRecord;

export type PersonalAlphaFinalGateDecisionList = {
  workspace_run_id: string;
  decisions: PersonalAlphaFinalGateDecisionRecord[];
  decision_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaFinalGateSummaryResponse = {
  workspace_run_id: string;
  summary: PersonalAlphaFinalGateSummary;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaFinalPacketStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  advisory_only: boolean;
  requires_final_gate_approval: boolean;
  requires_manual_review: boolean;
  final_report_generation_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  runtime_storage_enabled: boolean;
  runtime_storage_path: string;
  warnings: string[];
};

export type PersonalAlphaFinalPacketSafetyChecklist = {
  local_only: boolean;
  mock_first: boolean;
  controlled_first: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  advisory_only: boolean;
  manual_review_required: boolean;
  requires_final_gate_approval: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  raw_quote_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  llm_called: boolean;
  deepseek_live_called: boolean;
  real_ocr_called: boolean;
  real_legal_database_called: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  runtime_storage_ignored: boolean;
};

export type PersonalAlphaFinalPacketSection = {
  section_id: string;
  title: string;
  status: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  items: Record<string, unknown>[];
};

export type PersonalAlphaFinalPacketPreview = {
  workspace_run_id: string;
  status: string;
  packet_preview: {
    title?: string;
    case_id?: string;
    workspace_id?: string;
    workflow_mode?: string;
    packet_sections?: PersonalAlphaFinalPacketSection[];
    mock_or_redacted_only?: boolean;
    raw_content_included?: boolean;
    final_legal_opinion_generated?: boolean;
    final_report_generated?: boolean;
  };
  can_create_packet: boolean;
  requires_final_gate_approval: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaFinalPacketCreateRequest = {
  reviewer_id: string;
  manual_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  no_final_report_generation_confirmation: boolean;
};

export type PersonalAlphaFinalPacketCreateResult = {
  packet_id: string;
  workspace_run_id: string;
  status: string;
  can_proceed_to_controlled_final_review: boolean;
  packet: Record<string, unknown>;
  reviewer_id: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  manual_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  no_final_report_generation_confirmation: boolean;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaFinalPacketRecord = {
  packet_id: string;
  workspace_run_id: string;
  status: string;
  can_proceed_to_controlled_final_review: boolean;
  packet: Record<string, unknown>;
  reviewer_id: string;
  safety_checklist: PersonalAlphaFinalPacketSafetyChecklist;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  manual_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  no_final_report_generation_confirmation: boolean;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaFinalPacketList = {
  packets: PersonalAlphaFinalPacketRecord[];
  packet_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaLawyerFinalReviewStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  advisory_only: boolean;
  requires_final_packet: boolean;
  requires_manual_review: boolean;
  requires_lawyer_review: boolean;
  final_report_generation_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  runtime_storage_enabled: boolean;
  runtime_storage_path: string;
  warnings: string[];
};

export type PersonalAlphaLawyerFinalReviewSafetyChecklist = {
  local_only: boolean;
  mock_first: boolean;
  controlled_first: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  advisory_only: boolean;
  manual_review_required: boolean;
  lawyer_review_required: boolean;
  requires_final_packet: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  raw_quote_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  llm_called: boolean;
  deepseek_live_called: boolean;
  real_ocr_called: boolean;
  real_legal_database_called: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  runtime_storage_ignored: boolean;
};

export type PersonalAlphaLawyerFinalReviewSummary = {
  review_status: string;
  action_count: number;
  approved_packet_count: number;
  revision_requested_count: number;
  rejected_packet_count: number;
  latest_action: string | null;
  ready_for_controlled_final_lock: boolean;
  requires_packet_revision: boolean;
  requires_additional_lawyer_review: boolean;
};

export type PersonalAlphaLawyerFinalReviewActionRequest = {
  action: string;
  reviewer_id: string;
  reason: string;
  manual_review_confirmed: boolean;
  lawyer_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  no_final_report_generation_confirmation: boolean;
};

export type PersonalAlphaLawyerFinalReviewActionRecord = {
  action_id: string;
  packet_id: string;
  workspace_run_id: string;
  action: string;
  reviewer_id: string;
  reason: string;
  status: string;
  ready_for_controlled_final_lock: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  manual_review_confirmed: boolean;
  lawyer_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  no_final_report_generation_confirmation: boolean;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaLawyerFinalReviewActionResult = PersonalAlphaLawyerFinalReviewActionRecord;

export type PersonalAlphaLawyerFinalReviewActionList = {
  packet_id: string;
  actions: PersonalAlphaLawyerFinalReviewActionRecord[];
  action_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaLawyerFinalReviewPacketDetail = {
  packet_id: string;
  workspace_run_id: string;
  status: string;
  packet_status: string;
  review_status: string;
  latest_action: string | null;
  can_submit_review_action: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  packet_summary: Record<string, unknown>;
  review_actions: PersonalAlphaLawyerFinalReviewActionRecord[];
  safety_checklist: PersonalAlphaLawyerFinalReviewSafetyChecklist;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaFinalLockStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  advisory_only: boolean;
  requires_lawyer_final_review_approval: boolean;
  requires_manual_review: boolean;
  requires_lawyer_review: boolean;
  final_report_generation_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  runtime_storage_enabled: boolean;
  runtime_storage_path: string;
  warnings: string[];
};

export type PersonalAlphaFinalLockReadinessRequirements = {
  requires_packet_exists: boolean;
  requires_latest_lawyer_action_approve_packet: boolean;
  requires_metadata_only: boolean;
  requires_no_raw_content: boolean;
  requires_no_final_legal_opinion: boolean;
  requires_no_final_report: boolean;
};

export type PersonalAlphaFinalLockSafetyChecklist = {
  local_only: boolean;
  mock_first: boolean;
  controlled_first: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  advisory_only: boolean;
  manual_review_required: boolean;
  lawyer_review_required: boolean;
  requires_lawyer_final_review_approval: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  raw_quote_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  llm_called: boolean;
  deepseek_live_called: boolean;
  real_ocr_called: boolean;
  real_legal_database_called: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  runtime_storage_ignored: boolean;
};

export type PersonalAlphaFinalLockReadiness = {
  packet_id: string;
  workspace_run_id: string;
  status: string;
  can_create_final_lock: boolean;
  requires_lawyer_final_review_approval: boolean;
  latest_lawyer_review_action: string | null;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  readiness_requirements: PersonalAlphaFinalLockReadinessRequirements;
  safety_checklist: PersonalAlphaFinalLockSafetyChecklist;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaFinalLockCreateRequest = {
  reviewer_id: string;
  manual_review_confirmed: boolean;
  lawyer_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  no_final_report_generation_confirmation: boolean;
};

export type PersonalAlphaFinalLockRecord = {
  lock_id: string;
  packet_id: string;
  workspace_run_id: string;
  status: string;
  reviewer_id: string;
  lock_record: Record<string, unknown>;
  safety_checklist: PersonalAlphaFinalLockSafetyChecklist;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  manual_review_confirmed: boolean;
  lawyer_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  no_final_report_generation_confirmation: boolean;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaFinalLockCreateResult = {
  lock_id: string;
  packet_id: string;
  workspace_run_id: string;
  status: string;
  reviewer_id: string;
  lock_record: Record<string, unknown>;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  manual_review_confirmed: boolean;
  lawyer_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  no_final_report_generation_confirmation: boolean;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaFinalLockList = {
  locks: PersonalAlphaFinalLockRecord[];
  lock_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSStatus = {
  enabled: boolean;
  mode: string;
  production_enabled: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  advisory_only: boolean;
  manual_review_required: boolean;
  lawyer_review_required: boolean;
  aggregates_personal_alpha_workflow: boolean;
  aggregated_versions: string[];
  case_os_enabled: boolean;
  final_report_generation_enabled: boolean;
  final_legal_opinion_enabled: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSSafetyChecklist = {
  local_only: boolean;
  mock_first: boolean;
  controlled_first: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  preview_only: boolean;
  advisory_only: boolean;
  manual_review_required: boolean;
  lawyer_review_required: boolean;
  raw_material_text_included: boolean;
  raw_ocr_text_included: boolean;
  raw_legal_search_results_included: boolean;
  raw_quote_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  llm_live_enabled: boolean;
  deepseek_live_enabled: boolean;
  ocr_live_enabled: boolean;
  legal_search_live_enabled: boolean;
  auto_skill_publish_enabled: boolean;
  auto_workspace_runtime_enabled: boolean;
};

export type PersonalAlphaCaseOSProfile = {
  case_id: string;
  title: string;
  case_type: string;
  jurisdiction: string;
  client_name: string;
  opposing_party: string;
  mock_or_redacted_only: boolean;
};

export type PersonalAlphaCaseOSStageState = {
  stage_id: string;
  label: string;
  status: string;
  ready: boolean;
  blocked: boolean;
  required: boolean;
  next_action: string | null;
  target_route: string | null;
  target_id: string | null;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
};

export type PersonalAlphaCaseOSStageSummary = {
  workspace?: PersonalAlphaCaseOSStageState;
  source_review?: PersonalAlphaCaseOSStageState;
  source_review_decision?: PersonalAlphaCaseOSStageState;
  final_readiness?: PersonalAlphaCaseOSStageState;
  final_gate?: PersonalAlphaCaseOSStageState;
  final_packet?: PersonalAlphaCaseOSStageState;
  lawyer_final_review?: PersonalAlphaCaseOSStageState;
  final_lock?: PersonalAlphaCaseOSStageState;
};

export type PersonalAlphaCaseOSNextAction = {
  case_id: string;
  current_stage: string;
  next_action: string;
  next_action_label: string;
  target_route: string;
  target_id: string | null;
  blocked: boolean;
  blocked_reasons: string[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSActionEligibilityItem = {
  action: string;
  label: string;
  eligible: boolean;
  target_route: string;
  blocked_reasons: string[];
  required_confirmations: string[];
  requires: string[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
};

export type PersonalAlphaCaseOSActionEligibility = {
  case_id: string;
  actions: PersonalAlphaCaseOSActionEligibilityItem[];
  action: string | null;
  eligible: boolean;
  requires: string[];
  blocked_reasons: string[];
  current_stage: string;
  next_action: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSStageTransition = {
  from_stage: string;
  to_stage: string;
  transition_status: string;
  allowed: boolean;
  reason: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
};

export type PersonalAlphaCaseOSStageTransitions = {
  case_id: string;
  transitions: PersonalAlphaCaseOSStageTransition[];
  current_stage: string;
  next_action: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSStageBlocker = {
  stage_id: string;
  blocked: boolean;
  blocked_reasons: string[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
};

export type PersonalAlphaCaseOSBlockers = {
  case_id: string;
  blocked: boolean;
  blocked_reasons: string[];
  stage_blockers: PersonalAlphaCaseOSStageBlocker[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSStageOrchestration = {
  case_id: string;
  current_stage: string;
  next_action: string;
  next_action_label: string;
  target_route: string;
  blocked: boolean;
  blocked_reasons: string[];
  stage_order: string[];
  stages: PersonalAlphaCaseOSStageState[];
  action_eligibility: PersonalAlphaCaseOSActionEligibility;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSCaseListItem = {
  case_id: string;
  title: string;
  workspace_id: string;
  current_stage: string;
  blocked: boolean;
  blocked_reasons: string[];
  next_action: string;
  latest_workspace_run_id: string | null;
  latest_packet_id: string | null;
  latest_lock_id: string | null;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  updated_at: string;
};

export type PersonalAlphaCaseOSAuditEvent = {
  timeline_event_id: string;
  case_id: string;
  workspace_run_id: string;
  stage_id: string;
  event_type: string;
  result: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  created_at: string;
};

export type PersonalAlphaCaseOSAuditTimeline = {
  case_id: string;
  timeline: PersonalAlphaCaseOSAuditEvent[];
  event_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSAuditTimelineFilters = {
  stage_id?: string | null;
  event_type?: string | null;
  result?: string | null;
  safety_status?: string | null;
  limit: number;
  offset: number;
};

export type PersonalAlphaCaseOSUnifiedAuditEvent = {
  timeline_event_id: string;
  case_id: string;
  workspace_run_id: string | null;
  packet_id: string | null;
  lock_id: string | null;
  stage_id: string;
  module: string;
  event_type: string;
  result: string;
  safety_status: string;
  actor_id: string;
  action: string | null;
  target_id: string | null;
  message: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  redacted: boolean;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaCaseOSUnifiedAuditTimeline = {
  case_id: string;
  filters: PersonalAlphaCaseOSAuditTimelineFilters;
  timeline: PersonalAlphaCaseOSUnifiedAuditEvent[];
  event_count: number;
  returned_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSAuditStageSummary = {
  stage_id: string;
  event_count: number;
  latest_result: string | null;
  blocked: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSAuditTimelineSummaryStats = {
  total_events: number;
  stage_count: number;
  blocked_event_count: number;
  warning_event_count: number;
  redacted_event_count: number;
  unsafe_event_count: number;
  raw_content_event_count: number;
  latest_event_at: string | null;
  modules: string[];
  stages: PersonalAlphaCaseOSAuditStageSummary[];
};

export type PersonalAlphaCaseOSAuditTimelineSummary = {
  case_id: string;
  summary: PersonalAlphaCaseOSAuditTimelineSummaryStats;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSUnsafeAuditEventSummary = {
  timeline_event_id: string;
  field_name: string;
  reason: string;
};

export type PersonalAlphaCaseOSAuditTimelineRedactionCheck = {
  case_id: string;
  redaction_check: {
    passed: boolean;
    unsafe_event_count: number;
    raw_content_event_count: number;
    path_like_value_count: number;
    api_key_like_value_count: number;
    personal_identifier_like_value_count: number;
    redacted_event_count: number;
    checked_fields: string[];
  };
  unsafe_events: PersonalAlphaCaseOSUnsafeAuditEventSummary[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSAuditTimelineAvailableFilters = {
  case_id: string;
  available_filters: {
    stage_id: string[];
    event_type: string[];
    result: string[];
    safety_status: string[];
  };
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSReviewState = {
  case_id: string;
  review_state: string;
  review_state_label: string;
  current_stage: string;
  next_action: string;
  target_route: string | null;
  blocked: boolean;
  blocked_reasons: string[];
  terminal: boolean;
  completed_metadata_review: boolean;
  state_source: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSReviewStateHistoryItem = {
  state_history_id: string;
  from_state: string;
  to_state: string;
  transition: string;
  result: string;
  source_event_id: string;
  stage_id: string;
  module: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  created_at: string;
};

export type PersonalAlphaCaseOSReviewStateHistory = {
  case_id: string;
  history: PersonalAlphaCaseOSReviewStateHistoryItem[];
  history_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSReviewStateTransition = {
  transition: string;
  from_state: string;
  to_state: string;
  allowed: boolean;
  reason: string;
  target_action: string | null;
  target_route: string | null;
  required_confirmations: string[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
};

export type PersonalAlphaCaseOSReviewStateTransitions = {
  case_id: string;
  current_state: string;
  available_transitions: PersonalAlphaCaseOSReviewStateTransition[];
  blocked_transitions: PersonalAlphaCaseOSReviewStateTransition[];
  terminal: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSReviewStateTransitionValidation = {
  case_id: string;
  from_state: string;
  to_state: string;
  transition: string;
  allowed: boolean;
  valid_transition: boolean;
  would_execute_action: boolean;
  target_action: string | null;
  target_route: string | null;
  blocked_reasons: string[];
  required_confirmations: string[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSReviewStateSummaryStats = {
  review_state: string;
  terminal: boolean;
  completed_metadata_review: boolean;
  blocked: boolean;
  history_count: number;
  available_transition_count: number;
  blocked_transition_count: number;
  next_action: string;
  target_route: string | null;
  requires_manual_review: boolean;
  requires_lawyer_review: boolean;
};

export type PersonalAlphaCaseOSReviewStateSummary = {
  case_id: string;
  summary: PersonalAlphaCaseOSReviewStateSummaryStats;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSFinalLockSummary = {
  lock_id: string | null;
  packet_id: string | null;
  workspace_run_id: string | null;
  lock_status: string;
  locked_metadata_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  created_at: string | null;
};

export type PersonalAlphaCaseOSLinkedMetadata = {
  workspace_run_id: string | null;
  packet_id: string | null;
  lawyer_review_action_id: string | null;
  lock_id: string | null;
};

export type PersonalAlphaCaseOSFinalLockConsolidation = {
  case_id: string;
  consolidation_status: string;
  final_lock_created: boolean;
  latest_lock_id: string | null;
  latest_packet_id: string | null;
  latest_lawyer_review_action: string | null;
  review_state: string;
  completed_metadata_review: boolean;
  final_lock_summary: PersonalAlphaCaseOSFinalLockSummary;
  linked_metadata: PersonalAlphaCaseOSLinkedMetadata;
  safety_checklist: PersonalAlphaCaseOSSafetyChecklist;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSMetadataClosureSummary = {
  workspace_run_ready: boolean;
  source_review_completed: boolean;
  source_decision_completed: boolean;
  final_readiness_ready: boolean;
  final_gate_approved: boolean;
  final_packet_created: boolean;
  lawyer_review_approved: boolean;
  final_lock_created: boolean;
  audit_timeline_available: boolean;
  redaction_check_passed: boolean;
};

export type PersonalAlphaCaseOSMetadataClosureChecklistItem = {
  check_id: string;
  label: string;
  passed: boolean;
  required: boolean;
  source: string;
  mock_or_redacted_only: boolean;
};

export type PersonalAlphaCaseOSMetadataClosureChecklist = {
  case_id: string;
  checklist: PersonalAlphaCaseOSMetadataClosureChecklistItem[];
  passed_count: number;
  failed_count: number;
  required_failed_count: number;
  closure_ready: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSMetadataClosure = {
  case_id: string;
  closure_status: string;
  completed_metadata_review: boolean;
  closure_ready: boolean;
  review_state: string;
  terminal: boolean;
  blocked: boolean;
  blocked_reasons: string[];
  closure_summary: PersonalAlphaCaseOSMetadataClosureSummary;
  next_action: string;
  target_route: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSMetadataClosureBlocker = {
  blocker_id: string;
  stage_id: string;
  blocked: boolean;
  reason: string | null;
  required_action: string | null;
  target_route: string | null;
  mock_or_redacted_only: boolean;
};

export type PersonalAlphaCaseOSMetadataClosureBlockers = {
  case_id: string;
  blocked: boolean;
  blocked_reasons: string[];
  closure_blockers: PersonalAlphaCaseOSMetadataClosureBlocker[];
  required_blocker_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSMetadataClosureExportSection = {
  section_id: string;
  title: string;
  included: boolean;
  raw_content_included: boolean;
  item_count: number;
};

export type PersonalAlphaCaseOSMetadataClosureExportPreview = {
  case_id: string;
  export_preview: {
    title: string;
    export_type: string;
    sections: PersonalAlphaCaseOSMetadataClosureExportSection[];
  };
  can_export_metadata_preview: boolean;
  would_create_file: boolean;
  would_include_raw_content: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSExportPackageStatus = {
  case_id: string;
  enabled: boolean;
  mode: string;
  can_create_export_package: boolean;
  requires_metadata_closure: boolean;
  requires_manual_review: boolean;
  supported_formats: string[];
  storage_mode: string;
  production_enabled: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  advisory_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSExportPackageCreateRequest = {
  format: string;
  reviewer_id: string;
  manual_review_confirmed: boolean;
  lawyer_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  redacted_only_confirmation: boolean;
  no_raw_content_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  no_final_report_generation_confirmation: boolean;
};

export type PersonalAlphaCaseOSExportPackageContentSummary = {
  section_count: number;
  item_count: number;
  includes_case_profile: boolean;
  includes_stage_summary: boolean;
  includes_final_lock_summary: boolean;
  includes_metadata_closure: boolean;
  includes_audit_summary: boolean;
  includes_safety_checklist: boolean;
  includes_raw_content: boolean;
};

export type PersonalAlphaCaseOSExportPackageSafetyStats = {
  passed: boolean;
  raw_content_included: boolean;
  path_like_value_count: number;
  api_key_like_value_count: number;
  personal_identifier_like_value_count: number;
  unsafe_value_count: number;
  checked_fields: string[];
};

export type PersonalAlphaCaseOSExportPackageUnsafeItem = {
  field_name: string;
  reason: string;
};

export type PersonalAlphaCaseOSExportPackageRecord = {
  package_id: string;
  case_id: string;
  format: string;
  status: string;
  reviewer_id: string;
  storage_mode: string;
  file_path_redacted: boolean;
  file_name: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  created_at: string;
};

export type PersonalAlphaCaseOSExportPackageCreateResult = {
  package_id: string;
  case_id: string;
  format: string;
  status: string;
  reviewer_id: string;
  storage_mode: string;
  stored: boolean;
  file_created: boolean;
  file_path_redacted: boolean;
  file_name: string;
  content_summary: PersonalAlphaCaseOSExportPackageContentSummary;
  safety_check: PersonalAlphaCaseOSExportPackageSafetyStats;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  manual_review_confirmed: boolean;
  lawyer_review_confirmed: boolean;
  metadata_only_confirmation: boolean;
  redacted_only_confirmation: boolean;
  no_raw_content_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  no_final_report_generation_confirmation: boolean;
  warnings: string[];
  created_at: string;
};

export type PersonalAlphaCaseOSExportPackageList = {
  case_id: string;
  packages: PersonalAlphaCaseOSExportPackageRecord[];
  package_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSExportPackageDetail = {
  package: PersonalAlphaCaseOSExportPackageRecord | null;
  content_summary: PersonalAlphaCaseOSExportPackageContentSummary;
  safety_check: PersonalAlphaCaseOSExportPackageSafetyStats;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSExportPackageContent = {
  package_id: string;
  case_id: string;
  format: string;
  content_type: string;
  content: unknown;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSExportPackageSafetyCheck = {
  package_id: string;
  case_id: string;
  safety_check: PersonalAlphaCaseOSExportPackageSafetyStats;
  unsafe_items: PersonalAlphaCaseOSExportPackageUnsafeItem[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSExportPackageSummary = {
  case_id: string;
  summary: {
    package_count: number;
    json_package_count: number;
    markdown_package_count: number;
    latest_package_id: string | null;
    latest_package_created_at: string | null;
    all_packages_metadata_only: boolean;
    unsafe_package_count: number;
    raw_content_package_count: number;
  };
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSExportPackageSection = {
  section_id: string;
  title: string;
  item_count: number;
  raw_content_included: boolean;
};

export type PersonalAlphaCaseOSQualityStatus = {
  case_id: string;
  enabled: boolean;
  mode: string;
  quality_check_available: boolean;
  quality_result_is_advisory: boolean;
  production_enabled: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  advisory_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSQualityChecklistItem = {
  check_id: string;
  category: string;
  label: string;
  passed: boolean;
  required: boolean;
  severity: string;
  source: string;
  target_route: string;
  finding_code: string | null;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
};

export type PersonalAlphaCaseOSQualityChecklist = {
  case_id: string;
  checklist: PersonalAlphaCaseOSQualityChecklistItem[];
  passed_count: number;
  failed_count: number;
  required_failed_count: number;
  critical_failed_count: number;
  warning_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSQualityScoreDetail = {
  quality_score: number;
  quality_grade: string;
  max_score: number;
  passed_count: number;
  failed_count: number;
  required_failed_count: number;
  critical_failed_count: number;
  high_failed_count: number;
  medium_failed_count: number;
  low_failed_count: number;
  blocking_issue_count: number;
  advisory_warning_count: number;
  ready_for_personal_alpha_review: boolean;
};

export type PersonalAlphaCaseOSQualityScore = {
  case_id: string;
  score: PersonalAlphaCaseOSQualityScoreDetail;
  score_logic: Record<string, number>;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSQualityFinding = {
  finding_id: string;
  finding_code: string;
  category: string;
  severity: string;
  title: string;
  description: string;
  blocking: boolean;
  target_route: string;
  recommended_action: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
};

export type PersonalAlphaCaseOSQualityFindings = {
  case_id: string;
  findings: PersonalAlphaCaseOSQualityFinding[];
  finding_count: number;
  blocking_finding_count: number;
  critical_finding_count: number;
  high_finding_count: number;
  medium_finding_count: number;
  low_finding_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSQualityRecommendation = {
  recommendation_id: string;
  priority: string;
  action: string;
  label: string;
  target_route: string;
  reason: string;
  would_execute_action: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
};

export type PersonalAlphaCaseOSQualityRecommendations = {
  case_id: string;
  recommendations: PersonalAlphaCaseOSQualityRecommendation[];
  recommendation_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSQualityReportSection = {
  section_id: string;
  title: string;
  included: boolean;
  raw_content_included: boolean;
  item_count: number;
};

export type PersonalAlphaCaseOSQualityReportPreview = {
  case_id: string;
  report_preview: {
    title: string;
    report_type: string;
    sections: PersonalAlphaCaseOSQualityReportSection[];
  };
  would_create_file: boolean;
  would_generate_final_report: boolean;
  would_generate_legal_opinion: boolean;
  would_include_raw_content: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSQualitySummaryDetail = {
  quality_score: number;
  quality_grade: string;
  ready_for_personal_alpha_review: boolean;
  required_failed_count: number;
  critical_failed_count: number;
  blocking_finding_count: number;
  advisory_warning_count: number;
  top_findings: Record<string, unknown>[];
  top_recommendations: Record<string, unknown>[];
  metadata_closure_ready: boolean;
  export_package_available: boolean;
  redaction_check_passed: boolean;
};

export type PersonalAlphaCaseOSQualitySummary = {
  case_id: string;
  summary: PersonalAlphaCaseOSQualitySummaryDetail;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSHardeningStatus = {
  enabled: boolean;
  mode: string;
  safe_response_enabled: boolean;
  safe_not_found_enabled: boolean;
  blocked_response_enabled: boolean;
  redacted_response_enabled: boolean;
  no_raw_content_guard_enabled: boolean;
  runtime_storage_guard_enabled: boolean;
  response_consistency_check_enabled: boolean;
  production_enabled: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  advisory_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSHardeningUnsafeItem = {
  scope: string;
  field_name: string;
  reason: string;
};

export type PersonalAlphaCaseOSHardeningSafetyCheckDetail = {
  passed: boolean;
  unsafe_value_count: number;
  path_like_value_count: number;
  api_key_like_value_count: number;
  raw_content_like_value_count: number;
  checked_scopes: string[];
};

export type PersonalAlphaCaseOSHardeningSafetyCheck = {
  case_id: string;
  safety_check: PersonalAlphaCaseOSHardeningSafetyCheckDetail;
  unsafe_items: PersonalAlphaCaseOSHardeningUnsafeItem[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSResponseConsistencyIssue = {
  endpoint: string;
  field_name: string;
  reason: string;
};

export type PersonalAlphaCaseOSResponseConsistencyDetail = {
  passed: boolean;
  checked_endpoints: string[];
  missing_required_field_count: number;
  inconsistent_safety_flag_count: number;
  required_fields: string[];
};

export type PersonalAlphaCaseOSResponseConsistency = {
  case_id: string;
  response_consistency: PersonalAlphaCaseOSResponseConsistencyDetail;
  issues: PersonalAlphaCaseOSResponseConsistencyIssue[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSRuntimeStorageCheckDetail = {
  passed: boolean;
  storage_mode: string;
  runtime_root_redacted: boolean;
  absolute_path_returned: boolean;
  tracked_path_write_enabled: boolean;
  checked_paths: string[];
};

export type PersonalAlphaCaseOSRuntimeStorageCheck = {
  case_id: string;
  runtime_storage_check: PersonalAlphaCaseOSRuntimeStorageCheckDetail;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSReleaseCandidateStatus = {
  enabled: boolean;
  mode: string;
  release_candidate_version: string;
  release_candidate_name: string;
  production_enabled: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  metadata_only: boolean;
  redacted_only: boolean;
  advisory_only: boolean;
  regression_suite_required: boolean;
  hardening_required: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  raw_content_included: boolean;
  next_major_version: string;
  next_major_direction: string;
  warnings: string[];
};

export type PersonalAlphaCaseOSReleaseCandidateSummary = {
  release_candidate_version: string;
  summary: Record<string, boolean>;
  capability_count: number;
  ready_capability_count: number;
  missing_capabilities: string[];
  next_major_version: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSReleaseCandidateChecklistItem = {
  check_id: string;
  label: string;
  passed: boolean;
  required: boolean;
  category: string;
  source: string;
};

export type PersonalAlphaCaseOSReleaseCandidateChecklist = {
  release_candidate_version: string;
  checklist: PersonalAlphaCaseOSReleaseCandidateChecklistItem[];
  passed_count: number;
  failed_count: number;
  required_failed_count: number;
  release_candidate_ready: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSReleaseCandidateReadiness = {
  release_candidate_version: string;
  release_candidate_ready: boolean;
  readiness: Record<string, boolean | number>;
  next_action: string;
  next_major_version: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSReleaseCandidateUnsafeItem = {
  scope: string;
  field_name: string;
  reason: string;
};

export type PersonalAlphaCaseOSReleaseCandidateAudit = {
  release_candidate_version: string;
  audit: Record<string, boolean | number>;
  unsafe_items: PersonalAlphaCaseOSReleaseCandidateUnsafeItem[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSReleaseNotesPreviewSection = {
  section_id: string;
  title: string;
  included: boolean;
  raw_content_included: boolean;
};

export type PersonalAlphaCaseOSReleaseNotesPreview = {
  release_candidate_version: string;
  release_notes_preview: {
    title: string;
    release_type: string;
    sections: PersonalAlphaCaseOSReleaseNotesPreviewSection[];
  };
  next_major_version: string;
  next_major_direction: string;
  would_create_file: boolean;
  would_generate_final_report: boolean;
  would_generate_legal_opinion: boolean;
  would_include_raw_content: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSReleaseCandidateCaseReadiness = {
  case_id: string;
  release_candidate_case_ready: boolean;
  case_readiness: Record<string, boolean>;
  next_action: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAlphaCaseOSCaseDetail = {
  case_id: string;
  title: string;
  workspace_id: string;
  current_stage: string;
  blocked: boolean;
  blocked_reasons: string[];
  next_action: string;
  profile: PersonalAlphaCaseOSProfile;
  workspace_runs: Record<string, unknown>[];
  stage_summary: PersonalAlphaCaseOSStageSummary;
  source_review: Record<string, unknown>;
  source_review_decision: Record<string, unknown>;
  final_readiness: Record<string, unknown>;
  final_gate: Record<string, unknown>;
  final_packet: Record<string, unknown>;
  lawyer_final_review: Record<string, unknown>;
  final_lock: Record<string, unknown>;
  audit_timeline: PersonalAlphaCaseOSAuditEvent[];
  safety_checklist: PersonalAlphaCaseOSSafetyChecklist;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalProductionStatus = {
  enabled: boolean;
  mode: string;
  version: string;
  personal_production_phase: boolean;
  showcase_ready: boolean;
  production_validation_ready: boolean;
  external_client_delivery_ready: boolean;
  team_workspace_enabled: boolean;
  real_provider_call_enabled: boolean;
  ai_runtime_registered: boolean;
  ai_gateway_registered: boolean;
  material_parsing_runtime_registered: boolean;
  ocr_runtime_registered: boolean;
  legal_search_runtime_registered: boolean;
  skill_training_runtime_registered: boolean;
  delivery_runtime_registered: boolean;
  mock_first_enabled: boolean;
  controlled_first_enabled: boolean;
  lawyer_review_required: boolean;
  manual_final_lock_required: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalProductionMode = {
  personal_production_mode: string;
  personal_production_enabled: boolean;
  real_provider_enabled: boolean;
  external_delivery_enabled: boolean;
  team_workspace_enabled: boolean;
  showcase_mode_enabled: boolean;
  developer_diagnostics_enabled: boolean;
  lawyer_review_required: boolean;
  manual_final_lock_required: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalProductionShowcase = {
  showcase_mode_enabled: boolean;
  showcase_safe: boolean;
  public_demo_safe: boolean;
  developer_diagnostics_collapsed: boolean;
  raw_content_visible: boolean;
  internal_paths_visible: boolean;
  provider_secrets_visible: boolean;
  headline: string;
  subheadline: string;
  trust_badges: string[];
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalProductionRuntimeItem = {
  runtime_id: string;
  label: string;
  category: string;
  mode: string;
  enabled: boolean;
  live_enabled: boolean;
  mock_available: boolean;
  controlled_available: boolean;
  production_ready: boolean;
  provider_configured: boolean;
  gateway_registered: boolean;
  manual_approval_required: boolean;
  lawyer_review_required: boolean;
  status: string;
  target_route: string;
  warnings: string[];
};

export type PersonalProductionRuntimeRegistry = {
  runtimes: PersonalProductionRuntimeItem[];
  registered_runtime_count: number;
  live_runtime_count: number;
  controlled_runtime_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalProductionProviderCapability = {
  provider_id: string;
  label: string;
  category: string;
  configured: boolean;
  live_enabled: boolean;
  mock_supported: boolean;
  controlled_live_supported: boolean;
  requires_api_key: boolean;
  api_key_present: boolean;
  api_key_visible: boolean;
  status: string;
  next_action: string;
  target_route: string;
  gateway_registered: boolean;
};

export type PersonalProductionProviderCapabilities = {
  providers: PersonalProductionProviderCapability[];
  provider_count: number;
  configured_provider_count: number;
  live_provider_count: number;
  key_loaded_count: number;
  material_live_provider_count: number;
  material_key_loaded_count: number;
  intelligence_live_provider_count: number;
  intelligence_key_loaded_count: number;
  ai_live_gateway_status: string;
  ocr_document_live_gateway_status: string;
  legal_enterprise_live_gateway_status: string;
  controlled_case_analysis_runtime_status: string;
  fact_skill_baseline_detected: boolean;
  legal_analysis_skill_baseline_detected: boolean;
  open_case_analysis_draft_ready: boolean;
  training_data_generation_disabled: boolean;
  skill_auto_update_disabled: boolean;
  evaluation_reference_only: boolean;
  personal_production_pilot_status: string;
  personal_case_workspace_status: string;
  personal_production_pilot_dashboard_status: string;
  fact_preview_correction_workbench_status: string;
  legal_analysis_draft_workbench_status: string;
  skill_final_draft_workbench_status: string;
  owner_output_center_status: string;
  owner_output_center_ready: boolean;
  skill_final_drafts_aggregated: boolean;
  fact_outputs_aggregated: boolean;
  legal_drafts_aggregated: boolean;
  pilot_delivery_outputs_aggregated: boolean;
  fact_preview_owner_correction_ready: boolean;
  fact_preview_legal_analysis_input_ready: boolean;
  fact_preview_legal_analysis_auto_triggered: boolean;
  fact_preview_gate_reference_only: boolean;
  legal_analysis_draft_only: boolean;
  legal_analysis_draft_review_ready: boolean;
  legal_analysis_final_opinion_blocked: boolean;
  legal_analysis_final_report_blocked: boolean;
  legal_analysis_owner_download_metadata_ready: boolean;
  fact_skill_final_draft_ready: boolean;
  legal_analysis_skill_final_draft_ready: boolean;
  skill_final_draft_owner_download_ready: boolean;
  skill_final_draft_auto_publish_disabled: boolean;
  skill_final_draft_open_case_training_disabled: boolean;
  skill_final_draft_gate_reference_only: boolean;
  pilot_ai_ocr_legal_enterprise_skill_case_analysis_connected: boolean;
  case_workspace_owner_raw_view_gated: boolean;
  pilot_dashboard_quality_panels_ready: boolean;
  pilot_dashboard_optimization_suggestions_ready: boolean;
  owner_only_downloads_ready: boolean;
  owner_output_center_download_ready: boolean;
  external_delivery_disabled: boolean;
  public_link_disabled: boolean;
  email_sending_disabled: boolean;
  final_legal_opinion_auto_generation_disabled: boolean;
  final_report_auto_generation_disabled: boolean;
  open_case_training_data_generation_disabled: boolean;
  dry_run_ready: boolean;
  document_dry_run_ready: boolean;
  ocr_dry_run_ready: boolean;
  legal_dry_run_ready: boolean;
  enterprise_dry_run_ready: boolean;
  live_call_requires_confirmation: boolean;
  draft_only_output: boolean;
  raw_content_blocked_by_default: boolean;
  ai_prompt_injection_blocked_by_default: boolean;
  citation_finalization_blocked_by_default: boolean;
  provider_secrets_visible: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalProductionReadiness = {
  personal_production_ready: boolean;
  showcase_ready: boolean;
  readiness: Record<string, boolean>;
  missing_requirements: string[];
  next_action: string;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalProductionSafety = {
  safety: Record<string, boolean>;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalProductionConsoleSummary = {
  title: string;
  phase: string;
  version: string;
  showcase_ready: boolean;
  personal_production_ready: boolean;
  external_client_delivery_ready: boolean;
  team_workspace_enabled: boolean;
  next_steps: string[];
  runtime_summary: Record<string, number>;
  trust_summary: Record<string, boolean>;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAIGatewayStatus = {
  enabled: boolean;
  mode: string;
  version: string;
  mock_first_enabled: boolean;
  controlled_live_supported: boolean;
  live_provider_call_enabled: boolean;
  provider_gateway_enabled: boolean;
  prompt_registry_enabled: boolean;
  prompt_render_preview_enabled: boolean;
  mock_ai_run_enabled: boolean;
  manual_approval_required: boolean;
  lawyer_review_required: boolean;
  draft_only: boolean;
  source_trace_required: boolean;
  external_delivery_enabled: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalAIProvider = {
  provider_id: string;
  label: string;
  category: string;
  configured: boolean;
  live_enabled: boolean;
  mock_supported: boolean;
  controlled_live_supported: boolean;
  requires_api_key: boolean;
  api_key_present: boolean;
  api_key_visible: boolean;
  status: string;
  target_route: string;
  warnings: string[];
};

export type PersonalAIProviderList = {
  providers: PersonalAIProvider[];
  provider_count: number;
  configured_provider_count: number;
  live_provider_count: number;
  provider_credentials_visible: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAIPromptTemplate = {
  template_id: string;
  name: string;
  purpose: string;
  case_type: string;
  input_schema: Record<string, unknown>;
  output_schema: Record<string, unknown>;
  draft_only: boolean;
  requires_lawyer_review: boolean;
  source_trace_required: boolean;
  allowed_provider_categories: string[];
  version: string;
  enabled: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAIPromptTemplateList = {
  templates: PersonalAIPromptTemplate[];
  template_count: number;
  enabled_template_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAIPromptRenderPreviewRequest = {
  template_id: string;
  case_id?: string | null;
  variables: Record<string, unknown>;
  manual_review_confirmed: boolean;
  mock_data_only_confirmation: boolean;
  no_raw_content_confirmation: boolean;
};

export type PersonalAIPromptRenderPreviewResult = {
  template_id: string;
  case_id?: string | null;
  status: string;
  rendered_prompt_preview: string;
  would_call_provider: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  requires_lawyer_review: boolean;
  draft_only: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  blocked_reasons: string[];
  warnings: string[];
};

export type PersonalAITokenUsage = {
  estimated_input_tokens: number;
  estimated_output_tokens: number;
  estimated_total_tokens: number;
  actual_input_tokens: number | null;
  actual_output_tokens: number | null;
  actual_total_tokens: number | null;
  live_usage_available: boolean;
};

export type PersonalAIDraftOutput = {
  title: string;
  content: string;
  draft_only: boolean;
  requires_lawyer_review: boolean;
  source_trace_required: boolean;
};

export type PersonalAIMockRunRequest = {
  provider_id: string;
  template_id: string;
  case_id?: string | null;
  manual_approval_confirmed: boolean;
  lawyer_review_required_confirmation: boolean;
  draft_only_confirmation: boolean;
  source_trace_required_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  no_final_report_generation_confirmation: boolean;
};

export type PersonalAIMockRunResult = {
  ai_run_id?: string | null;
  provider_id: string;
  template_id: string;
  case_id?: string | null;
  mode: string;
  status: string;
  would_call_provider: boolean;
  live_call_executed: boolean;
  draft_output?: PersonalAIDraftOutput | null;
  token_usage: PersonalAITokenUsage;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  blocked_reasons: string[];
  warnings: string[];
};

export type PersonalAIRunRecord = {
  ai_run_id: string;
  provider_id: string;
  template_id: string;
  case_id?: string | null;
  purpose: string;
  mode: string;
  status: string;
  would_call_provider: boolean;
  live_call_executed: boolean;
  manual_approval_confirmed: boolean;
  draft_only: boolean;
  requires_lawyer_review: boolean;
  source_trace_required: boolean;
  token_usage: PersonalAITokenUsage;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  created_at: string;
  warnings: string[];
};

export type PersonalAIRunList = {
  runs: PersonalAIRunRecord[];
  run_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAIAuditEvent = {
  ai_run_id: string;
  provider_id: string;
  template_id: string;
  case_id?: string | null;
  purpose: string;
  mode: string;
  would_call_provider: boolean;
  live_call_executed: boolean;
  manual_approval_confirmed: boolean;
  draft_only: boolean;
  requires_lawyer_review: boolean;
  token_usage_estimate: Record<string, number>;
  created_at: string;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
};

export type PersonalAIAuditTimeline = {
  events: PersonalAIAuditEvent[];
  event_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAITokenUsageSummary = {
  run_count: number;
  estimated_total_tokens: number;
  actual_total_tokens: number | null;
  live_usage_available: boolean;
  provider_usage_breakdown: Record<string, number>;
  template_usage_breakdown: Record<string, number>;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAISafetyStatus = {
  safety: Record<string, boolean>;
  all_safety_checks_passed: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalAILiveProviderConfig = {
  provider_id: string;
  display_name: string;
  provider_type: string;
  live_supported: boolean;
  live_enabled: boolean;
  key_required: boolean;
  key_loaded: boolean;
  key_source: string;
  model_options: string[];
  timeout_seconds: number;
  safety_notes: string[];
  api_key_exposed: boolean;
};

export type PersonalAILiveProviderConfigList = {
  providers: PersonalAILiveProviderConfig[];
  provider_count: number;
  live_provider_count: number;
  key_loaded_count: number;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  api_key_exposed: boolean;
  raw_content_included: boolean;
  draft_only: boolean;
  lawyer_review_required: boolean;
  source_trace_required: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  warnings: string[];
};

export type PersonalAILiveGatewayStatus = {
  enabled: boolean;
  mode: string;
  version: string;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  dry_run_enabled: boolean;
  provider_count: number;
  live_provider_count: number;
  key_loaded_count: number;
  explicit_live_confirmation_required: boolean;
  lawyer_review_acknowledged_required: boolean;
  draft_only_acknowledged_required: boolean;
  no_final_opinion_acknowledged_required: boolean;
  api_key_exposed: boolean;
  raw_content_included: boolean;
  draft_only: boolean;
  lawyer_review_required: boolean;
  source_trace_required: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  warnings: string[];
};

export type PersonalAILiveRunRequest = {
  provider_id: string;
  model?: string | null;
  prompt_template_id: string;
  prompt_purpose: string;
  case_id?: string | null;
  source_trace_ids: string[];
  dry_run: boolean;
  actor_id: string;
  explicit_live_confirmation: boolean;
  lawyer_review_acknowledged: boolean;
  draft_only_acknowledged: boolean;
  no_final_opinion_acknowledged: boolean;
  no_final_report_acknowledged: boolean;
  no_external_delivery_acknowledged: boolean;
  raw_content_included: boolean;
  final_legal_opinion_requested: boolean;
  final_report_requested: boolean;
};

export type PersonalAILiveDraftMetadata = {
  ai_draft: string;
  draft_type: string;
  provider_id: string;
  model: string;
  token_usage: Record<string, number | null>;
  latency_ms?: number | null;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
};

export type PersonalAILiveRunRecord = {
  run_id: string;
  provider_id: string;
  model: string;
  prompt_template_id: string;
  prompt_purpose: string;
  case_id?: string | null;
  source_trace_ids: string[];
  status: string;
  dry_run: boolean;
  would_call_provider: boolean;
  live_call_requested: boolean;
  live_call_executed: boolean;
  blocked_reason?: string | null;
  confirmations: Record<string, boolean>;
  draft_output_metadata?: PersonalAILiveDraftMetadata | null;
  created_at: string;
  live_mode_enabled: boolean;
  api_key_exposed: boolean;
  raw_content_included: boolean;
  draft_only: boolean;
  lawyer_review_required: boolean;
  source_trace_required: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  warnings: string[];
};

export type PersonalAILiveRunList = {
  runs: PersonalAILiveRunRecord[];
  run_count: number;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  api_key_exposed: boolean;
  raw_content_included: boolean;
  draft_only: boolean;
  lawyer_review_required: boolean;
  source_trace_required: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  warnings: string[];
};

export type PersonalAILiveAuditEvent = {
  event_id: string;
  provider_id: string;
  action: string;
  actor_id: string;
  live_call_requested: boolean;
  live_call_executed: boolean;
  blocked_reason?: string | null;
  confirmations: Record<string, boolean>;
  token_usage: Record<string, number | null>;
  created_at: string;
  api_key_exposed: boolean;
  raw_content_included: boolean;
  draft_only: boolean;
  lawyer_review_required: boolean;
  source_trace_required: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
};

export type PersonalAILiveAuditTimeline = {
  events: PersonalAILiveAuditEvent[];
  event_count: number;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  api_key_exposed: boolean;
  raw_content_included: boolean;
  draft_only: boolean;
  lawyer_review_required: boolean;
  source_trace_required: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  warnings: string[];
};

export type PersonalAILiveSafetyStatus = {
  safety: Record<string, boolean>;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  api_key_exposed: boolean;
  raw_content_included: boolean;
  draft_only: boolean;
  lawyer_review_required: boolean;
  source_trace_required: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  warnings: string[];
};

export type PersonalMaterialRuntimeStatus = {
  enabled: boolean;
  mode: string;
  version: string;
  mock_first_enabled: boolean;
  controlled_live_supported: boolean;
  live_provider_call_enabled: boolean;
  material_parser_runtime_enabled: boolean;
  ocr_runtime_enabled: boolean;
  ocr_review_queue_enabled: boolean;
  source_trace_enabled: boolean;
  manual_approval_required: boolean;
  lawyer_review_required: boolean;
  raw_ocr_controlled: boolean;
  raw_ocr_text_exposed: boolean;
  external_delivery_enabled: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  raw_content_included: boolean;
  warnings: string[];
};

export type PersonalMaterialProvider = {
  provider_id: string;
  label: string;
  category: string;
  configured: boolean;
  live_enabled: boolean;
  mock_supported: boolean;
  controlled_live_supported: boolean;
  requires_api_key: boolean;
  api_key_present: boolean;
  api_key_visible: boolean;
  status: string;
  target_version: string;
  target_route: string;
  next_action: string;
  warnings: string[];
};

export type PersonalMaterialProviderList = {
  providers: PersonalMaterialProvider[];
  provider_count: number;
  configured_provider_count: number;
  live_provider_count: number;
  provider_credentials_visible: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  raw_ocr_text_exposed: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalMaterialParseSummary = {
  page_count: number;
  section_count: number;
  table_count: number;
  image_count: number;
  mock_preview_only: boolean;
};

export type PersonalMaterialParseJobRequest = {
  case_id: string;
  material_id: string;
  parser_provider_id: string;
  parse_type: string;
  manual_approval_confirmed: boolean;
  mock_data_only_confirmation: boolean;
  no_raw_content_confirmation: boolean;
  no_external_upload_confirmation: boolean;
};

export type PersonalMaterialParseJobResult = {
  parse_job_id?: string | null;
  case_id: string;
  material_id: string;
  parser_provider_id: string;
  parse_type: string;
  mode: string;
  status: string;
  would_call_provider: boolean;
  live_call_executed: boolean;
  parse_summary: PersonalMaterialParseSummary;
  source_trace_required: boolean;
  requires_lawyer_review: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  raw_material_text_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  controlled_preview_only: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_enabled: boolean;
  blocked_reasons: string[];
  warnings: string[];
};

export type PersonalMaterialParseJobRecord = PersonalMaterialParseJobResult & {
  parse_job_id: string;
  created_at: string;
};

export type PersonalMaterialParseJobList = {
  parse_jobs: PersonalMaterialParseJobRecord[];
  job_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  raw_ocr_text_exposed: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalOCRPreview = {
  ocr_job_id?: string | null;
  case_id?: string | null;
  material_id?: string | null;
  ocr_provider_id?: string | null;
  status: string;
  page_count: number;
  recognized_block_count: number;
  average_confidence: number;
  low_confidence_block_count: number;
  table_detected: boolean;
  layout_detected: boolean;
  key_information_detected: boolean;
  preview_blocks: Record<string, string | number | boolean>[];
  controlled_preview_only: boolean;
  raw_ocr_text_exposed: boolean;
  requires_lawyer_review: boolean;
  source_trace_required: boolean;
  used_in_ai_prompt: boolean;
  used_in_final_output: boolean;
  eligible_for_ai_prompt_after_review: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalOCRJobRequest = {
  case_id: string;
  material_id: string;
  ocr_provider_id: string;
  ocr_job_type: string;
  manual_approval_confirmed: boolean;
  lawyer_review_required_confirmation: boolean;
  source_trace_required_confirmation: boolean;
  no_raw_ocr_exposure_confirmation: boolean;
  no_final_legal_opinion_confirmation: boolean;
  no_final_report_generation_confirmation: boolean;
};

export type PersonalOCRJobResult = {
  ocr_job_id?: string | null;
  case_id: string;
  material_id: string;
  ocr_provider_id: string;
  ocr_job_type: string;
  mode: string;
  status: string;
  would_call_provider: boolean;
  live_call_executed: boolean;
  ocr_preview: PersonalOCRPreview;
  review_status: string;
  source_trace_required: boolean;
  requires_lawyer_review: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  raw_ocr_text_exposed: boolean;
  controlled_preview_only: boolean;
  used_in_ai_prompt: boolean;
  used_in_final_output: boolean;
  eligible_for_ai_prompt_after_review: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_enabled: boolean;
  blocked_reasons: string[];
  warnings: string[];
};

export type PersonalOCRJobRecord = PersonalOCRJobResult & {
  ocr_job_id: string;
  created_at: string;
};

export type PersonalOCRJobList = {
  ocr_jobs: PersonalOCRJobRecord[];
  job_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  raw_ocr_text_exposed: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalOCRReviewItem = {
  ocr_job_id: string;
  case_id: string;
  material_id: string;
  ocr_provider_id: string;
  review_status: string;
  confidence: number;
  low_confidence_block_count: number;
  requires_lawyer_review: boolean;
  source_trace_required: boolean;
  controlled_preview_only: boolean;
  raw_content_included: boolean;
  raw_ocr_text_exposed: boolean;
  used_in_ai_prompt: boolean;
  used_in_final_output: boolean;
  eligible_for_ai_prompt_after_review: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  created_at: string;
  updated_at: string;
  warnings: string[];
};

export type PersonalOCRReviewQueue = {
  items: PersonalOCRReviewItem[];
  item_count: number;
  pending_review_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  raw_ocr_text_exposed: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalOCRReviewActionRequest = {
  action: string;
  reviewer_id: string;
  manual_review_confirmed: boolean;
  no_raw_ocr_exposure_confirmation: boolean;
  lawyer_review_required_confirmation: boolean;
};

export type PersonalOCRReviewActionResult = {
  ocr_job_id: string;
  action: string;
  reviewer_id: string;
  status: string;
  review_status: string;
  manual_review_confirmed: boolean;
  controlled_preview_only: boolean;
  raw_content_included: boolean;
  raw_ocr_text_exposed: boolean;
  used_in_ai_prompt: boolean;
  used_in_final_output: boolean;
  eligible_for_ai_prompt_after_review: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  blocked_reasons: string[];
  warnings: string[];
};

export type PersonalMaterialSourceTrace = {
  source_trace_id: string;
  case_id: string;
  material_id: string;
  job_id: string;
  source_type: string;
  provider_id: string;
  page_number: number;
  block_id: string;
  bbox_redacted: boolean;
  bbox: Record<string, number>;
  confidence: number;
  created_at: string;
  manual_review_status: string;
  controlled_preview_only: boolean;
  raw_content_included: boolean;
  raw_ocr_text_exposed: boolean;
  used_in_ai_prompt: boolean;
  used_in_final_output: boolean;
  eligible_for_ai_prompt_after_review: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
};

export type PersonalMaterialSourceTraceList = {
  source_traces: PersonalMaterialSourceTrace[];
  source_trace_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  raw_ocr_text_exposed: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalMaterialAuditEvent = {
  event_id: string;
  event_type: string;
  case_id: string;
  material_id: string;
  provider_id: string;
  job_id: string;
  mode: string;
  live_call_executed: boolean;
  manual_approval_confirmed: boolean;
  raw_ocr_text_exposed: boolean;
  controlled_preview_only: boolean;
  raw_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  created_at: string;
};

export type PersonalMaterialAuditTimeline = {
  events: PersonalMaterialAuditEvent[];
  event_count: number;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  raw_ocr_text_exposed: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalMaterialSafetyStatus = {
  safety: Record<string, boolean>;
  all_safety_checks_passed: boolean;
  mock_or_redacted_only: boolean;
  raw_content_included: boolean;
  raw_ocr_text_exposed: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalMaterialLiveProviderConfig = {
  provider_id: string;
  display_name: string;
  provider_type: string;
  live_supported: boolean;
  live_enabled: boolean;
  key_required: boolean;
  key_loaded: boolean;
  key_source: string;
  supported_file_types: string[];
  max_file_size_mb: number;
  supports_page_range: boolean;
  supports_bbox: boolean;
  supports_table_extraction: boolean;
  supports_layout_extraction: boolean;
  timeout_seconds: number;
  safety_notes: string[];
};

export type PersonalMaterialLiveProviderConfigList = {
  providers: PersonalMaterialLiveProviderConfig[];
  provider_count: number;
  live_provider_count: number;
  key_loaded_count: number;
  provider_secrets_visible: boolean;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  warnings: string[];
};

export type PersonalMaterialLiveGatewayStatus = {
  enabled: boolean;
  mode: string;
  version: string;
  ocr_live_mode_enabled: boolean;
  document_live_mode_enabled: boolean;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  dry_run_ready: boolean;
  document_dry_run_ready: boolean;
  ocr_dry_run_ready: boolean;
  live_call_requires_confirmation: boolean;
  provider_gated: boolean;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
  fact_extraction_triggered: boolean;
  legal_analysis_triggered: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  warnings: string[];
};

export type PersonalMaterialLiveRunRequest = {
  provider_id: string;
  case_id: string;
  material_id: string;
  file_name: string;
  file_type: string;
  byte_size: number;
  page_range?: string | null;
  actor_id: string;
  dry_run: boolean;
  explicit_live_confirmation: boolean;
  material_owner_confirmation: boolean;
  raw_content_handling_acknowledged: boolean;
  no_ai_prompt_injection_acknowledged: boolean;
  lawyer_review_acknowledged: boolean;
  draft_only_acknowledged: boolean;
};

export type PersonalMaterialLiveMetadataPreview = {
  page_count: number;
  page_count_estimate: number;
  file_type: string;
  byte_size: number;
  parse_status: string;
  confidence_summary: string;
  layout_blocks_count: number;
  table_count: number;
  image_count: number;
  bbox_available: boolean;
  supports_bbox: boolean;
  supports_confidence: boolean;
  redacted_preview_available: boolean;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
};

export type PersonalMaterialLiveRunRecord = {
  run_id: string;
  run_type: string;
  provider_id: string;
  case_id: string;
  material_id: string;
  file_name: string;
  file_type: string;
  status: string;
  dry_run: boolean;
  would_call_provider: boolean;
  live_mode_enabled: boolean;
  live_call_requested: boolean;
  live_call_executed: boolean;
  blocked_reason?: string | null;
  blocked_reasons: string[];
  provider_adapter_unavailable: boolean;
  file_metadata_only: boolean;
  document_metadata: PersonalMaterialLiveMetadataPreview;
  ocr_metadata: PersonalMaterialLiveMetadataPreview;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
  fact_extraction_triggered: boolean;
  legal_analysis_triggered: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  source_trace_created: boolean;
  review_required: boolean;
  created_at: string;
  warnings: string[];
};

export type PersonalMaterialLiveRunList = {
  runs: PersonalMaterialLiveRunRecord[];
  run_count: number;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
  fact_extraction_triggered: boolean;
  legal_analysis_triggered: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  warnings: string[];
};

export type PersonalMaterialLiveReviewItem = {
  review_item_id: string;
  run_id: string;
  run_type: string;
  provider_id: string;
  case_id: string;
  material_id: string;
  review_status: string;
  confidence_summary: string;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  redacted_preview_allowed: boolean;
  raw_content_blocked: boolean;
  created_at: string;
  updated_at: string;
  warnings: string[];
};

export type PersonalMaterialLiveReviewQueue = {
  items: PersonalMaterialLiveReviewItem[];
  item_count: number;
  pending_review_count: number;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
  fact_extraction_triggered: boolean;
  legal_analysis_triggered: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  warnings: string[];
};

export type PersonalMaterialLiveReviewActionRequest = {
  action: string;
  actor_id: string;
  explicit_review_confirmation: boolean;
  raw_content_handling_acknowledged: boolean;
  no_ai_prompt_injection_acknowledged: boolean;
};

export type PersonalMaterialLiveReviewActionResult = {
  review_item_id: string;
  action: string;
  actor_id: string;
  status: string;
  review_status: string;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
  fact_extraction_triggered: boolean;
  legal_analysis_triggered: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  blocked_reasons: string[];
  warnings: string[];
};

export type PersonalMaterialLiveSourceTrace = {
  source_trace_id: string;
  run_id: string;
  run_type: string;
  provider_id: string;
  case_id: string;
  material_id: string;
  source_type: string;
  page_count: number;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  created_at: string;
};

export type PersonalMaterialLiveSourceTraceList = {
  source_traces: PersonalMaterialLiveSourceTrace[];
  source_trace_count: number;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
  fact_extraction_triggered: boolean;
  legal_analysis_triggered: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  warnings: string[];
};

export type PersonalMaterialLiveAuditEvent = {
  event_id: string;
  provider_id: string;
  action: string;
  actor_id: string;
  run_id?: string | null;
  review_item_id?: string | null;
  live_call_requested: boolean;
  live_call_executed: boolean;
  blocked_reason?: string | null;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
  source_trace_created: boolean;
  review_required: boolean;
  page_count: number;
  created_at: string;
};

export type PersonalMaterialLiveAuditTimeline = {
  events: PersonalMaterialLiveAuditEvent[];
  event_count: number;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
  fact_extraction_triggered: boolean;
  legal_analysis_triggered: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  warnings: string[];
};

export type PersonalMaterialLiveSafetyStatus = {
  safety: Record<string, boolean>;
  all_safety_checks_passed: boolean;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  raw_ocr_text_exposed: boolean;
  ai_prompt_injected: boolean;
  fact_extraction_triggered: boolean;
  legal_analysis_triggered: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  warnings: string[];
};

export type PersonalIntelligenceStatus = {
  enabled: boolean;
  mode: string;
  version: string;
  mock_first_enabled: boolean;
  provider_gated: boolean;
  legal_search_runtime_enabled: boolean;
  enterprise_intelligence_runtime_enabled: boolean;
  source_trace_enabled: boolean;
  confirmation_queue_enabled: boolean;
  live_provider_call_enabled: boolean;
  requires_lawyer_confirmation: boolean;
  source_trace_required: boolean;
  raw_external_content_included: boolean;
  used_in_ai_prompt: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalIntelligenceProvider = {
  provider_id: string;
  label: string;
  display_name: string;
  category: string;
  provider_type: string;
  capabilities: string[];
  enabled: boolean;
  configured: boolean;
  live_enabled: boolean;
  mock_available: boolean;
  provider_gated: boolean;
  api_key_required_for_live: boolean;
  api_key_present: boolean;
  api_key_visible: boolean;
  live_call_executed: boolean;
  status: string;
  target_version: string;
  target_route: string;
  warnings: string[];
};

export type PersonalIntelligenceProviderList = {
  providers: PersonalIntelligenceProvider[];
  provider_count: number;
  configured_provider_count: number;
  live_provider_count: number;
  provider_secrets_visible: boolean;
  mock_metadata_only: boolean;
  raw_external_content_included: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalLegalSearchMockRequest = {
  case_id: string;
  query: string;
  search_scope: string;
  jurisdiction: string;
  legal_area: string;
  provider_id: string;
  explicit_mock_confirmation: boolean;
  explicit_no_live_call_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
};

export type PersonalEnterpriseQueryMockRequest = {
  case_id: string;
  company_name: string;
  unified_social_credit_code?: string | null;
  query_scope: string;
  provider_id: string;
  explicit_mock_confirmation: boolean;
  explicit_no_live_call_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
};

export type PersonalIntelligenceSourceTrace = {
  source_trace_id: string;
  source_type: string;
  provider_id: string;
  external_source_label: string;
  source_category: string;
  query_id: string;
  citation_status: string;
  lawyer_confirmed: boolean;
  mock_or_placeholder_only: boolean;
  raw_content_stored: boolean;
  raw_content_returned: boolean;
  live_call_executed: boolean;
  used_in_ai_prompt: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  created_at: string;
  updated_at?: string | null;
};

export type PersonalIntelligenceSourceTraceList = {
  source_traces: PersonalIntelligenceSourceTrace[];
  source_trace_count: number;
  pending_confirmation_count: number;
  mock_metadata_only: boolean;
  raw_external_content_included: boolean;
  used_in_ai_prompt: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalLegalSearchResult = {
  legal_search_id: string;
  case_id: string;
  provider_id: string;
  query_summary: string;
  search_scope: string;
  jurisdiction: string;
  legal_area: string;
  result_count: number;
  mock_results: Record<string, string | number | boolean>[];
  citation_candidates: Record<string, string | boolean>[];
  source_trace_ids: string[];
  requires_lawyer_confirmation: boolean;
  source_trace_required: boolean;
  live_call_executed: boolean;
  raw_external_content_included: boolean;
  used_in_ai_prompt: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  safety_flags: Record<string, boolean>;
  created_at: string;
  warnings: string[];
};

export type PersonalLegalSearchList = {
  legal_search: PersonalLegalSearchResult[];
  result_count: number;
  mock_metadata_only: boolean;
  raw_external_content_included: boolean;
  used_in_ai_prompt: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalEnterpriseQueryResult = {
  enterprise_query_id: string;
  case_id: string;
  provider_id: string;
  company_match_summary: string;
  risk_signal_summary: string;
  query_scope: string;
  mock_results: Record<string, string | number | boolean>[];
  source_trace_ids: string[];
  requires_lawyer_confirmation: boolean;
  source_trace_required: boolean;
  live_call_executed: boolean;
  raw_external_content_included: boolean;
  used_in_ai_prompt: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  safety_flags: Record<string, boolean>;
  created_at: string;
  warnings: string[];
};

export type PersonalEnterpriseQueryList = {
  enterprise_query: PersonalEnterpriseQueryResult[];
  result_count: number;
  mock_metadata_only: boolean;
  raw_external_content_included: boolean;
  used_in_ai_prompt: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalIntelligenceConfirmationActionRequest = {
  action: string;
  reviewer_id: string;
  reviewer_note?: string | null;
  explicit_lawyer_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
};

export type PersonalIntelligenceConfirmationActionResult = {
  source_trace_id: string;
  action: string;
  reviewer_id: string;
  status: string;
  citation_status: string;
  lawyer_confirmed: boolean;
  live_call_executed: boolean;
  raw_content_returned: boolean;
  used_in_ai_prompt: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalIntelligenceAuditEvent = {
  audit_id: string;
  action: string;
  actor: string;
  provider_id: string;
  query_id: string;
  source_trace_id?: string | null;
  timestamp: string;
  safety_flags: Record<string, boolean>;
  no_live_call: boolean;
  no_raw_external_content: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
};

export type PersonalIntelligenceAuditTimeline = {
  events: PersonalIntelligenceAuditEvent[];
  event_count: number;
  mock_metadata_only: boolean;
  raw_external_content_included: boolean;
  used_in_ai_prompt: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalIntelligenceSafetyStatus = {
  safety_checklist: string[];
  safety_flags: Record<string, boolean>;
  all_safety_checks_passed: boolean;
  mock_metadata_only: boolean;
  raw_external_content_included: boolean;
  used_in_ai_prompt: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  warnings: string[];
};

export type PersonalIntelligenceLiveProviderConfig = {
  provider_id: string;
  display_name: string;
  provider_type: string;
  live_supported: boolean;
  live_enabled: boolean;
  key_required: boolean;
  key_loaded: boolean;
  key_source: string;
  supported_query_types: string[];
  max_query_size: number;
  supports_case_search: boolean;
  supports_law_search: boolean;
  supports_company_profile: boolean;
  supports_company_risk: boolean;
  supports_citation_metadata: boolean;
  timeout_seconds: number;
  safety_notes: string[];
};

export type PersonalIntelligenceLiveProviderConfigList = {
  providers: PersonalIntelligenceLiveProviderConfig[];
  provider_count: number;
  live_provider_count: number;
  key_loaded_count: number;
  provider_secrets_visible: boolean;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  legal_raw_content_exposed: boolean;
  enterprise_raw_content_exposed: boolean;
  ai_prompt_injected: boolean;
  citation_finalized: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  warnings: string[];
};

export type PersonalIntelligenceLiveGatewayStatus = {
  enabled: boolean;
  mode: string;
  version: string;
  legal_live_mode_enabled: boolean;
  enterprise_live_mode_enabled: boolean;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  legal_dry_run_ready: boolean;
  enterprise_dry_run_ready: boolean;
  live_call_requires_confirmation: boolean;
  provider_gated: boolean;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  legal_raw_content_exposed: boolean;
  enterprise_raw_content_exposed: boolean;
  ai_prompt_injected: boolean;
  fact_extraction_triggered: boolean;
  legal_analysis_triggered: boolean;
  citation_finalized: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  warnings: string[];
};

export type PersonalIntelligenceLiveRunRequest = {
  provider_id: string;
  query_text: string;
  query_type: string;
  case_id: string;
  jurisdiction: string;
  actor_id: string;
  dry_run: boolean;
  explicit_live_confirmation: boolean;
  query_owner_confirmation: boolean;
  raw_content_handling_acknowledged: boolean;
  no_ai_prompt_injection_acknowledged: boolean;
  lawyer_review_acknowledged: boolean;
  draft_only_acknowledged: boolean;
  no_final_citation_acknowledged: boolean;
};

export type PersonalIntelligenceLiveMetadataPreview = {
  query_id: string;
  query_text_redacted: string;
  query_type: string;
  provider_id: string;
  provider_type: string;
  jurisdiction: string;
  result_count_estimate: number;
  citation_candidate_count: number;
  enterprise_candidate_count: number;
  confidence_summary: string;
  source_trace_ids: string[];
  review_required: boolean;
  raw_content_exposed: boolean;
  legal_raw_content_exposed: boolean;
  enterprise_raw_content_exposed: boolean;
  ai_prompt_injected: boolean;
  citation_finalized: boolean;
};

export type PersonalIntelligenceLiveRunRecord = {
  run_id: string;
  run_type: string;
  provider_id: string;
  provider_type: string;
  query_type: string;
  status: string;
  dry_run: boolean;
  would_call_provider: boolean;
  live_mode_enabled: boolean;
  live_call_requested: boolean;
  live_call_executed: boolean;
  blocked_reason?: string | null;
  blocked_reasons: string[];
  provider_adapter_unavailable: boolean;
  query_metadata_only: boolean;
  citation_metadata_only: boolean;
  metadata_preview: PersonalIntelligenceLiveMetadataPreview;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  legal_raw_content_exposed: boolean;
  enterprise_raw_content_exposed: boolean;
  ai_prompt_injected: boolean;
  fact_extraction_triggered: boolean;
  legal_analysis_triggered: boolean;
  citation_finalized: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  source_trace_created: boolean;
  review_required: boolean;
  created_at: string;
  warnings: string[];
};

export type PersonalIntelligenceLiveRunList = {
  runs: PersonalIntelligenceLiveRunRecord[];
  run_count: number;
  live_mode_enabled: boolean;
  live_call_executed: boolean;
  api_key_exposed: boolean;
  raw_content_exposed: boolean;
  legal_raw_content_exposed: boolean;
  enterprise_raw_content_exposed: boolean;
  ai_prompt_injected: boolean;
  fact_extraction_triggered: boolean;
  legal_analysis_triggered: boolean;
  citation_finalized: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  external_delivery_triggered: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  warnings: string[];
};

export type PersonalIntelligenceLiveReviewItem = Record<string, unknown> & { review_item_id: string; review_status: string };
export type PersonalIntelligenceLiveReviewQueue = Record<string, unknown> & { items: PersonalIntelligenceLiveReviewItem[]; item_count: number };
export type PersonalIntelligenceLiveReviewActionRequest = {
  action: string;
  actor_id: string;
  explicit_review_confirmation: boolean;
  raw_content_handling_acknowledged: boolean;
  no_ai_prompt_injection_acknowledged: boolean;
  no_final_citation_acknowledged: boolean;
};
export type PersonalIntelligenceLiveReviewActionResult = Record<string, unknown> & { review_item_id: string; status: string; review_status: string };
export type PersonalIntelligenceLiveSourceTrace = Record<string, unknown> & { source_trace_id: string };
export type PersonalIntelligenceLiveSourceTraceList = Record<string, unknown> & { source_traces: PersonalIntelligenceLiveSourceTrace[]; source_trace_count: number };
export type PersonalIntelligenceLiveAuditTimeline = Record<string, unknown> & { events: Array<Record<string, unknown>>; event_count: number };
export type PersonalIntelligenceLiveSafetyStatus = Record<string, unknown> & { safety: Record<string, boolean>; all_safety_checks_passed: boolean };

export type PersonalSkillStudioStatus = Record<string, unknown>;
export type SkillTrainingRuntimeStatus = Record<string, unknown> & { runtime_id: string; status: string };
export type SkillSampleRegistry = Record<string, unknown>;
export type PersonalSkillStudioRuntime = Record<string, unknown> & { runtime_id: string; display_name: string; runtime_type: string };
export type PersonalSkillStudioRuntimeList = Record<string, unknown> & { runtimes: PersonalSkillStudioRuntime[] };
export type ExperiencePackageMockRequest = {
  case_id: string;
  source_trace_ids: string[];
  review_result_ids?: string[];
  package_title: string;
  legal_area: string;
  case_cause: string;
  jurisdiction: string;
  explicit_mock_confirmation: boolean;
  explicit_source_trace_confirmation: boolean;
  explicit_no_raw_content_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
  explicit_no_auto_publish_confirmation: boolean;
};
export type SkillCandidateMockRequest = {
  experience_package_id: string;
  skill_title: string;
  skill_type: string;
  target_legal_area: string;
  target_case_cause: string;
  explicit_mock_confirmation: boolean;
  explicit_lawyer_review_confirmation: boolean;
  explicit_no_auto_publish_confirmation: boolean;
};
export type TestCaseMockRequest = {
  skill_candidate_id: string;
  test_case_title: string;
  scenario_type: string;
  explicit_mock_confirmation: boolean;
  explicit_no_raw_content_confirmation: boolean;
};
export type EvaluationMockRequest = {
  skill_candidate_id: string;
  test_case_ids: string[];
  evaluation_scope: string;
  explicit_mock_confirmation: boolean;
  explicit_manual_review_confirmation: boolean;
  explicit_no_auto_publish_confirmation: boolean;
};
export type PromotionActionRequest = {
  action: string;
  reviewer_id: string;
  reviewer_note?: string | null;
  explicit_manual_confirmation: boolean;
  explicit_no_auto_publish_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
};
export type ExperiencePackageDraft = Record<string, unknown> & { experience_package_id: string; package_title: string; source_trace_ids: string[] };
export type ExperiencePackageDraftList = Record<string, unknown> & { experience_packages: ExperiencePackageDraft[] };
export type SkillCandidateDraft = Record<string, unknown> & { skill_candidate_id: string; skill_title: string; candidate_status: string };
export type SkillCandidateDraftList = Record<string, unknown> & { skill_candidates: SkillCandidateDraft[] };
export type SkillTestCaseDraft = Record<string, unknown> & { test_case_id: string; test_case_title: string };
export type SkillTestCaseDraftList = Record<string, unknown> & { test_cases: SkillTestCaseDraft[] };
export type SkillEvaluationDraft = Record<string, unknown> & { evaluation_id: string; recommendation: string };
export type SkillEvaluationDraftList = Record<string, unknown> & { evaluations: SkillEvaluationDraft[] };
export type PromotionActionResult = Record<string, unknown> & { skill_candidate_id: string; action: string; candidate_status: string };
export type SkillStudioSourceTrace = Record<string, unknown> & { source_trace_id: string; source_type: string; source_label: string };
export type SkillStudioSourceTraceList = Record<string, unknown> & { source_traces: SkillStudioSourceTrace[] };
export type SkillStudioAuditTimeline = Record<string, unknown>;
export type SkillStudioSafetyStatus = Record<string, unknown> & { safety_checklist: string[] };
export type SkillStudioFinalDraftSafetyBase = {
  owner_only: boolean;
  downloadable_by_owner_only: boolean;
  baseline_discovered: boolean;
  baseline_complete: boolean;
  gate_reference_only: boolean;
  blocks_next_stage: boolean;
  quality_reference_only: boolean;
  final_skill_published: boolean;
  skill_auto_published: boolean;
  training_data_generated: boolean;
  writes_to_training_set: boolean;
  open_case_data_used: boolean;
  public_link_created: boolean;
  email_sent: boolean;
  external_delivery_triggered: boolean;
  api_key_exposed: boolean;
  source_trace_required: boolean;
  audit_required: boolean;
};
export type SkillStudioFinalDraft = SkillStudioFinalDraftSafetyBase & Record<string, unknown> & {
  skill_id: string;
  skill_name: string;
  skill_type: string;
  source_skill_id: string;
  source_package_id?: string | null;
  derived_from: string[];
  optimization_suggestions: string[];
  quality_score: number;
  gate_status: string;
  available_formats: string[];
  warnings: string[];
};
export type SkillStudioFinalDraftList = SkillStudioFinalDraftSafetyBase & {
  final_drafts: SkillStudioFinalDraft[];
  draft_count: number;
  warnings: string[];
};
export type SkillStudioBaselineDiscovery = SkillStudioFinalDraftSafetyBase & Record<string, unknown> & {
  source_skill_files: string[];
  source_package_files: string[];
  source_evaluation_files: string[];
  source_gate_files: string[];
  source_test_case_files: string[];
  source_prompt_template_files: string[];
  source_pattern_files: string[];
  missing_baseline_items: string[];
  derived_from: string[];
};
export type SkillStudioFinalQuality = SkillStudioFinalDraftSafetyBase & Record<string, unknown> & { skill_id: string; quality_score: number; score_status: string; suggested_next_optimization: string[] };
export type SkillStudioFinalGate = SkillStudioFinalDraftSafetyBase & Record<string, unknown> & { skill_id: string; gate_status: string; missing_gate_files: string[] };
export type SkillStudioFinalOptimization = SkillStudioFinalDraftSafetyBase & Record<string, unknown> & { skill_id: string; optimization_suggestions: string[] };
export type SkillStudioFinalOwnerDownloadRequest = {
  requested_format: string;
  explicit_owner_confirmation: boolean;
  explicit_no_public_link_confirmation: boolean;
  explicit_no_email_confirmation: boolean;
  explicit_no_external_delivery_confirmation: boolean;
  explicit_no_auto_publish_confirmation: boolean;
};
export type SkillStudioFinalOwnerDownload = SkillStudioFinalDraftSafetyBase & Record<string, unknown> & { download_id: string; skill_id: string; requested_format: string; download_status: string; warnings: string[] };
export type SkillStudioFinalOwnerDownloadList = SkillStudioFinalDraftSafetyBase & { owner_downloads: SkillStudioFinalOwnerDownload[]; download_count: number; warnings: string[] };

export type PersonalCaseProductionStatus = Record<string, unknown>;
export type WorkflowStage = Record<string, unknown> & { stage_id: string; display_name: string; stage_type: string };
export type WorkflowStageList = Record<string, unknown> & { workflow_stages: WorkflowStage[] };
export type ProductionCaseMockRequest = {
  case_id: string;
  production_title: string;
  case_type: string;
  client_alias: string;
  jurisdiction: string;
  legal_area: string;
  desensitization_status: string;
  explicit_mock_confirmation: boolean;
  explicit_no_raw_content_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
  explicit_no_external_delivery_confirmation: boolean;
};
export type WorkflowRunMockRequest = {
  production_case_id: string;
  workflow_scope: string;
  selected_stage_ids: string[];
  explicit_mock_confirmation: boolean;
  explicit_lawyer_review_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
  explicit_no_external_delivery_confirmation: boolean;
};
export type StageRunMockRequest = {
  workflow_run_id: string;
  stage_id: string;
  linked_runtime_object_ids?: string[];
  stage_note?: string | null;
  explicit_mock_confirmation: boolean;
  explicit_no_live_provider_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
};
export type ReviewGateActionRequest = {
  action: string;
  reviewer_id: string;
  reviewer_note?: string | null;
  explicit_lawyer_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
  explicit_no_external_delivery_confirmation: boolean;
};
export type ProductionCaseRecord = Record<string, unknown> & { production_case_id: string; production_title: string; production_status: string };
export type ProductionCaseList = Record<string, unknown> & { production_cases: ProductionCaseRecord[] };
export type WorkflowRunRecord = Record<string, unknown> & { workflow_run_id: string; selected_stage_ids: string[] };
export type WorkflowRunList = Record<string, unknown> & { workflow_runs: WorkflowRunRecord[] };
export type StageRunRecord = Record<string, unknown> & { stage_run_id: string; stage_id: string };
export type StageRunList = Record<string, unknown> & { stage_runs: StageRunRecord[] };
export type ProductionReadiness = Record<string, unknown> & { production_case_id: string; readiness_status: string };
export type ProductionReadinessList = Record<string, unknown> & { readiness: ProductionReadiness[] };
export type ReviewGateActionResult = Record<string, unknown> & { production_case_id: string; action: string; production_status: string };
export type CaseProductionSourceTrace = Record<string, unknown> & { source_trace_id: string; source_type: string; source_label: string };
export type CaseProductionSourceTraceList = Record<string, unknown> & { source_traces: CaseProductionSourceTrace[] };
export type CaseProductionAuditTimeline = Record<string, unknown>;
export type CaseProductionSafetyStatus = Record<string, unknown> & { safety_checklist: string[] };

export type PersonalDeliveryPacketStatus = Record<string, unknown>;
export type DeliveryPacketRuntime = Record<string, unknown> & { runtime_id: string; display_name: string; runtime_type: string };
export type DeliveryPacketRuntimeList = Record<string, unknown> & { runtimes: DeliveryPacketRuntime[] };
export type DeliveryPacketMockRequest = {
  production_case_id: string;
  workflow_run_id?: string | null;
  packet_title: string;
  packet_scope: string;
  client_alias: string;
  delivery_purpose: string;
  explicit_mock_confirmation: boolean;
  explicit_lawyer_review_confirmation: boolean;
  explicit_no_raw_content_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
  explicit_no_external_delivery_confirmation: boolean;
};
export type DeliveryPacketRecord = Record<string, unknown> & { delivery_packet_id: string; packet_title: string; packet_status: string };
export type DeliveryPacketList = Record<string, unknown> & { delivery_packets: DeliveryPacketRecord[] };
export type PacketItemMockRequest = {
  delivery_packet_id: string;
  item_title: string;
  item_type: string;
  linked_object_type: string;
  linked_object_id: string;
  source_trace_ids: string[];
  explicit_mock_confirmation: boolean;
  explicit_no_raw_content_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
};
export type PacketItemRecord = Record<string, unknown> & { packet_item_id: string; delivery_packet_id: string; item_type: string };
export type PacketItemList = Record<string, unknown> & { packet_items: PacketItemRecord[] };
export type SourceBundleMockRequest = {
  delivery_packet_id: string;
  source_trace_ids: string[];
  bundle_scope: string;
  explicit_mock_confirmation: boolean;
  explicit_source_trace_confirmation: boolean;
  explicit_no_raw_content_confirmation: boolean;
};
export type SourceBundleRecord = Record<string, unknown> & { source_bundle_id: string; delivery_packet_id: string; source_trace_ids: string[] };
export type SourceBundleList = Record<string, unknown> & { source_bundles: SourceBundleRecord[] };
export type ExportReadiness = Record<string, unknown> & { delivery_packet_id: string; export_readiness_status: string };
export type ExportReadinessList = Record<string, unknown> & { readiness: ExportReadiness[] };
export type FinalLockActionRequest = {
  action: string;
  reviewer_id: string;
  reviewer_note?: string | null;
  explicit_lawyer_confirmation: boolean;
  explicit_final_lock_confirmation: boolean;
  explicit_no_real_export_confirmation: boolean;
  explicit_no_email_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
  explicit_no_final_report_confirmation: boolean;
  explicit_no_external_delivery_confirmation: boolean;
};
export type FinalLockRecord = Record<string, unknown> & { final_lock_id: string; delivery_packet_id: string; action: string };
export type FinalLockList = Record<string, unknown> & { final_locks: FinalLockRecord[] };
export type ReviewSummary = Record<string, unknown> & { delivery_packet_id: string; lawyer_review_status: string };
export type ReviewSummaryList = Record<string, unknown> & { review_summaries: ReviewSummary[] };
export type DeliveryPacketAuditTimeline = Record<string, unknown>;
export type DeliveryPacketSafetyStatus = Record<string, unknown> & { safety_checklist: string[] };

export type PersonalShowcasePackStatus = Record<string, unknown>;
export type ShowcaseRuntime = Record<string, unknown> & { runtime_id: string; display_name: string; runtime_type: string };
export type ShowcaseRuntimeList = Record<string, unknown> & { runtimes: ShowcaseRuntime[] };
export type PilotSampleMockRequest = {
  sample_title: string;
  sample_type: string;
  legal_area: string;
  case_cause: string;
  risk_level: string;
  demo_persona: string;
  linked_runtime_ids?: string[];
  explicit_mock_confirmation: boolean;
  explicit_no_real_case_confirmation: boolean;
  explicit_no_raw_content_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
  explicit_no_external_delivery_confirmation: boolean;
};
export type PilotSampleRecord = Record<string, unknown> & { pilot_sample_id: string; sample_title: string; sample_type: string };
export type PilotSampleList = Record<string, unknown> & { pilot_samples: PilotSampleRecord[] };
export type StoryFlowMockRequest = {
  pilot_sample_id: string;
  story_title: string;
  story_scope: string;
  selected_stage_ids: string[];
  explicit_mock_confirmation: boolean;
  explicit_no_real_case_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
  explicit_no_external_delivery_confirmation: boolean;
};
export type StoryStageCard = Record<string, unknown> & { stage_id: string; display_name: string; linked_runtime: string };
export type StoryFlowRecord = Record<string, unknown> & { story_flow_id: string; pilot_sample_id: string; story_title: string; stage_cards: StoryStageCard[] };
export type StoryFlowList = Record<string, unknown> & { story_flows: StoryFlowRecord[] };
export type ShowcaseMetrics = Record<string, unknown> & { pilot_sample_count: number; story_flow_count: number };
export type TrustPanel = Record<string, unknown> & { trust_items: string[]; flags: Record<string, boolean> };
export type ShowcaseAuditTimeline = Record<string, unknown>;
export type ShowcaseSafetyStatus = Record<string, unknown> & { safety_checklist: string[] };

export type CaseAnalysisSafetyBase = {
  owner_only: boolean;
  legal_analysis_draft_only: boolean;
  draft_only: boolean;
  metadata_only: boolean;
  open_case_runtime: boolean;
  closed_case_training: boolean;
  training_data_generated: boolean;
  writes_to_training_set: boolean;
  skill_updated: boolean;
  skill_published: boolean;
  final_skill_published: boolean;
  future_training_candidate: boolean;
  requires_manual_training_selection: boolean;
  source_trace_required: boolean;
  audit_required: boolean;
  lawyer_review_required: boolean;
  gate_reference_only: boolean;
  blocks_next_stage: boolean;
  raw_content_included: boolean;
  raw_ocr_text_included: boolean;
  raw_content_written_to_git: boolean;
  raw_content_written_to_docs: boolean;
  raw_content_written_to_diagnostics: boolean;
  raw_content_written_to_regression_output: boolean;
  ai_prompt_injected: boolean;
  controlled_prompt_only: boolean;
  live_call_executed: boolean;
  api_key_accessed: boolean;
  api_key_exposed: boolean;
  final_fact_finding: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  public_link_created: boolean;
  third_party_share_enabled: boolean;
  client_auto_delivery: boolean;
  external_delivery_triggered: boolean;
  email_sent: boolean;
  real_pdf_docx_generated: boolean;
};

export type PersonalCaseAnalysisStatus = CaseAnalysisSafetyBase & {
  enabled: boolean;
  mode: string;
  version: string;
  runtime_label: string;
  fact_analysis_enabled: boolean;
  legal_analysis_enabled: boolean;
  review_readiness_enabled: boolean;
  training_runtime_separated: boolean;
  open_case_analysis_only: boolean;
  warnings: string[];
};

export type CaseAnalysisRuntime = CaseAnalysisSafetyBase & {
  runtime_id: string;
  display_name: string;
  runtime_type: string;
  stage: string;
  enabled: boolean;
  live_enabled: boolean;
  skill_required: boolean;
  target_route: string;
  warnings: string[];
};

export type CaseAnalysisRuntimeList = CaseAnalysisSafetyBase & {
  runtimes: CaseAnalysisRuntime[];
  runtime_count: number;
  live_runtime_count: number;
  warnings: string[];
};

export type SkillBaselineMetadata = CaseAnalysisSafetyBase & {
  skill_key: string;
  skill_title_cn: string;
  expected_skill_id: string;
  source_skill_id: string;
  source_package_id?: string | null;
  source_candidate_id?: string | null;
  source_evaluation_files: string[];
  source_gate_files: string[];
  source_test_case_ids: string[];
  derived_from: string[];
  baseline_detected: boolean;
  prompt_template_detected: boolean;
  evaluation_detected: boolean;
  gate_detected: boolean;
  missing_baseline_report: string[];
  warnings: string[];
};

export type SkillBaselineReport = CaseAnalysisSafetyBase & {
  baselines: SkillBaselineMetadata[];
  baseline_count: number;
  detected_count: number;
  missing_baseline_report: string[];
  warnings: string[];
};

export type CaseAnalysisRunMockRequest = {
  case_id: string;
  case_alias: string;
  analysis_scope: string;
  material_metadata_ids: string[];
  source_trace_ids: string[];
  selected_skill_ids: string[];
  explicit_mock_confirmation: boolean;
  explicit_open_case_confirmation: boolean;
  explicit_no_training_data_confirmation: boolean;
  explicit_no_raw_content_confirmation: boolean;
  explicit_lawyer_review_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
};

export type FactDraftMockRequest = {
  case_id: string;
  run_id?: string | null;
  source_trace_ids: string[];
  material_metadata_ids: string[];
  case_fact_extraction_skill_id: string;
  explicit_mock_confirmation: boolean;
  explicit_no_training_data_confirmation: boolean;
  explicit_no_raw_content_confirmation: boolean;
  explicit_lawyer_review_confirmation: boolean;
};

export type LegalDraftMockRequest = {
  case_id: string;
  fact_draft_id?: string | null;
  source_trace_ids: string[];
  legal_search_metadata_ids: string[];
  enterprise_metadata_ids: string[];
  case_legal_analysis_skill_id: string;
  explicit_mock_confirmation: boolean;
  explicit_no_training_data_confirmation: boolean;
  explicit_no_raw_content_confirmation: boolean;
  explicit_lawyer_review_confirmation: boolean;
  explicit_no_final_opinion_confirmation: boolean;
};

export type CaseAnalysisRunRecord = CaseAnalysisSafetyBase & Record<string, unknown> & {
  run_id: string;
  case_id: string;
  case_alias: string;
  analysis_scope: string;
  run_status: string;
  fact_draft_id?: string | null;
  legal_draft_id?: string | null;
  source_trace_ids: string[];
  created_at: string;
  warnings: string[];
};

export type CaseAnalysisRunList = CaseAnalysisSafetyBase & { runs: CaseAnalysisRunRecord[]; run_count: number; warnings: string[] };
export type FactAnalysisDraft = CaseAnalysisSafetyBase & Record<string, unknown> & { fact_draft_id: string; case_id: string; source_trace_ids: string[]; created_at: string; warnings: string[] };
export type FactAnalysisDraftList = CaseAnalysisSafetyBase & { fact_drafts: FactAnalysisDraft[]; draft_count: number; warnings: string[] };
export type LegalAnalysisDraft = CaseAnalysisSafetyBase & Record<string, unknown> & {
  legal_draft_id: string;
  fact_draft_id?: string | null;
  fact_preview_id?: string | null;
  case_id: string;
  legal_analysis_summary_draft: string;
  legal_relationship_draft: string;
  legal_reasoning_draft: string[];
  dispute_focus_draft: string[];
  issue_spotting_draft: string[];
  claim_basis_draft: string[];
  defense_path_draft: string[];
  burden_of_proof_draft: string[];
  risk_flags_draft: string[];
  next_action_checklist_draft: string[];
  version_status: string;
  owner_confirmed: boolean;
  review_ready: boolean;
  owner_download_ready: boolean;
  source_trace_ids: string[];
  created_at: string;
  updated_at?: string | null;
  warnings: string[];
};
export type LegalAnalysisDraftList = CaseAnalysisSafetyBase & { legal_drafts: LegalAnalysisDraft[]; draft_count: number; warnings: string[] };
export type LegalDraftVersionRecord = CaseAnalysisSafetyBase & Record<string, unknown> & { version_id: string; legal_draft_id: string; version_number: number; version_type: string; created_from: string; change_summary: string; owner_confirmed: boolean; review_ready: boolean; created_at: string; warnings: string[] };
export type LegalDraftVersionList = CaseAnalysisSafetyBase & { legal_draft_id: string; versions: LegalDraftVersionRecord[]; version_count: number; warnings: string[] };
export type LegalDraftQualityReport = CaseAnalysisSafetyBase & { legal_draft_id: string; overall_score: number; dimension_scores: Record<string, number>; optimization_suggestions: string[]; warnings: string[] };
export type LegalDraftGateReport = CaseAnalysisSafetyBase & { gate_id: string; legal_draft_id: string; gate_status: string; gate_score: number; optimization_required: boolean; low_confidence_flags: string[]; missing_information_checklist: string[]; review_ready: boolean; warnings: string[] };
export type LegalDraftReviewConfirmation = CaseAnalysisSafetyBase & { legal_draft_id: string; review_item_id: string; review_status: string; owner_confirmed: boolean; review_ready: boolean; warnings: string[] };
export type CaseAnalysisEvaluation = CaseAnalysisSafetyBase & Record<string, unknown> & { evaluation_id: string; created_at: string; warnings: string[] };
export type CaseAnalysisEvaluationList = CaseAnalysisSafetyBase & { evaluations: CaseAnalysisEvaluation[]; evaluation_count: number; warnings: string[] };
export type CaseAnalysisGate = CaseAnalysisSafetyBase & Record<string, unknown> & { gate_id: string; created_at: string; warnings: string[] };
export type CaseAnalysisGateList = CaseAnalysisSafetyBase & { gates: CaseAnalysisGate[]; gate_count: number; warnings: string[] };
export type CaseAnalysisReviewItem = CaseAnalysisSafetyBase & Record<string, unknown> & { review_item_id: string; linked_object_type: string; linked_object_id: string; case_id: string; review_status: string; created_at: string; warnings: string[] };
export type CaseAnalysisReviewQueue = CaseAnalysisSafetyBase & { review_items: CaseAnalysisReviewItem[]; item_count: number; pending_count: number; warnings: string[] };
export type CaseAnalysisReviewActionRequest = { action: string; reviewer_id: string; reviewer_note?: string | null; explicit_lawyer_confirmation: boolean; explicit_no_training_data_confirmation: boolean; explicit_no_final_opinion_confirmation: boolean };
export type CaseAnalysisReviewActionResult = CaseAnalysisSafetyBase & { review_item_id: string; action: string; reviewer_id: string; review_status: string; warnings: string[] };
export type CaseAnalysisSourceTrace = CaseAnalysisSafetyBase & Record<string, unknown> & { source_trace_id: string; source_type: string; source_label: string; linked_object_type: string; linked_object_id: string; created_at: string };
export type CaseAnalysisSourceTraceList = CaseAnalysisSafetyBase & { source_traces: CaseAnalysisSourceTrace[]; source_trace_count: number; warnings: string[] };
export type CaseAnalysisAuditTimeline = CaseAnalysisSafetyBase & Record<string, unknown> & { events: Record<string, unknown>[]; event_count: number; warnings: string[] };
export type CaseAnalysisSafetyStatus = CaseAnalysisSafetyBase & { safety_checklist: string[]; safety_flags: Record<string, boolean>; all_safety_checks_passed: boolean; warnings: string[] };

export type PilotSafetyBase = {
  owner_only: boolean;
  owner_access_required: boolean;
  downloadable_by_owner_only: boolean;
  metadata_only: boolean;
  draft_only: boolean;
  dry_run_default: boolean;
  internal_case_analysis: boolean;
  draft_output_allowed: boolean;
  pdf_docx_generation_allowed_for_owner: boolean;
  public_link_created: boolean;
  email_sent: boolean;
  external_delivery_triggered: boolean;
  third_party_share_enabled: boolean;
  client_auto_delivery: boolean;
  final_legal_opinion_auto_generated: boolean;
  final_report_auto_generated: boolean;
  training_data_generated: boolean;
  writes_to_training_set: boolean;
  skill_updated: boolean;
  skill_published: boolean;
  source_trace_required: boolean;
  lawyer_review_required: boolean;
  final_lock_required: boolean;
  provider_gated: boolean;
  api_key_exposed: boolean;
  raw_content_written_to_git: boolean;
  raw_content_written_to_docs: boolean;
  raw_content_written_to_diagnostics: boolean;
  raw_content_written_to_regression_output: boolean;
  local_path_visible: boolean;
  raw_content_returned: boolean;
  real_pdf_docx_generated: boolean;
};

export type PilotStatus = PilotSafetyBase & Record<string, unknown> & { enabled: boolean; mode: string; version: string; runtime_label: string; warnings: string[] };
export type PilotRuntime = PilotSafetyBase & Record<string, unknown> & { runtime_id: string; display_name: string; category: string; target_route: string; connected: boolean; live_enabled: boolean; dry_run_ready: boolean; status: string; warnings: string[] };
export type PilotRuntimeList = PilotSafetyBase & { runtimes: PilotRuntime[]; runtime_count: number; connected_count: number; live_enabled_count: number; warnings: string[] };
export type PilotWorkflowStep = PilotSafetyBase & Record<string, unknown> & { step_id: string; display_name: string; target_runtime_id: string; stage: string; status: string; warnings: string[] };
export type PilotWorkflow = PilotSafetyBase & { steps: PilotWorkflowStep[]; step_count: number; warnings: string[] };
export type ProviderGate = PilotSafetyBase & Record<string, unknown> & { provider_id: string; display_name: string; category: string; live_enabled: boolean; dry_run_ready: boolean; warnings: string[] };
export type ProviderGateSummary = PilotSafetyBase & { provider_gates: ProviderGate[]; provider_count: number; live_enabled_count: number; dry_run_ready_count: number; warnings: string[] };
export type PilotReadiness = PilotSafetyBase & { pilot_ready: boolean; readiness: Record<string, boolean>; missing_requirements: string[]; next_action: string; warnings: string[] };
export type PilotRunMockRequest = { case_id: string; case_alias: string; workflow_scope: string; selected_runtime_ids: string[]; explicit_owner_confirmation: boolean; explicit_provider_gated_confirmation: boolean; explicit_no_external_delivery_confirmation: boolean; explicit_no_training_data_confirmation: boolean; explicit_no_final_opinion_confirmation: boolean };
export type PilotRunRecord = PilotSafetyBase & Record<string, unknown> & { run_id: string; case_id: string; case_alias: string; workflow_scope: string; selected_runtime_ids: string[]; run_status: string; output_ids: string[]; download_ids: string[]; source_trace_ids: string[]; created_at: string; warnings: string[] };
export type PilotRunList = PilotSafetyBase & { runs: PilotRunRecord[]; run_count: number; warnings: string[] };
export type SkillFinalDraft = PilotSafetyBase & Record<string, unknown> & { draft_id: string; skill_key: string; title: string; source_skill_id: string; available_formats: string[]; owner_download_ready: boolean; publish_action_available: boolean; warnings: string[] };
export type SkillFinalDraftList = PilotSafetyBase & { skill_final_drafts: SkillFinalDraft[]; draft_count: number; warnings: string[] };
export type PilotOutputMockRequest = { run_id?: string | null; output_type: string; title: string; format: string; explicit_owner_confirmation: boolean; explicit_no_external_delivery_confirmation: boolean; explicit_no_final_opinion_confirmation: boolean };
export type PilotOutputRecord = PilotSafetyBase & Record<string, unknown> & { output_id: string; run_id?: string | null; output_type: string; title: string; format: string; output_status: string; created_at: string; warnings: string[] };
export type PilotOutputList = PilotSafetyBase & { outputs: PilotOutputRecord[]; output_count: number; warnings: string[] };
export type OwnerDownloadMockRequest = { requested_format: string; explicit_owner_confirmation: boolean; explicit_no_public_link_confirmation: boolean; explicit_no_email_confirmation: boolean; explicit_no_external_delivery_confirmation: boolean };
export type OwnerDownloadRecord = PilotSafetyBase & Record<string, unknown> & { download_id: string; output_id: string; requested_format: string; download_status: string; file_generated: boolean; file_path_visible: boolean; created_at: string; warnings: string[] };
export type OwnerDownloadList = PilotSafetyBase & { owner_downloads: OwnerDownloadRecord[]; download_count: number; warnings: string[] };
export type PilotReviewQueue = PilotSafetyBase & Record<string, unknown> & { review_items: Record<string, unknown>[]; item_count: number; pending_count: number; warnings: string[] };
export type PilotReviewActionRequest = { action: string; reviewer_id: string; reviewer_note?: string | null; explicit_lawyer_confirmation: boolean; explicit_no_external_delivery_confirmation: boolean; explicit_no_final_opinion_confirmation: boolean };
export type PilotReviewActionResult = PilotSafetyBase & { review_item_id: string; action: string; reviewer_id: string; review_status: string; warnings: string[] };
export type PilotSourceTraceList = PilotSafetyBase & Record<string, unknown> & { source_traces: Record<string, unknown>[]; source_trace_count: number; warnings: string[] };
export type PilotAuditTimeline = PilotSafetyBase & Record<string, unknown> & { events: Record<string, unknown>[]; event_count: number; warnings: string[] };
export type ExportBoundary = PilotSafetyBase & Record<string, unknown> & { export_boundary_id: string; owner_download_enabled: boolean; public_share_disabled: boolean; email_disabled: boolean; external_delivery_disabled: boolean; final_labeling_disabled: boolean; warnings: string[] };
export type PilotSafetyStatus = PilotSafetyBase & { safety_checklist: string[]; safety_flags: Record<string, boolean>; all_safety_checks_passed: boolean; warnings: string[] };

export type CaseWorkspaceSafetyBase = {
  owner_only: boolean;
  owner_access_required: boolean;
  downloadable_by_owner_only: boolean;
  metadata_only: boolean;
  draft_only: boolean;
  provider_gated: boolean;
  dry_run_default: boolean;
  preview_only: boolean;
  correction_allowed: boolean;
  owner_correction_allowed: boolean;
  legal_analysis_input_allowed: boolean;
  legal_analysis_auto_triggered: boolean;
  export_allowed: boolean;
  public_link_created: boolean;
  email_sent: boolean;
  external_delivery_triggered: boolean;
  third_party_share_enabled: boolean;
  client_auto_delivery: boolean;
  training_data_generated: boolean;
  writes_to_training_set: boolean;
  skill_updated: boolean;
  skill_published: boolean;
  gate_reference_only: boolean;
  blocks_next_stage: boolean;
  final_fact_finding: boolean;
  raw_content_written_to_git: boolean;
  raw_content_written_to_docs: boolean;
  raw_content_written_to_diagnostics: boolean;
  raw_content_written_to_regression_output: boolean;
  source_trace_required: boolean;
  audit_required: boolean;
  lawyer_review_required: boolean;
  final_legal_opinion_generated: boolean;
  final_report_generated: boolean;
  real_pdf_docx_generated: boolean;
  raw_content_returned: boolean;
  local_path_visible: boolean;
  api_key_exposed: boolean;
};

export type CaseWorkspaceStatus = CaseWorkspaceSafetyBase & Record<string, unknown> & { enabled: boolean; mode: string; version: string; runtime_label: string; warnings: string[] };
export type CaseWorkspaceCase = CaseWorkspaceSafetyBase & Record<string, unknown> & { case_id: string; case_alias: string; material_count: number; source_trace_count: number; warnings: string[] };
export type CaseWorkspaceMaterial = CaseWorkspaceSafetyBase & Record<string, unknown> & { material_id: string; case_id: string; material_title: string; material_type: string; source_trace_ids: string[]; warnings: string[] };
export type CaseWorkspaceSourceTraceList = CaseWorkspaceSafetyBase & Record<string, unknown> & { source_traces: Record<string, unknown>[]; source_trace_count: number; confirmed_count: number; warnings: string[] };
export type FactPreviewRecord = CaseWorkspaceSafetyBase & Record<string, unknown> & {
  fact_preview_id: string;
  case_id: string;
  material_ids: string[];
  ocr_job_ids: string[];
  source_trace_ids: string[];
  fact_summary_draft: string;
  evidence_mapping_draft: string;
  timeline_draft: string;
  disputed_facts_draft: string;
  missing_facts_draft: string;
  confidence_metadata: Record<string, number | string>;
  preview_status: string;
  correction_status: string;
  legal_analysis_input_ready: boolean;
  owner_confirmed: boolean;
  created_at: string;
  updated_at?: string | null;
  warnings: string[];
};
export type FactPreviewList = CaseWorkspaceSafetyBase & { fact_previews: FactPreviewRecord[]; fact_preview_count: number; warnings: string[] };
export type FactCorrectionRecord = CaseWorkspaceSafetyBase & Record<string, unknown> & {
  correction_id: string;
  fact_preview_id: string;
  corrected_sections: string[];
  correction_reason: string;
  correction_type: string;
  corrected_by_owner: boolean;
  correction_status: string;
  created_at: string;
  updated_at: string;
  warnings: string[];
};
export type FactCorrectionList = CaseWorkspaceSafetyBase & { fact_preview_id: string; corrections: FactCorrectionRecord[]; correction_count: number; warnings: string[] };
export type FactVersionRecord = CaseWorkspaceSafetyBase & Record<string, unknown> & {
  version_id: string;
  fact_preview_id: string;
  version_number: number;
  version_type: string;
  created_from: string;
  change_summary: string;
  owner_confirmed: boolean;
  legal_analysis_input_ready: boolean;
  created_at: string;
  warnings: string[];
};
export type FactVersionList = CaseWorkspaceSafetyBase & { fact_preview_id: string; versions: FactVersionRecord[]; version_count: number; warnings: string[] };
export type FactQualityReport = CaseWorkspaceSafetyBase & {
  fact_preview_id: string;
  overall_score: number;
  dimension_scores: Record<string, number>;
  gate_status: string;
  optimization_suggestions: string[];
  warnings: string[];
};
export type FactGateReport = CaseWorkspaceSafetyBase & {
  gate_id: string;
  fact_preview_id: string;
  gate_status: string;
  gate_score: number;
  optimization_required: boolean;
  optimization_suggestions: string[];
  warnings: string[];
};
export type LegalAnalysisInputReadiness = CaseWorkspaceSafetyBase & {
  readiness_id: string;
  fact_preview_id: string;
  legal_analysis_input_ready: boolean;
  owner_confirmed: boolean;
  source_trace_ready: boolean;
  missing_fact_flags: string[];
  low_confidence_flags: string[];
  warnings: string[];
};
export type LegalAnalysisInputReadinessList = CaseWorkspaceSafetyBase & { readiness_items: LegalAnalysisInputReadiness[]; readiness_count: number; warnings: string[] };
export type PilotDashboardStatus = PilotSafetyBase & Record<string, unknown> & { dashboard_ready: boolean; workflow_overview_ready: boolean; quality_score_panels_ready: boolean; warnings: string[] };
export type PilotDashboardMetrics = PilotSafetyBase & Record<string, unknown> & { runtime_readiness: Record<string, string>; workflow_status: Record<string, unknown>[]; review_queue: Record<string, number>; source_trace_summary: Record<string, unknown>; export_boundary: Record<string, unknown>; warnings: string[] };
export type PilotDashboardQuality = PilotSafetyBase & Record<string, unknown> & { quality_items: Array<PilotSafetyBase & Record<string, unknown>>; item_count: number; average_quality_score: number; quality_gate_status: string; warnings: string[] };

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
