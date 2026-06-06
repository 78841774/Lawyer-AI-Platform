from personal_case_workspace.schemas import OCRStatus


def build_ocr_status(material_id: str) -> OCRStatus:
    return OCRStatus(
        material_id=material_id,
        ocr_job_id=f"ocr_status_{material_id}",
        warnings=[
            "OCR 状态为 mock metadata。",
            "raw OCR text 不返回、不写入 diagnostics、不注入 AI prompt。",
        ],
    )
