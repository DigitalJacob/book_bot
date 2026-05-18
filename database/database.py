import json
from pathlib import Path

import aiofiles

DB_PATH = Path(__file__).parent.parent / 'db.json'


def get_empty_db() -> dict:
    return {
        "user_template": {"page": 1, "bookmarks": []},
        "users": {}
    }


async def load_db() -> dict:
    if not DB_PATH.exists():
        return get_empty_db()

    async with aiofiles.open(DB_PATH, 'r', encoding='utf-8') as f:
        content = await f.read()
        data = json.loads(content)

    for user_id, user_data in data.get('users', {}).items():
        if 'bookmarks' in user_data and isinstance(user_data['bookmarks'], list):
            user_data['bookmarks'] = set(user_data['bookmarks'])

    return data


async def save_db(data: dict) -> None:
    data_copy = {
        "user_template": data["user_template"],
        "users": {}
    }

    for user_id, user_data in data.get('users', {}).items():
        user_copy = user_data.copy()
        if 'bookmarks' in user_copy:
            user_copy['bookmarks'] = list(user_copy['bookmarks'])
        data_copy['users'][user_id] = user_copy

    async with aiofiles.open(DB_PATH, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data_copy, indent=2, ensure_ascii=False))