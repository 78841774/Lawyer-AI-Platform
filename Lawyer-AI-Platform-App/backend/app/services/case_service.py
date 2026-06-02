from app.models.case import Case


class CaseService:
    def create_demo_case(self) -> Case:
        return Case(
            case_id="demo-case",
            title="Software Development Contract Dispute",
            case_type="contract_dispute",
            status="draft"
        )
