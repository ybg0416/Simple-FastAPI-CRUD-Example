from fastapi import APIRouter

from app.api import health
from app.api.v1.endpoints import member
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(
    member.router, prefix=f"/member/{settings.API_V1_STR}", tags=["Members"]
)
api_router.include_router(health.router, tags=["Health"])
