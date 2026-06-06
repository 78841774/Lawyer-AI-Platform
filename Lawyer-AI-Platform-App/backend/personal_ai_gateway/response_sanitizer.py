from personal_ai_gateway.schemas import PersonalAILiveDraftMetadata


def build_draft_metadata(provider_id: str, model: str, token_usage: dict[str, int | None]) -> PersonalAILiveDraftMetadata:
    return PersonalAILiveDraftMetadata(
        ai_draft="Controlled AI draft metadata placeholder. No final legal opinion generated.",
        draft_type="controlled_ai_draft_metadata",
        provider_id=provider_id,
        model=model,
        token_usage=token_usage,
        latency_ms=None,
    )
