import datetime

from database import get_db
from database.models import User, TimeInfo, TimeSettings
from bot_configs.states import States

db = get_db()


# ============================= Getters =============================
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


def get_user_attr(user_id: int, attr_name: str):
    user = get_user_by_id(user_id)
    return getattr(user, attr_name, None)


def get_user_time_settings_attr(user_id: int, attr_name: str):
    time_settings = get_timesettings_by_user_id(user_id)
    return getattr(time_settings, attr_name, None)


def get_timeinfo_by_user_id(user_id: int):
    user = get_user_by_id(user_id)
    print(f"user: {user}")
    print(f"user.name: {user.name}")
    if user:
        time_info = user.time_info
        print(f"time_info: {time_info}")
        return time_info



# ============================= Setters =============================
def setter_template(some_id, getter_func, attr_name, attr_value):
    entity = getter_func(some_id)
    setattr(entity, attr_name, attr_value)
    db.commit()


def set_user_state(user_id: int, value: States):
    setter_template(user_id, get_user_by_id, "state", value)


def set_user_name(user_id: int, user_name: str):
    setter_template(user_id, get_user_by_id, "name", user_name)


def set_user_age(user_id: int, user_age: int):
    setter_template(user_id, get_user_by_id, "age", user_age)


def set_user_current_retire_time(time_info_id: int, current_retire_time):
    setter_template(time_info_id, get_timeinfo_by_id, "current_retire_time", current_retire_time)


def set_user_best_retire_time(user_id: int, best_retire_time):
    setter_template(user_id, get_timesettings_by_id, "best_retire_time", best_retire_time)


def set_user_worst_retire_time(user_id: int, worst_retire_time):
    setter_template(user_id, get_timesettings_by_user_id, "worst_retire_time", worst_retire_time)


def set_user_best_wakeup_time(user_id: int, best_wakeup_time):
    setter_template(user_id, get_timesettings_by_user_id, "best_wakeup_time", best_wakeup_time)


def set_user_current_wakeup_time(user_id: int, current_wakeup_time):
    setter_template(user_id, get_timeinfo_by_user_id, "current_wakeup_time", current_wakeup_time)


def set_user_worst_wakeup_time(user_id: int, worst_wakeup_time):
    setter_template(user_id, get_timesettings_by_user_id, "worst_wakeup_time", worst_wakeup_time)


def set_user_best_duration_time(user_id: int, best_duration_time):
    setter_template(user_id, get_timesettings_by_user_id, "best_sleep_duration", best_duration_time)


def set_user_sleep_score(timeinfo: TimeInfo, sleep_score):
    timeinfo.sleep_score = sleep_score
    db.commit()


# ============================= Creators =============================
def create_new_time_info(user_id: int):
    user = get_user_by_id(user_id)
    new_time_info = TimeInfo(user_id=user_id,
                             settings_id=user.current_settings_id)
    db.add(new_time_info)
    db.commit()
    return new_time_info


def create_new_user(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        user = User(id=user_id, state="NAME_REG")
        settings_time = TimeSettings(user_id=user_id)
        db.add(settings_time)
        db.commit()
        user.current_settings_id = settings_time.id
        db.add(user)
        db.commit()
