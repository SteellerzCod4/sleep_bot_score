# ФАЙЛ ДЛЯ ДОБАВЛЕНИЯ ФУНКЦИЙ-ВАЛИДАТОРОВ ВВОДИМЫХ ПОЛЬЗОВАТЕЛЕМ ДАННЫХ (check_name и т.п.)
def is_correct_name(input_name: str):
    return input_name.isalpha()


def is_correct_age(input_age: str):
    return input_age.isdigit() and 10 <= int(input_age) <= 100
