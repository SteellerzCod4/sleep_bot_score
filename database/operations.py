from database import get_db
from database.models import User, TimeInfo
from bot_configs.states import States

db = get_db()


def get_user_by_id(user_id: int):
    """ Получает пользователя по его id """
    return db.query(User).filter(User.id == user_id).first()


def get_user_state(user_id: int):
    """ Получает состояние пользователя """
    user = get_user_by_id(user_id)

    if not user:
        return None

    return States(user.state)


def set_user_state(user_id: int, value: States):
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


def get_timeinfo_by_user_id(user_id: int):
    user = get_user_by_id(user_id)
    if user:
        time_info = user.time_info
        return time_info


def set_user_best_retire_time(user_id: int, best_retire_time):
    time_info = get_timeinfo_by_user_id(user_id)
    print(time_info)
    time_info.retire_time = best_retire_time
    db.commit()


def set_user_best_wakeup_time(user_id: int, best_wakeup_time):
    time_info = get_timeinfo_by_user_id(user_id)
    time_info.wakeup_time = best_wakeup_time
    db.commit()


def set_user_best_duration_time(user_id: int, best_duration_time):
    time_info = get_timeinfo_by_user_id(user_id)
    time_info.sleep_duration = best_duration_time
    db.commit()


def create_new_user(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        user = User(id=user_id, state="START")
        time_info = TimeInfo(user_id=user_id)

        db.add(user)
        db.add(time_info)
        db.commit()
