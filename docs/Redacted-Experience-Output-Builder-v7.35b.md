# Redacted Experience Output Builder v7.35b

v7.35b builds redacted and abstracted experience candidates and packages from v7.35a controlled parse metadata.

## Scope

- Builds raw-based experience candidates only after parse quality metadata is available.
- Produces redacted experience packages with experience cards, source candidate ids, parse gate ids, legal retrieval ids, rule alignment ids, audit bundle ids, and source trace bundle ids.
- Marks packages as `ready_for_training_dataset` when redaction and metadata safety checks pass.

## Safety

- Source material does not enter experience packages.
- OCR payload does not enter experience packages.
- Provider payloads and credential values are absent.
- Packages are metadata-only, redacted / abstracted, owner-only, source-traced, and audited.

## APIs

Prefix: `/personal-skill-studio/training-artifacts`

- `POST /training-materials/experience-candidates/build`
- `GET /training-materials/experience-candidates`
- `GET /training-materials/experience-candidates/{candidate_id}`
- `POST /training-materials/redacted-experience-packages/build`
- `GET /training-materials/redacted-experience-packages`
- `GET /training-materials/redacted-experience-packages/{package_id}`
- `GET /training-materials/redacted-experience-packages/{package_id}/redaction-report`
- `GET /training-materials/redacted-experience-packages/{package_id}/audit`
- `GET /training-materials/redacted-experience-packages/{package_id}/source-trace`
- `GET /v7-35b/status`

## Regression

- `scripts/regression/check_personal_redacted_experience_output_v735b_apis.sh`
