# ФАЙЛ ДЛЯ ДОБАВЛЕНИЯ ФУНКЦИЙ-ВАЛИДАТОРОВ ВВОДИМЫХ ПОЛЬЗОВАТЕЛЕМ ДАННЫХ (check_name и т.п.)
def is_correct_name(input_name: str):
    return input_name.isalpha()


def is_correct_age(input_age: str):
    return input_age.isdigit() and 10 <= int(input_age) <= 100

def is_correct_time(best_time: str):
    if ":" in best_time:
        hours, minutes = best_time.split(":")
        return hours.isdigit() and minutes.isdigite and 0 <= int(hours) <= 23 and 0 <= int(minutes) <= 59
    return False
