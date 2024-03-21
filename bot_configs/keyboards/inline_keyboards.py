from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import bot_configs.messages as msg
from bot_configs.states import States

SEPARATOR = "|"

# ----------------BUTTONS-----------------------------------------------------------------------------------------------
END_SLEEP_BUTTON = InlineKeyboardButton(text=msg.INLINE_BUTTON_END_SLEEP,
                                        callback_data=States.GO_TO_SLEEP.value + SEPARATOR + msg.END_SLEEP_CALLBACK)
CANCEL_SLEEP_BUTTON = InlineKeyboardButton(text=msg.INLINE_BUTTON_CANCEL_SLEEP,
                                           callback_data=States.GO_TO_SLEEP.value + SEPARATOR + msg.CANCEL_SLEEP_CALLBACK)


# -----------INLINE KEYBOARDS-------------------------------------------------------------------------------------------
def create_stop_sleep_keyboard(timeinfo_id):
    sleep_ikb = InlineKeyboardMarkup()
    END_SLEEP_BUTTON.callback_data += SEPARATOR + str(timeinfo_id)
    CANCEL_SLEEP_BUTTON.callback_data += SEPARATOR + str(timeinfo_id)
    sleep_ikb.add(END_SLEEP_BUTTON, CANCEL_SLEEP_BUTTON)
    return sleep_ikb

