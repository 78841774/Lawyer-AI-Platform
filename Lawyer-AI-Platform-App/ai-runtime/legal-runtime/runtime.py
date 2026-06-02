from runtime_interface import RuntimeRequest, RuntimeResponse


class LegalRuntime:
    def run(self, request: RuntimeRequest) -> RuntimeResponse:
        return RuntimeResponse(
            status="pending",
            output_data={
                "case_id": request.case_id,
                "legal_issues": []
            },
            warnings=["Legal analysis model integration is pending."]
        )
