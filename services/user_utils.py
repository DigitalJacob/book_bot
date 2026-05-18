from copy import deepcopy


def _ensure_user_in_db(event, db: dict) -> None:
    user_id = str(event.from_user.id)
    if user_id not in db['users']:
        new_user = deepcopy(db['user_template'])
        new_user['bookmarks'] = set(new_user.get('bookmarks', []))
        db['users'][user_id] = new_user


def get_user_data(event, db: dict) -> dict:
    user_id = str(event.from_user.id)
    _ensure_user_in_db(event, db)
    return db['users'][user_id]
