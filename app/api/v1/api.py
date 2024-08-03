from fastapi import APIRouter

from app.api import health
from app.api.v1.endpoints import member

api_router = APIRouter()

api_router.include_router(
    # member.router, prefix=f"/{settings.API_V1_STR}/member", tags=["Members"]
    member.router, prefix="/member", tags=["Members"]
)
api_router.include_router(health.router, tags=["Health"])
