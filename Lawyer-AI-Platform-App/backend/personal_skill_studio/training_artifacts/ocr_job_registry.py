from personal_skill_studio.training_artifacts.experience_candidate_safety_engine import v731b_safety_flags
from personal_skill_studio.training_artifacts.ocr_parse_engine import build_ocr_job
from personal_skill_studio.training_artifacts.schemas import OcrJob, OcrJobList, OcrJobRequest
from personal_skill_studio.training_artifacts.storage import OCR_JOBS_DIR, read_payload, read_payloads, write_payload


def create_ocr_job(request: OcrJobRequest) -> dict:
    job = build_ocr_job(request)
    write_payload(OCR_JOBS_DIR, job.job_id, job.model_dump())
    return job.model_dump()


def list_ocr_jobs() -> dict:
    jobs = [OcrJob(**payload) for payload in read_payloads(OCR_JOBS_DIR)]
    return OcrJobList(
        ocr_jobs=jobs,
        job_count=len(jobs),
        warnings=["OCR jobs expose demo-safe parse summaries only."],
        **v731b_safety_flags(),
    ).model_dump()


def get_ocr_job(job_id: str) -> dict | None:
    payload = read_payload(OCR_JOBS_DIR, job_id)
    if payload:
        return OcrJob(**payload).model_dump()
    for payload in read_payloads(OCR_JOBS_DIR):
        job = OcrJob(**payload)
        if job.job_id == job_id:
            return job.model_dump()
    return None
