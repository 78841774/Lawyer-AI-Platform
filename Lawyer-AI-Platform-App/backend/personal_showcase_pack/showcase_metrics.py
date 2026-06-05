from datetime import datetime, timezone

from personal_showcase_pack.audit_engine import record_audit_event
from personal_showcase_pack.pilot_sample_runtime import list_pilot_samples
from personal_showcase_pack.schemas import ShowcaseMetrics
from personal_showcase_pack.story_flow_runtime import list_story_flows
from personal_showcase_pack.storage import METRICS_DIR, write_payload


def build_showcase_metrics() -> dict:
    samples = list_pilot_samples()
    flows = list_story_flows()
    now = datetime.now(timezone.utc).isoformat()
    source_trace_coverage_rate = 0
    if samples:
        source_trace_coverage_rate = int(sum(sample.source_trace_coverage for sample in samples) / len(samples))
    metrics = ShowcaseMetrics(
        pilot_sample_count=len(samples),
        story_flow_count=len(flows),
        source_trace_coverage_rate=source_trace_coverage_rate,
        lawyer_review_required_count=sum(1 for sample in samples if sample.requires_lawyer_review),
        final_lock_ready_count=sum(1 for flow in flows if bool(flow.final_lock_summary.get("final_lock_required", False))),
        updated_at=now,
        warnings=["展示指标仅基于 synthetic mock metadata，不代表正式生产数据。"],
    )
    write_payload(METRICS_DIR, "latest", metrics.model_dump())
    record_audit_event(action="metrics_viewed", actor="system", object_type="showcase_metrics", object_id="latest", timestamp=now)
    return metrics.model_dump()
