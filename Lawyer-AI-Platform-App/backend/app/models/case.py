from dataclasses import dataclass


@dataclass
class Case:
    case_id: str
    title: str
    case_type: str
    status: str
