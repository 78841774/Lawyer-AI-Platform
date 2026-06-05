from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.case_cause_taxonomy import router as case_cause_taxonomy_router
from app.api.cases import router as cases_router
from app.api.experience_packages import router as experience_packages_router
from app.api.facts import router as facts_router
from app.api.health import router as health_router
from app.api.legal_analysis import router as legal_analysis_router
from app.api.llm import router as llm_router
from app.api.materials import router as materials_router
from app.api.reports import router as reports_router
from app.api.runtime_runs import router as runtime_runs_router
from app.api.skill_registry import router as skill_registry_router
from app.api.skills import router as skills_router
from app.api.users import router as users_router
from app.api.versioned_skill_training_packages import router as versioned_skill_training_packages_router
from app.api.workspace import router as workspace_router
from app.api.workspace_skills import router as workspace_skills_router
from app.api.workspaces import router as workspaces_router
from app.core.config import settings
from app.core.database import create_db_and_tables
from controlled_legal_search_pipeline.router import router as controlled_legal_search_router
from controlled_final_review_lock.router import router as controlled_final_review_lock_router
from controlled_lawyer_review.router import router as controlled_lawyer_review_router
from controlled_material_processing.router import router as controlled_material_router
from controlled_ocr_pipeline.router import router as controlled_ocr_router
from controlled_report_draft_pipeline.router import router as controlled_report_draft_router
from controlled_revision_workflow.router import router as controlled_revision_router
from internal_alpha.router import router as internal_alpha_router
from legal_search_adapter.router import router as legal_search_router
from local_sandbox.router import router as local_sandbox_router
from ocr_adapter.router import router as ocr_router
from personal_alpha_dashboard.router import router as personal_alpha_dashboard_router
from personal_alpha_case_os.router import router as personal_alpha_case_os_router
from personal_alpha_final_gate.router import router as personal_alpha_final_gate_router
from personal_alpha_final_lock.router import router as personal_alpha_final_lock_router
from personal_alpha_final_packet.router import router as personal_alpha_final_packet_router
from personal_alpha_final_readiness.router import router as personal_alpha_final_readiness_router
from personal_alpha_lawyer_final_review.router import router as personal_alpha_lawyer_final_review_router
from personal_alpha.router import router as personal_alpha_router
from personal_alpha_source_review.router import router as personal_alpha_source_review_router
from personal_alpha_workspace.router import router as personal_alpha_workspace_router
from personal_ai_gateway.router import router as personal_ai_gateway_router
from personal_material_runtime.router import router as personal_material_runtime_router
from personal_production.router import router as personal_production_router
from source_refs.router import router as source_refs_router
from versioned_skill_training_runs.router import router as versioned_skill_training_runs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(case_cause_taxonomy_router)
app.include_router(users_router)
app.include_router(workspaces_router)
app.include_router(workspace_router)
app.include_router(cases_router)
app.include_router(materials_router)
app.include_router(facts_router)
app.include_router(legal_analysis_router)
app.include_router(reports_router)
app.include_router(runtime_runs_router)
app.include_router(skills_router)
app.include_router(experience_packages_router)
app.include_router(skill_registry_router)
app.include_router(workspace_skills_router)
app.include_router(llm_router)
app.include_router(ocr_router)
app.include_router(legal_search_router)
app.include_router(source_refs_router)
app.include_router(local_sandbox_router)
app.include_router(internal_alpha_router)
app.include_router(personal_alpha_router)
app.include_router(personal_alpha_workspace_router)
app.include_router(personal_alpha_dashboard_router)
app.include_router(personal_alpha_source_review_router)
app.include_router(personal_alpha_final_readiness_router)
app.include_router(personal_alpha_final_gate_router)
app.include_router(personal_alpha_final_packet_router)
app.include_router(personal_alpha_lawyer_final_review_router)
app.include_router(personal_alpha_final_lock_router)
app.include_router(personal_alpha_case_os_router)
app.include_router(personal_production_router)
app.include_router(personal_ai_gateway_router)
app.include_router(personal_material_runtime_router)
app.include_router(controlled_material_router)
app.include_router(controlled_ocr_router)
app.include_router(controlled_legal_search_router)
app.include_router(controlled_report_draft_router)
app.include_router(controlled_lawyer_review_router)
app.include_router(controlled_revision_router)
app.include_router(controlled_final_review_lock_router)
app.include_router(versioned_skill_training_packages_router)
app.include_router(versioned_skill_training_runs_router)
