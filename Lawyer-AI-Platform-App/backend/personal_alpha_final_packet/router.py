from typing import Any

from fastapi import APIRouter

from personal_alpha_final_packet.packet_engine import (
    create_personal_alpha_final_packet,
    get_personal_alpha_final_packet,
    get_personal_alpha_final_packet_preview,
    get_personal_alpha_final_packet_status,
    list_personal_alpha_final_packets,
    list_personal_alpha_final_packets_for_run,
)
from personal_alpha_final_packet.schemas import PersonalAlphaFinalPacketCreateRequest

router = APIRouter(prefix="/personal-alpha-final-packet", tags=["personal-alpha-final-packet"])


@router.get("/status")
def personal_alpha_final_packet_status() -> dict[str, Any]:
    return get_personal_alpha_final_packet_status()


@router.get("/run/{workspace_run_id}/preview")
def personal_alpha_final_packet_preview(workspace_run_id: str) -> dict[str, Any]:
    return get_personal_alpha_final_packet_preview(workspace_run_id)


@router.post("/run/{workspace_run_id}/create")
def personal_alpha_final_packet_create(workspace_run_id: str, request: PersonalAlphaFinalPacketCreateRequest) -> dict[str, Any]:
    return create_personal_alpha_final_packet(workspace_run_id, request)


@router.get("/packets")
def personal_alpha_final_packet_list() -> dict[str, Any]:
    return list_personal_alpha_final_packets()


@router.get("/packets/{packet_id}")
def personal_alpha_final_packet_detail(packet_id: str) -> dict[str, Any]:
    return get_personal_alpha_final_packet(packet_id)


@router.get("/run/{workspace_run_id}/packets")
def personal_alpha_final_packet_run_packets(workspace_run_id: str) -> dict[str, Any]:
    return list_personal_alpha_final_packets_for_run(workspace_run_id)
