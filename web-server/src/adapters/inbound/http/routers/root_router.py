from fastapi import APIRouter
from src.adapters.inbound.http.routers.v1_router import v1_router

root_router = APIRouter(prefix="/api")

root_router.include_router(v1_router)
