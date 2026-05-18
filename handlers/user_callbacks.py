import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from filters import IsDigitCallbackData, IsDelBookmarkCallbackData
from keyboards import create_edit_keyboard, create_pagination_keyboard
from lexicon import LEXICON_RU
from database import save_db
from services import get_user_data
from log_config import user_log_info


logger = logging.getLogger(__name__)
user_callbacks_router = Router()


@user_callbacks_router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery, book: dict, db: dict) -> None:
    user_info = user_log_info(callback.from_user)
    user_data = get_user_data(callback, db)
    current_page = user_data['page']

    logger.debug(f"{user_info}: forward from page {current_page}")

    if current_page < len(book):
        user_data['page'] = current_page + 1
        new_page = user_data['page']
        text = book[new_page]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward', f'{new_page}/{len(book)}', 'forward',
            ),
        )
        logger.debug(f"{user_info}: moved to page {new_page}")

    await callback.answer()
    await save_db(db)


@user_callbacks_router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery, book: dict, db: dict) -> None:
    user_info = user_log_info(callback.from_user)
    user_data = get_user_data(callback, db)
    current_page = user_data['page']

    logger.debug(f"{user_info}: backward from page {current_page}")

    if current_page > 1:
        user_data['page'] = current_page - 1
        new_page = user_data['page']
        text = book[new_page]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward', f'{new_page}/{len(book)}', 'forward',
            ),
        )
        logger.debug(f"{user_info}: moved to page {new_page}")

    await callback.answer()
    await save_db(db)


@user_callbacks_router.callback_query(
    lambda x: '/' in x.data and x.data.replace('/', '').isdigit()
)
async def process_page_press(callback: CallbackQuery, db: dict) -> None:
    user_info = user_log_info(callback.from_user)
    user_data = get_user_data(callback, db)
    page = user_data['page']

    user_data['bookmarks'].add(page)
    logger.info(f"{user_info}: added page {page} to bookmarks")

    await callback.answer('Страница добавлена в закладки!')
    await save_db(db)


@user_callbacks_router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery, book: dict, db: dict) -> None:
    user_info = user_log_info(callback.from_user)
    page = int(callback.data)

    logger.info(f"{user_info}: jumped to bookmark page {page}")

    await callback.answer()

    user_data = get_user_data(callback, db)
    user_data['page'] = page

    text = book[page]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward', f'{user_data["page"]}/{len(book)}', 'forward',
        ),
    )
    await save_db(db)


@user_callbacks_router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery, book: dict, db: dict) -> None:
    user_info = user_log_info(callback.from_user)
    user_data = get_user_data(callback, db)

    logger.info(f"{user_info}: editing bookmarks")

    await callback.message.edit_text(
        text=LEXICON_RU[callback.data],
        reply_markup=create_edit_keyboard(
            *user_data['bookmarks'],
            book=book,
        ),
    )
    await save_db(db)


@user_callbacks_router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery) -> None:
    user_info = user_log_info(callback.from_user)
    logger.debug(f"{user_info}: cancelled editing")
    await callback.message.edit_text(text=LEXICON_RU['cancel_text'])


@user_callbacks_router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery, book: dict, db: dict):
    user_info = user_log_info(callback.from_user)
    bookmark_to_remove = int(callback.data[:-3])

    logger.info(f"{user_info}: removing bookmark page {bookmark_to_remove}")

    user_data = get_user_data(callback, db)
    user_data['bookmarks'].remove(bookmark_to_remove)

    if user_data['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON_RU['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *user_data['bookmarks'],
                book=book,
            ),
        )
    else:
        await callback.message.edit_text(text=LEXICON_RU['no_bookmarks'])

    await save_db(db)
