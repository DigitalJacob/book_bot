import logging

from aiogram import Router
from aiogram.types import Message

from lexicon import LEXICON_RU
from log_config import user_log_info


logger = logging.getLogger(__name__)
unknown_router = Router()


@unknown_router.message()
async def process_unknown_command(message: Message) -> None:
    user_info = user_log_info(message.from_user)
    logger.debug(f"{user_info}: unknown command '{message.text}'")
    await message.answer(text=LEXICON_RU['unknown_command_text'])