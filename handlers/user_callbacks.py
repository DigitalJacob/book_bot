import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from filters import IsDigitCallbackData, IsDelBookmarkCallbackData
from keyboards import create_edit_keyboard, create_pagination_keyboard
from lexicon import LEXICON_RU
from database import save_db
from services import get_user_data, book_manager, get_active_book_state, get_book_state
from log_config import user_log_info


logger = logging.getLogger(__name__)
user_callbacks_router = Router()


@user_callbacks_router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery, db: dict) -> None:
    user_info = user_log_info(callback.from_user)
    user_data = get_user_data(callback, db)
    state = get_active_book_state(user_data)
    if state is None:
        await callback.answer(LEXICON_RU['no_active_book'], show_alert=True)
        return

    book = book_manager.get_pages(user_data['current_book'])
    current_page = state['current_page']

    logger.debug(f"{user_info}: forward from page {current_page}")

    if current_page < len(book):
        state['current_page'] = current_page + 1
        new_page = state['current_page']
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
async def process_backward_press(callback: CallbackQuery, db: dict) -> None:
    user_info = user_log_info(callback.from_user)
    user_data = get_user_data(callback, db)
    state = get_active_book_state(user_data)
    if state is None:
        await callback.answer(LEXICON_RU['no_active_book'], show_alert=True)
        return

    book = book_manager.get_pages(user_data['current_book'])
    current_page = state['current_page']

    logger.debug(f"{user_info}: backward from page {current_page}")

    if current_page > 1:
        state['current_page'] = current_page - 1
        new_page = state['current_page']
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
    state = get_active_book_state(user_data)
    if state is None:
        await callback.answer(LEXICON_RU['no_active_book'], show_alert=True)
        return

    page = state['current_page']
    state['bookmarks'].add(page)
    logger.info(f"{user_info}: added page {page} to bookmarks")

    await callback.answer('Страница добавлена в закладки!')
    await save_db(db)


@user_callbacks_router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery, db: dict) -> None:
    user_info = user_log_info(callback.from_user)
    page = int(callback.data)

    logger.info(f"{user_info}: jumped to bookmark page {page}")

    user_data = get_user_data(callback, db)
    state = get_active_book_state(user_data)
    if state is None:
        await callback.answer(LEXICON_RU['no_active_book'], show_alert=True)
        return

    book = book_manager.get_pages(user_data['current_book'])
    state['current_page'] = page

    await callback.answer()
    await callback.message.edit_text(
        text=book[page],
        reply_markup=create_pagination_keyboard(
            'backward', f'{page}/{len(book)}', 'forward',
        ),
    )
    await save_db(db)


@user_callbacks_router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery, db: dict) -> None:
    user_info = user_log_info(callback.from_user)
    user_data = get_user_data(callback, db)
    state = get_active_book_state(user_data)
    if state is None:
        await callback.answer(LEXICON_RU['no_active_book'], show_alert=True)
        return

    book = book_manager.get_pages(user_data['current_book'])

    logger.info(f"{user_info}: editing bookmarks")

    await callback.message.edit_text(
        text=LEXICON_RU[callback.data],
        reply_markup=create_edit_keyboard(
            *state['bookmarks'],
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
async def process_del_bookmark_press(callback: CallbackQuery, db: dict):
    user_info = user_log_info(callback.from_user)
    bookmark_to_remove = int(callback.data[:-3])

    logger.info(f"{user_info}: removing bookmark page {bookmark_to_remove}")

    user_data = get_user_data(callback, db)
    state = get_active_book_state(user_data)
    if state is None:
        await callback.answer(LEXICON_RU['no_active_book'], show_alert=True)
        return

    book = book_manager.get_pages(user_data['current_book'])
    state['bookmarks'].remove(bookmark_to_remove)

    if state['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON_RU['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *state['bookmarks'],
                book=book,
            ),
        )
    else:
        await callback.message.edit_text(text=LEXICON_RU['no_bookmarks'])

    await save_db(db)


@user_callbacks_router.callback_query(F.data.startswith('book:'))
async def process_book_select(callback: CallbackQuery, db: dict) -> None:
    user_info = user_log_info(callback.from_user)
    book_id = callback.data.split(':', 1)[1]

    if not book_manager.book_exists(book_id):
        await callback.answer('Книга не найдена', show_alert=True)
        return

    user_data = get_user_data(callback, db)
    user_data['current_book'] = book_id
    state = get_book_state(user_data, book_id)

    book = book_manager.get_pages(book_id)
    page = state['current_page']
    title = book_manager.get_book_title(book_id)

    logger.info(f"{user_info}: selected book {book_id}, page {page}")

    await callback.message.edit_text(
        text=book[page],
        reply_markup=create_pagination_keyboard(
            'backward', f'{page}/{len(book)}', 'forward',
        ),
    )
    await callback.answer(LEXICON_RU['book_selected'].format(title=title))
    await save_db(db)
