#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Training External OCR v7.38c"

post_json() {
  local endpoint="$1"
  local payload="${2-}"
  if [ -z "${payload}" ]; then
    payload="{}"
  fi
  local response body code
  response="$(curl -sS -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" -w '\n%{http_code}' --json "${payload}" "${API_BASE}${endpoint}")"
  code="${response##*$'\n'}"
  body="${response%$'\n'*}"
  if [[ ! "${code}" =~ ^2 ]]; then
    printf '%s\n' "${body}" >&2
    fail "POST ${endpoint} returned HTTP ${code}"
  fi
  printf '%s' "${body}"
}

require_field_bool() {
  local body="$1"
  local label="$2"
  local field="$3"
  local expected="$4"
  if ! python3 -c 'import json,sys; data=json.loads(sys.stdin.read()); expected=sys.argv[2]=="true"; sys.exit(0 if data.get(sys.argv[1]) is expected else 1)' "${field}" "${expected}" <<<"${body}"; then
    fail "${label} expected ${field}=${expected}"
  fi
}

require_contains() {
  local body="$1"
  local label="$2"
  local pattern="$3"
  if ! printf '%s' "${body}" | grep -Eq "${pattern}"; then
    fail "${label} expected pattern: ${pattern}"
  fi
}

assert_external_ocr_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'api_key|token|authorization|bearer|provider_raw_response|raw_response|resultUrl|jsonUrl'
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|full_document_text|original_text|raw_material|local_path|absolute_path|file_path'
  assert_absent "${body}" "${label}" '张三|李四|未脱敏当事人信息|Bearer[[:space:]]+[A-Za-z0-9._-]+|sk-[A-Za-z0-9_-]+'
}

PYTHONPATH="${REPO_ROOT}/Lawyer-AI-Platform-App/backend" python3 - <<'PY'
from datetime import UTC, datetime, timedelta

from personal_skill_studio.training_artifacts.storage import EXTERNAL_OCR_JOBS_DIR, write_payload


def now():
    return datetime.now(UTC).isoformat()


def seed(
    job_id,
    parse_status,
    *,
    quality_score=None,
    summary=False,
    error=None,
    poll_attempt_count=0,
    created_at=None,
    provider_result_fetched=False,
):
    payload = {
        "job_id": job_id,
        "provider_job_id": job_id,
        "material_id": f"material_{job_id}",
        "file_ref": f"file_ref_{job_id}",
        "ocr_mode": "external_ocr_failed" if parse_status == "failed" else "external_ocr",
        "parse_status": parse_status,
        "credential_loaded": True,
        "provider_call_allowed": True,
        "redacted_error_summary": error,
        "created_at": created_at or now(),
        "updated_at": now(),
        "audit_id": f"audit_{job_id}",
        "source_trace_id": f"source_trace_{job_id}",
        "internal_provider_result_ref": f"internal_provider_result_{job_id}" if parse_status == "done" else None,
        "provider_result_fetched": provider_result_fetched,
        "provider_result_fetch_attempted": provider_result_fetched,
        "provider_result_fetch_succeeded": provider_result_fetched,
        "provider_result_available": provider_result_fetched,
        "provider_result_internal_ref_available": provider_result_fetched,
        "provider_result_internal_ref": f"internal_provider_result_{job_id}" if provider_result_fetched else None,
        "fetch_result_status": "succeeded" if provider_result_fetched else None,
        "fetch_result_error_type": None,
        "blocked_reason": None,
        "provider_result_metadata": {
            "page_count": 3,
            "extracted_pages": 3,
            "document_type_guess": "judgment",
            "section_titles_redacted": ["facts", "reasoning"],
            "key_entities_count": 4,
            "table_count": 1,
            "image_count": 0,
            "content_summary_redacted": "Redacted legal material summary only.",
            "possible_risks": ["quality_review_required"],
            "quality_score": quality_score if quality_score is not None else 0.82,
            "resultUrl": "https://provider.invalid/raw-result",
            "jsonUrl": "https://provider.invalid/raw-json",
            "raw_text": "张三 OCR 原文 should never leave runtime",
            "provider_raw_response": {"secret": "never-return"},
        },
        "per_file_parse_summary_redacted": None,
        "parse_quality_report": None,
        "provider_poll_attempted": False,
        "provider_poll_succeeded": False,
        "provider_state_seen": False,
        "provider_state_mapped": False,
        "provider_state_redacted": None,
        "poll_attempt_count": poll_attempt_count,
        "last_poll_at": None,
        "stale_running_warning": False,
        "last_safe_diagnostic_status": "provider_poll_not_attempted",
        "safe_provider_state_trace": [],
    }
    if summary:
        payload["per_file_parse_summary_redacted"] = [
            {
                "file_ref": payload["file_ref"],
                "material_id": payload["material_id"],
                "document_type_guess": "judgment",
                "page_count": 3,
                "extracted_pages": 3,
                "section_titles_redacted": ["section_1_redacted"],
                "key_entities_count": 4,
                "table_count": 1,
                "image_count": 0,
                "content_summary_redacted": "Redacted legal material summary only.",
                "possible_risks": ["quality_review_required"],
                "quality_score": quality_score if quality_score is not None else 0.82,
                "redaction_status": "passed",
                "source_trace_id": payload["source_trace_id"],
                "audit_id": payload["audit_id"],
            }
        ]
        payload["redacted_summary"] = {
            "file_ref": payload["file_ref"],
            "page_count": 3,
            "detected_sections_summary": {"section_count": 1, "section_titles_redacted": ["section_1_redacted"]},
            "table_count": 1,
            "image_count": 0,
            "possible_document_type": "judgment",
            "quality_score": quality_score if quality_score is not None else 0.82,
            "redaction_status": "passed",
            "source_trace_id": payload["source_trace_id"],
            "audit_id": payload["audit_id"],
        }
    write_payload(EXTERNAL_OCR_JOBS_DIR, job_id, payload)


seed("v738c_submitted_job", "submitted")
seed("v738c_running_job", "running")
seed("v738c_failed_job", "failed", error="Provider failed. Raw response was not exposed.")
seed("v738c_done_no_summary_job", "done")
seed("v738c_result_missing_job", "done")
seed("v738c_quality_low_job", "done", quality_score=0.45, provider_result_fetched=True)
seed("v738c_quality_pass_job", "done", quality_score=0.92, provider_result_fetched=True)
seed("v738c_stale_running_job", "running", poll_attempt_count=9, created_at=(datetime.now(UTC) - timedelta(seconds=181)).isoformat())
seed("v738c_unknown_state_job", "running")
PY

PYTHONPATH="${REPO_ROOT}/Lawyer-AI-Platform-App/backend" python3 - <<'PY'
import json
import os
from urllib import error as urlerror

from personal_skill_studio.training_artifacts import external_ocr_paddle_adapter as adapter

os.environ["PROVIDER_CALLS_ENABLED"] = "true"
os.environ["EXTERNAL_OCR_ENABLED"] = "true"
os.environ["OCR_PROVIDER_API_KEY"] = "dummy-regression-credential"

original_get_json = adapter._get_json
try:
    def set_response(payload):
        def fake_get_json(url, headers, timeout):
            assert "Authorization" in headers
            assert "56928651015348224" in url
            return 200, payload

        adapter._get_json = fake_get_json

    expected_states = [
        ("pending", "pending"),
        ("running", "running"),
        ("done", "done"),
        ("failed", "failed"),
    ]
    for provider_state, expected_status in expected_states:
        set_response({"data": {"state": provider_state, "extractProgress": {"percent": 50}, "resultUrl": "https://provider.invalid/raw"}})
        response = adapter.poll_paddle_ocr_job("56928651015348224")
        body = json.dumps(response, ensure_ascii=False)
        assert response["parse_status"] == expected_status
        assert response["provider_poll_attempted"] is True
        assert response["provider_poll_succeeded"] is True
        assert response["provider_state_seen"] is True
        assert response["provider_state_mapped"] is True
        assert response["provider_state_redacted"] == provider_state
        assert "resultUrl" not in body
        assert "https://provider.invalid" not in body
        assert "Authorization" not in body
        assert "bearer" not in body
        assert "provider_raw_response" not in body

    set_response({"data": {"status": "done"}})
    response = adapter.poll_paddle_ocr_job("56928651015348224")
    assert response["parse_status"] == "failed"
    assert response["provider_poll_succeeded"] is True
    assert response["provider_state_seen"] is False
    assert response["provider_state_mapped"] is False
    assert response["provider_connection_error_type"] == "provider_rejected_request"

    set_response({"data": {"state": "surprise_state"}})
    response = adapter.poll_paddle_ocr_job("56928651015348224")
    assert response["parse_status"] == "failed"
    assert response["provider_state_seen"] is True
    assert response["provider_state_mapped"] is False
    assert response["provider_connection_error_type"] == "unknown_provider_state"

    def raise_http_error(url, headers, timeout):
        raise urlerror.HTTPError(url="https://redacted.invalid", code=404, msg="safe not found", hdrs=None, fp=None)

    adapter._get_json = raise_http_error
    response = adapter.poll_paddle_ocr_job("56928651015348224")
    assert response["parse_status"] == "failed"
    assert response["provider_poll_attempted"] is True
    assert response["provider_poll_succeeded"] is False
    assert response["provider_connection_error_type"] == "provider_rejected_request"
finally:
    adapter._get_json = original_get_json
    os.environ.pop("OCR_PROVIDER_API_KEY", None)
    os.environ.pop("EXTERNAL_OCR_ENABLED", None)
    os.environ.pop("PROVIDER_CALLS_ENABLED", None)
print("PASS external OCR adapter provider poll state mapping and failure checks")
PY

PYTHONPATH="${REPO_ROOT}/Lawyer-AI-Platform-App/backend" python3 - <<'PY'
import json
import os
from urllib import error as urlerror

from personal_skill_studio.training_artifacts import external_ocr_paddle_adapter as adapter

os.environ["PROVIDER_CALLS_ENABLED"] = "true"
os.environ["EXTERNAL_OCR_ENABLED"] = "true"
os.environ["OCR_PROVIDER_API_KEY"] = "dummy-regression-credential"

original_get_json = adapter._get_json
try:
    captured = {}

    def fake_done_detail(url, headers, timeout):
        captured["url"] = url
        assert "Authorization" in headers
        assert url.endswith("/api/v2/ocr/jobs/56935129759133696")
        return 200, {
            "data": {
                "state": "done",
                "pageCount": 1,
                "extractProgress": {"pageCount": 1, "percent": 100},
                "resultUrl": "https://provider.invalid/raw-result",
                "jsonUrl": "https://provider.invalid/raw-json",
                "raw_text": "张三 OCR 原文 should never return",
            }
        }

    adapter._get_json = fake_done_detail
    response = adapter.fetch_paddle_ocr_result("56935129759133696")
    body = json.dumps(response, ensure_ascii=False)
    assert response["parse_status"] == "done"
    assert response["provider_result_fetch_attempted"] is True
    assert response["provider_result_fetch_succeeded"] is True
    assert response["provider_result_available"] is True
    assert response["provider_result_internal_ref_available"] is True
    assert response["fetch_result_status"] == "succeeded"
    assert response["provider_state_redacted"] == "done"
    assert "/result" not in captured["url"].removesuffix("/api/v2/ocr/jobs/56935129759133696")
    assert "resultUrl" not in body
    assert "jsonUrl" not in body
    assert "https://provider.invalid" not in body
    assert "raw_text" not in body
    assert "OCR 原文" not in body
    assert "Authorization" not in body
    assert "bearer" not in body

    def fake_done_without_result(url, headers, timeout):
        return 200, {"data": {"state": "done"}}

    adapter._get_json = fake_done_without_result
    response = adapter.fetch_paddle_ocr_result("56935129759133696")
    assert response["parse_status"] == "failed"
    assert response["provider_result_fetch_attempted"] is True
    assert response["provider_result_fetch_succeeded"] is False
    assert response["blocked_reason"] == "provider_result_not_available"

    def fake_404(url, headers, timeout):
        raise urlerror.HTTPError(url="https://redacted.invalid", code=404, msg="safe not found", hdrs=None, fp=None)

    adapter._get_json = fake_404
    response = adapter.fetch_paddle_ocr_result("56935129759133696")
    assert response["parse_status"] == "failed"
    assert response["provider_result_fetch_attempted"] is True
    assert response["provider_result_fetch_succeeded"] is False
    assert response["fetch_result_error_type"] == "provider_rejected_request"
    assert response["blocked_reason"] == "result_fetch_failed"
finally:
    adapter._get_json = original_get_json
    os.environ.pop("OCR_PROVIDER_API_KEY", None)
    os.environ.pop("EXTERNAL_OCR_ENABLED", None)
    os.environ.pop("PROVIDER_CALLS_ENABLED", None)
print("PASS external OCR adapter fetch-result job detail and safe failure checks")
PY

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/external-ocr/status")"
assert_external_ocr_safe "${status_body}" "external ocr status"

submit_body="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/submit" '{"material_id":"material_v738c_submit"}')"
assert_external_ocr_safe "${submit_body}" "external ocr submit"
require_field_bool "${submit_body}" "external ocr submit" "external_ocr_completed" "false"
require_field_bool "${submit_body}" "external ocr submit" "real_material_training_allowed" "false"
assert_absent "${submit_body}" "external ocr submit" 'ready_for_real_material_training'

submitted_status="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_submitted_job/status")"
assert_external_ocr_safe "${submitted_status}" "submitted status"
require_contains "${submitted_status}" "submitted status" '"parse_status"[[:space:]]*:[[:space:]]*"submitted"'
require_field_bool "${submitted_status}" "submitted status" "external_ocr_completed" "false"
require_field_bool "${submitted_status}" "submitted status" "document_content_parsed" "false"
require_field_bool "${submitted_status}" "submitted status" "per_file_parse_summary_available" "false"
require_field_bool "${submitted_status}" "submitted status" "real_material_training_allowed" "false"
require_contains "${submitted_status}" "submitted status" '"training_status"[[:space:]]*:[[:space:]]*"blocked_for_external_ocr"'

running_poll="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_running_job/poll" '{"controlled_poll_status":"running"}')"
assert_external_ocr_safe "${running_poll}" "running poll"
require_contains "${running_poll}" "running poll" '"parse_status"[[:space:]]*:[[:space:]]*"running"'
require_contains "${running_poll}" "running poll" '"provider_poll_succeeded"[[:space:]]*:[[:space:]]*true'
require_contains "${running_poll}" "running poll" '"provider_state_redacted"[[:space:]]*:[[:space:]]*"running"'
require_field_bool "${running_poll}" "running poll" "real_material_training_allowed" "false"
require_contains "${running_poll}" "running poll" '"training_status"[[:space:]]*:[[:space:]]*"blocked_for_external_ocr"'

stale_poll="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_stale_running_job/poll" '{"controlled_poll_status":"running"}')"
assert_external_ocr_safe "${stale_poll}" "stale running poll"
require_contains "${stale_poll}" "stale running poll" '"parse_status"[[:space:]]*:[[:space:]]*"running"'
require_field_bool "${stale_poll}" "stale running poll" "stale_running_warning" "true"
require_field_bool "${stale_poll}" "stale running poll" "real_material_training_allowed" "false"
require_contains "${stale_poll}" "stale running poll" '"redacted_error_summary"[[:space:]]*:[[:space:]]*"Provider job is still running beyond local threshold\. Real material training remains blocked\."'

unknown_poll="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_unknown_state_job/poll" '{"controlled_poll_status":"surprise_state"}')"
assert_external_ocr_safe "${unknown_poll}" "unknown provider state poll"
require_contains "${unknown_poll}" "unknown provider state poll" '"parse_status"[[:space:]]*:[[:space:]]*"failed"'
require_contains "${unknown_poll}" "unknown provider state poll" '"provider_connection_error_type"[[:space:]]*:[[:space:]]*"unknown_provider_state"'
require_field_bool "${unknown_poll}" "unknown provider state poll" "real_material_training_allowed" "false"

provider_diag="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_stale_running_job/provider-status-diagnostics")"
assert_external_ocr_safe "${provider_diag}" "provider status diagnostics"
require_contains "${provider_diag}" "provider status diagnostics" '"provider_poll_succeeded"[[:space:]]*:[[:space:]]*true'
require_contains "${provider_diag}" "provider status diagnostics" '"provider_state_redacted"[[:space:]]*:[[:space:]]*"running"'
require_field_bool "${provider_diag}" "provider status diagnostics" "stale_running_warning" "true"
assert_absent "${provider_diag}" "provider status diagnostics" 'resultUrl|jsonUrl|raw_text|ocr_text|provider_raw_response|https://provider\.invalid'

failed_status="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_failed_job/status")"
assert_external_ocr_safe "${failed_status}" "failed status"
require_contains "${failed_status}" "failed status" '"parse_status"[[:space:]]*:[[:space:]]*"failed"'
require_contains "${failed_status}" "failed status" '"ocr_mode"[[:space:]]*:[[:space:]]*"external_ocr_failed"'
require_contains "${failed_status}" "failed status" '"redacted_error_summary"[[:space:]]*:'
require_field_bool "${failed_status}" "failed status" "real_material_training_allowed" "false"

done_status="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_done_no_summary_job/status")"
assert_external_ocr_safe "${done_status}" "done before fetch status"
require_contains "${done_status}" "done before fetch status" '"parse_status"[[:space:]]*:[[:space:]]*"done"'
require_field_bool "${done_status}" "done before fetch status" "external_ocr_completed" "true"
require_field_bool "${done_status}" "done before fetch status" "document_content_parsed" "true"
require_field_bool "${done_status}" "done before fetch status" "per_file_parse_summary_available" "false"
require_field_bool "${done_status}" "done before fetch status" "parse_quality_passed" "false"
require_field_bool "${done_status}" "done before fetch status" "real_material_training_allowed" "false"
require_contains "${done_status}" "done before fetch status" '"training_status"[[:space:]]*:[[:space:]]*"blocked_for_parse_quality"'

fetch_body="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_done_no_summary_job/fetch-result" '{"provider_result_metadata":{"page_count":3,"extracted_pages":3,"document_type_guess":"judgment","section_titles_redacted":["facts"],"resultUrl":"https://provider.invalid/raw-result","jsonUrl":"https://provider.invalid/raw-json","raw_text":"张三 OCR 原文 should never leave runtime"}}')"
assert_external_ocr_safe "${fetch_body}" "fetch result"
require_contains "${fetch_body}" "fetch result" '"parse_status"[[:space:]]*:[[:space:]]*"done"'
require_field_bool "${fetch_body}" "fetch result" "external_ocr_completed" "true"
require_field_bool "${fetch_body}" "fetch result" "document_content_parsed" "true"
require_field_bool "${fetch_body}" "fetch result" "provider_result_fetch_attempted" "true"
require_field_bool "${fetch_body}" "fetch result" "provider_result_fetch_succeeded" "true"
require_field_bool "${fetch_body}" "fetch result" "provider_result_available" "true"
require_field_bool "${fetch_body}" "fetch result" "provider_result_internal_ref_available" "true"
require_field_bool "${fetch_body}" "fetch result" "provider_result_fetched" "true"
require_field_bool "${fetch_body}" "fetch result" "per_file_parse_summary_available" "false"
require_field_bool "${fetch_body}" "fetch result" "real_material_training_allowed" "false"
require_contains "${fetch_body}" "fetch result" '"training_status"[[:space:]]*:[[:space:]]*"blocked_for_parse_quality"'

missing_summary="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_result_missing_job/build-redacted-summary" '{}')"
assert_external_ocr_safe "${missing_summary}" "missing result summary blocked"
require_field_bool "${missing_summary}" "missing result summary blocked" "per_file_parse_summary_available" "false"
require_field_bool "${missing_summary}" "missing result summary blocked" "parse_quality_passed" "false"
require_field_bool "${missing_summary}" "missing result summary blocked" "real_material_training_allowed" "false"
require_contains "${missing_summary}" "missing result summary blocked" '"blocked_reason"[[:space:]]*:[[:space:]]*"result_fetch_not_available"'

missing_gate="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_result_missing_job/parse-quality-gate" '{}')"
assert_external_ocr_safe "${missing_gate}" "missing result quality gate blocked"
require_field_bool "${missing_gate}" "missing result quality gate blocked" "parse_quality_passed" "false"
require_field_bool "${missing_gate}" "missing result quality gate blocked" "real_material_training_allowed" "false"
require_contains "${missing_gate}" "missing result quality gate blocked" '"blocked_reason"[[:space:]]*:[[:space:]]*"result_fetch_not_available"'

low_summary="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_quality_low_job/build-redacted-summary" '{"quality_score":0.45}')"
assert_external_ocr_safe "${low_summary}" "low summary"
require_contains "${low_summary}" "low summary" '"per_file_parse_summary_redacted"[[:space:]]*:'
require_field_bool "${low_summary}" "low summary" "per_file_parse_summary_available" "true"
require_field_bool "${low_summary}" "low summary" "parse_quality_passed" "false"

low_gate="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_quality_low_job/parse-quality-gate" '{}')"
assert_external_ocr_safe "${low_gate}" "low quality gate"
require_field_bool "${low_gate}" "low quality gate" "parse_quality_passed" "false"
require_field_bool "${low_gate}" "low quality gate" "real_material_training_allowed" "false"
require_contains "${low_gate}" "low quality gate" '"training_status"[[:space:]]*:[[:space:]]*"blocked_for_parse_quality"'
require_contains "${low_gate}" "low quality gate" '"blocked_reason"[[:space:]]*:[[:space:]]*"parse_quality_below_threshold"'

pass_summary="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_quality_pass_job/build-redacted-summary" '{"quality_score":0.92}')"
assert_external_ocr_safe "${pass_summary}" "pass summary"
require_field_bool "${pass_summary}" "pass summary" "per_file_parse_summary_available" "true"
require_field_bool "${pass_summary}" "pass summary" "parse_quality_passed" "false"
require_field_bool "${pass_summary}" "pass summary" "real_material_training_allowed" "false"
require_contains "${pass_summary}" "pass summary" '"training_status"[[:space:]]*:[[:space:]]*"blocked_for_parse_quality"'

pass_gate="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_quality_pass_job/parse-quality-gate" '{}')"
assert_external_ocr_safe "${pass_gate}" "pass quality gate"
require_field_bool "${pass_gate}" "pass quality gate" "external_ocr_completed" "true"
require_field_bool "${pass_gate}" "pass quality gate" "document_content_parsed" "true"
require_field_bool "${pass_gate}" "pass quality gate" "per_file_parse_summary_available" "true"
require_field_bool "${pass_gate}" "pass quality gate" "parse_quality_passed" "true"
require_field_bool "${pass_gate}" "pass quality gate" "real_material_training_allowed" "true"
require_contains "${pass_gate}" "pass quality gate" '"training_status"[[:space:]]*:[[:space:]]*"ready_for_real_material_training"'
require_contains "${pass_gate}" "pass quality gate" '"parse_quality_report"[[:space:]]*:'
require_contains "${pass_gate}" "pass quality gate" '"raw_content_not_exported"[[:space:]]*:[[:space:]]*true'

audit_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_quality_pass_job/audit")"
assert_external_ocr_safe "${audit_body}" "external ocr audit"
require_contains "${audit_body}" "external ocr audit" '"audit_complete"[[:space:]]*:[[:space:]]*true'

trace_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/external-ocr/jobs/v738c_quality_pass_job/source-trace")"
assert_external_ocr_safe "${trace_body}" "external ocr source trace"
require_contains "${trace_body}" "external ocr source trace" '"source_trace_complete"[[:space:]]*:[[:space:]]*true'

pass "personal training external OCR v7.38c"
