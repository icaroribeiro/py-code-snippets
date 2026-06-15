from fastapi import APIRouter

from adapters.inbound.http.routers.v1.router import v1_router
from adapters.inbound.http.controllers.v1.telegram.controller import router as telegram_router


root_router = APIRouter()
# Ecosystem routes and integrations with frontend/mobile (Versioned)
root_router.include_router(v1_router, prefix="/api")
# Infrastructure Webhook Routes (Global, No Version)
root_router.include_router(telegram_router)
