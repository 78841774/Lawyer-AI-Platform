from dataclasses import dataclass

from personal_alpha_case_os.stage_routes import route_for_action

REVIEW_STATES = [
    "draft",
    "intake_ready",
    "workspace_run_ready",
    "source_review_pending",
    "source_reviewed",
    "source_decision_pending",
    "source_decision_completed",
    "final_readiness_pending",
    "final_readiness_ready",
    "final_gate_pending",
    "final_gate_approved",
    "final_packet_pending",
    "final_packet_created",
    "lawyer_final_review_pending",
    "lawyer_review_approved",
    "lawyer_review_revision_requested",
    "lawyer_review_rejected",
    "final_lock_pending",
    "final_lock_created",
    "completed_metadata_review",
    "blocked",
]

STATE_LABELS = {state: state.replace("_", " ").title() for state in REVIEW_STATES}
TERMINAL_STATES = {"completed_metadata_review", "blocked"}
BLOCKED_STATES = {"blocked"}

MANUAL_CONFIRMATIONS = ["manual_review_confirmed", "metadata_only_confirmation"]
LAWYER_CONFIRMATIONS = ["manual_review_confirmed", "lawyer_review_confirmed", "metadata_only_confirmation"]
FINAL_LOCK_CONFIRMATIONS = [
    "manual_review_confirmed",
    "lawyer_review_confirmed",
    "metadata_only_confirmation",
    "no_final_legal_opinion_confirmation",
    "no_final_report_generation_confirmation",
]


@dataclass(frozen=True)
class ReviewTransitionRule:
    from_state: str
    to_state: str
    reason: str
    target_action: str | None = None
    required_confirmations: tuple[str, ...] = ()

    @property
    def transition(self) -> str:
        return f"{self.from_state}_to_{self.to_state}"

    @property
    def target_route(self) -> str | None:
        if not self.target_action:
            return None
        return route_for_action(self.target_action)


TRANSITION_RULES = [
    ReviewTransitionRule("draft", "intake_ready", "Case metadata intake can be prepared.", "create_workspace_run", tuple(MANUAL_CONFIRMATIONS)),
    ReviewTransitionRule("intake_ready", "workspace_run_ready", "Workspace run metadata can be created after manual intake confirmation.", "create_workspace_run", tuple(MANUAL_CONFIRMATIONS)),
    ReviewTransitionRule("workspace_run_ready", "source_review_pending", "Workspace metadata is ready for source review.", "review_sources", tuple(MANUAL_CONFIRMATIONS)),
    ReviewTransitionRule("source_review_pending", "source_reviewed", "Source metadata review can be marked reviewed.", "review_sources", tuple(MANUAL_CONFIRMATIONS)),
    ReviewTransitionRule("source_reviewed", "source_decision_pending", "Reviewed source metadata is ready for a source decision.", "submit_source_review_decision", tuple(MANUAL_CONFIRMATIONS)),
    ReviewTransitionRule("source_decision_pending", "source_decision_completed", "Source review decision metadata can be recorded.", "submit_source_review_decision", tuple(MANUAL_CONFIRMATIONS)),
    ReviewTransitionRule("source_decision_completed", "final_readiness_pending", "Source decision metadata can move to final readiness preview.", "check_final_readiness", tuple(MANUAL_CONFIRMATIONS)),
    ReviewTransitionRule("final_readiness_pending", "final_readiness_ready", "Final readiness metadata can be confirmed.", "check_final_readiness", tuple(MANUAL_CONFIRMATIONS)),
    ReviewTransitionRule("final_readiness_ready", "final_gate_pending", "Readiness metadata is ready for final gate review.", "submit_final_gate_decision", tuple(LAWYER_CONFIRMATIONS)),
    ReviewTransitionRule("final_gate_pending", "final_gate_approved", "Final gate metadata decision can be approved.", "submit_final_gate_decision", tuple(LAWYER_CONFIRMATIONS)),
    ReviewTransitionRule("final_gate_approved", "final_packet_pending", "Approved gate metadata can move to final packet creation.", "create_final_packet", tuple(LAWYER_CONFIRMATIONS)),
    ReviewTransitionRule("final_packet_pending", "final_packet_created", "Final packet metadata can be created.", "create_final_packet", tuple(LAWYER_CONFIRMATIONS)),
    ReviewTransitionRule("final_packet_created", "lawyer_final_review_pending", "Final packet metadata can move to lawyer final review.", "submit_lawyer_final_review", tuple(LAWYER_CONFIRMATIONS)),
    ReviewTransitionRule("lawyer_final_review_pending", "lawyer_review_approved", "Lawyer review can approve packet metadata.", "submit_lawyer_final_review", tuple(LAWYER_CONFIRMATIONS)),
    ReviewTransitionRule("lawyer_final_review_pending", "lawyer_review_revision_requested", "Lawyer review can request packet metadata revision.", "submit_lawyer_final_review", tuple(LAWYER_CONFIRMATIONS)),
    ReviewTransitionRule("lawyer_final_review_pending", "lawyer_review_rejected", "Lawyer review can reject packet metadata.", "submit_lawyer_final_review", tuple(LAWYER_CONFIRMATIONS)),
    ReviewTransitionRule("lawyer_review_revision_requested", "final_packet_pending", "Revision request returns metadata review to packet preparation.", "create_final_packet", tuple(LAWYER_CONFIRMATIONS)),
    ReviewTransitionRule("lawyer_review_rejected", "blocked", "Rejected lawyer review metadata blocks final lock.", "resolve_blockers", tuple(LAWYER_CONFIRMATIONS)),
    ReviewTransitionRule("lawyer_review_approved", "final_lock_pending", "Approved lawyer review metadata can move to final lock preview.", "create_final_lock", tuple(FINAL_LOCK_CONFIRMATIONS)),
    ReviewTransitionRule("final_lock_pending", "final_lock_created", "Final lock can be created when lawyer review has approved packet and confirmations are present.", "create_final_lock", tuple(FINAL_LOCK_CONFIRMATIONS)),
    ReviewTransitionRule("final_lock_created", "completed_metadata_review", "Final lock metadata completes the metadata review workflow.", "view_completed_metadata_review", tuple(FINAL_LOCK_CONFIRMATIONS)),
]

RULE_BY_PAIR = {(rule.from_state, rule.to_state): rule for rule in TRANSITION_RULES}
RULES_BY_FROM: dict[str, list[ReviewTransitionRule]] = {}
for rule in TRANSITION_RULES:
    RULES_BY_FROM.setdefault(rule.from_state, []).append(rule)


def transition_name(from_state: str, to_state: str) -> str:
    return f"{from_state}_to_{to_state}"


def is_terminal_state(state: str) -> bool:
    return state in TERMINAL_STATES


def state_label(state: str) -> str:
    return STATE_LABELS.get(state, state.replace("_", " ").title())
