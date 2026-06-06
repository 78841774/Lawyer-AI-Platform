from personal_skill_studio.training_artifacts.experience_package_builder import build_experience_package
from personal_skill_studio.training_artifacts.internal_training_task_builder import (
    build_internal_training_task,
    v731e_safety_flags,
)
from personal_skill_studio.training_artifacts.schemas import (
    ExperiencePackage,
    ExperiencePackageBuildRequest,
    ExperiencePackageBuildResponse,
    ExperiencePackageList,
    TrainingPackageAudit,
    TrainingTask,
    TrainingTaskBuildRequest,
    TrainingTaskBuildResponse,
    TrainingTaskList,
    V731eTrainingPipelineStatus,
)
from personal_skill_studio.training_artifacts.storage import (
    INTERNAL_TRAINING_TASKS_DIR,
    TRAINING_PACKAGES_DIR,
    read_payload,
    read_payloads,
    write_payload,
)


def build_training_task_record(request: TrainingTaskBuildRequest) -> dict | None:
    task = build_internal_training_task(request)
    if task is None:
        return None
    write_payload(INTERNAL_TRAINING_TASKS_DIR, task.training_task_id, task.model_dump())
    return TrainingTaskBuildResponse(
        training_task=task,
        sample_count=task.sample_count,
        warnings=["Training task is built from system-validated Skill Package metadata only."],
        **v731e_safety_flags(),
    ).model_dump()


def list_training_task_records() -> dict:
    tasks = _all_tasks()
    return TrainingTaskList(
        training_tasks=tasks,
        task_count=len(tasks),
        training_completed_count=sum(1 for task in tasks if task.training_task_status == "training_completed"),
        warnings=["Training tasks contain structured, redacted metadata only."],
        **v731e_safety_flags(),
    ).model_dump()


def build_experience_package_record(request: ExperiencePackageBuildRequest) -> dict | None:
    package = build_experience_package(request)
    if package is None:
        return None
    write_payload(TRAINING_PACKAGES_DIR, package.package_id, package.model_dump())
    return ExperiencePackageBuildResponse(
        training_package=package,
        sample_count=package.sample_count,
        warnings=["Experience package is pending practice runtime load review in v7.31f."],
        **v731e_safety_flags(),
    ).model_dump()


def list_experience_package_records() -> dict:
    packages = _all_packages()
    return ExperiencePackageList(
        training_packages=packages,
        package_count=len(packages),
        pending_practice_load_review_count=sum(
            1 for package in packages if package.package_status == "pending_practice_load_review"
        ),
        warnings=["Training packages are not loaded into practice runtime until v7.31f review."],
        **v731e_safety_flags(),
    ).model_dump()


def get_experience_package_record(package_id: str) -> dict | None:
    package = _read_package(package_id)
    return package.model_dump() if package else None


def get_experience_package_audit_record(package_id: str) -> dict | None:
    package = _read_package(package_id)
    if package is None:
        return None
    return TrainingPackageAudit(
        package_id=package.package_id,
        events=package.audit_events,
        event_count=len(package.audit_events),
        warnings=["Audit bundle records internal training metadata events only."],
        **v731e_safety_flags(),
    ).model_dump()


def get_experience_package_source_trace_record(package_id: str) -> dict | None:
    package = _read_package(package_id)
    return package.source_trace_bundle.model_dump() if package else None


def build_v731e_status() -> dict:
    tasks = _all_tasks()
    packages = _all_packages()
    return V731eTrainingPipelineStatus(
        training_task_count=len(tasks),
        training_package_count=len(packages),
        pending_practice_load_review_count=sum(
            1 for package in packages if package.package_status == "pending_practice_load_review"
        ),
        warnings=[
            "v7.31e creates internal training task and experience package metadata only.",
            "Practice runtime load review is deferred to v7.31f.",
        ],
        **v731e_safety_flags(),
    ).model_dump()


def _read_package(package_id: str) -> ExperiencePackage | None:
    payload = read_payload(TRAINING_PACKAGES_DIR, package_id)
    if payload:
        return ExperiencePackage(**payload)
    return None


def _all_tasks() -> list[TrainingTask]:
    return [TrainingTask(**payload) for payload in read_payloads(INTERNAL_TRAINING_TASKS_DIR)]


def _all_packages() -> list[ExperiencePackage]:
    return [ExperiencePackage(**payload) for payload in read_payloads(TRAINING_PACKAGES_DIR)]
