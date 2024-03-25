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
    kb, button_text, *params = data.split(ikb.SEPARATOR)
    if kb == States.GO_TO_SLEEP.value:
        time_info_id = params[0]
        if button_text == msg.END_SLEEP_CALLBACK:
            current_wakeup_time = datetime.datetime.now().strftime("%H:%M")
            time_info = operations.get_timeinfo_by_id(time_info_id)
            time_settings = operations.get_timesettings_by_user_id(user_id)
            print(f"time_info.current_retire_time in data: {time_info.current_retire_time}")
            current_retire_time = time_info.current_retire_time
            best_retire_time = time_settings.best_retire_time
            worst_retire_time = time_settings.worst_retire_time

            best_wakeup_time = time_settings.best_wakeup_time
            worst_wakeup_time = time_settings.worst_wakeup_time

            best_sleep_duration = time_settings.best_sleep_duration
            # TODO: переписать функцию, чтобы она принимала только объект TimeInfo
            sleep_score = f1_sleep_score(current_retire_time, worst_retire_time, best_retire_time,
                                         current_wakeup_time, worst_wakeup_time, best_wakeup_time,
                                         best_sleep_duration, 3)
            print(f"sleep_score: {sleep_score}")
            operations.set_user_sleep_score(time_info, sleep_score)
            operations.set_user_state(user_id, States.START)
            await callback.answer(text=msg.SLEEP_SCORE_ACHIEVED_MES + str(sleep_score))

        elif button_text == msg.CANCEL_SLEEP_CALLBACK:
            operations.set_user_state(user_id, States.START)
            print("тута")
            await callback.answer(text=msg.CANCELED_SLEEP_MES)


# if __name__ == "__main__":
#     print(datetime.datetime.now().strftime("%H:%M"))