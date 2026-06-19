from fastapi import APIRouter

from adapters.inbound.http.controllers.webhook.controller import (
    router as webhook_router,
)
from adapters.inbound.http.routers.v1_router import v1_router

root_router = APIRouter()
root_router.include_router(v1_router, prefix="/api")
root_router.include_router(webhook_router)
