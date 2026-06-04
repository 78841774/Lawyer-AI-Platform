#!/usr/bin/env python3
"""Local v3.5 run history and deterministic fact dedup validation."""

from __future__ import annotations

import json
import mimetypes
import os
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any
from urllib import error, parse, request


API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8001").rstrip("/")
LOCAL_USER_ID = os.environ.get("LOCAL_USER_ID", "user_local_001")
LOCAL_DEV_TOKEN = os.environ.get("LOCAL_DEV_TOKEN", "dev-local-token")


def main() -> int:
    client = ApiClient(API_BASE)
    print(f"API base: {API_BASE}")

    try:
        token = login(client)
        headers = {"Authorization": f"Bearer {token}"}
        case = create_case(client, headers)
        case_id = str(case["case_id"])
        upload_temp_materials(client, headers, case_id)

        first_extraction = client.post(f"/cases/{case_id}/facts/extract", headers=headers)
        second_extraction = client.post(f"/cases/{case_id}/facts/extract", headers=headers)
        runs = client.get(f"/cases/{case_id}/runtime-runs", headers=headers)
        latest_runs = client.get(f"/cases/{case_id}/runtime-runs/latest", headers=headers)
        assert_latest_state(runs["extraction_runs"], latest_runs["latest_extraction_run"], minimum=2)
        if second_extraction.get("facts_created_count", 0) > 0:
            raise AssertionError("second extraction created duplicate facts")
        if second_extraction.get("facts_reused_count", 0) <= 0:
            raise AssertionError("second extraction did not reuse existing facts")

        first_analysis = client.post(f"/cases/{case_id}/analysis/run", headers=headers)
        second_analysis = client.post(f"/cases/{case_id}/analysis/run", headers=headers)
        runs = client.get(f"/cases/{case_id}/runtime-runs", headers=headers)
        latest_runs = client.get(f"/cases/{case_id}/runtime-runs/latest", headers=headers)
        assert_latest_state(runs["analysis_runs"], latest_runs["latest_analysis_run"], minimum=2)

        first_report = client.post(f"/cases/{case_id}/reports/generate", headers=headers)
        second_report = client.post(f"/cases/{case_id}/reports/generate", headers=headers)
        runs = client.get(f"/cases/{case_id}/runtime-runs", headers=headers)
        latest_runs = client.get(f"/cases/{case_id}/runtime-runs/latest", headers=headers)
        assert_latest_state(runs["report_runs"], latest_runs["latest_report_run"], minimum=2)

        summary = {
            "case_id": case_id,
            "first_extraction_run_id": first_extraction.get("run_id"),
            "second_extraction_run_id": second_extraction.get("run_id"),
            "facts_created_count": second_extraction.get("facts_created_count"),
            "facts_reused_count": second_extraction.get("facts_reused_count"),
            "facts_skipped_count": second_extraction.get("facts_skipped_count"),
            "extraction_runs_count": len(runs["extraction_runs"]),
            "latest_extraction_run_id": latest_runs["latest_extraction_run"]["run_id"],
            "first_analysis_run_id": first_analysis.get("run_id"),
            "second_analysis_run_id": second_analysis.get("run_id"),
            "analysis_runs_count": len(runs["analysis_runs"]),
            "latest_analysis_run_id": latest_runs["latest_analysis_run"]["run_id"],
            "first_report_run_id": first_report.get("run_id"),
            "second_report_run_id": second_report.get("run_id"),
            "report_runs_count": len(runs["report_runs"]),
            "latest_report_run_id": latest_runs["latest_report_run"]["run_id"]
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    except ConnectionError as exc:
        print(f"Backend is not available: {exc}", file=sys.stderr)
        return 1
    except (AssertionError, HttpError, KeyError) as exc:
        print(f"v3.5 validation failed: {exc}", file=sys.stderr)
        return 1


def login(client: "ApiClient") -> str:
    payload = {"user_id": LOCAL_USER_ID, "dev_token": LOCAL_DEV_TOKEN}
    response = client.post("/auth/login", payload)
    token = response.get("access_token")
    if not token:
        raise HttpError("auth/login did not return access_token")
    return str(token)


def create_case(client: "ApiClient", headers: dict[str, str]) -> dict[str, Any]:
    payload = {
        "title": "v3.5 Run History / Fact Dedup 测试",
        "case_type": "contract_dispute",
        "description": "用于验证运行历史、latest 标记和确定性事实去重的脱敏样本。",
        "jurisdiction": "CN",
        "client_name": "测试客户A",
        "opposing_party": "测试相对方B",
        "counterparty_name": "测试相对方B",
        "priority": "normal",
        "tags": ["v3.5", "run-history", "dedup"],
        "objective": "验证多次运行不会造成事实无限重复。"
    }
    return client.post("/cases", payload, headers=headers)


def upload_temp_materials(client: "ApiClient", headers: dict[str, str], case_id: str) -> None:
    samples = [
        ("01_合同/采购合同.txt", "采购合同约定交货、验收和付款期限。"),
        ("02_付款/付款记录.txt", "付款记录显示仍有部分货款未支付。"),
        ("03_聊天/微信记录.txt", "沟通记录显示双方曾协商延期付款。")
    ]
    with tempfile.TemporaryDirectory() as temp_dir:
        files: list[tuple[str, Path, str]] = []
        for relative_path, content in samples:
            file_path = Path(temp_dir) / relative_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            files.append((relative_path, file_path, "document"))

        uploaded = client.post_multipart(
            f"/cases/{case_id}/materials/batch",
            files=files,
            fields={"upload_batch_id": f"v35_{uuid.uuid4().hex[:8]}"},
            headers=headers
        )
        if len(uploaded) != len(samples):
            raise AssertionError("folder-aware material upload count mismatch")


def assert_latest_state(runs: list[dict[str, Any]], latest_run: dict[str, Any], *, minimum: int) -> None:
    if len(runs) < minimum:
        raise AssertionError(f"expected at least {minimum} runs, got {len(runs)}")
    latest_marked = [run for run in runs if run.get("is_latest") is True]
    if len(latest_marked) != 1:
        raise AssertionError(f"expected exactly one latest run, got {len(latest_marked)}")
    if latest_run.get("run_id") != latest_marked[0].get("run_id"):
        raise AssertionError("latest endpoint does not match latest marked run")


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.opener = request.build_opener(request.ProxyHandler({}))

    def get(self, path: str, headers: dict[str, str] | None = None) -> Any:
        return self._send("GET", path, headers=headers)

    def post(
        self,
        path: str,
        payload: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None
    ) -> Any:
        body = json.dumps(payload or {}).encode("utf-8")
        request_headers = {"Content-Type": "application/json", **(headers or {})}
        return self._send("POST", path, body=body, headers=request_headers)

    def post_multipart(
        self,
        path: str,
        *,
        files: list[tuple[str, Path, str]],
        fields: dict[str, str],
        headers: dict[str, str]
    ) -> Any:
        boundary = f"----v35-{uuid.uuid4().hex}"
        body = build_multipart_body(boundary=boundary, files=files, fields=fields)
        request_headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            **headers
        }
        return self._send("POST", path, body=body, headers=request_headers)

    def _send(
        self,
        method: str,
        path: str,
        body: bytes | None = None,
        headers: dict[str, str] | None = None
    ) -> Any:
        url = parse.urljoin(f"{self.base_url}/", path.lstrip("/"))
        req = request.Request(url, data=body, headers=headers or {}, method=method)
        try:
            with self.opener.open(req, timeout=45) as response:
                data = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise HttpError(f"{method} {path} returned {exc.code}: {detail}", status=exc.code) from exc
        except error.URLError as exc:
            raise ConnectionError(str(exc.reason)) from exc
        if not data:
            return {}
        return json.loads(data)


def build_multipart_body(
    *,
    boundary: str,
    files: list[tuple[str, Path, str]],
    fields: dict[str, str]
) -> bytes:
    chunks: list[bytes] = []
    for key, value in fields.items():
        add_field(chunks, boundary, key, value)

    for relative_path, file_path, material_type in files:
        add_file(chunks, boundary, "files", file_path)
        add_field(chunks, boundary, "relative_paths", relative_path)
        add_field(chunks, boundary, "material_types", material_type)

    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks)


def add_field(chunks: list[bytes], boundary: str, name: str, value: str) -> None:
    chunks.append(f"--{boundary}\r\n".encode("utf-8"))
    chunks.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
    chunks.append(str(value).encode("utf-8"))
    chunks.append(b"\r\n")


def add_file(chunks: list[bytes], boundary: str, name: str, file_path: Path) -> None:
    filename = file_path.name
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    chunks.append(f"--{boundary}\r\n".encode("utf-8"))
    chunks.append(
        (
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8")
    )
    chunks.append(file_path.read_bytes())
    chunks.append(b"\r\n")


class HttpError(Exception):
    def __init__(self, message: str, *, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


if __name__ == "__main__":
    raise SystemExit(main())
