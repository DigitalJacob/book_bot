import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards import create_bookmarks_keyboard, create_pagination_keyboard
from lexicon import LEXICON_RU
from services import get_user_data
from database import save_db
from log_config import user_log_info


logger = logging.getLogger(__name__)
user_commands_router = Router()


@user_commands_router.message(CommandStart())
async def process_start_command(message: Message, db: dict) -> None:
    user_info = user_log_info(message.from_user)
    logger.info(f"{user_info}: /start")

    await message.answer(LEXICON_RU[message.text])
    get_user_data(message, db)
    await save_db(db)


@user_commands_router.message(Command(commands='help'))
async def process_help_command(message: Message, db: dict) -> None:
    user_info = user_log_info(message.from_user)
    logger.info(f"{user_info}: /help")

    await message.answer(LEXICON_RU[message.text])
    get_user_data(message, db)


@user_commands_router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message, book: dict, db: dict) -> None:
    user_info = user_log_info(message.from_user)
    logger.info(f"{user_info}: go to page 1")

    user_data = get_user_data(message, db)
    user_data['page'] = 1
    await save_db(db)

    text = book[1]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward', f'1/{len(book)}', 'forward',
        ),
    )


@user_commands_router.message(Command(commands='continue'))
async def process_continue_command(message: Message, book: dict, db: dict) -> None:
    user_data = get_user_data(message, db)
    page = user_data['page']
    user_info = user_log_info(message.from_user)

    logger.info(f"{user_info}: continue from page {page}")

    text = book[page]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward', f'{page}/{len(book)}', 'forward',
        ),
    )


@user_commands_router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message, book: dict, db: dict) -> None:
    user_data = get_user_data(message, db)
    user_info = user_log_info(message.from_user)

    logger.info(f"{user_info}: viewing bookmarks")

    if user_data['bookmarks']:
        await message.answer(
            text=LEXICON_RU[message.text],
            reply_markup=create_bookmarks_keyboard(
                *user_data['bookmarks'],
                book=book,
            ),
        )
    else:
        await message.answer(text=LEXICON_RU['no_bookmarks'])

    await save_db(db)
