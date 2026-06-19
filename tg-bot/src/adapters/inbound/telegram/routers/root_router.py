from aiogram import Router

from adapters.inbound.telegram.routers.welcome_router import router as welcome_router

root_router = Router()
root_router.include_router(welcome_router)
