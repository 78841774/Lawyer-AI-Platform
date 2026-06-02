from runtime_interface import RuntimeRequest, RuntimeResponse


class ReportRuntime:
    def run(self, request: RuntimeRequest) -> RuntimeResponse:
        return RuntimeResponse(
            status="pending",
            output_data={
                "case_id": request.case_id,
                "reports": []
            },
            warnings=["Report generation model integration is pending."]
        )
