from personal_skill_studio.training_artifacts.experience_candidate_safety_engine import v731b_safety_flags
from personal_skill_studio.training_artifacts.legal_retrieval_engine import build_legal_retrieval_job
from personal_skill_studio.training_artifacts.schemas import LegalRetrievalJob, LegalRetrievalJobList, LegalRetrievalJobRequest
from personal_skill_studio.training_artifacts.storage import LEGAL_RETRIEVAL_JOBS_DIR, read_payload, read_payloads, write_payload


def create_legal_retrieval_job(request: LegalRetrievalJobRequest) -> dict:
    job = build_legal_retrieval_job(request)
    write_payload(LEGAL_RETRIEVAL_JOBS_DIR, job.retrieval_job_id, job.model_dump())
    return job.model_dump()


def list_legal_retrieval_jobs() -> dict:
    jobs = [LegalRetrievalJob(**payload) for payload in read_payloads(LEGAL_RETRIEVAL_JOBS_DIR)]
    return LegalRetrievalJobList(
        legal_retrieval_jobs=jobs,
        job_count=len(jobs),
        warnings=["Legal retrieval jobs expose demo-safe candidates only."],
        **v731b_safety_flags(),
    ).model_dump()


def get_legal_retrieval_job(job_id: str) -> dict | None:
    payload = read_payload(LEGAL_RETRIEVAL_JOBS_DIR, job_id)
    if payload:
        return LegalRetrievalJob(**payload).model_dump()
    for payload in read_payloads(LEGAL_RETRIEVAL_JOBS_DIR):
        job = LegalRetrievalJob(**payload)
        if job.retrieval_job_id == job_id:
            return job.model_dump()
    return None
