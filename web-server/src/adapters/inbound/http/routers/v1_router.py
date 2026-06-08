from fastapi import APIRouter

from adapters.inbound.http.controllers.v1 import health_controller, task_controller

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(health_controller.router, tags=["Health V1"])
v1_router.include_router(task_controller.router, tags=["Tasks V1"])
