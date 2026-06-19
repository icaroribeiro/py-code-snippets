from fastapi import APIRouter, Depends, Request, Response, status

from adapters.inbound.http.controllers.webhook.mapper import TgMapper
from adapters.inbound.http.dependencies.dependencies import Dependencies
from core.ports.inbound.webhook_port import TgFeedUpdateInputPort
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
    tg_feed_update_use_case: TgFeedUpdateInputPort = Depends(
        Dependencies.tg_feed_update_use_case
    ),
) -> Response:
    # if telegram_settings.api_key and x_api_key != telegram_settings.api_key:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid API key",
    #     )
    raw_json_payload = await request.json()
    domain_payload = TgMapper.request_to_domain_dict(raw_json_payload)

    await tg_feed_update_use_case.process_update(raw_update=domain_payload)

    response.status_code = status.HTTP_200_OK
    return response
