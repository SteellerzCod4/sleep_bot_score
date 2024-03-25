import datetime

from database import get_db
from database.models import User, TimeInfo, TimeSettings
from bot_configs.states import States

db = get_db()


def get_user_by_id(user_id: int):
    """ Получает пользователя по его id """
    return db.query(User).filter(User.id == user_id).first()


def get_timeinfo_by_id(timeinfo_id: int):
    """ Получает Timeinfo юзера по его id """
    return db.query(TimeInfo).filter(TimeInfo.id == timeinfo_id).first()


def get_timesettings_by_user_id(user_id: int):
    """ Получает TimeSettings юзера по его id """
    return db.query(TimeSettings).filter(TimeSettings.user_id == user_id).first()

def get_timesettings_by_id(user_id):
    user = get_user_by_id(user_id)
    print(f"user: {user}")
    current_settings_id = user.current_settings_id
    print(f"current_settings_id: {current_settings_id}")
    time_settings = db.query(TimeSettings).filter(TimeSettings.id == current_settings_id).first()
    print(f"type(time_settings): {type(time_settings)}")
    print(f"time_settings: {time_settings}")
    return time_settings


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
    print(f"user.name: {user.name}")
    db.commit()

    return user


def set_user_age(user_id: int, user_age: int):
    """ Устанавливает возраст пользователя """
    user = get_user_by_id(user_id)
    if not user:
        user = User(id=user_id, age=user_age)
        db.add(user)

    user.age = user_age
    db.commit()

    return user


def get_timeinfo_by_user_id(user_id: int):
    user = get_user_by_id(user_id)
    print(f"user: {user}")
    print(f"user.name: {user.name}")
    if user:
        time_info = user.time_info
        print(f"time_info: {time_info}")
        return time_info


def create_new_time_info(user_id: int):
    user = get_user_by_id(user_id)
    new_time_info = TimeInfo(user_id=user_id,
                             settings_id=user.current_settings_id)
    db.add(new_time_info)
    db.commit()
    return new_time_info


def set_user_current_retire_time(time_info_id: int, current_retire_time):
    time_info = get_timeinfo_by_id(time_info_id)
    print(time_info)
    time_info.current_retire_time = current_retire_time
    print(f"time_info.current_retire_time: {time_info.current_retire_time}")
    db.commit()


def set_user_best_retire_time(user_id: int, best_retire_time):
    time_settings = get_timesettings_by_id(user_id)
    print(f"time_settings: {time_settings}")
    time_settings.best_retire_time = best_retire_time
    db.commit()


def set_user_worst_retire_time(user_id: int, worst_retire_time):
    time_settings = get_timesettings_by_user_id(user_id)
    time_settings.worst_retire_time = worst_retire_time
    db.commit()


def set_user_best_wakeup_time(user_id: int, best_wakeup_time):
    time_settings = get_timesettings_by_user_id(user_id)
    time_settings.best_wakeup_time = best_wakeup_time
    db.commit()


def set_user_current_wakeup_time(user_id: int, current_wakeup_time):
    time_info = get_timeinfo_by_user_id(user_id)
    time_info.current_wakeup_time = current_wakeup_time
    db.add(time_info)
    db.commit()


def set_user_worst_wakeup_time(user_id: int, worst_wakeup_time):
    time_settings = get_timesettings_by_user_id(user_id)
    time_settings.worst_wakeup_time = worst_wakeup_time
    db.commit()


def set_user_best_duration_time(user_id: int, best_duration_time):
    time_settings = get_timesettings_by_user_id(user_id)
    time_settings.best_sleep_duration = best_duration_time
    db.commit()


def set_user_sleep_score(timeinfo: TimeInfo, sleep_score):
    timeinfo.sleep_score = sleep_score
    db.commit()


def create_new_user(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        user = User(id=user_id, state="NAME_REG")
        settings_time = TimeSettings(user_id=user_id)
        db.add(settings_time)
        db.commit()
        print(f"settings_time: {settings_time}")
        user.current_settings_id = settings_time.id
        print(f"user.current_settings_id: {user.current_settings_id}")
        print(f"user.time_settings: {user.time_settings}")
        db.add(user)
        db.commit()
