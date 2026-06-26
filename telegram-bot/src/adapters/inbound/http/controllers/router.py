from fastapi import APIRouter

from adapters.inbound.http.controllers.bot import (
    bot_router,
)
from adapters.inbound.http.controllers.v1.health import (
    health_router,
)

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(health_router, tags=["Health Checks V1 Endpoints"])

controllers_router = APIRouter()
controllers_router.include_router(v1_router, prefix="/api")
controllers_router.include_router(bot_router, tags=["Bot Endpoints"])
