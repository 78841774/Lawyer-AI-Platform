# Training Dataset Builder & Gate Compatibility v7.36

v7.36 keeps the completed v7.35 Training Dataset Builder and adds plural alias endpoints for the corrected v7.35a-v7.38 chain.

## Scope

- Reuses existing v7.35 dataset manifest, examples, task plan, and reference-only gate.
- Adds `/training-datasets/*` alias endpoints expected by the corrected pipeline.
- Does not change the already completed v7.35 `/training-dataset/*` endpoints.

## Safety

Datasets remain metadata-only and abstracted. They do not include source payloads, OCR payloads, provider payloads, credential values, filesystem locations, final legal opinions, formal reports, public links, email, or external delivery.

## Regression

- Existing: `scripts/regression/check_personal_training_dataset_v735_apis.sh`
- Added alias check: `scripts/regression/check_personal_training_dataset_v736_apis.sh`
