import json
from pathlib import Path
from copy import deepcopy

import aiofiles


DB_PATH = Path(__file__).parent.parent / 'db.json'


def get_empty_db() -> dict:
    return {
        "user_template": {"current_book": None, "books": {}},
        "users": {}
    }


async def load_db() -> dict:
    if not DB_PATH.exists():
        return get_empty_db()

    async with aiofiles.open(DB_PATH, 'r', encoding='utf-8') as f:
        content = await f.read()
        data = json.loads(content)

    for user_data in data.get('users', {}).values():
        for book_data in user_data.get('books', {}).values():
            if 'bookmarks' in book_data and isinstance(book_data['bookmarks'], list):
                book_data['bookmarks'] = set(book_data['bookmarks'])

    return data


async def save_db(data: dict) -> None:
    data_copy = {
        "user_template": data["user_template"],
        "users": {}
    }

    for user_id, user_data in data.get('users', {}).items():
        user_copy = deepcopy(user_data)
        for book_data in user_copy.get('books', {}).values():
            if 'bookmarks' in book_data:
                book_data['bookmarks'] = list(book_data['bookmarks'])
        data_copy['users'][user_id] = user_copy

    async with aiofiles.open(DB_PATH, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data_copy, indent=2, ensure_ascii=False))