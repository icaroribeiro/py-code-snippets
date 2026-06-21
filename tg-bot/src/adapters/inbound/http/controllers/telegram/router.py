from fastapi import APIRouter, Depends, Request, Response, status

from adapters.inbound.http.controllers.telegram.mapper import (
    TelegramTaskCallbackMapper,
    TelegramTaskCallbackRequestSchema,
    TelegramWebhookMapper,
)
from adapters.inbound.http.dependencies.dependencies import Dependencies
from core.ports.inbound.telegram_port import (
    TelegramTaskCallbackInputPort,
    TelegramWebhookInputPort,
)
from infrastructure.config import get_telegram_settings
from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)

telegram_settings = get_telegram_settings()

telegram_router = APIRouter(prefix="/telegram", tags=["Telegram"])


@telegram_router.post(
    f"/webooks/{telegram_settings.bot_token}",
    status_code=status.HTTP_200_OK,
    summary="Receive real-time encoded payload updates from Telegram Bot API",
)
async def handle_telegram_webhook(
    request: Request,
    response: Response,
    telegram_webhook_use_case: TelegramWebhookInputPort = Depends(
        Dependencies.telegram_webhook_use_case
    ),
) -> Response:
    raw_json_payload = await request.json()
    domain_payload = TelegramWebhookMapper.request_to_domain_dict(raw_json_payload)

    await telegram_webhook_use_case.process_update(raw_update=domain_payload)

    response.status_code = status.HTTP_200_OK
    return response


@telegram_router.post("/task-callbacks", status_code=status.HTTP_200_OK)
async def handle_task_callback(
    payload: TelegramTaskCallbackRequestSchema,
    response: Response,
    telegram_task_callback_use_case: TelegramTaskCallbackInputPort = Depends(
        Dependencies.telegram_task_callback_use_case
    ),
) -> Response:
    logger.info(f"Callback HTTP hit for task_id: {payload.task_id}")
    task_domain = TelegramTaskCallbackMapper.request_to_domain(payload)

    await telegram_task_callback_use_case.process_result(task_result=task_domain)

    return response
