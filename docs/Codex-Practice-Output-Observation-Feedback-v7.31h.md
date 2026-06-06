# Codex Practice Output Observation & Lawyer Feedback v7.31h

v7.31h adds practice runtime output observation and lawyer feedback metadata after v7.31g controlled loading.

## Scope

- Backend modules: `practice_output_observation.py`, `practice_lawyer_feedback.py`, `practice_feedback_registry.py`, `practice_risk_event_registry.py`, `practice_feedback_classifier.py`, `practice_feedback_audit_engine.py`, `practice_feedback_source_trace_engine.py`, and `practice_feedback_safety_engine.py`.
- API prefix: `/personal-skill-studio/training-artifacts/practice-output-observations`, `/practice-lawyer-feedback`, and `/practice-risk-events`.
- Regression script: `scripts/regression/check_personal_practice_feedback_v731h_apis.sh`.

## Feedback Flow

- Start from v7.31g runtime usage event metadata.
- Record redacted output observation metadata.
- Collect lawyer feedback metadata linked to the observation, usage event, runtime load, and package.
- Classify feedback by rule only; no provider call is made.
- Record risk event metadata when needed.
- Produce a feedback summary for later v7.31i iteration candidate preparation.

## Boundaries

- v7.31h does not modify loaded packages.
- v7.31h does not automatically disable or rollback packages.
- v7.31h does not update Skills, trigger training, publish Skills, generate final legal opinions, generate final reports, create public links, send email, or externally deliver anything.
- Feedback and risk events are candidate signals only; v7.31g controls remain the only disable/rollback path.
