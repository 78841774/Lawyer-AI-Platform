# Safe Callable Training Skill Interface

This interface document defines how Training Skills can call OCR, legal retrieval, and enterprise APIs without storing real credentials.

## Skill Spec Contract

Each callable provider entry stores only:

- `provider_type`: `OCR_API`, `Legal_API`, or `Enterprise_API`
- `credential_alias`: backend environment variable name or credential alias
- `credential_loaded`: boolean status returned by the adapter
- `gate_requirements`: pre-call checks
- `output_schema`: metadata-only result shape
- `prompt_strategy`: instruction-generation template

## Differentiated Experience Output

The Training Skill must generate a redacted, abstracted experience package with:

- `legal_summary`: legal point summary from reviewed legal retrieval, court reasoning, issue, and rule metadata
- `facts.common_fact_extraction_framework`: shared structure only, including parties, legal relationship, timeline, right / duty source, performance / breach / damage facts, evidence mapping, disputed facts, court-accepted facts, and risk facts
- `facts.case_cause_specific_fact_points`: case-cause-specific points learned from desensitized judgment, lawyer work-product, evidence, court-reasoning, and legal-retrieval metadata
- `facts.fact_extraction_summary`: common framework plus case-cause differentiated summary
- `audit` and `source_trace`: required metadata for lawyer review

The shared template must not hardcode case-cause details. Case-cause points are learned per training material profile, such as private lending, sales contract, labor dispute, and marriage / family dispute patterns.

## Procedural And Substantive Impact Profiles

The experience package separates:

- `substantive_experience_profiles`: substantive experience organized by case cause, substantive issue, fact pattern, and evidence pattern
- `procedural_experience_profiles`: procedural experience organized strictly by procedure type and procedure stage
- `case_cause_profiles[]`: case-cause-level container that nests the matching substantive and procedural profile references

Substantive experience may cross procedure for reference only when all boundary conditions pass: case-cause hierarchy, substantive issue, fact pattern, evidence pattern, usage boundary, audit, and source trace. Procedural experience must not cross procedure or stage.

Each procedural profile includes:

- `required_material_patterns`
- `fact_extraction_points`
- `evidence_review_points`
- `legal_summary_points`
- `substantive_impact_points`
- `procedural_transition_rules`
- `risk_warnings`
- `metadata` with profile match and review requirements

Practice loading uses `case_cause_code + procedure_type + procedure_stage` to select the profile and load facts, legal points, material emphasis, substantive impact, and risk warnings. Missing procedure or stage routes to manual confirmation / review queue.

Runtime loading is two-layer:

- Substantive layer: match `case_cause + substantive_issue + fact_pattern + evidence_pattern`; may aggregate cross-procedure substantive references with source-stage labels.
- Procedural layer: match `procedure_type + procedure_stage` exactly; only exact-match procedural profiles are loaded.

Frontend display must distinguish substantive references from procedural applicability. Substantive references may show cross-procedure source stage with the warning that they are not procedural rules. Procedural experience must only appear as exact-stage applicable experience.

## Adapter Contract

The adapter:

- Loads real credentials only inside the backend secure runtime.
- Initializes provider clients only after gates pass.
- Returns `credential_loaded` and provider status metadata.
- Provides API call methods that return result metadata or blocked status.
- Records audit and source trace metadata.

The adapter never returns credential values to Training Skill, frontend, logs, docs, or regression output.

## Current Implementation

The current implementation provides provider-gated adapter placeholder APIs. They verify credential alias presence and return safe status metadata, but keep live provider execution disabled by default.

## Output Boundary

Outputs are not final legal opinions, formal reports, final citations, final fact findings, publishable Skills, or runtime-loadable packages.
