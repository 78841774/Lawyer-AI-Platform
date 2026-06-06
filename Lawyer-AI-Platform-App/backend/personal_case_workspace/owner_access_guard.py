from personal_case_workspace.schemas import OwnerRawViewRequest, OwnerRawViewResponse


def build_owner_raw_view_response(material_id: str, request: OwnerRawViewRequest) -> OwnerRawViewResponse:
    allowed = (
        request.explicit_owner_confirmation
        and request.explicit_no_external_delivery_confirmation
        and request.explicit_no_training_data_confirmation
        and request.explicit_no_ai_prompt_confirmation
    )
    return OwnerRawViewResponse(
        material_id=material_id,
        owner_confirmation_received=allowed,
        owner_raw_view_allowed=allowed,
        owner_raw_view_status="owner_metadata_gate_passed" if allowed else "blocked_until_owner_confirmation",
        warnings=[
            "即使确认通过，API 仍不返回真实 raw content。",
            "owner-only 查看动作不会写 Git/docs/diagnostics/regression output。",
        ],
    )
