from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_books_keyboard(books: list[dict]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for book in books:
        kb_builder.row(
            InlineKeyboardButton(
                text=book['title'],
                callback_data=f"book:{book['id']}",
            )
        )
    return kb_builder.as_markup()
