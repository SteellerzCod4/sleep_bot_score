from database import get_db
from database.models import User

db = get_db()


def get_user_by_id(user_id: int):
    """ Получает пользователя по его id """
    return db.query(User).filter(User.id == user_id).first()


def get_user_state(user_id: int):
    """ Получает состояние пользователя """
    user = get_user_by_id(user_id)

    if not user:
        return None

    return user.state


def set_user_state(user_id: int, value: str):
    """ Устанавливает состояние пользователя """
    user = get_user_by_id(user_id)
    if not user:
        user = User(id=user_id, state=value)
        db.add(user)

    user.state = value
    db.commit()

    return user


def set_user_name(user_id: int, user_name: str):
    """ Устанавливает имя пользователя """
    user = get_user_by_id(user_id)
    if not user:
        user = User(id=user_id, name=user_name)
        db.add(user)

    user.name = user_name
    db.commit()

    return user


def set_user_last_name(user_id: int, user_last_name: str):
    """ Устанавливает фамилию пользователя """
    user = get_user_by_id(user_id)
    if not user:
        user = User(id=user_id, last_name=user_last_name)
        db.add(user)

    user.last_name = user_last_name
    db.commit()

    return user


def set_user_gender(user_id: int, user_gender: str):
    """ Устанавливает пол пользователя """
    user = get_user_by_id(user_id)
    if not user:
        user = User(id=user_id, gender=user_gender)
        db.add(user)

    user.gender = user_gender
    db.commit()

    return user


def create_new_user(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        user = User(id=user_id, state="START")
        db.add(user)
        db.commit()
