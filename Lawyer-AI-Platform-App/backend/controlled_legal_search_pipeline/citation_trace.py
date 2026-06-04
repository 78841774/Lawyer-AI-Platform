from typing import Any


def build_legal_search_source_refs(search_preview_id: str, citations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "source_ref_id": citation["source_ref_id"],
            "source_type": "controlled_legal_search",
            "search_preview_id": search_preview_id,
            "citation_id": citation["citation_id"],
            "title": citation["title"],
            "quote": "Mock legal citation placeholder. No real legal database was called.",
            "provider": "controlled_legal_search",
            "provider_mode": "mock",
            "mock_or_redacted_only": True,
        }
        for citation in citations
    ]


def build_mock_citation_resolution_source_ref(citation_id: str, search_preview_id: str) -> dict[str, Any]:
    return {
        "source_ref_id": f"source_ref_resolution_{citation_id}",
        "source_type": "controlled_legal_search_resolution",
        "search_preview_id": search_preview_id,
        "citation_id": citation_id,
        "title": f"Mock resolution for {citation_id}",
        "quote": "Mock legal citation placeholder. No real legal database was called.",
        "provider": "controlled_legal_search",
        "provider_mode": "mock",
        "mock_or_redacted_only": True,
    }
