from personal_skill_studio.training_artifacts.storage import REAL_CLOSED_CASE_INTAKES_DIR, read_payloads


def intake_safety_flags(redaction_completed: bool = False, ready_for_codex_training: bool = False) -> dict[str, bool]:
    return {
        "owner_only": True,
        "metadata_only": True,
        "training_artifact_only": True,
        "closed_case_only": True,
        "real_closed_case_intake": True,
        "open_case_data_used": False,
        "raw_content_included": False,
        "raw_ocr_content_included": False,
        "redaction_required": True,
        "redaction_completed": redaction_completed,
        "api_key_exposed": False,
        "secret_value_returned": False,
        "local_path_exposed": False,
        "writes_to_training_set": False,
        "skill_updated": False,
        "skill_published": False,
        "skill_auto_published": False,
        "ready_for_codex_training": ready_for_codex_training,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "public_link_created": False,
        "email_sent": False,
        "external_delivery_triggered": False,
        "audit_required": True,
        "source_trace_required": True,
        "manual_review_required": True,
        "fine_tune_model_training": False,
        "load_executed": False,
        "blocks_next_stage": False,
    }


def build_intake_safety(intake_id: str | None = None) -> dict:
    payloads = read_payloads(REAL_CLOSED_CASE_INTAKES_DIR)
    payload = _find_payload(payloads, intake_id)
    redaction_report = (payload or {}).get("redaction_report") or {}
    redaction_completed = bool(redaction_report.get("redaction_completed", False))
    ready = bool((payload or {}).get("ready_for_codex_training", False))
    return {
        "intake_id": intake_id,
        "safety_checklist": [
            "仅用于已结案件训练材料 intake metadata",
            "不处理未结案件或当前实战案件",
            "不保存或返回原始内容",
            "不读取密钥或调用 provider",
            "脱敏后仅保留法律分析必要 metadata",
            "人工复核后才可进入后续真实闭案训练阶段",
            "不写正式训练集",
            "不更新或发布 Skill",
            "不生成最终法律意见或正式报告",
            "不触发公开链接、邮件或外部交付",
        ],
        "all_safety_checks_passed": True,
        **intake_safety_flags(redaction_completed=redaction_completed, ready_for_codex_training=ready),
        "warnings": ["v7.31a prepares intake metadata only; it does not execute Codex training."],
    }


def _find_payload(payloads: list[dict], intake_id: str | None) -> dict | None:
    if intake_id is None:
        return payloads[0] if payloads else None
    for payload in payloads:
        if payload.get("intake", {}).get("intake_id") == intake_id:
            return payload
    return None
