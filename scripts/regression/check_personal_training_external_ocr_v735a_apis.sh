#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Training External OCR v7.35a"

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

require_true_field() {
  local body="$1"
  local label="$2"
  local field="$3"
  if ! python3 -c 'import json,sys; data=json.loads(sys.stdin.read()); sys.exit(0 if data.get(sys.argv[1]) is True else 1)' "${field}" <<<"${body}"; then
    fail "${label} expected ${field}=true"
  fi
}

require_false_field() {
  local body="$1"
  local label="$2"
  local field="$3"
  if ! python3 -c 'import json,sys; data=json.loads(sys.stdin.read()); sys.exit(0 if data.get(sys.argv[1]) is False else 1)' "${field}" <<<"${body}"; then
    fail "${label} expected ${field}=false"
  fi
}

require_exact_keys() {
  local body="$1"
  local label="$2"
  shift 2
  BODY="${body}" python3 - "$label" "$@" <<'PY'
import json
import os
import sys

data = json.loads(os.environ["BODY"])
label = sys.argv[1]
expected = set(sys.argv[2:])
actual = set(data)
if actual != expected:
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    raise SystemExit(f"{label} key mismatch missing={missing} extra={extra}")
PY
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
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|private_key|access_token|refresh_token|provider_response|provider_raw_response|raw_response|resultUrl|jsonUrl|unredacted'
  assert_absent "${body}" "${label}" 'Authorization|bearer|Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '\btoken\b'
  assert_absent "${body}" "${label}" 'https://www\.w3\.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy\.pdf'
  assert_absent "${body}" "${label}" 'File not found'
}

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/external-ocr/status")"
assert_external_ocr_safe "${status_body}" "external ocr status"
require_exact_keys "${status_body}" "external ocr status" provider_type credential_alias credential_loaded provider_configured provider_call_allowed last_check_status redacted_error_summary
require_contains "${status_body}" "external ocr status" '"provider_type"[[:space:]]*:[[:space:]]*"external_ocr"'
require_contains "${status_body}" "external ocr status" '"credential_alias"[[:space:]]*:'
require_contains "${status_body}" "external ocr status" '"credential_loaded"[[:space:]]*:'
require_contains "${status_body}" "external ocr status" '"provider_configured"[[:space:]]*:'
require_contains "${status_body}" "external ocr status" '"provider_call_allowed"[[:space:]]*:'
require_contains "${status_body}" "external ocr status" '"last_check_status"[[:space:]]*:'
require_contains "${status_body}" "external ocr status" '"redacted_error_summary"[[:space:]]*:'

test_url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

submit_body="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/submit" "{\"material_id\":\"material_alpha\",\"file_url\":\"${test_url}\"}")"
assert_external_ocr_safe "${submit_body}" "external ocr submit material id"
require_contains "${submit_body}" "external ocr submit material id" '"ocr_mode"[[:space:]]*:[[:space:]]*"external_ocr(_failed)?"'
require_contains "${submit_body}" "external ocr submit material id" '"parse_status"[[:space:]]*:[[:space:]]*"(blocked|failed|submitted)"'
require_contains "${submit_body}" "external ocr submit material id" '"provider_job_id"[[:space:]]*:'
require_contains "${submit_body}" "external ocr submit material id" '"provider_connection_error_type"[[:space:]]*:'
require_contains "${submit_body}" "external ocr submit material id" '"file_ref"[[:space:]]*:'
require_contains "${submit_body}" "external ocr submit material id" '"credential_loaded"[[:space:]]*:'
require_contains "${submit_body}" "external ocr submit material id" '"provider_call_allowed"[[:space:]]*:'
require_false_field "${submit_body}" "external ocr submit material id" "external_ocr_completed"
require_false_field "${submit_body}" "external ocr submit material id" "document_content_parsed"
require_false_field "${submit_body}" "external ocr submit material id" "per_file_parse_summary_available"
require_false_field "${submit_body}" "external ocr submit material id" "parse_quality_passed"
require_false_field "${submit_body}" "external ocr submit material id" "real_material_training_allowed"
require_contains "${submit_body}" "external ocr submit material id" '"training_status"[[:space:]]*:[[:space:]]*"blocked_for_external_ocr"'

file_url_body="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/submit" "{\"material_id\":\"material_beta\",\"fileUrl\":\"${test_url}\"}")"
assert_external_ocr_safe "${file_url_body}" "external ocr submit fileUrl"
require_contains "${file_url_body}" "external ocr submit fileUrl" '"parse_status"[[:space:]]*:[[:space:]]*"(blocked|failed|submitted)"'
require_contains "${file_url_body}" "external ocr submit fileUrl" '"provider_connection_error_type"[[:space:]]*:'
require_false_field "${file_url_body}" "external ocr submit fileUrl" "external_ocr_completed"
require_false_field "${file_url_body}" "external ocr submit fileUrl" "real_material_training_allowed"

file_path_or_url_body="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/submit" "{\"material_id\":\"material_gamma\",\"file_path_or_url\":\"${test_url}\"}")"
assert_external_ocr_safe "${file_path_or_url_body}" "external ocr submit file_path_or_url"
require_contains "${file_path_or_url_body}" "external ocr submit file_path_or_url" '"parse_status"[[:space:]]*:[[:space:]]*"(blocked|failed|submitted)"'
require_contains "${file_path_or_url_body}" "external ocr submit file_path_or_url" '"provider_connection_error_type"[[:space:]]*:'
require_false_field "${file_path_or_url_body}" "external ocr submit file_path_or_url" "external_ocr_completed"
require_false_field "${file_path_or_url_body}" "external ocr submit file_path_or_url" "real_material_training_allowed"

path_submit_body="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/submit" '{"file_path_or_url":"/Users/example/should-not-return.pdf"}')"
assert_external_ocr_safe "${path_submit_body}" "external ocr submit local path blocked"
require_contains "${path_submit_body}" "external ocr submit local path blocked" '"ocr_mode"[[:space:]]*:[[:space:]]*"external_ocr_failed"'
require_contains "${path_submit_body}" "external ocr submit local path blocked" '"parse_status"[[:space:]]*:[[:space:]]*"failed"'
require_false_field "${path_submit_body}" "external ocr submit local path blocked" "external_ocr_completed"
require_false_field "${path_submit_body}" "external ocr submit local path blocked" "real_material_training_allowed"
require_contains "${path_submit_body}" "external ocr submit local path blocked" '"training_status"[[:space:]]*:[[:space:]]*"blocked_for_external_ocr"'
require_contains "${path_submit_body}" "external ocr submit local path blocked" '"redacted_error_summary"[[:space:]]*:[[:space:]]*"Invalid file reference\. Raw path was not exposed\."'

file_scheme_body="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/submit" '{"file_url":"file:///Users/example/should-not-return.pdf"}')"
assert_external_ocr_safe "${file_scheme_body}" "external ocr submit file scheme blocked"
require_contains "${file_scheme_body}" "external ocr submit file scheme blocked" '"ocr_mode"[[:space:]]*:[[:space:]]*"external_ocr_failed"'
require_contains "${file_scheme_body}" "external ocr submit file scheme blocked" '"parse_status"[[:space:]]*:[[:space:]]*"failed"'
require_false_field "${file_scheme_body}" "external ocr submit file scheme blocked" "external_ocr_completed"
require_false_field "${file_scheme_body}" "external ocr submit file scheme blocked" "real_material_training_allowed"
require_contains "${file_scheme_body}" "external ocr submit file scheme blocked" '"redacted_error_summary"[[:space:]]*:[[:space:]]*"Invalid file reference\. Raw path was not exposed\."'

unknown_file_ref_body="$(post_json "/personal-skill-studio/training-artifacts/external-ocr/jobs/submit" '{"fileRef":"unknown_controlled_ref_v735a"}')"
assert_external_ocr_safe "${unknown_file_ref_body}" "external ocr submit unknown fileRef blocked"
require_contains "${unknown_file_ref_body}" "external ocr submit unknown fileRef blocked" '"ocr_mode"[[:space:]]*:[[:space:]]*"external_ocr_failed"'
require_contains "${unknown_file_ref_body}" "external ocr submit unknown fileRef blocked" '"parse_status"[[:space:]]*:[[:space:]]*"failed"'
require_false_field "${unknown_file_ref_body}" "external ocr submit unknown fileRef blocked" "external_ocr_completed"
require_false_field "${unknown_file_ref_body}" "external ocr submit unknown fileRef blocked" "real_material_training_allowed"
require_contains "${unknown_file_ref_body}" "external ocr submit unknown fileRef blocked" '"redacted_error_summary"[[:space:]]*:[[:space:]]*"Controlled file reference not found\."'

body="$(post_json "/personal-skill-studio/training-artifacts/training-materials/external-ocr/parse" '{"task_id":"regression_external_ocr_v735a","provider_alias":"REGRESSION_OCR_CREDENTIAL","training_material_files":["material_alpha","/Users/example/should-not-return.pdf"],"explicit_authorized_training_material_confirmation":true,"explicit_external_ocr_confirmation":true,"explicit_no_source_payload_return_confirmation":true}')"
assert_external_ocr_safe "${body}" "external ocr blocked run"
require_contains "${body}" "external ocr blocked run" '"ocr_mode"[[:space:]]*:[[:space:]]*"external_ocr"'
require_contains "${body}" "external ocr blocked run" '"parse_status"[[:space:]]*:[[:space:]]*"failed"'
require_contains "${body}" "external ocr blocked run" '"training_status"[[:space:]]*:[[:space:]]*"blocked_for_external_ocr"'
require_contains "${body}" "external ocr blocked run" '"per_file_parse_summary"[[:space:]]*:'
require_contains "${body}" "external ocr blocked run" '"source_trace"[[:space:]]*:'
require_false_field "${body}" "external ocr blocked run" "credential_loaded"
require_false_field "${body}" "external ocr blocked run" "external_ocr_completed"
require_false_field "${body}" "external ocr blocked run" "document_content_parsed"
require_true_field "${body}" "external ocr blocked run" "per_file_parse_summary_available"
require_false_field "${body}" "external ocr blocked run" "parse_quality_passed"

run_id="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("external_ocr_run_id",""))' <<<"${body}")"
[ -n "${run_id}" ] || fail "missing external_ocr_run_id"

list_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-materials/external-ocr/runs")"
assert_external_ocr_safe "${list_body}" "external ocr run list"
require_contains "${list_body}" "external ocr run list" '"run_count"[[:space:]]*:[[:space:]]*[1-9]'

detail_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-materials/external-ocr/runs/${run_id}")"
assert_external_ocr_safe "${detail_body}" "external ocr run detail"
require_contains "${detail_body}" "external ocr run detail" '"training_status"[[:space:]]*:[[:space:]]*"blocked_for_external_ocr"'

PYTHONPATH="${REPO_ROOT}/Lawyer-AI-Platform-App/backend" python3 - <<'PY'
import json
import os
import tempfile
from pathlib import Path

from personal_skill_studio.training_artifacts import external_ocr_training_runtime as runtime

with tempfile.TemporaryDirectory() as tmpdir:
    secret_file = Path(tmpdir) / "provider_secrets.local.json"
    secret_file.write_text(
        json.dumps(
            {
                "credentials": {"BAIDU_PADDLE_AI_STUDIO_API_KEY": "loaded-for-regression-only"},
                "adapters": {"TRAINING_EXTERNAL_OCR_ADAPTER_URL": "http://adapter.invalid/ocr"},
            }
        ),
        encoding="utf-8",
    )
    os.environ["LAWYER_AI_PROVIDER_SECRETS_FILE"] = str(secret_file)

    original = runtime._call_provider_gated_loader
    captured = {}


    def safe_loader(adapter_url, task_id, provider_alias, material_refs):
        captured["material_refs"] = material_refs
        captured["adapter_url"] = adapter_url
        return {
            "payload": {
                "parse_status": "completed",
                "redacted_summary": {"summary_status": "available", "case_material": "redacted_metadata_only"},
                "per_file_parse_summary": [
                    {
                        "file_ref_id": material_refs[0]["file_ref_id"],
                        "parse_status": "completed",
                        "redacted_summary": "外部 OCR 已返回脱敏摘要 metadata。",
                    }
                ],
                "source_trace": [
                    {
                        "file_ref_id": material_refs[0]["file_ref_id"],
                        "trace_status": "complete_metadata_only",
                        "source_reference_type": "controlled_file_reference",
                    }
                ],
            }
        }


    runtime._call_provider_gated_loader = safe_loader
    completed = runtime.start_external_ocr_parse(
        {
            "task_id": "regression_external_ocr_alias_completed",
            "provider_alias": "baidu_paddle_ai_studio_placeholder",
            "training_material_files": ["/Users/example/controlled-source.pdf"],
            "explicit_authorized_training_material_confirmation": True,
            "explicit_external_ocr_confirmation": True,
            "explicit_no_source_payload_return_confirmation": True,
        }
    )
    body = json.dumps(completed, ensure_ascii=False)
    assert completed["credential_loaded"] is True
    assert completed["parse_status"] == "completed"
    assert completed["training_status"] == "ready_for_real_material_training"
    assert completed["external_ocr_completed"] is True
    assert completed["document_content_parsed"] is True
    assert completed["parse_quality_passed"] is True
    assert captured["adapter_url"] == "http://adapter.invalid/ocr"
    assert "/Users/" not in body
    assert "source_locator" not in body
    assert "API_KEY" not in body
    assert captured["material_refs"][0]["_controlled_source_locator"] == "/Users/example/controlled-source.pdf"


    def unsafe_loader(adapter_url, task_id, provider_alias, material_refs):
        return {
            "payload": {
                "parse_status": "completed",
                "redacted_summary": {"summary_status": "available", "note": "/Users/example/should-not-return.pdf"},
                "per_file_parse_summary": [],
                "source_trace": [],
            }
        }


    runtime._call_provider_gated_loader = unsafe_loader
    blocked = runtime.start_external_ocr_parse(
        {
            "task_id": "regression_external_ocr_unsafe_blocked",
            "provider_alias": "paddleocr",
            "training_material_files": ["/Users/example/controlled-source.pdf"],
            "explicit_authorized_training_material_confirmation": True,
            "explicit_external_ocr_confirmation": True,
            "explicit_no_source_payload_return_confirmation": True,
        }
    )
    blocked_body = json.dumps(blocked, ensure_ascii=False)
    assert blocked["parse_status"] == "failed"
    assert blocked["training_status"] == "blocked_for_external_ocr"
    assert "/Users/" not in blocked_body
    assert "source_locator" not in blocked_body

    runtime._call_provider_gated_loader = original
print("PASS external OCR alias, controlled source locator, and unsafe-response checks")
PY

PYTHONPATH="${REPO_ROOT}/Lawyer-AI-Platform-App/backend" python3 - <<'PY'
import json
import os

from personal_skill_studio.training_artifacts import external_ocr_paddle_adapter as adapter

os.environ["PROVIDER_CALLS_ENABLED"] = "true"
os.environ["EXTERNAL_OCR_ENABLED"] = "true"
os.environ["OCR_PROVIDER_API_KEY"] = "dummy-regression-credential"

original_exists = adapter.os.path.exists
original_post_json = adapter._post_json


def fail_if_exists_called(path):
    raise AssertionError("URL mode must not call os.path.exists")


def fake_post_json(url, payload, headers, timeout):
    assert payload["fileUrl"].startswith("https://")
    assert "Authorization" in headers
    return 200, {"data": {"jobId": "provider_job_regression_url_mode"}}


adapter.os.path.exists = fail_if_exists_called
adapter._post_json = fake_post_json
try:
    response = adapter.submit_paddle_ocr_job(
        adapter.ExternalOCRRequest(
            material_id="url_mode_regression",
            file_path_or_url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        )
    )
    body = json.dumps(response)
    assert response["parse_status"] == "submitted"
    assert response["ocr_mode"] == "external_ocr"
    assert response["external_ocr_completed"] is False
    assert response["document_content_parsed"] is False
    assert response["per_file_parse_summary_available"] is False
    assert response["parse_quality_passed"] is False
    assert response["real_material_training_allowed"] is False
    assert response["training_status"] == "blocked_for_external_ocr"
    assert response["provider_connection_error_type"] is None
    assert "https://www.w3.org" not in body
    assert "File not found" not in body
finally:
    adapter.os.path.exists = original_exists
    adapter._post_json = original_post_json
    os.environ.pop("OCR_PROVIDER_API_KEY", None)
    os.environ.pop("EXTERNAL_OCR_ENABLED", None)
    os.environ.pop("PROVIDER_CALLS_ENABLED", None)
print("PASS external OCR adapter URL mode avoids local path check")
PY

PYTHONPATH="${REPO_ROOT}/Lawyer-AI-Platform-App/backend" python3 - <<'PY'
import json
import os
import socket
from urllib import error as urlerror

from personal_skill_studio.training_artifacts import external_ocr_paddle_adapter as adapter

os.environ["PROVIDER_CALLS_ENABLED"] = "true"
os.environ["EXTERNAL_OCR_ENABLED"] = "true"
os.environ["OCR_PROVIDER_API_KEY"] = "dummy-regression-credential"

original_post_json = adapter._post_json
request = adapter.ExternalOCRRequest(
    material_id="url_mode_error_regression",
    file_path_or_url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
)
cases = [
    ("provider_url_error", lambda: urlerror.URLError("safe regression url error")),
    (
        "provider_rejected_request",
        lambda: urlerror.HTTPError(
            url="https://redacted.invalid",
            code=405,
            msg="safe regression http error",
            hdrs=None,
            fp=None,
        ),
    ),
    ("provider_timeout", lambda: TimeoutError("safe regression timeout")),
    ("provider_timeout", lambda: socket.timeout("safe regression socket timeout")),
    (
        "provider_json_decode_error",
        lambda: json.JSONDecodeError("safe regression json decode", "{}", 0),
    ),
]
try:
    for expected, exc_factory in cases:
        def raise_error(url, payload, headers, timeout, exc=exc_factory()):
            raise exc

        adapter._post_json = raise_error
        response = adapter.submit_paddle_ocr_job(request)
        body = json.dumps(response, ensure_ascii=False)
        assert response["parse_status"] == "failed"
        assert response["ocr_mode"] == "external_ocr_failed"
        assert response["provider_connection_error_type"] == expected
        assert response["external_ocr_completed"] is False
        assert response["real_material_training_allowed"] is False
        assert "https://www.w3.org" not in body
        assert "Authorization" not in body
        assert "bearer" not in body
        assert "provider_raw_response" not in body
        assert "raw_response" not in body
        assert "ocr_text" not in body
        assert "/Users/" not in body
finally:
    adapter._post_json = original_post_json
    os.environ.pop("OCR_PROVIDER_API_KEY", None)
    os.environ.pop("EXTERNAL_OCR_ENABLED", None)
    os.environ.pop("PROVIDER_CALLS_ENABLED", None)
print("PASS external OCR adapter provider connection error classification")
PY

pass "personal training external OCR v7.35a"
