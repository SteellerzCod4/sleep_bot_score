from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import bot_configs.messages as msg

# ----------------BUTTONS-----------------------------------------------------------------------------------------------
button_go_asleep = KeyboardButton(msg.BUTTON_GO_ASLEEP)
button_edit = KeyboardButton(msg.BUTTON_EDIT)
button_stats = KeyboardButton(msg.BUTTON_STATS)

# ----------------KEYBOARDS---------------------------------------------------------------------------------------------
main_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_kb.add(button_go_asleep).add(button_edit).add(button_stats)