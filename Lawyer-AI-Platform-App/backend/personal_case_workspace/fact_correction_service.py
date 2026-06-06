from personal_case_workspace.schemas import FactCorrectionMockRequest, FactCorrectionResult, FactInputStatus


def build_fact_input(material_id: str) -> FactInputStatus:
    return FactInputStatus(
        material_id=material_id,
        fact_input_id=f"fact_input_{material_id}",
        warnings=["事实输入仅作为 metadata 草稿入口；需要律师复核和来源追踪。"],
    )


def create_fact_correction(material_id: str, request: FactCorrectionMockRequest) -> FactCorrectionResult:
    allowed = (
        request.explicit_owner_confirmation
        and request.explicit_lawyer_confirmation
        and request.explicit_no_training_data_confirmation
        and request.explicit_no_external_delivery_confirmation
    )
    return FactCorrectionResult(
        material_id=material_id,
        correction_id=f"fact_correction_{material_id}",
        correction_status="mock_fact_correction_metadata_created" if allowed else "blocked_until_confirmations",
        warnings=[
            "纠正说明不作为 raw content 返回。",
            "不写训练集、不触发 AI prompt、不生成最终法律意见。",
        ],
    )
