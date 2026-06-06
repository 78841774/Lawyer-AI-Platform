# Codex Practice Feedback Candidate Pack v7.31i

v7.31i adds the Practice Feedback Candidate Pack layer for the Personal Skill Studio training artifacts route.

## Scope

- Builds next-iteration candidate pack metadata from v7.31h triaged lawyer feedback, risk events, and output observations.
- Maps feedback and risk records into experience iteration candidates.
- Produces a candidate diff covering added cards, revised cards, removed cards, narrowed or expanded usage boundaries, added risk warnings, rollback recommendations, disable recommendations, and next-version recommendation metadata.
- Preserves source package, source runtime load, feedback, risk event, observation, audit, and source-trace lineage.
- Allows a candidate pack to be marked `ready_for_next_experience_build` or `archived`.

## API

- `GET /personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/status`
- `POST /personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/build`
- `GET /personal-skill-studio/training-artifacts/practice-feedback-candidate-packs`
- `GET /personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/{candidate_pack_id}`
- `GET /personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/{candidate_pack_id}/diff`
- `GET /personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/{candidate_pack_id}/audit`
- `GET /personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/{candidate_pack_id}/source-trace`
- `POST /personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/{candidate_pack_id}/mark-ready`
- `POST /personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/{candidate_pack_id}/archive`
- `GET /personal-skill-studio/training-artifacts/v7-31i/status`

## Safety Boundary

v7.31i is metadata-only and owner-only. It does not modify loaded packages, lawyer-approved packages, runtime policy, Skills, training artifacts, or delivery state.

`ready_for_next_experience_build` only prepares the candidate pack for a later rebuild stage. v7.31i does not generate the next experience package draft and does not load any next package into practice runtime.

Provider calls, key value reads, source content exposure, final legal opinions, final reports, public links, email, and external delivery remain disabled.

## Validation

The lightweight API regression is:

`scripts/regression/check_personal_practice_feedback_candidate_pack_v731i_apis.sh`

The script first prepares v7.31h feedback metadata, then verifies build, list, detail, diff, audit, source trace, mark-ready, archive, and safety response boundaries.
