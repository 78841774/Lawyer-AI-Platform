from typing import Any

from source_refs.schemas import CitationResolutionResult, SourceRef


def resolve_mock_citation(citation_id: str) -> dict[str, Any]:
    if citation_id != "citation_mock_001":
        return CitationResolutionResult(
            citation_id=citation_id,
            resolved=False,
            source_ref=None,
            warnings=["Mock citation id not found."],
            mock_only=True
        ).model_dump()

    source_ref = SourceRef(
        source_ref_id="source_ref_mock_material_001",
        source_type="material",
        source_id="material_demo_001",
        material_id="material_demo_001",
        filename="demo.pdf",
        relative_path="demo/demo.pdf",
        page_number=1,
        char_start=0,
        char_end=64,
        bbox=None,
        quote="Mock citation quote only. No real material content used.",
        citation="Mock Citation",
        url=None,
        provider="mock",
        provider_mode="mock",
        mock_only=True
    )
    return CitationResolutionResult(
        citation_id=citation_id,
        resolved=True,
        source_ref=source_ref,
        warnings=[
            "Mock citation resolver only.",
            "No real material content used.",
            "No real OCR provider used.",
            "No external legal database queried.",
            "No LLM call performed."
        ],
        mock_only=True
    ).model_dump()
