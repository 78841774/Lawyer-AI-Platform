#!/usr/bin/env python3
"""Local v3.4-C real case intake E2E validation.

This script uses only sanitized temporary text files. It does not write test
materials into the repository.
"""

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
        case_id = case["case_id"]
        print(f"created case_id: {case_id}")

        before_status = client.get(f"/cases/{case_id}/intake/status", headers=headers)
        print_status("intake status before materials", before_status)

        materials = upload_temp_materials(client, headers, case_id)
        print(f"materials count: {len(materials)}")
        print("sample material relative_paths:")
        for material in materials[:4]:
            print(f"- {material.get('relative_path')}")

        after_status = client.get(f"/cases/{case_id}/intake/status", headers=headers)
        print_status("intake status after materials", after_status)

        facts_result = client.post(f"/cases/{case_id}/facts/extract", headers=headers)
        facts = facts_result.get("facts", [])
        print(f"facts count: {len(facts)}")
        print(f"fact source_refs sample: {summarize_source_refs(facts[0].get('source_refs') if facts else None)}")

        analysis = client.post(f"/cases/{case_id}/analysis/run", headers=headers)
        analyses = client.get(f"/cases/{case_id}/analysis", headers=headers).get("analyses", [])
        print(f"analysis count: {len(analyses)}")
        print(f"analysis_id: {analysis.get('analysis_id') or (analyses[-1].get('analysis_id') if analyses else '暂无')}")

        report = client.post(f"/cases/{case_id}/reports/generate", headers=headers)
        reports = client.get(f"/cases/{case_id}/reports", headers=headers).get("reports", [])
        latest_report = report if isinstance(report, dict) else (reports[-1] if reports else {})
        print(f"report_id: {latest_report.get('report_id', '暂无')}")
        print(f"source_refs summary: {summarize_source_refs(latest_report.get('source_refs'))}")
        print(
            "llm_provider / llm_status: "
            f"{latest_report.get('llm_provider') or latest_report.get('source_refs', {}).get('llm_provider') or facts_result.get('llm_provider') or '暂无'} / "
            f"{latest_report.get('llm_status') or latest_report.get('source_refs', {}).get('llm_status') or facts_result.get('llm_status') or '暂无'}"
        )

        final_status = client.get(f"/cases/{case_id}/intake/status", headers=headers)
        print_status("final intake status", final_status)
        print(f"next_recommended_action: {final_status.get('next_recommended_action')}")
        return 0
    except ConnectionError as exc:
        print(f"Backend is not available: {exc}", file=sys.stderr)
        print("Start local backend on http://127.0.0.1:8001 and retry.", file=sys.stderr)
        return 1
    except HttpError as exc:
        print(f"HTTP error: {exc}", file=sys.stderr)
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
        "title": "v3.4-C 真实案件录入闭环测试",
        "case_type": "contract_dispute",
        "description": "用于验证真实案件录入、文件夹材料上传、事实抽取、法律分析和报告生成闭环的脱敏样本。",
        "jurisdiction": "CN",
        "client_name": "测试客户A",
        "opposing_party": "测试相对方B",
        "counterparty_name": "测试相对方B",
        "priority": "normal",
        "tags": ["合同", "付款争议", "v3.4-C"],
        "objective": "验证 intake 到报告生成的闭环。",
        "intake_notes": "本地脱敏测试样本，不含真实客户信息。"
    }
    return client.post("/cases", payload, headers=headers)


def upload_temp_materials(
    client: "ApiClient",
    headers: dict[str, str],
    case_id: str
) -> list[dict[str, Any]]:
    samples = [
        ("01_合同/采购合同.txt", "采购合同约定交货、验收和付款期限。"),
        ("02_履行/送货记录.txt", "送货记录显示货物已经签收。"),
        ("03_付款/付款记录.txt", "付款记录显示仍有部分货款未支付。"),
        ("04_沟通/微信沟通记录.txt", "沟通记录显示双方曾协商延期付款。")
    ]
    with tempfile.TemporaryDirectory() as temp_dir:
        files: list[tuple[str, Path, str]] = []
        for relative_path, content in samples:
            file_path = Path(temp_dir) / relative_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            files.append((relative_path, file_path, "document"))

        try:
            return client.post_multipart(
                f"/cases/{case_id}/materials/batch",
                files=files,
                fields={"upload_batch_id": f"v34c_{uuid.uuid4().hex[:8]}"},
                headers=headers
            )
        except HttpError as exc:
            if exc.status not in {404, 405}:
                raise
            print("batch upload API not found, fallback to single upload if supported")
            uploaded = []
            for relative_path, file_path, material_type in files:
                uploaded.append(
                    client.post_multipart(
                        f"/cases/{case_id}/materials",
                        files=[(relative_path, file_path, material_type)],
                        fields={"relative_path": relative_path, "material_type": material_type},
                        headers=headers,
                        single_file_field=True
                    )
                )
            return uploaded


def print_status(label: str, status: dict[str, Any]) -> None:
    print(
        f"{label}: "
        f"materials={status.get('materials_count')} "
        f"facts={status.get('facts_count')} "
        f"analyses={status.get('analyses_count')} "
        f"reports={status.get('reports_count')} "
        f"next={status.get('next_recommended_action')}"
    )


def summarize_source_refs(value: Any) -> str:
    if not value:
        return "暂无"
    if isinstance(value, dict):
        keys = ["material_id", "filename", "relative_path", "fact_ids", "analysis_id", "llm_provider", "llm_status"]
        parts = [f"{key}={value.get(key)}" for key in keys if value.get(key) is not None]
        material_refs = value.get("material_refs")
        if isinstance(material_refs, list):
            first_ref = material_refs[0] if material_refs else {}
            parts.append(
                "material_refs="
                f"{len(material_refs)}"
                f" first_relative_path={first_ref.get('relative_path') if isinstance(first_ref, dict) else '暂无'}"
            )
        return "; ".join(parts) if parts else json.dumps(value, ensure_ascii=False)
    return str(value)


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.opener = request.build_opener(request.ProxyHandler({}))

    def get(self, path: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
        return self._send("GET", path, headers=headers)

    def post(
        self,
        path: str,
        payload: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        body = json.dumps(payload or {}).encode("utf-8")
        request_headers = {"Content-Type": "application/json", **(headers or {})}
        return self._send("POST", path, body=body, headers=request_headers)

    def post_multipart(
        self,
        path: str,
        *,
        files: list[tuple[str, Path, str]],
        fields: dict[str, str],
        headers: dict[str, str],
        single_file_field: bool = False
    ) -> Any:
        boundary = f"----v34c-{uuid.uuid4().hex}"
        body = build_multipart_body(
            boundary=boundary,
            files=files,
            fields=fields,
            single_file_field=single_file_field
        )
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
            with self.opener.open(req, timeout=30) as response:
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
    fields: dict[str, str],
    single_file_field: bool
) -> bytes:
    chunks: list[bytes] = []
    for key, value in fields.items():
        add_field(chunks, boundary, key, value)

    for relative_path, file_path, material_type in files:
        field_name = "file" if single_file_field else "files"
        add_file(chunks, boundary, field_name, file_path)
        if not single_file_field:
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
