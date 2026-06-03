from app.skill_training.case_miner import MinedCase


class FactPatternExtractor:
    def extract(self, mined_case: MinedCase) -> list[dict[str, object]]:
        extracted_facts = [
            fact for fact in mined_case.facts
            if fact.status == "extracted"
        ]
        fact_types = sorted({fact.fact_type for fact in extracted_facts})
        evidence_refs = [
            {
                "fact_id": fact.fact_id,
                "material_id": fact.material_id,
                "source_text": fact.source_text or fact.content
            }
            for fact in extracted_facts
        ]

        return [
            {
                "pattern": "case_fact_inventory",
                "description": "Structured inventory of extracted case facts.",
                "fact_count": len(extracted_facts),
                "fact_types": fact_types,
                "required_fields": [
                    "parties",
                    "timeline",
                    "claims",
                    "evidence_map",
                    "missing_facts"
                ]
            },
            {
                "pattern": "evidence_mapping",
                "description": "Map facts back to material evidence references.",
                "evidence_refs": evidence_refs
            }
        ]

