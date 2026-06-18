from fastapi import APIRouter, Depends, Request, Response, status

from adapters.inbound.http.controllers.v1.telegram.mapper import TelegramMapper
from adapters.inbound.http.dependencies.dependencies import Dependencies
from core.ports.inbound.telegram_port import TelegramInputPort
from infrastructure.config import get_telegram_settings

telegram_settings = get_telegram_settings()

router = APIRouter(prefix="/webhooks")


@router.post(
    f"/{telegram_settings.bot_token}",
    status_code=status.HTTP_200_OK,
    summary="Receive real-time encoded payload updates from Telegram Bot API",
)
async def handle_telegram_webhook(
    request: Request,
    response: Response,
    # x_api_key: Annotated[str | None, Header(alias="x-api-secret")] = None,
    telegram_use_case: TelegramInputPort = Depends(Dependencies.telegram_use_case),
) -> Response:
    # if telegram_settings.api_key and x_api_key != telegram_settings.api_key:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid API key",
    #     )
    raw_json_payload = await request.json()
    domain_payload = TelegramMapper.request_to_domain_dict(raw_json_payload)

    await telegram_use_case.process_update(raw_update=domain_payload)

    response.status_code = status.HTTP_200_OK
    return response
