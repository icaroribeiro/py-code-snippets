from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request, Response, status
from fastapi_utils.cbv import cbv
from adapters.inbound.http.dependencies.dependencies import Dependencies
from core.use_cases.telegram_use_case import TelegramUseCase
from infrastructure.config import get_telegram_settings
from infrastructure.cross_cutting.logging import get_logger

telegam_settings = get_telegram_settings()

router = APIRouter(prefix="/webhooks")

@cbv(router)
class TelegramController:
    telegram_use_case: TelegramUseCase = Depends(Dependencies.telegram_use_case)

    @router.post(
        f"/{telegam_settings.bot_token}",
        status_code=status.HTTP_200_OK,
        summary="Receive real-time encoded payload updates from Telegram Bot API",
    )
    async def handle_telegram_webhook(
        self,
        request: Request,
        response: Response,
        x_api_secret: Annotated[
            str | None, Header(alias="x-api-secret")
        ] = None,
    ) -> Response:
        return response
