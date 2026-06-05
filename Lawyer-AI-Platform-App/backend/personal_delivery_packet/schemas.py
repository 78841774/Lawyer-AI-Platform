from pydantic import BaseModel, Field


class PersonalDeliveryPacketStatus(BaseModel):
    enabled: bool = True
    mode: str = "personal_delivery_packet"
    version: str = "v7.6"
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    delivery_packet_runtime_enabled: bool = True
    packet_item_runtime_enabled: bool = True
    source_bundle_runtime_enabled: bool = True
    export_readiness_engine_enabled: bool = True
    final_lock_engine_enabled: bool = True
    review_summary_enabled: bool = True
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    final_lock_required: bool = True
    raw_content_included: bool = False
    raw_case_content_read: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class DeliveryPacketRuntime(BaseModel):
    runtime_id: str
    display_name: str
    runtime_type: str
    capabilities: list[str] = Field(default_factory=list)
    enabled: bool = True
    live_enabled: bool = False
    mock_available: bool = True
    manual_review_required: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    final_lock_required: bool = True
    auto_delivery_enabled: bool = False
    warning: str = "当前仅生成交付包草案和导出 metadata，不会自动生成最终法律意见或对外交付。"


class DeliveryPacketRuntimeList(BaseModel):
    runtimes: list[DeliveryPacketRuntime] = Field(default_factory=list)
    runtime_count: int = 0
    live_runtime_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    raw_case_content_read: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class DeliveryPacketMockRequest(BaseModel):
    production_case_id: str
    workflow_run_id: str | None = None
    packet_title: str
    packet_scope: str
    client_alias: str
    delivery_purpose: str
    explicit_mock_confirmation: bool = False
    explicit_lawyer_review_confirmation: bool = False
    explicit_no_raw_content_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False


class DeliveryPacketRecord(BaseModel):
    delivery_packet_id: str
    production_case_id: str
    workflow_run_id: str | None = None
    packet_title: str
    packet_scope: str
    client_alias: str
    delivery_purpose: str
    packet_status: str = "draft"
    mock_or_placeholder_only: bool = True
    raw_content_included: bool = False
    raw_case_content_read: bool = False
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    final_lock_required: bool = True
    export_ready: bool = False
    final_locked: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    created_at: str
    updated_at: str | None = None
    warnings: list[str] = Field(default_factory=list)


class DeliveryPacketList(BaseModel):
    delivery_packets: list[DeliveryPacketRecord] = Field(default_factory=list)
    packet_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    raw_case_content_read: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PacketItemMockRequest(BaseModel):
    delivery_packet_id: str
    item_title: str
    item_type: str
    linked_object_type: str
    linked_object_id: str
    source_trace_ids: list[str] = Field(default_factory=list)
    explicit_mock_confirmation: bool = False
    explicit_no_raw_content_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False


class PacketItemRecord(BaseModel):
    packet_item_id: str
    delivery_packet_id: str
    item_title: str
    item_type: str
    linked_object_type: str
    linked_object_id: str
    source_trace_ids: list[str] = Field(default_factory=list)
    item_status: str = "draft"
    raw_content_included: bool = False
    mock_or_placeholder_only: bool = True
    requires_lawyer_review: bool = True
    final_lock_required: bool = True
    source_trace_required: bool = True
    included_in_export: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class PacketItemList(BaseModel):
    packet_items: list[PacketItemRecord] = Field(default_factory=list)
    item_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    raw_case_content_read: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class SourceBundleMockRequest(BaseModel):
    delivery_packet_id: str
    source_trace_ids: list[str] = Field(default_factory=list)
    bundle_scope: str
    explicit_mock_confirmation: bool = False
    explicit_source_trace_confirmation: bool = False
    explicit_no_raw_content_confirmation: bool = False


class SourceBundleRecord(BaseModel):
    source_bundle_id: str
    delivery_packet_id: str
    source_trace_ids: list[str] = Field(default_factory=list)
    bundle_scope: str
    bundle_status: str = "draft"
    source_trace_count: int = 0
    confirmed_source_count: int = 0
    unconfirmed_source_count: int = 0
    raw_content_included: bool = False
    raw_content_returned: bool = False
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    final_lock_required: bool = True
    mock_or_placeholder_only: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class SourceBundleList(BaseModel):
    source_bundles: list[SourceBundleRecord] = Field(default_factory=list)
    bundle_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    raw_case_content_read: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class ExportReadiness(BaseModel):
    delivery_packet_id: str
    export_readiness_status: str
    required_item_count: int = 8
    included_item_count: int = 0
    missing_item_types: list[str] = Field(default_factory=list)
    source_trace_complete: bool = False
    lawyer_review_complete: bool = False
    final_lock_ready: bool = False
    export_ready: bool = False
    external_delivery_ready: bool = False
    risk_flags: list[str] = Field(default_factory=list)
    checklist: list[str] = Field(default_factory=list)
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False


class ExportReadinessList(BaseModel):
    readiness: list[ExportReadiness] = Field(default_factory=list)
    readiness_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    raw_case_content_read: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class FinalLockActionRequest(BaseModel):
    action: str
    reviewer_id: str
    reviewer_note: str | None = None
    explicit_lawyer_confirmation: bool = False
    explicit_final_lock_confirmation: bool = False
    explicit_no_real_export_confirmation: bool = False
    explicit_no_email_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False
    explicit_no_final_report_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False


class FinalLockRecord(BaseModel):
    final_lock_id: str
    delivery_packet_id: str
    action: str
    reviewer_id: str = "redacted_reviewer"
    final_lock_status: str
    final_locked: bool = False
    controlled_export_placeholder_only: bool = True
    export_ready: bool = False
    external_delivery_ready: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    timestamp: str
    warnings: list[str] = Field(default_factory=list)


class FinalLockList(BaseModel):
    final_locks: list[FinalLockRecord] = Field(default_factory=list)
    final_lock_queue: list[DeliveryPacketRecord] = Field(default_factory=list)
    lock_count: int = 0
    queue_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    raw_case_content_read: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class ReviewSummary(BaseModel):
    delivery_packet_id: str
    lawyer_review_status: str
    reviewer_id: str | None = None
    review_summary_placeholder: str
    revision_required: bool = False
    risk_flags: list[str] = Field(default_factory=list)
    final_lock_ready: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    raw_content_included: bool = False


class ReviewSummaryList(BaseModel):
    review_summaries: list[ReviewSummary] = Field(default_factory=list)
    summary_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    raw_case_content_read: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class DeliveryPacketAuditEvent(BaseModel):
    audit_id: str
    action: str
    actor: str
    object_type: str
    object_id: str
    timestamp: str
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    no_raw_content: bool = True
    no_live_provider_call: bool = True
    no_final_opinion: bool = True
    no_final_report: bool = True
    no_external_delivery: bool = True
    no_email_sent: bool = True


class DeliveryPacketAuditTimeline(BaseModel):
    events: list[DeliveryPacketAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    raw_case_content_read: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class DeliveryPacketSafetyStatus(BaseModel):
    safety_checklist: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    raw_case_content_read: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    requires_lawyer_review: bool = True
    final_lock_required: bool = True
    source_trace_required: bool = True
    warnings: list[str] = Field(default_factory=list)
