import bot_configs.keyboards as kb
import bot_configs.messages as msg
from aiogram import types
from bot_configs import dp
import database.operations as operations
# from bot_configs.forms import form
from bot_configs.states import States


@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    user_id = message.from_user.id
    if operations.get_user_state(user_id):
        await message.reply(msg.WELCOME)
    else:
        await message.reply(text=msg.START_REG_MES)
        operations.set_user_state(user_id, States.NAME_REG)
    operations.create_new_user(message.from_user.id)


# @dp.message_handler(commands=['form_start'])
# async def start_form(message: types.Message):
#     await message.reply(form.get_first_message())
#     state = form.get_first_state()
#     operations.set_user_state(message.from_user.id, state)

