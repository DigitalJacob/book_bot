from copy import deepcopy


def _ensure_user_in_db(event, db: dict) -> None:
    user_id = str(event.from_user.id)
    if user_id not in db['users']:
        new_user = deepcopy(db['user_template'])
        db['users'][user_id] = new_user


def get_user_data(event, db: dict) -> dict:
    user_id = str(event.from_user.id)
    _ensure_user_in_db(event, db)
    return db['users'][user_id]

def get_current_book_id(user_data: dict) -> str:
    return user_data['current_book']

def get_book_state(user_data: dict, book_id: str) -> dict:
    if book_id not in user_data['books']:
        user_data['books'][book_id] = {'current_page': 1, 'bookmarks': set()}
    return user_data['books'][book_id]

def get_active_book_state(user_data: dict) -> dict:
    book_id = get_current_book_id(user_data)
    if not book_id:
        return None
    return get_book_state(user_data, book_id)