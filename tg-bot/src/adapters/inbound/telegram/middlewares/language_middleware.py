# adapters/inbound/telegram/middlewares/language_middleware.py
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_lang = "en-US"

        if event.from_user:
            match event.from_user.language_code:
                case "en":
                    user_lang = "en-US"
                case "pt":
                    user_lang = "pt-BR"
                case _:
                    pass

        data["user_lang"] = user_lang
        return await handler(event, data)
