from personal_skill_studio.training_artifacts.case_analysis_output_audit_engine import build_output_audit
from personal_skill_studio.training_artifacts.case_analysis_output_feedback_engine import build_output_feedback
from personal_skill_studio.training_artifacts.case_analysis_output_risk_event_engine import build_output_risk_event
from personal_skill_studio.training_artifacts.case_analysis_output_safety_engine import (
    case_analysis_output_metadata_safe,
    v733_safety_flags,
)
from personal_skill_studio.training_artifacts.case_analysis_output_source_trace_engine import build_output_source_trace
from personal_skill_studio.training_artifacts.case_analysis_output_view_builder import build_case_analysis_workbench_view
from personal_skill_studio.training_artifacts.case_analysis_skill_output_schema import build_case_analysis_skill_output_schema
from personal_skill_studio.training_artifacts.practice_load_review_gate import list_practice_load_packages
from personal_skill_studio.training_artifacts.practice_runtime_registry import list_runtime_load_records, list_usage_events
from personal_skill_studio.training_artifacts.schemas import (
    CaseAnalysisOutputFeedback,
    CaseAnalysisOutputFeedbackList,
    CaseAnalysisOutputFeedbackRequest,
    CaseAnalysisOutputRiskEvent,
    CaseAnalysisOutputRiskEventList,
    CaseAnalysisOutputRiskEventRequest,
    CaseAnalysisRuntimeOutput,
    CaseAnalysisRuntimeOutputList,
    CaseAnalysisSkillOutputSchema,
    CaseAnalysisWorkbenchView,
    CaseAnalysisWorkbenchViewList,
    V733CaseAnalysisWorkbenchStatus,
)
from personal_skill_studio.training_artifacts.storage import (
    CASE_ANALYSIS_OUTPUT_FEEDBACK_DIR,
    CASE_ANALYSIS_OUTPUT_RISK_EVENTS_DIR,
    CASE_ANALYSIS_WORKBENCH_VIEWS_DIR,
    read_payload,
    read_payloads,
    write_payload,
)


DEFAULT_VIEW_ID = "case_analysis_workbench_v733_owner"


def build_or_get_default_workbench_view() -> CaseAnalysisWorkbenchView:
    existing = _read_view(DEFAULT_VIEW_ID)
    if existing:
        return existing
    view = _build_default_view()
    write_payload(CASE_ANALYSIS_WORKBENCH_VIEWS_DIR, view.view_id, view.model_dump())
    return view


def list_workbench_views() -> dict:
    views = _all_views()
    if not views:
        views = [build_or_get_default_workbench_view()]
    return CaseAnalysisWorkbenchViewList(
        views=views,
        view_count=len(views),
        warnings=["Workbench views are schema-driven metadata views only."],
        **v733_safety_flags(),
    ).model_dump()


def get_workbench_view(view_id: str) -> dict | None:
    view = _read_view(view_id)
    if view is None and view_id == DEFAULT_VIEW_ID:
        view = build_or_get_default_workbench_view()
    return view.model_dump() if view else None


def get_workbench_schema(view_id: str) -> dict | None:
    view = _read_view(view_id)
    if view is None and view_id == DEFAULT_VIEW_ID:
        view = build_or_get_default_workbench_view()
    if view is None:
        return None
    schema = CaseAnalysisSkillOutputSchema(
        skill_id=view.skill_id,
        skill_name=view.skill_name,
        skill_version=view.skill_version,
        package_id=view.package_id,
        package_version=view.package_version,
        runtime_load_id=view.runtime_load_id,
        output_groups=view.output_groups,
        created_at=view.created_at,
        audit_id=f"{view.view_id}_schema_audit",
        source_trace_id=f"{view.view_id}_schema_source_trace",
        safety_flags=v733_safety_flags(),
        warnings=[
            "Frontend must render these output groups and outputs directly.",
            "Output titles, types, counts, and order come from this schema.",
        ],
        **v733_safety_flags(),
    )
    return schema.model_dump()


def list_workbench_outputs(view_id: str) -> dict | None:
    view = _read_view(view_id)
    if view is None and view_id == DEFAULT_VIEW_ID:
        view = build_or_get_default_workbench_view()
    if view is None:
        return None
    outputs = _view_outputs(view)
    return CaseAnalysisRuntimeOutputList(
        outputs=outputs,
        output_count=len(outputs),
        warnings=["Runtime outputs are rendered from backend schema only."],
        **v733_safety_flags(),
    ).model_dump()


def get_runtime_output(output_id: str) -> dict | None:
    output = _find_output(output_id)
    return output.model_dump() if output else None


def mark_output_reviewed(output_id: str) -> dict | None:
    view, output = _find_view_and_output(output_id)
    if view is None or output is None:
        return None
    updated = _replace_output(view, output.model_copy(update={"output_status": "reviewed"}))
    write_payload(CASE_ANALYSIS_WORKBENCH_VIEWS_DIR, updated.view_id, updated.model_dump())
    return _find_output(output_id).model_dump()


def submit_output_feedback(output_id: str, request: CaseAnalysisOutputFeedbackRequest) -> dict | None:
    output = _find_output(output_id)
    if output is None:
        return None
    feedback = build_output_feedback(output_id, request)
    if feedback is None or not case_analysis_output_metadata_safe(feedback.model_dump()):
        return None
    write_payload(CASE_ANALYSIS_OUTPUT_FEEDBACK_DIR, feedback.feedback_id, feedback.model_dump())
    _increment_output_counter(output_id, "feedback_count", "feedback_submitted")
    return feedback.model_dump()


def submit_output_risk_event(output_id: str, request: CaseAnalysisOutputRiskEventRequest) -> dict | None:
    output = _find_output(output_id)
    if output is None:
        return None
    risk_event = build_output_risk_event(output_id, request)
    if risk_event is None or not case_analysis_output_metadata_safe(risk_event.model_dump()):
        return None
    write_payload(CASE_ANALYSIS_OUTPUT_RISK_EVENTS_DIR, risk_event.risk_event_id, risk_event.model_dump())
    _increment_output_counter(output_id, "risk_event_count", "risk_flagged")
    return risk_event.model_dump()


def list_output_feedback(output_id: str) -> dict:
    records = [
        CaseAnalysisOutputFeedback(**payload)
        for payload in read_payloads(CASE_ANALYSIS_OUTPUT_FEEDBACK_DIR)
        if payload.get("output_id") == output_id
    ]
    return CaseAnalysisOutputFeedbackList(
        output_id=output_id,
        feedback=sorted(records, key=lambda item: item.created_at, reverse=True),
        feedback_count=len(records),
        warnings=["Feedback list contains metadata summaries only."],
        **v733_safety_flags(),
    ).model_dump()


def list_output_risk_events(output_id: str) -> dict:
    records = [
        CaseAnalysisOutputRiskEvent(**payload)
        for payload in read_payloads(CASE_ANALYSIS_OUTPUT_RISK_EVENTS_DIR)
        if payload.get("output_id") == output_id
    ]
    return CaseAnalysisOutputRiskEventList(
        output_id=output_id,
        risk_events=sorted(records, key=lambda item: item.created_at, reverse=True),
        risk_event_count=len(records),
        warnings=["Risk event list contains metadata summaries only."],
        **v733_safety_flags(),
    ).model_dump()


def get_output_audit(output_id: str) -> dict | None:
    if _find_output(output_id) is None:
        return None
    return build_output_audit(output_id).model_dump()


def get_output_source_trace(output_id: str) -> dict | None:
    output = _find_output(output_id)
    return build_output_source_trace(output).model_dump() if output else None


def build_v733_workbench_status() -> dict:
    views = _all_views()
    if not views:
        views = [build_or_get_default_workbench_view()]
    outputs = [output for view in views for output in _view_outputs(view)]
    return V733CaseAnalysisWorkbenchStatus(
        view_count=len(views),
        output_count=len(outputs),
        fact_group_count=sum(1 for view in views for group in view.output_groups if group.group_type == "fact_extraction"),
        legal_analysis_group_count=sum(1 for view in views for group in view.output_groups if group.group_type == "legal_analysis"),
        feedback_count=len(read_payloads(CASE_ANALYSIS_OUTPUT_FEEDBACK_DIR)),
        risk_event_count=len(read_payloads(CASE_ANALYSIS_OUTPUT_RISK_EVENTS_DIR)),
        warnings=[
            "v7.33 renders case-analysis outputs strictly from backend Skill Output Schema.",
            "It does not process source materials, call providers, train, publish, deliver, or produce final legal work.",
        ],
        **v733_safety_flags(),
    ).model_dump()


def _build_default_view() -> CaseAnalysisWorkbenchView:
    runtime_loads = list_runtime_load_records()
    usage_events = list_usage_events()
    review_packages = list_practice_load_packages().get("packages", [])
    runtime_load = runtime_loads[0] if runtime_loads else None
    review_package = _latest_approved_package(review_packages) or (review_packages[0] if review_packages else None)
    package_id = runtime_load.experience_package_id if runtime_load else _get(review_package, "package_id", "lawyer_approved_package_pending_v733")
    package_version = runtime_load.package_version if runtime_load else _get(review_package, "package_version", "v7.33.pending")
    runtime_load_id = runtime_load.runtime_load_id if runtime_load else "practice_runtime_load_pending_v733"
    runtime_load_status = runtime_load.load_status if runtime_load else "not_loaded"
    usage_event_id = usage_events[0].usage_event_id if usage_events else None
    experience_ids = _experience_ids(runtime_load, review_package)
    schema = build_case_analysis_skill_output_schema(
        package_id=package_id,
        package_version=package_version,
        runtime_load_id=runtime_load_id,
        usage_event_id=usage_event_id,
        experience_ids=experience_ids,
    )
    return build_case_analysis_workbench_view(
        case_id="owner_demo_case_schema_driven_v733",
        case_cause_name="买卖合同纠纷",
        runtime_load_status=runtime_load_status,
        skill_output_schema=schema,
    )


def _all_views() -> list[CaseAnalysisWorkbenchView]:
    return [
        CaseAnalysisWorkbenchView(**payload)
        for payload in read_payloads(CASE_ANALYSIS_WORKBENCH_VIEWS_DIR)
        if payload.get("view_id")
    ]


def _read_view(view_id: str) -> CaseAnalysisWorkbenchView | None:
    payload = read_payload(CASE_ANALYSIS_WORKBENCH_VIEWS_DIR, view_id)
    return CaseAnalysisWorkbenchView(**payload) if payload else None


def _find_output(output_id: str) -> CaseAnalysisRuntimeOutput | None:
    _view, output = _find_view_and_output(output_id)
    return output


def _find_view_and_output(output_id: str):
    views = _all_views() or [build_or_get_default_workbench_view()]
    for view in views:
        for output in _view_outputs(view):
            if output.output_id == output_id:
                return view, output
    return None, None


def _view_outputs(view: CaseAnalysisWorkbenchView) -> list[CaseAnalysisRuntimeOutput]:
    return [output for group in view.output_groups for output in group.outputs]


def _replace_output(view: CaseAnalysisWorkbenchView, replacement: CaseAnalysisRuntimeOutput) -> CaseAnalysisWorkbenchView:
    updated = view.model_copy(deep=True)
    for group in updated.output_groups:
        group.outputs = [replacement if output.output_id == replacement.output_id else output for output in group.outputs]
        group.actual_count = len(group.outputs)
    outputs = _view_outputs(updated)
    updated.summary_metrics.total_outputs = len(outputs)
    updated.summary_metrics.feedback_count = sum(output.feedback_count for output in outputs)
    updated.summary_metrics.reviewed_count = sum(1 for output in outputs if output.output_status == "reviewed")
    updated.summary_metrics.risk_flagged_count = sum(1 for output in outputs if output.risk_level in {"medium", "high"} or output.risk_event_count)
    updated.summary_metrics.high_risk_count = sum(1 for output in outputs if output.risk_level == "high")
    return updated


def _increment_output_counter(output_id: str, counter: str, status: str) -> None:
    view, output = _find_view_and_output(output_id)
    if view is None or output is None:
        return
    value = getattr(output, counter) + 1
    updated_output = output.model_copy(update={counter: value, "output_status": status})
    updated = _replace_output(view, updated_output)
    write_payload(CASE_ANALYSIS_WORKBENCH_VIEWS_DIR, updated.view_id, updated.model_dump())


def _latest_approved_package(packages: list[dict]) -> dict | None:
    for package in packages:
        if package.get("review_status") == "approved_for_practice_load":
            return package
    return None


def _experience_ids(runtime_load, review_package) -> list[str]:
    if runtime_load:
        ids = runtime_load.source_trace_bundle.source_experience_ids
        if ids:
            return ids
    cards = _get(review_package, "experience_cards", []) or []
    return [_get(card, "card_id", f"experience_card_{index}") for index, card in enumerate(cards, start=1)] or ["experience_schema_anchor_v733"]


def _get(item, key: str, default=None):
    if item is None:
        return default
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)
