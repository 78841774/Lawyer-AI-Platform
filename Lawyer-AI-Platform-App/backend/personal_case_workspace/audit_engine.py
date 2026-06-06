from personal_case_workspace.schemas import CaseWorkspaceAuditEvent, CaseWorkspaceAuditTimeline


def build_audit_timeline() -> CaseWorkspaceAuditTimeline:
    events = [
        CaseWorkspaceAuditEvent(
            event_id="cw_audit_001",
            event_type="workspace_status_checked",
            linked_object_type="case_workspace",
            linked_object_id="case_workspace_mock_001",
            message="案件与材料工作台状态已检查；未读取真实原文。",
            created_at="2026-06-06T09:10:00Z",
        ),
        CaseWorkspaceAuditEvent(
            event_id="cw_audit_002",
            event_type="owner_raw_view_gate_presented",
            linked_object_type="material",
            linked_object_id="material_contract_metadata_001",
            message="用户本人原文查看动作仅返回受控 metadata，占位不加载 raw content。",
            created_at="2026-06-06T09:12:00Z",
        ),
        CaseWorkspaceAuditEvent(
            event_id="cw_audit_003",
            event_type="fact_correction_metadata_ready",
            linked_object_type="material",
            linked_object_id="material_chat_metadata_001",
            message="事实输入纠正入口已准备；不生成训练数据，不触发 AI prompt。",
            created_at="2026-06-06T09:14:00Z",
        ),
    ]
    return CaseWorkspaceAuditTimeline(
        events=events,
        event_count=len(events),
        warnings=["审计只记录安全事件 metadata；不记录 raw content、本地路径或密钥值。"],
    )


def build_fact_audit_timeline() -> CaseWorkspaceAuditTimeline:
    events = [
        CaseWorkspaceAuditEvent(
            event_id="fact_audit_001",
            event_type="fact_preview_created",
            linked_object_type="fact_preview",
            linked_object_id="fact_preview_mock_001",
            message="事实预览 metadata 已生成；不是最终事实认定。",
            created_at="2026-06-06T10:20:00Z",
        ),
        CaseWorkspaceAuditEvent(
            event_id="fact_audit_002",
            event_type="owner_fact_correction_recorded",
            linked_object_type="fact_correction",
            linked_object_id="fact_correction_mock_001",
            message="用户本人事实纠正 metadata 已记录；不进入训练集、不更新 Skill。",
            created_at="2026-06-06T10:26:00Z",
        ),
        CaseWorkspaceAuditEvent(
            event_id="fact_audit_003",
            event_type="legal_analysis_input_ready_checked",
            linked_object_type="fact_preview",
            linked_object_id="fact_preview_mock_001",
            message="法律分析输入 ready 状态已检查；不会自动触发法律分析。",
            created_at="2026-06-06T10:32:00Z",
        ),
    ]
    return CaseWorkspaceAuditTimeline(
        events=events,
        event_count=len(events),
        warnings=["fact audit 只记录 metadata，不记录 raw content 或本地路径。"],
    )
