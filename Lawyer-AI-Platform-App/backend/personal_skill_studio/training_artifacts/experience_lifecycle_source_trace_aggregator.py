from personal_skill_studio.training_artifacts.experience_lifecycle_source_trace_view import build_source_trace_view


def aggregate_lifecycle_source_trace(record):
    return build_source_trace_view(record)
