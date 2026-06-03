from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.cases import router as cases_router
from app.api.experience_packages import router as experience_packages_router
from app.api.facts import router as facts_router
from app.api.health import router as health_router
from app.api.legal_analysis import router as legal_analysis_router
from app.api.materials import router as materials_router
from app.api.reports import router as reports_router
from app.api.skill_registry import router as skill_registry_router
from app.api.skills import router as skills_router
from app.api.workspace import router as workspace_router
from app.api.workspace_skills import router as workspace_skills_router
from app.core.config import settings
from app.core.database import create_db_and_tables


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
app.include_router(workspace_router)
app.include_router(cases_router)
app.include_router(materials_router)
app.include_router(facts_router)
app.include_router(legal_analysis_router)
app.include_router(reports_router)
app.include_router(skills_router)
app.include_router(experience_packages_router)
app.include_router(skill_registry_router)
app.include_router(workspace_skills_router)
