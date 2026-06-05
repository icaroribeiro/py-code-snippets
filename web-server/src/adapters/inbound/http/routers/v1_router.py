from fastapi import APIRouter

from src.adapters.inbound.http.controllers.v1 import health_controller

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(health_controller.router, tags=["Health V1"])
