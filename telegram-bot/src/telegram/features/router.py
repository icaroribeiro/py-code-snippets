from aiogram import Router

from telegram.features.welcome import welcome_router

features_router = Router()
features_router.include_router(welcome_router)
