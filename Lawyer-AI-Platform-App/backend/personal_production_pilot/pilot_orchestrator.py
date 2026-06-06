from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_production_pilot.audit_engine import record_audit_event
from personal_production_pilot.document_output_engine import create_mock_output
from personal_production_pilot.owner_download_engine import create_owner_download
from personal_production_pilot.pilot_registry import get_runtime_ids
from personal_production_pilot.schemas import OwnerDownloadMockRequest, PilotOutputMockRequest, PilotRunList, PilotRunMockRequest, PilotRunRecord
from personal_production_pilot.source_trace_engine import create_source_trace
from personal_production_pilot.storage import RUNS_DIR, read_payload, read_payloads, write_payload


def _validate_request(request: PilotRunMockRequest) -> list[str]:
    blocked: list[str] = []
    for field in [
        "explicit_owner_confirmation",
        "explicit_provider_gated_confirmation",
        "explicit_no_external_delivery_confirmation",
        "explicit_no_training_data_confirmation",
        "explicit_no_final_opinion_confirmation",
    ]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if not request.case_id.strip():
        blocked.append("case_id 不能为空")
    return blocked


def create_mock_run(request: PilotRunMockRequest) -> dict:
    blocked = _validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "pilot run 请求被阻断", "blocked_reasons": blocked})
    run_id = f"pilot_run_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    runtime_ids = request.selected_runtime_ids or get_runtime_ids()
    trace = create_source_trace(
        source_trace_id=f"pilot_source_trace_{run_id}_1",
        source_type="pilot_run_metadata",
        source_label="Personal production pilot run metadata",
        linked_object_type="pilot_run",
        linked_object_id=run_id,
        run_id=run_id,
        created_at=created_at,
    )
    output = create_mock_output(
        PilotOutputMockRequest(
            run_id=run_id,
            output_type="case_analysis_draft",
            title="案件分析草稿",
            format="Markdown",
            explicit_owner_confirmation=True,
            explicit_no_external_delivery_confirmation=True,
            explicit_no_final_opinion_confirmation=True,
        )
    )
    download = create_owner_download(
        output["output_id"],
        OwnerDownloadMockRequest(
            requested_format="Markdown",
            explicit_owner_confirmation=True,
            explicit_no_public_link_confirmation=True,
            explicit_no_email_confirmation=True,
            explicit_no_external_delivery_confirmation=True,
        ),
    )
    record = PilotRunRecord(
        run_id=run_id,
        case_id=request.case_id,
        case_alias=request.case_alias,
        workflow_scope=request.workflow_scope,
        selected_runtime_ids=runtime_ids,
        workflow_step_status={
            "materials_ocr": "gated_ready",
            "controlled_ai_analysis": "gated_ready",
            "legal_enterprise_lookup": "gated_ready",
            "skill_invocation": "metadata_ready",
            "fact_preview_correction": "draft_ready",
            "legal_analysis_draft": "draft_ready",
            "delivery_packet_draft": "draft_ready",
            "owner_download": "owner_download_metadata_ready",
        },
        case_analysis_summary_id="case_analysis_summary_metadata",
        output_ids=[output["output_id"]],
        download_ids=[download["download_id"]],
        source_trace_ids=[trace.source_trace_id],
        created_at=created_at,
        warnings=[
            "Pilot run connects v7.10-v7.17 modules as gated metadata.",
            "Real providers remain disabled by default.",
            "Owner download metadata is created without public link, email, or external delivery.",
        ],
    )
    write_payload(RUNS_DIR, run_id, record.model_dump())
    record_audit_event(action="pilot_run_mock_created", actor="system", object_type="pilot_run", object_id=run_id, timestamp=created_at)
    payload = record.model_dump()
    payload["output"] = output
    payload["owner_download"] = download
    return payload


def get_run(run_id: str) -> PilotRunRecord | None:
    payload = read_payload(RUNS_DIR, run_id)
    return PilotRunRecord(**payload) if payload else None


def list_runs() -> list[PilotRunRecord]:
    return [PilotRunRecord(**payload) for payload in read_payloads(RUNS_DIR)]


def build_run_list() -> dict:
    runs = sorted(list_runs(), key=lambda run: run.created_at, reverse=True)
    return PilotRunList(runs=runs, run_count=len(runs), warnings=["Pilot runs are owner-only, provider-gated metadata."]).model_dump()


def build_case_analysis_summary() -> dict:
    return {
        "summary_id": "case_analysis_summary_metadata",
        "fact_part": "事实预览与纠正稿 metadata ready",
        "legal_part": "法律分析草稿 metadata ready",
        "delivery_packet_part": "交付包草稿 metadata ready",
        **PilotRunList().model_dump(exclude={"runs", "run_count", "warnings"}),
        "warnings": ["Case analysis summary is metadata-only and is not a final legal opinion or formal report."],
    }
