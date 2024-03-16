import bot_configs.keyboards as kb
import bot_configs.messages as msg
from aiogram import types
from bot_configs import dp
import database.operations as operations
import datetime


@dp.callback_query_handler()
async def call_back_data(callback: types.CallbackQuery):
    data = callback.data
    user_id = callback.from_user.id

    if data == msg.END_SLEEP_CALLBACK:
        wakeup_time = datetime.datetime.now().strftime("%H:%M")


# if __name__ == "__main__":
#     print(datetime.datetime.now().strftime("%H:%M"))