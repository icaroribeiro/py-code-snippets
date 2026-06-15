from typing import Annotated, Any
from fastapi import APIRouter, Depends, Header, Request, Response, status, HTTPException
from fastapi_utils.cbv import cbv

from adapters.inbound.http.dependencies.dependencies import Dependencies
from adapters.inbound.http.controllers.v1.telegram.mapper import TelegramMapper
from core.use_cases.telegram_use_case import TelegramUseCase
from infrastructure.config import get_telegram_settings

router = APIRouter(prefix="/webhooks")
telegram_settings = get_telegram_settings()

@cbv(router)
class TelegramController:
    telegram_use_case: TelegramUseCase = Depends(Dependencies.telegram_use_case)

    @router.post(
        f"/{telegram_settings.bot_token}",
        status_code=status.HTTP_200_OK,
        summary="Receive real-time encoded payload updates from Telegram Bot API",
    )
    async def handle_telegram_webhook(
        self,
        request: Request,
        response: Response,
        x_api_secret: Annotated[str | None, Header(alias="x-api-secret")] = None,
    ) -> Response:
        if telegram_settings.api_secret and x_api_secret != telegram_settings.api_secret:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Secret token sequence")

        raw_json_payload = await request.json()
        domain_payload = TelegramMapper.request_to_domain_dict(raw_json_payload)

        await self.telegram_use_case.process_update(raw_update=domain_payload)

        response.status_code = status.HTTP_200_OK
        return response
