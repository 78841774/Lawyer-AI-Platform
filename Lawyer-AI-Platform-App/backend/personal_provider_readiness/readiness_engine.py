from personal_provider_readiness.provider_registry import build_provider_list
from personal_provider_readiness.schemas import ProviderStatus


def build_status() -> dict:
    providers = build_provider_list()
    return ProviderStatus(
        provider_count=int(providers["provider_count"]),
        key_loaded_count=int(providers["key_loaded_count"]),
        warnings=[
            "v7.26 only checks provider readiness metadata and secret boundary booleans.",
            "Live provider calls remain disabled and are not executed.",
        ],
    ).model_dump()

