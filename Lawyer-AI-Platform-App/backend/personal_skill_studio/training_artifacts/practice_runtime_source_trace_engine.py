from personal_skill_studio.training_artifacts.practice_runtime_safety_engine import v731g_safety_flags
from personal_skill_studio.training_artifacts.schemas import PracticeLoadReviewPackage, PracticeRuntimeSourceTraceBundle


def build_runtime_source_trace(
    runtime_load_id: str,
    package: PracticeLoadReviewPackage,
) -> PracticeRuntimeSourceTraceBundle:
    return PracticeRuntimeSourceTraceBundle(
        source_trace_bundle_id=f"{runtime_load_id}_source_trace_bundle",
        runtime_load_id=runtime_load_id,
        experience_package_id=package.package_id,
        lawyer_approved_package_id=f"{package.package_id}_lawyer_approved_package",
        source_review_package_id=package.package_id,
        source_training_package_id=package.source_training_package_id,
        source_skill_package_id=package.source_skill_package_id,
        inherited_source_trace_ids=package.source_trace_bundle.source_trace_ids,
        source_experience_ids=package.source_trace_bundle.source_experience_ids,
        warnings=["Practice runtime source trace inherits metadata identifiers from v7.31f review only."],
        **v731g_safety_flags(),
    )
