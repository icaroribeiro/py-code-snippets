from fastapi import APIRouter

from adapters.inbound.http.routers.v1.router import v1_router

root_router = APIRouter(prefix="/api")
root_router.include_router(v1_router)
