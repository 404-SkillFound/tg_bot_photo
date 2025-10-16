from fastapi import APIRouter

from .controllers import health_check


v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(health_check.router)
