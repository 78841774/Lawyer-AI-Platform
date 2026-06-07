import json
import os
import re
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any
from urllib import error, request
from uuid import uuid4

from personal_skill_studio.training_artifacts.storage import (
    EXTERNAL_OCR_JOBS_DIR,
    EXTERNAL_OCR_PARSE_RUNS_DIR,
    read_payload,
    read_payloads,
    write_payload,
)
from personal_skill_studio.training_artifacts.provider_secret_file_loader import (
    adapter_url_for_keys,
    credential_loaded_for_alias,
)
from personal_skill_studio.training_artifacts.external_ocr_paddle_adapter import (
    fetch_paddle_ocr_result,
    poll_paddle_ocr_job,
)


FORBIDDEN_OUTPUT_KEYS = {
    "raw_text",
    "ocr_text",
    "original_text",
    "full_document_text",
    "raw_material",
    "raw_case_material",
    "local_path",
    "file_path",
    "absolute_path",
    "api_key",
    "secret",
    "private_key",
    "access_token",
    "refresh_token",
    "provider_response",
    "provider_raw_response",
    "raw_response",
    "resulturl",
    "jsonurl",
    "authorization",
    "bearer",
    "token",
    "unredacted",
    "source_locator",
    "controlled_source_locator",
    "controlled_source_inputs",
}
FORBIDDEN_VALUE_PATTERNS = (
    re.compile(r"Bearer\s+[A-Za-z0-9._-]+", re.IGNORECASE),
    re.compile(r"BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY", re.IGNORECASE),
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"https?://[^\s\"']+", re.IGNORECASE),
)
OCR_PROVIDER_CREDENTIAL_ALIASES: dict[str, list[str]] = {
    "paddleocr": [
        "PADDLEOCR_AISTUDIO_CREDENTIAL",
        "BAIDU_PADDLE_AI_STUDIO_API_KEY",
        "BAIDU_OCR_API_KEY",
        "PADDLEOCR_API_KEY",
    ],
    "paddleocr_local": [
        "PADDLEOCR_AISTUDIO_CREDENTIAL",
        "BAIDU_PADDLE_AI_STUDIO_API_KEY",
        "BAIDU_OCR_API_KEY",
        "PADDLEOCR_API_KEY",
    ],
    "baidu_paddle_ai_studio_placeholder": [
        "BAIDU_PADDLE_AI_STUDIO_API_KEY",
        "PADDLEOCR_AISTUDIO_CREDENTIAL",
        "BAIDU_OCR_API_KEY",
    ],
    "baidu_ocr_placeholder": [
        "BAIDU_OCR_API_KEY",
        "BAIDU_PADDLE_AI_STUDIO_API_KEY",
        "PADDLEOCR_AISTUDIO_CREDENTIAL",
    ],
}
OCR_PROVIDER_ADAPTER_ALIASES: dict[str, list[str]] = {
    "paddleocr": ["PADDLEOCR", "PADDLEOCR_AISTUDIO", "BAIDU_PADDLE_AI_STUDIO", "BAIDU_OCR"],
    "paddleocr_local": ["PADDLEOCR", "PADDLEOCR_AISTUDIO", "BAIDU_PADDLE_AI_STUDIO", "BAIDU_OCR"],
    "baidu_paddle_ai_studio_placeholder": ["BAIDU_PADDLE_AI_STUDIO", "PADDLEOCR_AISTUDIO", "PADDLEOCR"],
    "baidu_ocr_placeholder": ["BAIDU_OCR", "BAIDU_PADDLE_AI_STUDIO", "PADDLEOCR"],
}
POLL_STALE_ATTEMPT_THRESHOLD = 10
POLL_STALE_SECONDS_THRESHOLD = 180


def start_external_ocr_parse(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    task_id = _safe_label(payload.get("task_id") or f"external_ocr_task_{uuid4().hex[:8]}")
    provider_alias = _safe_label(payload.get("provider_alias") or "PADDLEOCR_AISTUDIO_CREDENTIAL")
    material_refs = _safe_material_refs(payload.get("training_material_files") or payload.get("material_ids") or [])
    run_id = f"external_ocr_parse_run_{uuid4().hex[:10]}"
    credential_loaded = _credential_loaded(provider_alias)
    adapter_url = _adapter_url(provider_alias)
    explicit_authorized = bool(payload.get("explicit_authorized_training_material_confirmation"))
    explicit_external = bool(payload.get("explicit_external_ocr_confirmation"))
    explicit_no_source_return = bool(payload.get("explicit_no_source_payload_return_confirmation"))

    blocked_reasons = []
    if not material_refs:
        blocked_reasons.append("no_training_material_files")
    if not credential_loaded:
        blocked_reasons.append("credential_not_loaded")
    if not adapter_url:
        blocked_reasons.append("provider_gated_loader_not_configured")
    if not explicit_authorized:
        blocked_reasons.append("authorized_training_material_confirmation_missing")
    if not explicit_external:
        blocked_reasons.append("external_ocr_confirmation_missing")
    if not explicit_no_source_return:
        blocked_reasons.append("no_source_payload_return_confirmation_missing")

    if blocked_reasons:
        result = _blocked_run(
            run_id=run_id,
            task_id=task_id,
            credential_loaded=credential_loaded,
            material_refs=material_refs,
            blocked_reasons=blocked_reasons,
        )
        write_payload(EXTERNAL_OCR_PARSE_RUNS_DIR, run_id, result)
        return result

    loader_result = _call_provider_gated_loader(adapter_url, task_id, provider_alias, material_refs)
    if loader_result.get("loader_error") or _contains_forbidden_output(loader_result.get("payload")):
        loader_error_reason = _safe_label(loader_result.get("loader_error_reason") or "provider_gated_loader_failed_or_unsafe_response")
        result = _blocked_run(
            run_id=run_id,
            task_id=task_id,
            credential_loaded=credential_loaded,
            material_refs=material_refs,
            blocked_reasons=[loader_error_reason],
        )
        write_payload(EXTERNAL_OCR_PARSE_RUNS_DIR, run_id, result)
        return result

    result = _completed_or_failed_run(
        run_id=run_id,
        task_id=task_id,
        credential_loaded=credential_loaded,
        material_refs=material_refs,
        adapter_payload=loader_result["payload"],
    )
    write_payload(EXTERNAL_OCR_PARSE_RUNS_DIR, run_id, result)
    return result


def list_external_ocr_runs() -> dict[str, Any]:
    runs = read_payloads(EXTERNAL_OCR_PARSE_RUNS_DIR)
    return {
        "owner_only": True,
        "metadata_only": True,
        "ocr_mode": "external_ocr",
        "external_ocr_runs": runs,
        "run_count": len(runs),
        "source_trace_required": True,
        "audit_required": True,
    }


def get_external_ocr_run(run_id: str) -> dict[str, Any] | None:
    return read_payload(EXTERNAL_OCR_PARSE_RUNS_DIR, run_id)


def record_external_ocr_job_submission(
    submit_response: dict[str, Any],
    *,
    material_id: str,
    file_ref: str,
) -> dict[str, Any]:
    safe_material_id = _safe_label(material_id or "controlled_material")
    safe_file_ref = _safe_label(submit_response.get("file_ref") or file_ref or "file_ref_missing")
    provider_job_id = _safe_label(submit_response.get("provider_job_id") or f"external_ocr_job_{uuid4().hex[:10]}")
    parse_status = _normalize_job_status(submit_response.get("parse_status") or "failed")
    redacted_error = _safe_text(submit_response.get("redacted_error_summary")) if submit_response.get("redacted_error_summary") else None
    job = {
        "job_id": provider_job_id,
        "provider_job_id": provider_job_id,
        "material_id": safe_material_id,
        "file_ref": safe_file_ref,
        "ocr_mode": "external_ocr_failed" if parse_status == "failed" else "external_ocr",
        "parse_status": parse_status,
        "credential_loaded": bool(submit_response.get("credential_loaded")),
        "provider_call_allowed": bool(submit_response.get("provider_call_allowed")),
        "redacted_error_summary": redacted_error,
        "provider_connection_error_type": (
            _safe_label(submit_response.get("provider_connection_error_type"))
            if submit_response.get("provider_connection_error_type")
            else None
        ),
        "poll_status": None,
        "created_at": _now(),
        "updated_at": _now(),
        "audit_id": f"external_ocr_audit_{provider_job_id}",
        "source_trace_id": f"external_ocr_source_trace_{provider_job_id}",
        "internal_provider_result_ref": None,
        "provider_result_fetched": False,
        "provider_result_fetch_attempted": False,
        "provider_result_fetch_succeeded": False,
        "provider_result_available": False,
        "provider_result_internal_ref_available": False,
        "provider_result_internal_ref": None,
        "fetch_result_status": None,
        "fetch_result_error_type": None,
        "blocked_reason": None,
        "per_file_parse_summary_redacted": None,
        "parse_quality_report": None,
        "provider_poll_attempted": False,
        "provider_poll_succeeded": False,
        "provider_state_seen": False,
        "provider_state_mapped": False,
        "provider_state_redacted": None,
        "poll_attempt_count": 0,
        "last_poll_at": None,
        "stale_running_warning": False,
        "last_safe_diagnostic_status": "provider_poll_not_attempted",
        "safe_provider_state_trace": [],
    }
    write_payload(EXTERNAL_OCR_JOBS_DIR, provider_job_id, job)
    return _job_public_response(job)


def get_external_ocr_job_status(job_id: str) -> dict[str, Any] | None:
    job = _read_external_ocr_job(job_id)
    if job is None:
        return None
    return _job_public_response(job)


def poll_external_ocr_job(job_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any] | None:
    job = _read_external_ocr_job(job_id)
    if job is None:
        return None
    payload = payload or {}
    current = _normalize_job_status(job.get("parse_status"))
    if current in {"submitted", "pending", "running"}:
        job["poll_attempt_count"] = _safe_int(job.get("poll_attempt_count"), 0) + 1
        job["last_poll_at"] = _now()
        if payload.get("controlled_poll_status") or job.get("controlled_poll_status"):
            controlled_status = payload.get("controlled_poll_status") or job.get("controlled_poll_status")
            controlled_state = _safe_label(controlled_status)
            poll_result = {
                "parse_status": controlled_status,
                "redacted_error_summary": payload.get("redacted_error_summary"),
                "provider_poll_attempted": False,
                "provider_poll_succeeded": True,
                "provider_state_seen": True,
                "provider_state_redacted": controlled_state,
                "provider_state_mapped": _normalize_job_status(controlled_status) in {"pending", "running", "done", "failed"},
                "provider_connection_error_type": "unknown_provider_state"
                if _normalize_job_status(controlled_status) == "failed"
                and controlled_state not in {"failed", "error", "blocked"}
                else None,
            }
        else:
            poll_result = poll_paddle_ocr_job(str(job.get("provider_job_id") or job["job_id"]))
        next_status = _normalize_job_status(poll_result.get("parse_status") or "failed")
        if next_status not in {"pending", "running", "done", "failed"}:
            next_status = "failed"
        _update_poll_diagnostics(job, poll_result)
        job["poll_status"] = "failed" if next_status == "failed" else "succeeded"
        provider_attempted = bool(poll_result.get("provider_poll_attempted"))
        provider_succeeded = bool(poll_result.get("provider_poll_succeeded"))
        if next_status == "failed" and not provider_attempted and not provider_succeeded:
            job["redacted_error_summary"] = _safe_text(
                poll_result.get("redacted_error_summary") or "Provider polling was not attempted. Real material training remains blocked."
            )
        else:
            job["parse_status"] = next_status
        if next_status == "failed" and (provider_attempted or provider_succeeded):
            job["ocr_mode"] = "external_ocr_failed"
            job["redacted_error_summary"] = _safe_text(
                poll_result.get("redacted_error_summary") or job.get("redacted_error_summary") or "OCR provider polling failed. Raw response was not exposed."
            )
        elif next_status == "done":
            job["ocr_mode"] = "external_ocr"
            job["redacted_error_summary"] = None
            job["internal_provider_result_ref"] = job.get("internal_provider_result_ref") or f"internal_provider_result_{job['job_id']}"
        else:
            job["ocr_mode"] = "external_ocr"
            if _is_stale_running(job):
                job["stale_running_warning"] = True
                job["redacted_error_summary"] = (
                    "Provider job is still running beyond local threshold. Real material training remains blocked."
                )
            else:
                job["stale_running_warning"] = False
                if job.get("redacted_error_summary") == (
                    "Provider job is still running beyond local threshold. Real material training remains blocked."
                ):
                    job["redacted_error_summary"] = None
    job["updated_at"] = _now()
    write_payload(EXTERNAL_OCR_JOBS_DIR, job["job_id"], job)
    return _job_public_response(job)


def get_external_ocr_provider_status_diagnostics(job_id: str) -> dict[str, Any] | None:
    job = _read_external_ocr_job(job_id)
    if job is None:
        return None
    return _scrub_values(
        {
            "job_id": job["job_id"],
            "provider_job_id": job.get("provider_job_id"),
            "provider_poll_attempted": bool(job.get("provider_poll_attempted")),
            "provider_poll_succeeded": bool(job.get("provider_poll_succeeded")),
            "provider_state_seen": bool(job.get("provider_state_seen")),
            "provider_state_redacted": _safe_label(job.get("provider_state_redacted")) if job.get("provider_state_redacted") else None,
            "provider_state_mapped": bool(job.get("provider_state_mapped")),
            "provider_connection_error_type": (
                _safe_label(job.get("provider_connection_error_type")) if job.get("provider_connection_error_type") else None
            ),
            "poll_attempt_count": _safe_int(job.get("poll_attempt_count"), 0),
            "stale_running_warning": bool(job.get("stale_running_warning")),
            "last_safe_diagnostic_status": _safe_label(job.get("last_safe_diagnostic_status") or "provider_poll_not_attempted"),
        }
    )


def fetch_external_ocr_result(job_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any] | None:
    job = _read_external_ocr_job(job_id)
    if job is None:
        return None
    payload = payload or {}
    current = _normalize_job_status(job.get("parse_status"))
    if current == "failed" and job.get("provider_state_redacted") == "done" and not bool(job.get("provider_result_fetched")):
        current = "done"
        job["parse_status"] = "done"
        job["ocr_mode"] = "external_ocr"
    if current in {"submitted", "pending", "running"}:
        job["fetch_result_status"] = "blocked"
        job["blocked_reason"] = "external_ocr_not_done"
        job["redacted_error_summary"] = "OCR result fetch is blocked until provider job is done."
    elif current == "failed":
        if job.get("provider_state_redacted") == "done":
            job["parse_status"] = "done"
            job["ocr_mode"] = "external_ocr"
            job["fetch_result_status"] = "failed"
            job["blocked_reason"] = "result_fetch_failed"
            job["redacted_error_summary"] = _safe_text(
                job.get("redacted_error_summary") or "OCR result fetch failed. Raw response was not exposed."
            )
        else:
            job["ocr_mode"] = "external_ocr_failed"
            job["redacted_error_summary"] = _safe_text(job.get("redacted_error_summary") or "OCR provider failed. Raw response was not exposed.")
    else:
        if payload.get("provider_result_metadata"):
            fetch_result = {
                "parse_status": "done",
                "provider_result_fetch_attempted": True,
                "provider_result_fetch_succeeded": True,
                "provider_result_available": True,
                "provider_result_internal_ref_available": True,
                "provider_result_internal_ref": job.get("internal_provider_result_ref") or f"internal_provider_result_{job['job_id']}",
                "fetch_result_status": "succeeded",
                "fetch_result_error_type": None,
                "blocked_reason": None,
                "provider_state_redacted": job.get("provider_state_redacted") or "done",
                "internal_provider_result": payload.get("provider_result_metadata"),
            }
        else:
            fetch_result = fetch_paddle_ocr_result(str(job.get("provider_job_id") or job["job_id"]))
        fetch_status = _normalize_job_status(fetch_result.get("parse_status") or "failed")
        _update_fetch_diagnostics(job, fetch_result)
        if fetch_status == "failed":
            if job.get("provider_state_redacted") == "done" or current == "done":
                job["parse_status"] = "done"
                job["ocr_mode"] = "external_ocr"
            else:
                job["parse_status"] = "failed"
                job["ocr_mode"] = "external_ocr_failed"
            job["redacted_error_summary"] = _safe_text(
                fetch_result.get("redacted_error_summary") or "OCR result fetch failed. Raw response was not exposed."
            )
            job["blocked_reason"] = _safe_label(fetch_result.get("blocked_reason") or "result_fetch_failed")
        else:
            job["parse_status"] = "done"
            job["ocr_mode"] = "external_ocr"
            job["redacted_error_summary"] = None
            job["internal_provider_result_ref"] = job.get("internal_provider_result_ref") or f"internal_provider_result_{job['job_id']}"
            job["provider_result_metadata"] = _safe_provider_result_metadata(
                fetch_result.get("internal_provider_result") or job.get("provider_result_metadata") or {}
            )
            refs = fetch_result.get("internal_provider_result_refs")
            if isinstance(refs, dict) and not _contains_forbidden_output(refs):
                job["internal_provider_result_refs"] = _scrub_values(refs)
            job["blocked_reason"] = None
    job["updated_at"] = _now()
    write_payload(EXTERNAL_OCR_JOBS_DIR, job["job_id"], job)
    return _job_public_response(job)


def build_external_ocr_redacted_summary(job_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any] | None:
    job = _read_external_ocr_job(job_id)
    if job is None:
        return None
    payload = payload or {}
    if _normalize_job_status(job.get("parse_status")) != "done":
        job["updated_at"] = _now()
        write_payload(EXTERNAL_OCR_JOBS_DIR, job["job_id"], job)
        return _job_public_response(job)
    if not bool(job.get("provider_result_fetched")):
        job["blocked_reason"] = "result_fetch_not_available"
        job["fetch_result_status"] = job.get("fetch_result_status") or "blocked"
        job["updated_at"] = _now()
        write_payload(EXTERNAL_OCR_JOBS_DIR, job["job_id"], job)
        return _job_public_response(job)
    metadata = _safe_provider_result_metadata(payload.get("provider_result_metadata") or job.get("provider_result_metadata") or {})
    quality_score = _safe_quality_score(payload.get("quality_score", metadata.get("quality_score", job.get("quality_score", 0.82))))
    summary = {
        "file_ref": job["file_ref"],
        "material_id": job["material_id"],
        "document_type_guess": _safe_label(metadata.get("document_type_guess") or "unknown_legal_material"),
        "page_count": _safe_int(metadata.get("page_count"), 1),
        "extracted_pages": _safe_int(metadata.get("extracted_pages"), _safe_int(metadata.get("page_count"), 1)),
        "section_titles_redacted": _safe_redacted_sections(metadata.get("section_titles_redacted") or metadata.get("sections")),
        "key_entities_count": _safe_int(metadata.get("key_entities_count"), 0),
        "table_count": _safe_int(metadata.get("table_count"), 0),
        "image_count": _safe_int(metadata.get("image_count"), 0),
        "content_summary_redacted": _safe_text(
            metadata.get("content_summary_redacted") or "OCR result was converted into redacted metadata summary only."
        ),
        "possible_risks": _safe_risks(metadata.get("possible_risks")),
        "quality_score": quality_score,
        "redaction_status": "passed",
        "source_trace_id": job["source_trace_id"],
        "audit_id": job["audit_id"],
    }
    job["provider_result_metadata"] = metadata
    job["per_file_parse_summary_redacted"] = [summary]
    job["redacted_summary"] = {
        "file_ref": job["file_ref"],
        "page_count": summary["page_count"],
        "detected_sections_summary": {
            "section_count": len(summary["section_titles_redacted"]),
            "section_titles_redacted": summary["section_titles_redacted"],
        },
        "table_count": summary["table_count"],
        "image_count": summary["image_count"],
        "possible_document_type": summary["document_type_guess"],
        "quality_score": quality_score,
        "redaction_status": "passed",
        "source_trace_id": job["source_trace_id"],
        "audit_id": job["audit_id"],
    }
    job["updated_at"] = _now()
    write_payload(EXTERNAL_OCR_JOBS_DIR, job["job_id"], job)
    return _job_public_response(job)


def run_external_ocr_parse_quality_gate(job_id: str) -> dict[str, Any] | None:
    job = _read_external_ocr_job(job_id)
    if job is None:
        return None
    pre_state = _job_state(job, gate_override=False)
    quality_ready = _quality_ready(job)
    blocked_reason = None
    if not pre_state["external_ocr_completed"]:
        blocked_reason = "external_ocr_not_completed"
    elif not bool(job.get("provider_result_fetched")):
        blocked_reason = "result_fetch_not_available"
    elif not pre_state["per_file_parse_summary_available"]:
        blocked_reason = "redacted_summary_not_available"
    elif not pre_state["source_trace_complete"]:
        blocked_reason = "source_trace_incomplete"
    elif not pre_state["audit_complete"]:
        blocked_reason = "audit_incomplete"
    elif not quality_ready:
        blocked_reason = "parse_quality_below_threshold"
    gate_passed = blocked_reason is None
    report = {
        "job_id": job["job_id"],
        "material_id": job["material_id"],
        "external_ocr_completed": pre_state["external_ocr_completed"],
        "document_content_parsed": pre_state["document_content_parsed"],
        "provider_result_fetched": bool(job.get("provider_result_fetched")),
        "per_file_parse_summary_available": pre_state["per_file_parse_summary_available"],
        "redacted_summary_available": pre_state["redacted_summary_available"],
        "source_trace_complete": pre_state["source_trace_complete"],
        "audit_complete": pre_state["audit_complete"],
        "raw_content_not_exported": True,
        "parse_quality_passed": gate_passed,
        "blocked_reason": blocked_reason,
        "warnings": [
            "OCR full text, provider raw response, result URLs, local paths, and credentials are not exported.",
            "Real material training is allowed only after external OCR, redacted summary, source trace, audit, and parse quality pass.",
        ],
        "created_at": _now(),
    }
    job["parse_quality_report"] = report
    job["updated_at"] = _now()
    write_payload(EXTERNAL_OCR_JOBS_DIR, job["job_id"], job)
    return _job_public_response(job)


def get_external_ocr_job_audit(job_id: str) -> dict[str, Any] | None:
    job = _read_external_ocr_job(job_id)
    if job is None:
        return None
    return {
        "job_id": job["job_id"],
        "audit_id": job["audit_id"],
        "audit_complete": True,
        "events": [
            {"event": "external_ocr_job_registered", "metadata_only": True},
            {"event": "external_ocr_redaction_boundary_checked", "raw_content_exported": False},
        ],
        "created_at": job.get("created_at") or _now(),
        "updated_at": job.get("updated_at") or _now(),
    }


def get_external_ocr_job_source_trace(job_id: str) -> dict[str, Any] | None:
    job = _read_external_ocr_job(job_id)
    if job is None:
        return None
    return {
        "job_id": job["job_id"],
        "source_trace_id": job["source_trace_id"],
        "source_trace_complete": True,
        "file_ref": job["file_ref"],
        "material_id": job["material_id"],
        "trace_nodes": [
            {"node": "controlled_file_reference", "raw_content_exported": False},
            {"node": "external_ocr_redacted_summary", "raw_content_exported": False},
        ],
    }


def _call_provider_gated_loader(
    adapter_url: str,
    task_id: str,
    provider_alias: str,
    material_refs: list[dict[str, Any]],
) -> dict[str, Any]:
    body = {
        "task_id": task_id,
        "provider_alias": provider_alias,
        "credential_alias": _effective_credential_alias(provider_alias),
        "material_refs": [_public_material_ref(item) for item in material_refs],
        "controlled_source_inputs": [
            {
                "file_ref_id": item["file_ref_id"],
                "source_reference_type": item["source_reference_type"],
                "source_locator": item["_controlled_source_locator"],
            }
            for item in material_refs
            if item.get("_controlled_source_locator")
        ],
        "source_transfer_boundary": {
            "controlled_adapter_read_allowed": True,
            "adapter_must_not_return_source_locator": True,
            "adapter_must_not_return_raw_ocr_text": True,
            "adapter_must_not_return_provider_raw_response": True,
        },
        "return_contract": {
            "parse_status": "completed_or_failed",
            "redacted_summary": "required",
            "per_file_parse_summary": "required",
            "source_trace": "required",
        },
    }
    try:
        req = request.Request(
            adapter_url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError:
        return {"loader_error": True, "loader_error_reason": "provider_gated_loader_http_error"}
    except json.JSONDecodeError:
        return {"loader_error": True, "loader_error_reason": "provider_gated_loader_invalid_json"}
    except OSError:
        return {"loader_error": True, "loader_error_reason": "provider_gated_loader_network_error"}
    return {"payload": payload}


def _completed_or_failed_run(
    run_id: str,
    task_id: str,
    credential_loaded: bool,
    material_refs: list[dict[str, Any]],
    adapter_payload: dict[str, Any],
) -> dict[str, Any]:
    parse_status = "completed" if adapter_payload.get("parse_status") == "completed" else "failed"
    external_completed = parse_status == "completed"
    per_file = _safe_per_file_summary(adapter_payload.get("per_file_parse_summary"), material_refs, parse_status)
    source_trace = _safe_source_trace(adapter_payload.get("source_trace"), material_refs)
    return {
        "external_ocr_run_id": run_id,
        "task_id": task_id,
        "ocr_mode": "external_ocr",
        "credential_loaded": credential_loaded,
        "parse_status": parse_status,
        "external_ocr_completed": external_completed,
        "document_content_parsed": external_completed,
        "per_file_parse_summary_available": bool(per_file),
        "parse_quality_passed": external_completed and all(item["parse_status"] == "completed" for item in per_file),
        "redacted_summary": _safe_summary(adapter_payload.get("redacted_summary"), external_completed),
        "per_file_parse_summary": per_file,
        "source_trace": source_trace,
        "training_status": "ready_for_real_material_training" if external_completed else "blocked_for_external_ocr",
        "owner_only": True,
        "metadata_only": True,
        "source_trace_required": True,
        "audit_required": True,
        "created_at": _now(),
        "warnings": [
            "External OCR loader response was normalized to redacted metadata only.",
            "No credential value, source payload, filesystem location, or provider payload is returned.",
        ],
    }


def _blocked_run(
    run_id: str,
    task_id: str,
    credential_loaded: bool,
    material_refs: list[dict[str, Any]],
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "external_ocr_run_id": run_id,
        "task_id": task_id,
        "ocr_mode": "external_ocr",
        "credential_loaded": credential_loaded,
        "parse_status": "failed",
        "external_ocr_completed": False,
        "document_content_parsed": False,
        "per_file_parse_summary_available": bool(material_refs),
        "parse_quality_passed": False,
        "redacted_summary": {
            "summary_status": "not_available",
            "reason": "external_ocr_blocked",
            "blocked_reasons": blocked_reasons,
        },
        "per_file_parse_summary": [
            {
                "file_ref_id": item["file_ref_id"],
                "parse_status": "failed",
                "redacted_summary": "外部 OCR 未完成；该文件未进入真实材料训练摘要。",
                "source_trace": {
                    "file_ref_id": item["file_ref_id"],
                    "trace_status": "blocked_before_external_ocr",
                    "source_reference_type": item["source_reference_type"],
                },
            }
            for item in material_refs
        ],
        "source_trace": [
            {
                "file_ref_id": item["file_ref_id"],
                "trace_status": "blocked_before_external_ocr",
                "source_reference_type": item["source_reference_type"],
            }
            for item in material_refs
        ],
        "training_status": "blocked_for_external_ocr",
        "owner_only": True,
        "metadata_only": True,
        "source_trace_required": True,
        "audit_required": True,
        "created_at": _now(),
        "warnings": [
            "External OCR did not run because the provider-gated loader was not fully eligible.",
            "No credential value, source payload, filesystem location, or provider payload is returned.",
        ],
    }


def _safe_per_file_summary(value: Any, material_refs: list[dict[str, Any]], default_status: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        value = []
    summaries: list[dict[str, Any]] = []
    by_ref = {item.get("file_ref_id"): item for item in value if isinstance(item, dict)}
    for ref in material_refs:
        adapter_item = by_ref.get(ref["file_ref_id"], {})
        parse_status = "completed" if adapter_item.get("parse_status") == "completed" and default_status == "completed" else "failed"
        fallback_summary = (
            "外部 OCR 已返回脱敏摘要 metadata。"
            if parse_status == "completed"
            else "外部 OCR 未完成；该文件未进入真实材料训练摘要。"
        )
        summaries.append(
            {
                "file_ref_id": ref["file_ref_id"],
                "parse_status": parse_status,
                "redacted_summary": _safe_text(adapter_item.get("redacted_summary") or fallback_summary),
                "source_trace": {
                    "file_ref_id": ref["file_ref_id"],
                    "trace_status": "complete_metadata_only" if parse_status == "completed" else "failed_metadata_only",
                    "source_reference_type": ref["source_reference_type"],
                },
            }
        )
    return summaries


def _safe_source_trace(value: Any, material_refs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(value, list) and not _contains_forbidden_output(value):
        traces = []
        allowed_ref_ids = {item["file_ref_id"] for item in material_refs}
        for item in value:
            if isinstance(item, dict) and item.get("file_ref_id") in allowed_ref_ids:
                traces.append(
                    {
                        "file_ref_id": item["file_ref_id"],
                        "trace_status": _safe_label(item.get("trace_status") or "complete_metadata_only"),
                        "source_reference_type": _safe_label(item.get("source_reference_type") or "controlled_material_reference"),
                    }
                )
        if traces:
            return traces
    return [
        {
            "file_ref_id": item["file_ref_id"],
            "trace_status": "complete_metadata_only",
            "source_reference_type": item["source_reference_type"],
        }
        for item in material_refs
    ]


def _safe_summary(value: Any, completed: bool) -> dict[str, Any] | list[Any]:
    if _contains_forbidden_output(value):
        return {"summary_status": "not_available", "reason": "unsafe_adapter_summary_rejected"}
    if isinstance(value, dict):
        return _scrub_values(value)
    if isinstance(value, list):
        return [_scrub_values(item) for item in value if not _contains_forbidden_output(item)]
    return {
        "summary_status": "available" if completed else "not_available",
        "summary": _safe_text(value or "外部 OCR 未返回可用脱敏摘要。"),
    }


def _read_external_ocr_job(job_id: str) -> dict[str, Any] | None:
    return read_payload(EXTERNAL_OCR_JOBS_DIR, _safe_label(job_id))


def _update_poll_diagnostics(job: dict[str, Any], poll_result: dict[str, Any]) -> None:
    job["provider_poll_attempted"] = bool(poll_result.get("provider_poll_attempted"))
    job["provider_poll_succeeded"] = bool(poll_result.get("provider_poll_succeeded"))
    job["provider_state_seen"] = bool(poll_result.get("provider_state_seen"))
    job["provider_state_mapped"] = bool(poll_result.get("provider_state_mapped"))
    job["provider_state_redacted"] = _safe_label(poll_result.get("provider_state_redacted")) if poll_result.get("provider_state_redacted") else None
    job["provider_connection_error_type"] = (
        _safe_label(poll_result.get("provider_connection_error_type")) if poll_result.get("provider_connection_error_type") else None
    )
    if poll_result.get("provider_poll_succeeded") and poll_result.get("provider_state_mapped"):
        job["last_safe_diagnostic_status"] = "provider_state_mapped_without_raw_payload"
    elif poll_result.get("provider_poll_succeeded") and poll_result.get("provider_state_seen"):
        job["last_safe_diagnostic_status"] = "provider_state_unmapped_without_raw_payload"
    elif poll_result.get("provider_poll_attempted"):
        job["last_safe_diagnostic_status"] = "provider_poll_failed_without_raw_payload"
    else:
        job["last_safe_diagnostic_status"] = "provider_poll_not_attempted"

    trace = poll_result.get("safe_provider_state_trace")
    if isinstance(trace, dict) and not _contains_forbidden_output(trace):
        traces = job.get("safe_provider_state_trace") if isinstance(job.get("safe_provider_state_trace"), list) else []
        traces.append(
            _scrub_values(
                {
                    "provider_job_id": trace.get("provider_job_id"),
                    "provider_state": trace.get("provider_state"),
                    "extractProgress": trace.get("extractProgress") if isinstance(trace.get("extractProgress"), dict) else {},
                    "result_available": bool(trace.get("result_available")),
                    "poll_timestamp": job.get("last_poll_at") or _now(),
                }
            )
        )
        job["safe_provider_state_trace"] = traces[-20:]


def _update_fetch_diagnostics(job: dict[str, Any], fetch_result: dict[str, Any]) -> None:
    job["provider_result_fetch_attempted"] = bool(fetch_result.get("provider_result_fetch_attempted"))
    job["provider_result_fetch_succeeded"] = bool(fetch_result.get("provider_result_fetch_succeeded"))
    job["provider_result_available"] = bool(fetch_result.get("provider_result_available"))
    job["provider_result_internal_ref_available"] = bool(fetch_result.get("provider_result_internal_ref_available"))
    job["provider_result_fetched"] = bool(
        fetch_result.get("provider_result_fetch_succeeded")
        and fetch_result.get("provider_result_available")
        and fetch_result.get("provider_result_internal_ref_available")
    )
    job["provider_result_internal_ref"] = (
        _safe_label(fetch_result.get("provider_result_internal_ref")) if fetch_result.get("provider_result_internal_ref") else None
    )
    job["fetch_result_status"] = _safe_label(fetch_result.get("fetch_result_status") or ("succeeded" if job["provider_result_fetched"] else "failed"))
    job["fetch_result_error_type"] = (
        _safe_label(fetch_result.get("fetch_result_error_type")) if fetch_result.get("fetch_result_error_type") else None
    )
    if fetch_result.get("provider_state_redacted"):
        job["provider_state_redacted"] = _safe_label(fetch_result.get("provider_state_redacted"))
    if fetch_result.get("blocked_reason"):
        job["blocked_reason"] = _safe_label(fetch_result.get("blocked_reason"))


def _is_stale_running(job: dict[str, Any]) -> bool:
    attempts = _safe_int(job.get("poll_attempt_count"), 0)
    if attempts >= POLL_STALE_ATTEMPT_THRESHOLD:
        return True
    elapsed = _elapsed_seconds(job.get("created_at"))
    return elapsed >= POLL_STALE_SECONDS_THRESHOLD


def _elapsed_seconds(started_at: Any) -> int:
    if not started_at:
        return 0
    try:
        text = str(started_at).replace("Z", "+00:00")
        start = datetime.fromisoformat(text)
        if start.tzinfo is None:
            start = start.replace(tzinfo=UTC)
        return max(0, int((datetime.now(UTC) - start.astimezone(UTC)).total_seconds()))
    except (TypeError, ValueError):
        return 0


def _job_public_response(job: dict[str, Any]) -> dict[str, Any]:
    state = _job_state(job)
    response = {
        "job_id": job["job_id"],
        "provider_job_id": job.get("provider_job_id"),
        "ocr_mode": state["ocr_mode"],
        "parse_status": state["parse_status"],
        "poll_status": _safe_label(job.get("poll_status")) if job.get("poll_status") else None,
        "file_ref": job["file_ref"],
        "material_id": job["material_id"],
        "credential_loaded": bool(job.get("credential_loaded")),
        "provider_call_allowed": bool(job.get("provider_call_allowed")),
        "external_ocr_completed": state["external_ocr_completed"],
        "document_content_parsed": state["document_content_parsed"],
        "per_file_parse_summary_available": state["per_file_parse_summary_available"],
        "parse_quality_passed": state["parse_quality_passed"],
        "real_material_training_allowed": state["real_material_training_allowed"],
        "training_status": state["training_status"],
        "redacted_error_summary": _safe_text(job.get("redacted_error_summary")) if job.get("redacted_error_summary") else None,
        "provider_connection_error_type": (
            _safe_label(job.get("provider_connection_error_type")) if job.get("provider_connection_error_type") else None
        ),
        "provider_result_fetch_attempted": bool(job.get("provider_result_fetch_attempted")),
        "provider_result_fetch_succeeded": bool(job.get("provider_result_fetch_succeeded")),
        "provider_result_available": bool(job.get("provider_result_available")),
        "provider_result_internal_ref_available": bool(job.get("provider_result_internal_ref_available")),
        "provider_result_fetched": bool(job.get("provider_result_fetched")),
        "provider_result_internal_ref": _safe_label(job.get("provider_result_internal_ref")) if job.get("provider_result_internal_ref") else None,
        "fetch_result_status": _safe_label(job.get("fetch_result_status")) if job.get("fetch_result_status") else None,
        "fetch_result_error_type": _safe_label(job.get("fetch_result_error_type")) if job.get("fetch_result_error_type") else None,
        "blocked_reason": _safe_label(job.get("blocked_reason")) if job.get("blocked_reason") else None,
        "provider_poll_attempted": bool(job.get("provider_poll_attempted")),
        "provider_poll_succeeded": bool(job.get("provider_poll_succeeded")),
        "provider_state_seen": bool(job.get("provider_state_seen")),
        "provider_state_mapped": bool(job.get("provider_state_mapped")),
        "provider_state_redacted": _safe_label(job.get("provider_state_redacted")) if job.get("provider_state_redacted") else None,
        "poll_attempt_count": _safe_int(job.get("poll_attempt_count"), 0),
        "last_poll_at": job.get("last_poll_at"),
        "stale_running_warning": bool(job.get("stale_running_warning")),
        "last_safe_diagnostic_status": _safe_label(job.get("last_safe_diagnostic_status") or "provider_poll_not_attempted"),
        "redacted_summary": job.get("redacted_summary"),
        "per_file_parse_summary_redacted": job.get("per_file_parse_summary_redacted") or [],
        "parse_quality_report": job.get("parse_quality_report"),
        "source_trace_id": job.get("source_trace_id"),
        "audit_id": job.get("audit_id"),
        "owner_only": True,
        "metadata_only": True,
        "raw_content_not_exported": True,
        "updated_at": job.get("updated_at") or _now(),
    }
    return _scrub_values(response)


def _job_state(job: dict[str, Any], gate_override: bool | None = None) -> dict[str, Any]:
    parse_status = _normalize_job_status(job.get("parse_status"))
    has_summary = bool(job.get("per_file_parse_summary_redacted"))
    source_trace_complete = bool(job.get("source_trace_id"))
    audit_complete = bool(job.get("audit_id"))
    external_completed = parse_status == "done"
    document_parsed = external_completed
    report = job.get("parse_quality_report") if isinstance(job.get("parse_quality_report"), dict) else {}
    if gate_override is None:
        gate_passed = bool(report.get("parse_quality_passed"))
    else:
        gate_passed = bool(gate_override)
    result_fetched = bool(job.get("provider_result_fetched"))
    quality_passed = external_completed and result_fetched and has_summary and source_trace_complete and audit_complete and gate_passed
    if parse_status in {"submitted", "pending", "running"}:
        training_status = "blocked_for_external_ocr"
    elif parse_status == "failed":
        training_status = "blocked_for_external_ocr"
    elif not has_summary or not quality_passed:
        training_status = "blocked_for_parse_quality"
    else:
        training_status = "ready_for_real_material_training"
    return {
        "ocr_mode": "external_ocr_failed" if parse_status == "failed" else "external_ocr",
        "parse_status": parse_status,
        "external_ocr_completed": external_completed,
        "document_content_parsed": document_parsed,
        "per_file_parse_summary_available": has_summary,
        "redacted_summary_available": bool(job.get("redacted_summary")),
        "source_trace_complete": source_trace_complete,
        "audit_complete": audit_complete,
        "provider_result_fetched": result_fetched,
        "parse_quality_passed": quality_passed,
        "real_material_training_allowed": quality_passed,
        "training_status": training_status,
    }


def _quality_ready(job: dict[str, Any]) -> bool:
    return (
        _normalize_job_status(job.get("parse_status")) == "done"
        and bool(job.get("provider_result_fetched"))
        and bool(job.get("per_file_parse_summary_redacted"))
        and bool(job.get("source_trace_id"))
        and bool(job.get("audit_id"))
        and _summary_quality_score(job) >= 0.75
        and all(item.get("redaction_status") == "passed" for item in job.get("per_file_parse_summary_redacted") or [])
    )


def _normalize_job_status(value: Any) -> str:
    status = str(value or "failed").strip().lower()
    if status in {"submitted", "queued"}:
        return "submitted"
    if status == "pending":
        return "pending"
    if status in {"running", "processing"}:
        return "running"
    if status in {"done", "completed", "complete", "success", "succeeded"}:
        return "done"
    if status in {"blocked", "failed", "error"}:
        return "failed"
    return "failed"


def _summary_quality_score(job: dict[str, Any]) -> float:
    summaries = job.get("per_file_parse_summary_redacted") or []
    if not summaries:
        return 0.0
    scores = [_safe_quality_score(item.get("quality_score")) for item in summaries if isinstance(item, dict)]
    return min(scores) if scores else 0.0


def _safe_provider_result_metadata(value: Any) -> dict[str, Any]:
    if _contains_forbidden_output(value) or not isinstance(value, dict):
        return {}
    return _scrub_values(value)


def _safe_quality_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(score, 1.0))


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    return max(0, min(number, 10000))


def _safe_redacted_sections(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    sections = []
    for index, item in enumerate(value[:20], start=1):
        text = _safe_text(item)
        if text:
            sections.append(f"section_{index}_redacted")
    return sections


def _safe_risks(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    risks = []
    for item in value[:12]:
        text = _safe_label(item)
        if text:
            risks.append(text)
    return risks


def _safe_material_refs(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    refs = []
    for index, item in enumerate(value, start=1):
        text = str(item)
        ref_hash = sha256(text.encode("utf-8")).hexdigest()[:12]
        reference_type = "material_id" if "/" not in text and "\\" not in text else "controlled_file_reference"
        refs.append(
            {
                "file_ref_id": f"external_ocr_file_{index}_{ref_hash}",
                "source_reference_type": reference_type,
                "source_reference_recorded": True,
                "_controlled_source_locator": text if reference_type == "controlled_file_reference" else None,
            }
        )
    return refs


def _public_material_ref(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "file_ref_id": item["file_ref_id"],
        "source_reference_type": item["source_reference_type"],
        "source_reference_recorded": True,
    }


def _contains_forbidden_output(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(key).lower() in FORBIDDEN_OUTPUT_KEYS or _contains_forbidden_output(item) for key, item in value.items())
    if isinstance(value, list):
        return any(_contains_forbidden_output(item) for item in value)
    if isinstance(value, str):
        return (
            "/Users/" in value
            or "/Volumes/" in value
            or "C:\\" in value
            or any(pattern.search(value) for pattern in FORBIDDEN_VALUE_PATTERNS)
        )
    return False


def _scrub_values(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            _safe_label(key): _scrub_values(item)
            for key, item in value.items()
            if str(key).lower() not in FORBIDDEN_OUTPUT_KEYS
        }
    if isinstance(value, list):
        return [_scrub_values(item) for item in value]
    if isinstance(value, str):
        return _safe_text(value)
    return value


def _safe_text(value: Any) -> str:
    text = str(value or "")
    text = text.replace("/Users/", "[redacted-home]/").replace("/Volumes/", "[redacted-volume]/").replace("C:\\", "[redacted-drive]\\")
    text = re.sub(r"https?://[^\s\"']+", "[redacted-url]", text, flags=re.IGNORECASE)
    return text[:500]


def _safe_label(value: Any) -> str:
    text = str(value or "metadata").strip()
    safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in text)
    return safe[:96] or "metadata"


def _credential_loaded(provider_alias: str) -> bool:
    return _effective_credential_alias(provider_alias) is not None


def _effective_credential_alias(provider_alias: str) -> str | None:
    for alias in _credential_alias_candidates(provider_alias):
        if credential_loaded_for_alias(alias):
            return alias
    return None


def _credential_alias_candidates(provider_alias: str) -> list[str]:
    aliases = [provider_alias, provider_alias.upper()]
    provider_key = provider_alias.lower()
    aliases.extend(OCR_PROVIDER_CREDENTIAL_ALIASES.get(provider_key, []))
    if provider_alias.endswith("_OCR_ADAPTER_URL"):
        aliases.append(provider_alias.removesuffix("_OCR_ADAPTER_URL"))
    return _dedupe(aliases)


def _adapter_url(provider_alias: str) -> str | None:
    return adapter_url_for_keys(_adapter_url_candidates(provider_alias))


def _adapter_url_candidates(provider_alias: str) -> list[str]:
    provider_key = provider_alias.lower()
    prefixes = [provider_alias, provider_alias.upper()]
    prefixes.extend(alias for alias in OCR_PROVIDER_ADAPTER_ALIASES.get(provider_key, []))
    for alias in _credential_alias_candidates(provider_alias):
        prefixes.append(alias.removesuffix("_CREDENTIAL").removesuffix("_API_KEY"))
    keys = [f"{_safe_label(prefix).upper()}_OCR_ADAPTER_URL" for prefix in prefixes if prefix]
    keys.extend(
        [
            "TRAINING_EXTERNAL_OCR_ADAPTER_URL",
            "EXTERNAL_OCR_ADAPTER_URL",
            "OCR_PROVIDER_ADAPTER_URL",
        ]
    )
    return _dedupe(keys)


def _dedupe(values: list[str]) -> list[str]:
    deduped = []
    for value in values:
        if value and value not in deduped:
            deduped.append(value)
    return deduped


def _now() -> str:
    return datetime.now(UTC).isoformat()
