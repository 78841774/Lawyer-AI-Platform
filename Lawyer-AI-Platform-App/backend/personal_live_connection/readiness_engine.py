from personal_live_connection.provider_registry import list_providers
from personal_live_connection.schemas import LiveConnectionStatus


def build_status() -> dict:
    providers = list_providers()
    return LiveConnectionStatus(
        provider_count=len(providers),
        dry_run_ready_count=sum(1 for provider in providers if provider.dry_run_ready),
        key_loaded_count=sum(1 for provider in providers if provider.key_loaded),
        live_disabled_count=len(providers),
        warnings=[
            "Personal Live Connection is dry-run first and live-disabled by default.",
            "No provider network call is executed by status/readiness endpoints.",
        ],
    ).model_dump()

