import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards import create_bookmarks_keyboard, create_pagination_keyboard, create_books_keyboard
from lexicon import LEXICON_RU
from services import get_user_data, book_manager, get_active_book_state
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
async def process_beginning_command(message: Message, db: dict) -> None:
    user_info = user_log_info(message.from_user)
    logger.info(f"{user_info}: go to page 1")

    user_data = get_user_data(message, db)
    state = get_active_book_state(user_data)

    if state is None:
        await message.answer(LEXICON_RU['no_active_book'])
        return

    book_id = user_data['current_book']
    book = book_manager.get_pages(book_id)

    state['current_page'] = 1
    await save_db(db)

    text = book[1]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward', f'1/{len(book)}', 'forward',
        ),
    )


@user_commands_router.message(Command(commands='continue'))
async def process_continue_command(message: Message, db: dict) -> None:
    user_data = get_user_data(message, db)
    state = get_active_book_state(user_data)
    if state is None:
        await message.answer(LEXICON_RU['no_active_book'])
        return
    
    book = book_manager.get_pages(user_data['current_book'])
    page = state['current_page']
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
async def process_bookmarks_command(message: Message, db: dict) -> None:
    user_data = get_user_data(message, db)
    state = get_active_book_state(user_data)
    if state is None:
        await message.answer(LEXICON_RU['no_active_book'])
        return
    
    book = book_manager.get_pages(user_data['current_book'])
    
    user_info = user_log_info(message.from_user)

    logger.info(f"{user_info}: viewing bookmarks")

    if state['bookmarks']:
        await message.answer(
            text=LEXICON_RU[message.text],
            reply_markup=create_bookmarks_keyboard(
                *state['bookmarks'],
                book=book,
            ),
        )
    else:
        await message.answer(text=LEXICON_RU['no_bookmarks'])


@user_commands_router.message(Command(commands='books'))
async def process_books_command(message: Message, db: dict) -> None:
    user_info = user_log_info(message.from_user)
    logger.info(f"{user_info}: /books")

    get_user_data(message, db)

    books = book_manager.get_books_list()
    if not books:
        await message.answer(text=LEXICON_RU['no_books'])
        return

    await message.answer(
        text=LEXICON_RU['/books'],
        reply_markup=create_books_keyboard(books),
    )