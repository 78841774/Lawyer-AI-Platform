from datetime import UTC, datetime
from uuid import uuid4

from personal_skill_studio.training_artifacts.schemas import (
    SkillExperienceBinding,
    SkillExperienceBindingList,
    SkillExperienceBindingRequest,
)
from personal_skill_studio.training_artifacts.skill_experience_pool import mark_entries_bound, read_entries_by_ids
from personal_skill_studio.training_artifacts.skill_experience_safety_engine import v731c_safety_flags
from personal_skill_studio.training_artifacts.storage import SKILL_EXPERIENCE_BINDINGS_DIR, read_payload, read_payloads, write_payload


def create_binding(request: SkillExperienceBindingRequest) -> dict:
    entries = read_entries_by_ids(request.experience_ids)
    experience_ids = [entry.experience_id for entry in entries]
    now = _now()
    binding = SkillExperienceBinding(
        binding_id=f"skill_exp_binding_v731c_{uuid4().hex[:10]}",
        experience_ids=experience_ids,
        skill_domain=request.skill_domain,
        skill_name_candidate=request.skill_name_candidate,
        case_cause_scope=request.case_cause_scope,
        experience_types=request.experience_types or sorted({entry.experience_type for entry in entries}),
        draft_target_id=request.draft_target_id,
        created_at=now,
        updated_at=now,
        warnings=["Binding prepares approved experience metadata for draft construction only."],
        **v731c_safety_flags(),
    )
    write_payload(SKILL_EXPERIENCE_BINDINGS_DIR, binding.binding_id, binding.model_dump())
    mark_entries_bound(experience_ids)
    return binding.model_dump()


def list_bindings() -> dict:
    bindings = _all_bindings()
    return SkillExperienceBindingList(
        bindings=bindings,
        binding_count=len(bindings),
        warnings=["Bindings do not publish Skills or trigger training."],
        **v731c_safety_flags(),
    ).model_dump()


def get_binding(binding_id: str) -> dict | None:
    binding = _read_binding(binding_id)
    return binding.model_dump() if binding else None


def read_binding(binding_id: str) -> SkillExperienceBinding | None:
    return _read_binding(binding_id)


def _read_binding(binding_id: str) -> SkillExperienceBinding | None:
    payload = read_payload(SKILL_EXPERIENCE_BINDINGS_DIR, binding_id)
    if payload:
        return SkillExperienceBinding(**payload)
    return None


def _all_bindings() -> list[SkillExperienceBinding]:
    return [SkillExperienceBinding(**payload) for payload in read_payloads(SKILL_EXPERIENCE_BINDINGS_DIR)]


def _now() -> str:
    return datetime.now(UTC).isoformat()
