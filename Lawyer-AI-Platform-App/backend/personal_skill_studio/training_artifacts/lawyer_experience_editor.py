from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.schemas import (
    ExperienceCard,
    ExperiencePackage,
    PracticeLoadReviewAuditEvent,
    PracticeLoadReviewEditRequest,
    PracticeLoadReviewPackage,
    PracticeLoadReviewSaveRequest,
    PracticeLoadReviewSourceTraceBundle,
)


def v731f_safety_flags() -> dict[str, bool]:
    return {
        "owner_only": True,
        "local_private_processing_only": True,
        "generated_package_read_only": True,
        "lawyer_review_required": True,
        "practice_load_review_required": True,
        "approved_for_practice_load_required": True,
        "redacted_output_only": True,
        "abstracted_experience_only": True,
        "source_trace_required": True,
        "audit_required": True,
        "sensitive_field_scan_required": True,
        "provider_call_executed": False,
        "key_value_read": False,
        "credential_value_returned": False,
        "provider_result_payload_returned": False,
        "source_content_returned": False,
        "source_material_returned": False,
        "unreviewed_package_loaded": False,
        "unredacted_content_loaded": False,
        "non_pending_review_package_loaded": False,
        "missing_source_trace_loaded": False,
        "real_codex_training_triggered": False,
        "formal_training_set_written": False,
        "skill_updated": False,
        "skill_published": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "public_link_created": False,
        "email_sent": False,
        "external_delivery_triggered": False,
    }


def build_review_package(source_package: ExperiencePackage) -> PracticeLoadReviewPackage:
    now = datetime.now(UTC).isoformat()
    source_trace_bundle = PracticeLoadReviewSourceTraceBundle(
        source_trace_bundle_id=f"{source_package.package_id}_practice_load_source_trace_bundle",
        package_id=source_package.package_id,
        source_training_package_id=source_package.package_id,
        source_training_task_id=source_package.source_training_task_id,
        source_skill_package_id=source_package.source_skill_package_id,
        source_trace_ids=source_package.source_trace_bundle.source_trace_ids,
        source_experience_ids=source_package.source_experience_ids,
        trace_count=len(source_package.source_trace_bundle.source_trace_ids),
        warnings=["Practice load review source trace contains metadata identifiers only."],
        **v731f_safety_flags(),
    )
    return PracticeLoadReviewPackage(
        package_id=source_package.package_id,
        source_training_package_id=source_package.package_id,
        source_training_task_id=source_package.source_training_task_id,
        source_skill_package_id=source_package.source_skill_package_id,
        package_name=source_package.package_name,
        generated_experience_package={
            "source_training_package_id": source_package.package_id,
            "source_training_task_id": source_package.source_training_task_id,
            "source_skill_package_id": source_package.source_skill_package_id,
            "package_status": source_package.package_status,
            "experience_count": source_package.sample_count,
            "generated_version": source_package.package_version,
            "generated_package_preserved": True,
            "metadata_only": True,
        },
        experience_cards=[_build_card(source_package, index) for index, _ in enumerate(source_package.samples)],
        source_trace_bundle=source_trace_bundle,
        audit_events=[
            _audit_event(source_package.package_id, "pending_practice_load_review"),
        ],
        created_at=now,
        updated_at=now,
        warnings=[
            "Generated experience package is read-only metadata.",
            "Lawyer-approved package is created only after edit, save, revalidation, and approval.",
        ],
        **v731f_safety_flags(),
    )


def start_edit(package: PracticeLoadReviewPackage, request: PracticeLoadReviewEditRequest) -> PracticeLoadReviewPackage:
    updated = package.model_copy(deep=True)
    updated.review_status = "review_editing"
    updated.load_gate_status = "review_editing"
    updated.can_load_to_practice_runtime = False
    updated.updated_at = datetime.now(UTC).isoformat()
    updated.audit_events.append(_audit_event(package.package_id, "review_editing", request.reviewer_id, request.reviewer_note))
    return updated


def save_edits(package: PracticeLoadReviewPackage, request: PracticeLoadReviewSaveRequest) -> PracticeLoadReviewPackage:
    updated = package.model_copy(deep=True)
    edits_by_id = {edit.card_id: edit for edit in request.edited_cards}
    next_cards: list[ExperienceCard] = []
    for card in updated.experience_cards:
        edit = edits_by_id.get(card.card_id)
        if edit is None:
            next_cards.append(card)
            continue
        next_cards.append(
            card.model_copy(
                update={
                    "title": edit.title,
                    "lawyer_experience_text": edit.lawyer_experience_text,
                    "applicable_scenarios": edit.applicable_scenarios,
                    "not_applicable_scenarios": edit.not_applicable_scenarios,
                    "risk_warnings": edit.risk_warnings,
                    "usage_boundaries": edit.usage_boundaries,
                    "gray_load_enabled": edit.gray_load_enabled,
                    "review_status": "review_changes_saved",
                }
            )
        )
    updated.experience_cards = next_cards
    updated.review_status = "review_changes_saved"
    updated.load_gate_status = "review_changes_saved"
    updated.validation_status = "system_revalidation_required"
    updated.gray_load_enabled = request.gray_load_enabled
    updated.can_load_to_practice_runtime = False
    updated.lawyer_approved_experience_package = _lawyer_approved_package_metadata(updated)
    updated.revalidation_result = None
    updated.updated_at = datetime.now(UTC).isoformat()
    updated.audit_events.append(_audit_event(package.package_id, "review_changes_saved", request.reviewer_id, request.reviewer_note))
    updated.audit_events.append(_audit_event(package.package_id, "system_revalidation_required", request.reviewer_id, request.reviewer_note))
    return updated


def _build_card(source_package: ExperiencePackage, index: int) -> ExperienceCard:
    sample = source_package.samples[index]
    title = f"脱敏经验卡片 {index + 1}"
    generated_text = (
        f"基于脱敏经验 metadata {sample.source_experience_id} 生成的结构化经验："
        "关注事实模式、证据组织、风险提示、适用场景和使用边界。"
    )
    return ExperienceCard(
        card_id=f"{source_package.package_id}_card_{index + 1}",
        source_sample_id=sample.sample_id,
        source_experience_id=sample.source_experience_id,
        title=title,
        generated_experience_text=generated_text,
        lawyer_experience_text=generated_text,
        applicable_scenarios=["同类案由的脱敏经验复用", "律师确认后的实战辅助提示"],
        not_applicable_scenarios=["未脱敏材料", "未结案件训练写入", "自动生成最终法律意见"],
        risk_warnings=["仅作为实战系统加载前经验提示，不替代律师判断。"],
        usage_boundaries=["必须来源可追踪", "必须律师复核后才允许进入实战加载候选"],
    )


def _lawyer_approved_package_metadata(package: PracticeLoadReviewPackage) -> dict[str, str | int | bool | list[str]]:
    return {
        "source_training_package_id": package.source_training_package_id,
        "approved_card_count": len(package.experience_cards),
        "review_status": package.review_status,
        "validation_status": package.validation_status,
        "gray_load_enabled": package.gray_load_enabled,
        "practice_runtime_load_status": "not_loaded",
        "metadata_only": True,
        "card_ids": [card.card_id for card in package.experience_cards],
    }


def _audit_event(package_id: str, action: str, reviewer_id: str | None = None, reviewer_note: str | None = None) -> PracticeLoadReviewAuditEvent:
    return PracticeLoadReviewAuditEvent(
        event_id=f"{package_id}_practice_load_audit_{action}_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}",
        package_id=package_id,
        action=action,
        reviewer_id=reviewer_id,
        reviewer_note=reviewer_note,
        timestamp=datetime.now(UTC).isoformat(),
    )
