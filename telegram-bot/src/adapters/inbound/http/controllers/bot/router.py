from fastapi import APIRouter, Depends, Request, Response, status

from adapters.inbound.http.controllers.bot.mapper import (
    BotTaskCallbackMapper,
    BotTaskCallbackRequestSchema,
    BotWebhookMapper,
)
from adapters.inbound.http.dependencies import Dependencies
from core.ports.inbound.bot_port import (
    BotTaskCallbackInputPort,
    BotWebhookInputPort,
)
from infrastructure.config import get_telegram_settings
from infrastructure.cross_cutting import get_logger

logger = get_logger(__name__)

telegram_settings = get_telegram_settings()

bot_router = APIRouter(prefix=f"/bots/{telegram_settings.bot_slug}")


@bot_router.post(
    "/webhook",
    status_code=status.HTTP_200_OK,
    summary="Receive real-time encoded payload updates from Telegram Bot API",
)
async def handle_webhook(
    request: Request,
    response: Response,
    bot_webhook_use_case: BotWebhookInputPort = Depends(
        Dependencies.bot_webhook_use_case
    ),
) -> Response:
    raw_json_payload = await request.json()
    domain_payload = BotWebhookMapper.request_to_domain_dict(raw_json_payload)

    await bot_webhook_use_case.process_update(raw_update=domain_payload)

    response.status_code = status.HTTP_200_OK
    return response


@bot_router.post("/task-callbacks", status_code=status.HTTP_200_OK)
async def handle_task_callback(
    payload: BotTaskCallbackRequestSchema,
    response: Response,
    bot_task_callback_use_case: BotTaskCallbackInputPort = Depends(
        Dependencies.bot_task_callback_use_case
    ),
) -> Response:
    logger.info(f"Callback HTTP hit for task_id: {payload.task_id}")
    task_domain = BotTaskCallbackMapper.request_to_domain(payload)

    await bot_task_callback_use_case.process_result(task_result=task_domain)

    return response
