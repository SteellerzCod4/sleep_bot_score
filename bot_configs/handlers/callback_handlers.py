import bot_configs.keyboards as kb
import bot_configs.messages as msg
from aiogram import types
from bot_configs import dp
from bot_configs.score_functions import f1_sleep_score
from bot_configs.states import States
import database.operations as operations
import datetime


@dp.callback_query_handler()
async def call_back_data(callback: types.CallbackQuery):
    data = callback.data
    user_id = callback.from_user.id

    if data == msg.END_SLEEP_CALLBACK:
        current_wakeup_time = datetime.datetime.now().strftime("%H:%M")
        time_info = operations.get_timeinfo_by_user_id(user_id)
        current_retire_time = time_info.current_retire_time
        best_retire_time = time_info.best_retire_time
        worst_retire_time = time_info.worst_retire_time
        best_wakeup_time = time_info.best_wakeup_time
        worst_wakeup_time = time_info.worst_wakeup_time
        best_sleep_duration = time_info.best_sleep_duration

        sleep_score = f1_sleep_score(current_retire_time, worst_retire_time, best_retire_time,
                                     current_wakeup_time, worst_wakeup_time, best_wakeup_time,
                                     best_sleep_duration, 3)

        operations.set_user_sleep_score(user_id, sleep_score)
        operations.set_user_state(user_id, States.START)
        await callback.answer(text=msg.SLEEP_SCORE_ACHIEVED_MES + str(sleep_score))

    elif data == msg.CANCEL_SLEEP_CALLBACK:
        operations.set_user_state(user_id, States.START)
        print("тута")
        await callback.answer(text=msg.CANCELED_SLEEP_MES)


# if __name__ == "__main__":
#     print(datetime.datetime.now().strftime("%H:%M"))