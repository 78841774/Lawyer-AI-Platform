from personal_skill_studio.training_artifacts.experience_lifecycle_lineage_graph import build_lineage
from personal_skill_studio.training_artifacts.experience_lifecycle_safety_engine import v732_safety_flags
from personal_skill_studio.training_artifacts.schemas import ExperienceLifecycleGraph, ExperienceLifecycleGraphEdge, ExperienceLifecycleGraphNode, ExperienceLifecycleRecord


def build_lifecycle_graph(record: ExperienceLifecycleRecord, training_packages: list, review_packages: list, runtime_loads: list, candidate_packs: list, next_packages: list) -> ExperienceLifecycleGraph:
    nodes = [
        ExperienceLifecycleGraphNode(
            id=event.stage_event_id,
            type="stage",
            label=event.stage_name,
            status=event.stage_status,
            created_at=event.created_at,
            **v732_safety_flags(),
        )
        for event in record.stage_events
    ]
    edges = [
        ExperienceLifecycleGraphEdge(
            from_id=record.stage_events[index - 1].stage_event_id,
            to_id=event.stage_event_id,
            relation="next_stage",
            created_at=event.created_at,
        )
        for index, event in enumerate(record.stage_events)
        if index > 0
    ]
    lineage = build_lineage(training_packages, review_packages, runtime_loads, candidate_packs, next_packages)
    for item in lineage:
        nodes.append(
            ExperienceLifecycleGraphNode(
                id=item.lineage_id,
                type=item.package_kind,
                label=item.package_id,
                status=item.lineage_status,
                version=item.package_version,
                created_at=item.created_at,
                **v732_safety_flags(),
            )
        )
        if item.parent_package_id:
            edges.append(ExperienceLifecycleGraphEdge(from_id=item.parent_package_id, to_id=item.lineage_id, relation="derived_from", created_at=item.created_at))
        if item.derived_from_candidate_pack_id:
            edges.append(ExperienceLifecycleGraphEdge(from_id=item.derived_from_candidate_pack_id, to_id=item.lineage_id, relation="rebuilt_from", created_at=item.created_at))
    return ExperienceLifecycleGraph(
        lifecycle_id=record.lifecycle_id,
        nodes=nodes,
        edges=edges,
        lineage=lineage,
        warnings=["Graph contains metadata nodes and edges only."],
        **v732_safety_flags(),
    )
