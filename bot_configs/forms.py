# from bot_configs.utilities.form_builder import Form, Step
# import bot_configs.states as st
# from database.operations import set_user_name, set_user_last_name, set_user_gender
#
#
# def check_name(name):
#     bad_symbols = {'\n', '\t', '\r', ',', '.', '/', '>', '<', '\\', '|', ':',
#                    ';', '\'', '"', '`', '~', '!', '@', '#', '$', '%', '^', '&',
#                    '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '?', '№'}
#     if bad_symbols & set(name) or len(name) > 30:
#         return False
#     return True
#
#
# input_name_step = Step("Введите ваше имя",
#                        st.NAME, set_user_name,
#                        "Имя сохранено",
#                        "Имя отредактировано",
#                        check_name,
#                        "Имя некорректно")
#
# input_last_name_step = Step("Введите вашу фамилию",
#                             st.LAST_NAME, set_user_last_name,
#                             "Фамилия сохранена",
#                             "Фамилия отредактирована",
#                             check_name,
#                             "Фамилия некорректна")
#
# input_gender_step = Step("Введите ваш пол",
#                          st.GENDER, set_user_gender,
#                          "Пол сохранён",
#                          "Пол отредактирован")
#
# form = Form("WAIT_FOR_ACTION", finish_message="Форма успешно заполнена!")
# form.add_step(input_name_step)
# form.add_step(input_last_name_step)
# form.add_step(input_gender_step)
