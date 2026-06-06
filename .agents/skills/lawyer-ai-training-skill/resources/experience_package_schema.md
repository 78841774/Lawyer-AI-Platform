# Experience Package Schema

CaseAnalysisExperiencePackage must stay unified while separating substantive and procedural experience boundaries.

## Required Structure

```text
CaseAnalysisExperiencePackage
  common_framework
  substantive_experience_profiles
  procedural_experience_profiles
  profile_loading_contract
  audit
  source_trace
  safety_flags
```

## Substantive Experience

`substantive_experience_profiles` may be referenced across procedures only when all of the following match or are explainable:

- case_cause or same case-cause hierarchy
- substantive_issue
- fact_pattern
- evidence_pattern
- usage_boundary
- audit and source trace

Each substantive profile must include source_procedure_type, source_procedure_stage, runtime_reference_type, usage_boundary, audit_id, and source_trace_id.

## Procedural Experience

`procedural_experience_profiles` must match procedure_type + procedure_stage exactly.

Procedural experience must not be used across procedures or stages. If procedure_type or procedure_stage is unclear, route to manual confirmation / review queue.

## Differentiation Output

Training output must differentiate:

- case-cause-specific fact points
- substantive legal points
- required material patterns
- evidence review points
- procedural transition rules
- substantive impact points
- risk warnings
