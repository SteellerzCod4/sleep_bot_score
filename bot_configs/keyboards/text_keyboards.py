from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import bot_configs.messages as msg

# ----------------BUTTONS-----------------------------------------------------------------------------------------------
button_go_asleep = KeyboardButton(msg.BUTTON_GO_ASLEEP)
button_edit = KeyboardButton(msg.BUTTON_EDIT)
button_stats = KeyboardButton(msg.BUTTON_STATS)

button_edit_all = KeyboardButton(msg.BUTTON_EDIT_ALL)
button_edit_name = KeyboardButton(msg.BUTTON_EDIT_NAME)
button_edit_age = KeyboardButton(msg.BUTTON_EDIT_AGE)
button_edit_best_ret_time = KeyboardButton(msg.BUTTON_EDIT_BEST_RET_TIME)
button_edit_worst_ret_time = KeyboardButton(msg.BUTTON_EDIT_WORST_RET_TIME)
button_edit_best_wakeup_time = KeyboardButton(msg.BUTTON_EDIT_BEST_WAKEUP_TIME)
button_edit_worst_wakeup_time = KeyboardButton(msg.BUTTON_EDIT_WORST_WAKEUP_TIME)
button_edit_sleep_duration_time = KeyboardButton(msg.BUTTON_EDIT_SLEEP_DURATION_TIME)

# ----------------KEYBOARDS---------------------------------------------------------------------------------------------
main_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_kb.add(button_go_asleep).add(button_edit).add(button_stats)

edit_time_kb = ReplyKeyboardMarkup(resize_keyboard=True)
edit_time_kb.add(button_edit_name).add(button_edit_age).add(button_edit_best_ret_time).add(button_edit_worst_ret_time).add(
    button_edit_best_wakeup_time).add(button_edit_worst_wakeup_time).add(button_edit_sleep_duration_time)
