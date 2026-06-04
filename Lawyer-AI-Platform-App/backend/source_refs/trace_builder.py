from typing import Any

from source_refs.schemas import SourceTrace, SourceTraceEdge, SourceTraceNode, utc_now


def build_mock_source_trace(report_id: str, case_id: str | None = None) -> dict[str, Any]:
    trace = SourceTrace(
        trace_id=f"source_trace_mock_{report_id}",
        report_id=report_id,
        case_id=case_id,
        nodes=[
            SourceTraceNode(
                node_id="material_demo_001",
                node_type="material",
                label="Demo Material",
                source_ref_id="source_ref_mock_material_001",
                metadata={
                    "filename": "demo.pdf",
                    "relative_path": "demo/demo.pdf",
                    "mock_only": True
                }
            ),
            SourceTraceNode(
                node_id="ocr_result_demo_001",
                node_type="ocr_result",
                label="Mock OCR Result",
                source_ref_id="source_ref_mock_ocr_001",
                metadata={
                    "provider": "mock_ocr",
                    "provider_mode": "mock",
                    "mock_only": True
                }
            ),
            SourceTraceNode(
                node_id="legal_search_hit_demo_001",
                node_type="legal_search_hit",
                label="Mock Legal Search Hit",
                source_ref_id="source_ref_mock_legal_search_001",
                metadata={
                    "provider": "mock_legal_search",
                    "citation": "Mock Citation",
                    "mock_only": True
                }
            ),
            SourceTraceNode(
                node_id="report_section_demo_001",
                node_type="report_section",
                label="Mock Report Section",
                source_ref_id=None,
                metadata={"section_id": "report_section_demo_001", "mock_only": True}
            ),
            SourceTraceNode(
                node_id="citation_demo_001",
                node_type="citation",
                label="Mock Citation",
                source_ref_id="source_ref_mock_material_001",
                metadata={"citation_id": "citation_mock_001", "mock_only": True}
            )
        ],
        edges=[
            SourceTraceEdge(
                edge_id="edge_mock_material_to_ocr",
                from_node_id="material_demo_001",
                to_node_id="ocr_result_demo_001",
                relation="derived_from",
                metadata={"mock_only": True}
            ),
            SourceTraceEdge(
                edge_id="edge_mock_ocr_to_section",
                from_node_id="ocr_result_demo_001",
                to_node_id="report_section_demo_001",
                relation="cited_by",
                metadata={"mock_only": True}
            ),
            SourceTraceEdge(
                edge_id="edge_mock_legal_to_section",
                from_node_id="legal_search_hit_demo_001",
                to_node_id="report_section_demo_001",
                relation="supports",
                metadata={"mock_only": True}
            ),
            SourceTraceEdge(
                edge_id="edge_mock_section_to_citation",
                from_node_id="report_section_demo_001",
                to_node_id="citation_demo_001",
                relation="referenced_in",
                metadata={"mock_only": True}
            )
        ],
        warnings=[
            "Mock source trace only.",
            "No real case material read.",
            "No real OCR provider used.",
            "No external legal database queried.",
            "No LLM call performed."
        ],
        created_at=utc_now(),
        mock_only=True
    )
    return trace.model_dump()
