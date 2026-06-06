from datetime import UTC, datetime


def build_next_package_name(source_package_id: str, requested_name: str | None = None) -> str:
    if requested_name:
        return requested_name
    return f"{source_package_id} next iteration candidate"


def build_next_package_version(source_package_version: str, requested_version: str | None = None) -> str:
    if requested_version:
        return requested_version
    timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    base_version = source_package_version or "unknown"
    return f"{base_version}.v731i-candidate.{timestamp}"
