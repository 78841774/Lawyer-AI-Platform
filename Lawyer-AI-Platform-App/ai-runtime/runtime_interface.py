from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class RuntimeRequest:
    case_id: str
    task_type: str
    input_data: dict[str, Any]
    package_id: str | None = None
    request_id: str | None = None


@dataclass
class RuntimeResponse:
    status: str
    output_data: dict[str, Any]
    warnings: list[str] = field(default_factory=list)


class Runtime(Protocol):
    def run(self, request: RuntimeRequest) -> RuntimeResponse:
        """Execute a runtime task and return structured output."""
