from runtime_interface import RuntimeRequest, RuntimeResponse


class FactRuntime:
    def run(self, request: RuntimeRequest) -> RuntimeResponse:
        return RuntimeResponse(
            status="pending",
            output_data={
                "case_id": request.case_id,
                "facts": []
            },
            warnings=["Fact extraction model integration is pending."]
        )
