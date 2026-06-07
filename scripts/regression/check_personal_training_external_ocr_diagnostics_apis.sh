#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Training External OCR Diagnostics"

assert_external_ocr_diagnostics_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'api_key|token|Authorization|bearer|provider_raw_response|raw_response|resultUrl|jsonUrl'
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|full_document_text|original_text|raw_material'
  assert_absent "${body}" "${label}" 'local_path|absolute_path|file_path'
  assert_absent "${body}" "${label}" 'https://paddleocr\.aistudio-app\.com/api/v2/ocr/jobs'
  assert_absent "${body}" "${label}" 'https://www\.w3\.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy\.pdf'
}

diagnostics_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/external-ocr/diagnostics")"
assert_external_ocr_diagnostics_safe "${diagnostics_body}" "external ocr diagnostics"

BODY="${diagnostics_body}" python3 - <<'PY'
import json
import os

data = json.loads(os.environ["BODY"])
expected = {
    "credential_loaded",
    "provider_configured",
    "provider_call_allowed",
    "endpoint_reachable",
    "endpoint_head_status",
    "endpoint_head_405_is_reachable",
    "provider_connection_error_type",
    "last_safe_diagnostic_status",
}
actual = set(data)
missing = expected - actual
extra = actual - expected
if missing or extra:
    raise SystemExit(f"diagnostics key mismatch missing={sorted(missing)} extra={sorted(extra)}")
if data.get("endpoint_head_status") == 405:
    assert data.get("endpoint_reachable") is True
    assert data.get("endpoint_head_405_is_reachable") is True
if data.get("provider_connection_error_type") is not None:
    assert data["provider_connection_error_type"] in {
        "provider_http_reachable_status",
        "provider_dns_error",
        "provider_ssl_error",
        "provider_url_error",
        "provider_timeout",
        "provider_connection_refused",
        "unknown_provider_connection_error",
    }
assert "file_ref" not in data
assert "material_id" not in data
PY

PYTHONPATH="${REPO_ROOT}/Lawyer-AI-Platform-App/backend" python3 - <<'PY'
import json
import os
import socket
import ssl
from urllib import error as urlerror

from personal_skill_studio.training_artifacts import external_ocr_paddle_adapter as adapter

os.environ["PROVIDER_CALLS_ENABLED"] = "true"
os.environ["EXTERNAL_OCR_ENABLED"] = "true"
os.environ["OCR_PROVIDER_API_KEY"] = "dummy-regression-credential"

original_head_endpoint = adapter._head_endpoint
original_options_endpoint = adapter._options_endpoint
try:
    def head_405(url, timeout):
        raise urlerror.HTTPError(
            url="https://redacted.invalid",
            code=405,
            msg="safe regression method not allowed",
            hdrs=None,
            fp=None,
        )

    adapter._head_endpoint = head_405
    diagnostics = adapter.external_ocr_diagnostics()
    body = json.dumps(diagnostics, ensure_ascii=False)
    assert diagnostics["credential_loaded"] is True
    assert diagnostics["provider_configured"] is True
    assert diagnostics["provider_call_allowed"] is True
    assert diagnostics["endpoint_reachable"] is True
    assert diagnostics["endpoint_head_status"] == 405
    assert diagnostics["endpoint_head_405_is_reachable"] is True
    assert diagnostics["provider_connection_error_type"] == "provider_http_reachable_status"
    assert diagnostics["last_safe_diagnostic_status"] == "endpoint_reachable_without_raw_payload"
    assert "https://paddleocr" not in body
    assert "Authorization" not in body
    assert "bearer" not in body
    assert "raw_response" not in body
    assert "provider_raw_response" not in body
    assert "file_ref" not in body
    assert "material_id" not in body

    cases = [
        ("provider_dns_error", urlerror.URLError(socket.gaierror("safe regression dns error"))),
        ("provider_ssl_error", urlerror.URLError(ssl.SSLError("safe regression ssl error"))),
        ("provider_timeout", urlerror.URLError(socket.timeout("safe regression timeout"))),
        ("provider_connection_refused", urlerror.URLError(ConnectionRefusedError("safe regression refused"))),
        ("provider_url_error", urlerror.URLError("safe regression url error")),
    ]
    for expected, exc in cases:
        def raise_error(url, timeout, error=exc):
            raise error

        adapter._head_endpoint = raise_error
        adapter._options_endpoint = raise_error
        diagnostics = adapter.external_ocr_diagnostics()
        body = json.dumps(diagnostics, ensure_ascii=False)
        assert diagnostics["endpoint_reachable"] is False
        assert diagnostics["endpoint_head_status"] is None
        assert diagnostics["endpoint_head_405_is_reachable"] is False
        assert diagnostics["provider_connection_error_type"] == expected
        assert "https://paddleocr" not in body
        assert "Authorization" not in body
        assert "bearer" not in body
        assert "raw_response" not in body
finally:
    adapter._head_endpoint = original_head_endpoint
    adapter._options_endpoint = original_options_endpoint
    os.environ.pop("OCR_PROVIDER_API_KEY", None)
    os.environ.pop("EXTERNAL_OCR_ENABLED", None)
    os.environ.pop("PROVIDER_CALLS_ENABLED", None)
print("PASS external OCR diagnostics HEAD 405 safe reachable classification")
PY

pass "personal training external OCR diagnostics"
