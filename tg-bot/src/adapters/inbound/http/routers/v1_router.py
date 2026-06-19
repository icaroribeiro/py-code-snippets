from fastapi import APIRouter

from adapters.inbound.http.controllers.v1.health.controller import (
    router as health_router,
)
from adapters.inbound.http.controllers.v1.task.controller import (
    router as task_callback_router,
)

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(health_router, tags=["Health Checks V1"])
v1_router.include_router(task_callback_router, tags=["Task Callbacks V1"])
