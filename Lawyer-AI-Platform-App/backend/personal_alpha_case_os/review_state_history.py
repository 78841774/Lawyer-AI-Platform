from typing import Any

from personal_alpha_case_os.review_state_rules import RULE_BY_PAIR
from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSReviewStateHistory,
    PersonalAlphaCaseOSReviewStateHistoryItem,
)
from personal_alpha_case_os.unified_audit_engine import build_unified_audit_timeline

EVENT_STATE_HINTS = [
    ("workspace_run", None, "draft", "intake_ready"),
    ("workspace_run", None, "intake_ready", "workspace_run_ready"),
    ("workspace_run", None, "workspace_run_ready", "source_review_pending"),
    ("source_review_decision", None, "source_review_pending", "source_reviewed"),
    ("source_review_decision", None, "source_reviewed", "source_decision_pending"),
    ("source_review_decision", None, "source_decision_pending", "source_decision_completed"),
    ("source_review_decision", None, "source_decision_completed", "final_readiness_pending"),
    ("source_review_decision", None, "final_readiness_pending", "final_readiness_ready"),
    ("source_review_decision", None, "final_readiness_ready", "final_gate_pending"),
    ("final_gate", None, "final_gate_pending", "final_gate_approved"),
    ("final_gate", None, "final_gate_approved", "final_packet_pending"),
    ("final_packet", None, "final_packet_pending", "final_packet_created"),
    ("final_packet", None, "final_packet_created", "lawyer_final_review_pending"),
    ("lawyer_final_review", "approved", "lawyer_final_review_pending", "lawyer_review_approved"),
    ("lawyer_final_review", "revision_requested", "lawyer_final_review_pending", "lawyer_review_revision_requested"),
    ("lawyer_final_review", "rejected", "lawyer_final_review_pending", "lawyer_review_rejected"),
    ("lawyer_final_review", "approved", "lawyer_review_approved", "final_lock_pending"),
    ("final_lock", None, "final_lock_pending", "final_lock_created"),
    ("final_lock", None, "final_lock_created", "completed_metadata_review"),
]


def build_review_state_history(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    timeline = build_unified_audit_timeline(case_id, context, limit=200)
    history: list[PersonalAlphaCaseOSReviewStateHistoryItem] = []
    seen_pairs: set[tuple[str, str]] = set()
    for event in timeline.get("timeline", []):
        for from_state, to_state in _states_for_event(event):
            pair = (from_state, to_state)
            if pair in seen_pairs or pair not in RULE_BY_PAIR:
                continue
            seen_pairs.add(pair)
            rule = RULE_BY_PAIR[pair]
            history.append(
                PersonalAlphaCaseOSReviewStateHistoryItem(
                    state_history_id=f"state_history_{len(history) + 1:03d}",
                    from_state=from_state,
                    to_state=to_state,
                    transition=rule.transition,
                    result="metadata_transition_available",
                    source_event_id=str(event.get("timeline_event_id", "")),
                    stage_id=str(event.get("stage_id", "case_os")),
                    module=str(event.get("module", "personal_alpha_case_os")),
                    mock_or_redacted_only=True,
                    raw_content_included=False,
                    created_at=str(event.get("created_at", "")),
                )
            )
    return PersonalAlphaCaseOSReviewStateHistory(
        case_id=case_id,
        history=history,
        history_count=len(history),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Review state history is derived from metadata-only audit events."],
    ).model_dump()


def _states_for_event(event: dict[str, Any]) -> list[tuple[str, str]]:
    stage_id = str(event.get("stage_id", ""))
    result = str(event.get("result", ""))
    pairs = []
    for hint_stage, hint_result, from_state, to_state in EVENT_STATE_HINTS:
        if stage_id != hint_stage:
            continue
        if hint_result and result != hint_result:
            continue
        pairs.append((from_state, to_state))
    return pairs
