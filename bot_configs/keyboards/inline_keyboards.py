from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import bot_configs.messages as msg


# ----------------BUTTONS-----------------------------------------------------------------------------------------------
END_SLEEP_BUTTON = InlineKeyboardButton(text=msg.INLINE_BUTTON_END_SLEEP, callback_data=msg.END_SLEEP_CALLBACK)
CANCEL_SLEEP_BUTTON = InlineKeyboardButton(text=msg.INLINE_BUTTON_CANCEL_SLEEP, callback_data=msg.CANCEL_SLEEP_CALLBACK)

# -----------INLINE KEYBOARDS-------------------------------------------------------------------------------------------
sleep_ikb = InlineKeyboardMarkup()
sleep_ikb.add(END_SLEEP_BUTTON, CANCEL_SLEEP_BUTTON)