# Raw Training Material Boundary OCR / Legal Retrieval v7.35a

v7.35a adds the controlled raw training material processing layer before redacted experience output.

## Scope

- Registers training material metadata for a controlled private processing zone.
- Runs OCR, document parse, judgment structuring, lawyer work-product structuring, evidence indexing, legal retrieval metadata, rule alignment, and parse quality gate metadata.
- Allows unredacted source material only inside the controlled processing zone.
- Returns only status, redacted summaries, quality scores, audit ids, and source trace ids.

## Safety

- No source text or OCR payload is returned.
- No filesystem location is returned.
- No provider call is executed.
- No credential value is read or returned.
- No training, Skill publishing, runtime package replacement, final legal opinion, formal report, public link, email, or external delivery is triggered.

## APIs

Prefix: `/personal-skill-studio/training-artifacts`

- `GET /training-materials/raw-boundary/status`
- `POST /training-materials/register`
- `GET /training-materials`
- `POST /training-materials/ocr-jobs/run`
- `POST /training-materials/document-parse-jobs/run`
- `POST /training-materials/structure-jobs/run`
- `POST /training-materials/legal-retrieval-jobs/run`
- `POST /training-materials/rule-alignment/run`
- `POST /training-materials/parse-quality-gate/run`
- `GET /v7-35a/status`

## Regression

- `scripts/regression/check_personal_raw_training_material_v735a_apis.sh`
