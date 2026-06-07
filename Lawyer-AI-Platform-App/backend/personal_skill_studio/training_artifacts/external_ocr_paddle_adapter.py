"""PaddleOCR AIStudio adapter skeleton.

Important:
- Reads API token only from environment variable alias.
- Never returns token, Authorization header, provider raw response, local path, or OCR full text.
- Returns redacted per-file status for training gate decisions.

This file is a safe integration skeleton. Wire it into existing router/storage
after project-specific service conventions are confirmed.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import socket
import ssl
from dataclasses import dataclass
from typing import Any
from urllib import error as urlerror
from urllib import request as urlrequest

from .provider_env_aliases import OCR_PROVIDER
from .safe_provider_adapter_runtime import (
    check_provider_credential,
    redact_provider_error,
    safe_provider_status_dict,
)


DEFAULT_JOB_URL = "https://paddleocr.aistudio-app.com/api/v2/ocr/jobs"
DEFAULT_MODEL = "PaddleOCR-VL-1.6"
DEFAULT_STATUS_URL_TEMPLATE = "https://paddleocr.aistudio-app.com/api/v2/ocr/jobs/{job_id}"
PROVIDER_HTTP_ERROR = "provider_http_error"
PROVIDER_JSON_DECODE_ERROR = "provider_json_decode_error"
PROVIDER_URL_ERROR = "provider_url_error"
PROVIDER_TIMEOUT = "provider_timeout"
PROVIDER_REJECTED_REQUEST = "provider_rejected_request"
PROVIDER_HTTP_REACHABLE_STATUS = "provider_http_reachable_status"
PROVIDER_DNS_ERROR = "provider_dns_error"
PROVIDER_SSL_ERROR = "provider_ssl_error"
PROVIDER_CONNECTION_REFUSED = "provider_connection_refused"
UNKNOWN_PROVIDER_CONNECTION_ERROR = "unknown_provider_connection_error"
UNKNOWN_PROVIDER_STATE = "unknown_provider_state"


@dataclass
class ExternalOCRRequest:
    material_id: str
    file_path_or_url: str
    use_doc_orientation_classify: bool = False
    use_doc_unwarping: bool = False
    use_chart_recognition: bool = False


def redacted_file_ref(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"file_ref_{digest}"


def _redacted_file_ref(value: str) -> str:
    return redacted_file_ref(value)


def _safe_provider_job_id(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    if "/Users/" in text or "/Volumes/" in text or "C:\\" in text:
        return "provider_job_id_redacted"
    safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in text)
    return safe[:96] or None


def _submit_response(
    *,
    safe_status: dict[str, Any],
    ocr_mode: str,
    parse_status: str,
    file_ref: str,
    redacted_error_summary: str | None = None,
    provider_job_id: Any = None,
    provider_connection_error_type: str | None = None,
) -> dict[str, Any]:
    external_ocr_completed = False
    safe_provider_job_id = _safe_provider_job_id(provider_job_id)
    if parse_status == "submitted" and not safe_provider_job_id:
        safe_provider_job_id = f"external_ocr_job_{hashlib.sha256(file_ref.encode('utf-8')).hexdigest()[:16]}"
    return {
        "ocr_mode": ocr_mode,
        "parse_status": parse_status,
        "provider_job_id": safe_provider_job_id,
        "file_ref": file_ref,
        "credential_loaded": bool(safe_status.get("credential_loaded")),
        "provider_call_allowed": bool(safe_status.get("provider_call_allowed")),
        "external_ocr_completed": external_ocr_completed,
        "document_content_parsed": False,
        "per_file_parse_summary_available": False,
        "parse_quality_passed": False,
        "real_material_training_allowed": False,
        "training_status": "blocked_for_external_ocr",
        "redacted_error_summary": redacted_error_summary,
        "provider_connection_error_type": provider_connection_error_type,
    }


def _post_json(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int) -> tuple[int, dict[str, Any]]:
    body = json.dumps(payload).encode("utf-8")
    req = urlrequest.Request(
        url,
        data=body,
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    with urlrequest.urlopen(req, timeout=timeout, context=_provider_ssl_context()) as response:
        response_body = response.read().decode("utf-8")
        parsed = json.loads(response_body) if response_body else {}
        return response.status, parsed


def _provider_ssl_context() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore[import-not-found]

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # noqa: BLE001
        return ssl.create_default_context()


def _provider_job_url() -> str:
    value = str(os.getenv("OCR_PROVIDER_JOB_URL") or "").strip()
    return value or DEFAULT_JOB_URL


def _provider_status_url(provider_job_id: str) -> str:
    template = str(os.getenv("OCR_PROVIDER_STATUS_URL_TEMPLATE") or "").strip() or DEFAULT_STATUS_URL_TEMPLATE
    return template.format(job_id=_safe_provider_job_id(provider_job_id) or "redacted_job")


def _endpoint_probe_request(url: str, *, method: str, timeout: int) -> int:
    req = urlrequest.Request(
        url,
        headers={"User-Agent": "LawyerAI-External-OCR-Diagnostics/1.0", "Accept": "*/*"},
        method=method,
    )
    with urlrequest.urlopen(req, timeout=timeout, context=_provider_ssl_context()) as response:
        return response.status


def _head_endpoint(url: str, timeout: int) -> int:
    return _endpoint_probe_request(url, method="HEAD", timeout=timeout)


def _options_endpoint(url: str, timeout: int) -> int:
    return _endpoint_probe_request(url, method="OPTIONS", timeout=timeout)


def _get_json(url: str, headers: dict[str, str], timeout: int) -> tuple[int, dict[str, Any]]:
    req = urlrequest.Request(url, headers=headers, method="GET")
    with urlrequest.urlopen(req, timeout=timeout, context=_provider_ssl_context()) as response:
        response_body = response.read().decode("utf-8")
        parsed = json.loads(response_body) if response_body else {}
        return response.status, parsed


def _post_multipart(
    url: str,
    *,
    fields: dict[str, str],
    file_field: str,
    file_path: str,
    headers: dict[str, str],
    timeout: int,
) -> tuple[int, dict[str, Any]]:
    boundary = f"lawyer_ai_ocr_{hashlib.sha256(file_path.encode('utf-8')).hexdigest()[:16]}"
    parts: list[bytes] = []
    for key, value in fields.items():
        parts.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"),
                str(value).encode("utf-8"),
                b"\r\n",
            ]
        )
    filename = os.path.basename(file_path) or "controlled_file"
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    parts.extend(
        [
            f"--{boundary}\r\n".encode("utf-8"),
            f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'.encode("utf-8"),
            f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"),
        ]
    )
    with open(file_path, "rb") as f:
        parts.append(f.read())
    parts.extend([b"\r\n", f"--{boundary}--\r\n".encode("utf-8")])
    body = b"".join(parts)
    req = urlrequest.Request(
        url,
        data=body,
        headers={**headers, "Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urlrequest.urlopen(req, timeout=timeout, context=_provider_ssl_context()) as response:
        response_body = response.read().decode("utf-8")
        parsed = json.loads(response_body) if response_body else {}
        return response.status, parsed


def check_external_ocr_ready() -> dict[str, Any]:
    status = check_provider_credential(
        provider_type=OCR_PROVIDER.provider_type,
        credential_alias=OCR_PROVIDER.credential_alias,
        enabled_flag_alias=OCR_PROVIDER.enabled_flag_alias,
    )
    return safe_provider_status_dict(status)


def _is_http_url(value: str) -> bool:
    text = str(value or "").strip().lower()
    return text.startswith("http://") or text.startswith("https://")


def _http_error_type(code: int | None) -> str:
    if code in {400, 401, 403, 404, 405, 409, 413, 415, 422, 429}:
        return PROVIDER_REJECTED_REQUEST
    return PROVIDER_HTTP_ERROR


def _safe_http_error_summary(code: int | None) -> str:
    if code is None:
        return "OCR provider returned a non-success response. Raw response was not exposed."
    return f"OCR provider returned HTTP {code}. Raw response was not exposed."


def _safe_connection_error_response(
    *,
    safe_status: dict[str, Any],
    file_ref_source: str,
    exc: Exception,
    provider_connection_error_type: str | None = None,
) -> dict[str, Any]:
    if isinstance(exc, urlerror.HTTPError):
        error_type = provider_connection_error_type or _http_error_type(exc.code)
        summary = _safe_http_error_summary(exc.code)
    elif isinstance(exc, json.JSONDecodeError):
        error_type = PROVIDER_JSON_DECODE_ERROR
        summary = redact_provider_error(exc)
    elif isinstance(exc, (TimeoutError, socket.timeout)):
        error_type = PROVIDER_TIMEOUT
        summary = redact_provider_error(exc)
    elif isinstance(exc, urlerror.URLError):
        error_type = PROVIDER_URL_ERROR
        summary = redact_provider_error(exc)
    else:
        error_type = provider_connection_error_type or UNKNOWN_PROVIDER_CONNECTION_ERROR
        summary = redact_provider_error(exc)
    return _submit_response(
        safe_status=safe_status,
        ocr_mode="external_ocr_failed",
        parse_status="failed",
        file_ref=_redacted_file_ref(file_ref_source),
        redacted_error_summary=summary,
        provider_connection_error_type=error_type,
    )


def _safe_poll_error_response(
    *,
    provider_call_allowed: bool = True,
    redacted_error_summary: str,
    provider_connection_error_type: str,
    provider_poll_attempted: bool = True,
    provider_poll_succeeded: bool = False,
    provider_state_seen: bool = False,
    provider_state_redacted: str | None = None,
    provider_state_mapped: bool = False,
) -> dict[str, Any]:
    return {
        "provider_call_allowed": provider_call_allowed,
        "parse_status": "failed",
        "redacted_error_summary": redacted_error_summary,
        "provider_connection_error_type": provider_connection_error_type,
        "provider_poll_attempted": provider_poll_attempted,
        "provider_poll_succeeded": provider_poll_succeeded,
        "provider_state_seen": provider_state_seen,
        "provider_state_redacted": _safe_provider_state(provider_state_redacted),
        "provider_state_mapped": provider_state_mapped,
    }


def _diagnostic_error_type(exc: Exception) -> str:
    reason = exc.reason if isinstance(exc, urlerror.URLError) else exc
    if isinstance(reason, ssl.SSLError):
        return PROVIDER_SSL_ERROR
    if isinstance(reason, socket.gaierror):
        return PROVIDER_DNS_ERROR
    if isinstance(reason, (TimeoutError, socket.timeout)):
        return PROVIDER_TIMEOUT
    if isinstance(reason, ConnectionRefusedError):
        return PROVIDER_CONNECTION_REFUSED
    if isinstance(reason, OSError):
        if getattr(reason, "errno", None) in {54, 61, 111, 10061}:
            return PROVIDER_CONNECTION_REFUSED
        text = str(reason).lower()
        if "name or service not known" in text or "nodename nor servname" in text:
            return PROVIDER_DNS_ERROR
        if "timed out" in text or "timeout" in text:
            return PROVIDER_TIMEOUT
        if "ssl" in text or "certificate" in text or "tls" in text:
            return PROVIDER_SSL_ERROR
        if "connection refused" in text:
            return PROVIDER_CONNECTION_REFUSED
    if isinstance(reason, str):
        text = reason.lower()
        if "name or service not known" in text or "nodename nor servname" in text:
            return PROVIDER_DNS_ERROR
        if "timed out" in text or "timeout" in text:
            return PROVIDER_TIMEOUT
        if "ssl" in text or "certificate" in text or "tls" in text:
            return PROVIDER_SSL_ERROR
        if "connection refused" in text:
            return PROVIDER_CONNECTION_REFUSED
    return PROVIDER_URL_ERROR if isinstance(exc, urlerror.URLError) else UNKNOWN_PROVIDER_CONNECTION_ERROR


def _provider_connection_error_type(exc: Exception) -> str:
    if isinstance(exc, urlerror.HTTPError):
        return _http_error_type(exc.code)
    if isinstance(exc, json.JSONDecodeError):
        return PROVIDER_JSON_DECODE_ERROR
    if isinstance(exc, (TimeoutError, socket.timeout)):
        return PROVIDER_TIMEOUT
    if isinstance(exc, urlerror.URLError):
        return _diagnostic_error_type(exc)
    return UNKNOWN_PROVIDER_CONNECTION_ERROR


def _safe_provider_state(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in text)
    return safe[:40] or "unknown"


def _safe_extract_progress(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    safe: dict[str, Any] = {}
    for key in ("pageCount", "processedPages", "percent", "status"):
        if key in value:
            item = value.get(key)
            if isinstance(item, (int, float, bool)):
                safe[key] = item
            elif isinstance(item, str):
                safe[key] = _safe_provider_state(item)
    return safe


def _result_availability(data: dict[str, Any]) -> bool:
    for key in ("resultUrl", "jsonUrl", "result_url", "json_url", "result", "output", "pages", "documents"):
        if data.get(key):
            return True
    return False


def _internal_ref(provider_job_id: str, label: str, value: Any) -> str | None:
    if not value:
        return None
    digest = hashlib.sha256(f"{provider_job_id}:{label}:{value}".encode("utf-8")).hexdigest()[:16]
    return f"internal_ocr_{label}_{digest}"


def _safe_result_metadata(data: dict[str, Any]) -> dict[str, Any]:
    page_count = _safe_page_count(data)
    metadata = {
        "page_count": page_count,
        "extracted_pages": page_count,
        "document_type_guess": _safe_provider_state(data.get("documentType") or data.get("type") or "ocr_document"),
        "section_titles_redacted": _safe_section_markers(data),
        "key_entities_count": 0,
        "table_count": _safe_count(data.get("tables")),
        "image_count": _safe_count(data.get("images")),
        "content_summary_redacted": "OCR provider result was fetched and retained internally; raw text was not exported.",
        "possible_risks": ["lawyer_review_required", "raw_content_not_exported"],
        "quality_score": 0.82,
    }
    return metadata


def _safe_page_count(data: dict[str, Any]) -> int:
    for key in ("pageCount", "page_count", "pages"):
        value = data.get(key)
        if isinstance(value, list):
            return max(1, min(len(value), 10000))
        try:
            number = int(value)
        except (TypeError, ValueError):
            continue
        return max(1, min(number, 10000))
    progress = data.get("extractProgress")
    if isinstance(progress, dict):
        try:
            return max(1, min(int(progress.get("pageCount")), 10000))
        except (TypeError, ValueError):
            return 1
    return 1


def _safe_count(value: Any) -> int:
    if isinstance(value, list):
        return min(len(value), 10000)
    try:
        return max(0, min(int(value), 10000))
    except (TypeError, ValueError):
        return 0


def _safe_section_markers(data: dict[str, Any]) -> list[str]:
    sections = data.get("sections")
    if isinstance(sections, list) and sections:
        return [f"section_{index}_redacted" for index, _ in enumerate(sections[:20], start=1)]
    return ["ocr_result_redacted"]


def _probe_diagnostic_endpoint(url: str, timeout: int) -> int:
    try:
        return _head_endpoint(url, timeout=timeout)
    except urlerror.HTTPError as exc:
        return exc.code
    except Exception as head_exc:  # noqa: BLE001
        try:
            return _options_endpoint(url, timeout=timeout)
        except urlerror.HTTPError as exc:
            return exc.code
        except Exception:
            raise head_exc


def external_ocr_diagnostics() -> dict[str, Any]:
    safe_status = check_external_ocr_ready()
    job_url = _provider_job_url()
    endpoint_head_status: int | None = None
    endpoint_reachable = False
    provider_connection_error_type: str | None = None
    last_safe_diagnostic_status = "endpoint_not_checked"

    try:
        endpoint_head_status = _probe_diagnostic_endpoint(job_url, timeout=10)
        endpoint_reachable = True
        provider_connection_error_type = PROVIDER_HTTP_REACHABLE_STATUS
        last_safe_diagnostic_status = "endpoint_reachable_without_raw_payload"
    except (TimeoutError, socket.timeout):
        provider_connection_error_type = PROVIDER_TIMEOUT
        last_safe_diagnostic_status = "endpoint_timeout_without_raw_payload"
    except urlerror.URLError as exc:
        provider_connection_error_type = _diagnostic_error_type(exc)
        last_safe_diagnostic_status = f"endpoint_{provider_connection_error_type.removeprefix('provider_')}_without_raw_payload"
    except Exception as exc:  # noqa: BLE001
        provider_connection_error_type = _diagnostic_error_type(exc)
        if provider_connection_error_type == UNKNOWN_PROVIDER_CONNECTION_ERROR:
            last_safe_diagnostic_status = "endpoint_unknown_error_without_raw_payload"
        else:
            last_safe_diagnostic_status = f"endpoint_{provider_connection_error_type.removeprefix('provider_')}_without_raw_payload"

    return {
        "credential_loaded": bool(safe_status.get("credential_loaded")),
        "provider_configured": bool(safe_status.get("provider_configured")),
        "provider_call_allowed": bool(safe_status.get("provider_call_allowed")),
        "endpoint_reachable": endpoint_reachable,
        "endpoint_head_status": endpoint_head_status,
        "endpoint_head_405_is_reachable": endpoint_head_status == 405 and endpoint_reachable,
        "provider_connection_error_type": provider_connection_error_type,
        "last_safe_diagnostic_status": last_safe_diagnostic_status,
    }


def submit_paddle_ocr_job(request: ExternalOCRRequest) -> dict[str, Any]:
    """Submit OCR job and return safe job metadata only.

    This function intentionally does not download or return OCR full text.
    Use a separate internal runtime step to fetch provider output and build
    redacted parse summaries.
    """
    status = check_provider_credential(
        provider_type=OCR_PROVIDER.provider_type,
        credential_alias=OCR_PROVIDER.credential_alias,
        enabled_flag_alias=OCR_PROVIDER.enabled_flag_alias,
    )
    safe_status = safe_provider_status_dict(status)

    if not status.provider_call_allowed:
        return _submit_response(
            safe_status=safe_status,
            ocr_mode="external_ocr",
            parse_status="blocked",
            file_ref=_redacted_file_ref(request.file_path_or_url),
            redacted_error_summary=safe_status.get("redacted_error_summary"),
        )

    token = os.getenv(OCR_PROVIDER.credential_alias)
    job_url = _provider_job_url()
    model = os.getenv("OCR_PROVIDER_MODEL", DEFAULT_MODEL)

    headers = {"Authorization": f"bearer {token}"}
    optional_payload = {
        "useDocOrientationClassify": request.use_doc_orientation_classify,
        "useDocUnwarping": request.use_doc_unwarping,
        "useChartRecognition": request.use_chart_recognition,
    }

    try:
        if _is_http_url(request.file_path_or_url):
            payload = {
                "fileUrl": request.file_path_or_url,
                "model": model,
                "optionalPayload": optional_payload,
            }
            status_code, payload = _post_json(job_url, payload, headers, timeout=60)
        else:
            if not os.path.exists(request.file_path_or_url):
                return _submit_response(
                    safe_status=safe_status,
                    ocr_mode="external_ocr_failed",
                    parse_status="failed",
                    file_ref=_redacted_file_ref(request.file_path_or_url),
                    redacted_error_summary="Invalid file reference. Raw path was not exposed.",
                )
            data = {
                "model": model,
                "optionalPayload": json.dumps(optional_payload),
            }
            status_code, payload = _post_multipart(
                job_url,
                fields=data,
                file_field="file",
                file_path=request.file_path_or_url,
                headers=headers,
                timeout=120,
            )

        if status_code != 200:
            return _submit_response(
                safe_status=safe_status,
                ocr_mode="external_ocr_failed",
                parse_status="failed",
                file_ref=_redacted_file_ref(request.file_path_or_url),
                redacted_error_summary=_safe_http_error_summary(status_code),
                provider_connection_error_type=_http_error_type(status_code),
            )

        job_id = payload.get("data", {}).get("jobId")
        if not job_id:
            return _submit_response(
                safe_status=safe_status,
                ocr_mode="external_ocr_failed",
                parse_status="failed",
                file_ref=_redacted_file_ref(request.file_path_or_url),
                redacted_error_summary="OCR provider did not return a usable job id. Raw response was not exposed.",
                provider_connection_error_type=PROVIDER_REJECTED_REQUEST,
            )
        return _submit_response(
            safe_status=safe_status,
            ocr_mode="external_ocr",
            parse_status="submitted",
            file_ref=_redacted_file_ref(request.file_path_or_url),
            provider_job_id=job_id,
        )
    except urlerror.HTTPError as exc:
        return _safe_connection_error_response(
            safe_status=safe_status,
            file_ref_source=request.file_path_or_url,
            exc=exc,
        )
    except json.JSONDecodeError as exc:
        return _safe_connection_error_response(
            safe_status=safe_status,
            file_ref_source=request.file_path_or_url,
            exc=exc,
        )
    except (TimeoutError, socket.timeout) as exc:
        return _safe_connection_error_response(
            safe_status=safe_status,
            file_ref_source=request.file_path_or_url,
            exc=exc,
        )
    except urlerror.URLError as exc:
        return _safe_connection_error_response(
            safe_status=safe_status,
            file_ref_source=request.file_path_or_url,
            exc=exc,
        )
    except Exception as exc:  # noqa: BLE001
        return _safe_connection_error_response(
            safe_status=safe_status,
            file_ref_source=request.file_path_or_url,
            exc=exc,
        )


def poll_paddle_ocr_job(provider_job_id: str) -> dict[str, Any]:
    status = check_provider_credential(
        provider_type=OCR_PROVIDER.provider_type,
        credential_alias=OCR_PROVIDER.credential_alias,
        enabled_flag_alias=OCR_PROVIDER.enabled_flag_alias,
    )
    safe_status = safe_provider_status_dict(status)
    if not status.provider_call_allowed:
        return _safe_poll_error_response(
            provider_call_allowed=False,
            redacted_error_summary=safe_status.get("redacted_error_summary") or "Provider polling is blocked by safety gate.",
            provider_connection_error_type=PROVIDER_REJECTED_REQUEST,
            provider_poll_attempted=False,
        )

    token = os.getenv(OCR_PROVIDER.credential_alias)
    url = _provider_status_url(provider_job_id)
    try:
        status_code, payload = _get_json(url, {"Authorization": f"bearer {token}"}, timeout=60)
        if status_code != 200:
            return _safe_poll_error_response(
                redacted_error_summary=_safe_http_error_summary(status_code),
                provider_connection_error_type=_http_error_type(status_code),
            )
        data = payload.get("data")
        if not isinstance(data, dict):
            return _safe_poll_error_response(
                redacted_error_summary="Provider job data was missing. Raw response was not exposed.",
                provider_connection_error_type=PROVIDER_REJECTED_REQUEST,
                provider_poll_succeeded=True,
            )
        provider_state = _safe_provider_state(data.get("state"))
        if not provider_state:
            return _safe_poll_error_response(
                redacted_error_summary="Provider job state was missing. Raw response was not exposed.",
                provider_connection_error_type=PROVIDER_REJECTED_REQUEST,
                provider_poll_succeeded=True,
            )
        state_map = {
            "pending": "pending",
            "running": "running",
            "done": "done",
            "failed": "failed",
        }
        parse_status = state_map.get(provider_state)
        if parse_status is None:
            return _safe_poll_error_response(
                redacted_error_summary="Provider returned unknown job state.",
                provider_connection_error_type=UNKNOWN_PROVIDER_STATE,
                provider_poll_succeeded=True,
                provider_state_seen=True,
                provider_state_redacted=provider_state,
            )
        result = {
            "provider_call_allowed": True,
            "parse_status": parse_status,
            "provider_connection_error_type": None,
            "provider_poll_attempted": True,
            "provider_poll_succeeded": True,
            "provider_state_seen": True,
            "provider_state_redacted": provider_state,
            "provider_state_mapped": True,
            "safe_provider_state_trace": {
                "provider_job_id": _safe_provider_job_id(provider_job_id),
                "provider_state": provider_state,
                "extractProgress": _safe_extract_progress(data.get("extractProgress")),
                "result_available": _result_availability(data),
            },
        }
        if parse_status == "failed":
            result["redacted_error_summary"] = "OCR provider reported failure. Raw response was not exposed."
        return result
    except urlerror.HTTPError as exc:
        return _safe_poll_error_response(
            redacted_error_summary=_safe_http_error_summary(exc.code),
            provider_connection_error_type=_http_error_type(exc.code),
        )
    except json.JSONDecodeError as exc:
        return _safe_poll_error_response(
            redacted_error_summary=redact_provider_error(exc),
            provider_connection_error_type=PROVIDER_JSON_DECODE_ERROR,
        )
    except (TimeoutError, socket.timeout) as exc:
        return _safe_poll_error_response(
            redacted_error_summary=redact_provider_error(exc),
            provider_connection_error_type=PROVIDER_TIMEOUT,
        )
    except urlerror.URLError as exc:
        return _safe_poll_error_response(
            redacted_error_summary=redact_provider_error(exc),
            provider_connection_error_type=_diagnostic_error_type(exc),
        )
    except Exception as exc:  # noqa: BLE001
        return _safe_poll_error_response(
            redacted_error_summary=redact_provider_error(exc),
            provider_connection_error_type=UNKNOWN_PROVIDER_CONNECTION_ERROR,
        )


def fetch_paddle_ocr_result(provider_job_id: str) -> dict[str, Any]:
    status = check_provider_credential(
        provider_type=OCR_PROVIDER.provider_type,
        credential_alias=OCR_PROVIDER.credential_alias,
        enabled_flag_alias=OCR_PROVIDER.enabled_flag_alias,
    )
    safe_status = safe_provider_status_dict(status)
    if not status.provider_call_allowed:
        return {
            "provider_call_allowed": False,
            "parse_status": "failed",
            "provider_result_fetch_attempted": False,
            "provider_result_fetch_succeeded": False,
            "provider_result_available": False,
            "provider_result_internal_ref_available": False,
            "fetch_result_status": "failed",
            "fetch_result_error_type": PROVIDER_REJECTED_REQUEST,
            "blocked_reason": "provider_result_fetch_blocked_by_gate",
            "redacted_error_summary": safe_status.get("redacted_error_summary") or "Provider result fetch is blocked by safety gate.",
        }

    token = os.getenv(OCR_PROVIDER.credential_alias)
    url = _provider_status_url(provider_job_id)
    try:
        status_code, payload = _get_json(url, {"Authorization": f"bearer {token}"}, timeout=60)
        if status_code != 200:
            return {
                "provider_call_allowed": True,
                "parse_status": "failed",
                "provider_result_fetch_attempted": True,
                "provider_result_fetch_succeeded": False,
                "provider_result_available": False,
                "provider_result_internal_ref_available": False,
                "fetch_result_status": "failed",
                "fetch_result_error_type": _http_error_type(status_code),
                "blocked_reason": "result_fetch_failed",
                "redacted_error_summary": "OCR result fetch failed. Raw response was not exposed.",
            }
        data = payload.get("data")
        if not isinstance(data, dict):
            return _fetch_failed_response(
                fetch_result_error_type=PROVIDER_REJECTED_REQUEST,
                blocked_reason="missing_provider_job_data",
                provider_state_redacted=None,
            )
        provider_state = _safe_provider_state(data.get("state"))
        if provider_state != "done":
            return _fetch_failed_response(
                fetch_result_error_type=PROVIDER_REJECTED_REQUEST,
                blocked_reason="provider_job_not_done",
                provider_state_redacted=provider_state,
            )
        result_available = _result_availability(data)
        if not result_available:
            return _fetch_failed_response(
                fetch_result_error_type=PROVIDER_REJECTED_REQUEST,
                blocked_reason="provider_result_not_available",
                provider_state_redacted=provider_state,
            )
        result_url_ref = _internal_ref(provider_job_id, "result_ref", data.get("resultUrl") or data.get("result_url"))
        json_url_ref = _internal_ref(provider_job_id, "json_ref", data.get("jsonUrl") or data.get("json_url"))
        result_ref = result_url_ref or json_url_ref or _internal_ref(provider_job_id, "detail_ref", provider_state)
        return {
            "provider_call_allowed": True,
            "parse_status": "done",
            "provider_result_fetch_attempted": True,
            "provider_result_fetch_succeeded": True,
            "provider_result_available": True,
            "provider_result_internal_ref_available": bool(result_ref),
            "provider_result_internal_ref": result_ref,
            "fetch_result_status": "succeeded",
            "fetch_result_error_type": None,
            "provider_state_redacted": provider_state,
            "blocked_reason": None,
            "internal_provider_result": _safe_result_metadata(data),
            "internal_provider_result_refs": {
                "provider_job_id": _safe_provider_job_id(provider_job_id),
                "result_url_internal_ref": result_url_ref,
                "json_url_internal_ref": json_url_ref,
                "job_detail_internal_ref": _internal_ref(provider_job_id, "job_detail_ref", provider_state),
                "result_available": True,
            },
        }
    except urlerror.HTTPError as exc:
        return _fetch_failed_response(fetch_result_error_type=_http_error_type(exc.code), blocked_reason="result_fetch_failed")
    except json.JSONDecodeError as exc:
        return _fetch_failed_response(fetch_result_error_type=PROVIDER_JSON_DECODE_ERROR, redacted_error_summary=redact_provider_error(exc))
    except (TimeoutError, socket.timeout) as exc:
        return _fetch_failed_response(fetch_result_error_type=PROVIDER_TIMEOUT, redacted_error_summary=redact_provider_error(exc))
    except urlerror.URLError as exc:
        return _fetch_failed_response(fetch_result_error_type=_diagnostic_error_type(exc), redacted_error_summary=redact_provider_error(exc))
    except Exception as exc:  # noqa: BLE001
        return _fetch_failed_response(fetch_result_error_type=UNKNOWN_PROVIDER_CONNECTION_ERROR, redacted_error_summary=redact_provider_error(exc))


def _fetch_failed_response(
    *,
    fetch_result_error_type: str,
    blocked_reason: str = "result_fetch_failed",
    provider_state_redacted: str | None = None,
    redacted_error_summary: str = "OCR result fetch failed. Raw response was not exposed.",
) -> dict[str, Any]:
    return {
        "provider_call_allowed": True,
        "parse_status": "failed",
        "provider_result_fetch_attempted": True,
        "provider_result_fetch_succeeded": False,
        "provider_result_available": False,
        "provider_result_internal_ref_available": False,
        "fetch_result_status": "failed",
        "fetch_result_error_type": fetch_result_error_type,
        "provider_state_redacted": _safe_provider_state(provider_state_redacted),
        "blocked_reason": blocked_reason,
        "redacted_error_summary": redacted_error_summary,
    }
