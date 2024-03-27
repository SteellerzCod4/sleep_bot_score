import bot_configs.keyboards as kb
import bot_configs.messages as msg
from aiogram import types
from bot_configs import dp
from bot_configs.score_functions import f1_sleep_score
from bot_configs.states import States
from bot_configs.keyboards import inline_keyboards as ikb
import database.operations as operations
import datetime


@dp.callback_query_handler()
async def call_back_data(callback: types.CallbackQuery):
    data = callback.data
    user_id = callback.from_user.id
    kb_type, button_text, *params = data.split(ikb.SEPARATOR)

    handle_kb_functions = {
        States.GO_TO_SLEEP.value: process_go_to_sleep_kb
    }

    function = handle_kb_functions.get(kb_type)
    if function:
        await function(callback, button_text, params[0], user_id)


async def process_go_to_sleep_kb(callback: types.CallbackQuery, button_text, time_info_id, user_id):
    if button_text == msg.END_SLEEP_CALLBACK:
        current_wakeup_time = datetime.datetime.now().strftime("%H:%M")
        time_info = operations.get_timeinfo_by_id(time_info_id)
        time_settings = operations.get_timesettings_by_user_id(user_id)

        sleep_score = f1_sleep_score(current_wakeup_time, time_info, time_settings, 3)
        print(f"sleep_score: {sleep_score}")

        operations.set_user_sleep_score(time_info, sleep_score)
        operations.set_user_state(user_id, States.START)

        await callback.answer(text=msg.SLEEP_SCORE_ACHIEVED_MES + str(sleep_score))

    elif button_text == msg.CANCEL_SLEEP_CALLBACK:
        operations.delete_time_info_by_id(time_info_id)
        operations.set_user_state(user_id, States.START)
        await callback.answer(text=msg.CANCELED_SLEEP_MES)

# if __name__ == "__main__":
#     print(datetime.datetime.now().strftime("%H:%M"))
