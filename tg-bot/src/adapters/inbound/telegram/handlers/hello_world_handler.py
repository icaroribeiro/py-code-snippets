from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.use_cases.hello_world_use_case import HelloWorldUseCase

router = Router()


@router.message(Command("hello_world"))
async def handle_hello_world_command(
    message: Message, hello_world_use_case: HelloWorldUseCase
) -> None:
    await hello_world_use_case.execute(chat_id=message.chat.id)
