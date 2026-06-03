from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.cases import router as cases_router
from app.api.facts import router as facts_router
from app.api.health import router as health_router
from app.api.materials import router as materials_router
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
app.include_router(health_router)
app.include_router(cases_router)
app.include_router(materials_router)
app.include_router(facts_router)
