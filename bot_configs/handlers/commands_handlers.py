import bot_configs.keyboards as kb
import bot_configs.messages as msg
from aiogram import types
from bot_configs import dp
import database.operations as operations
from bot_configs.forms import form


@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    print(message.text)
    await message.reply(msg.WELCOME)
    operations.create_new_user(message.from_user.id)


@dp.message_handler(commands=['form_start'])
async def start_form(message: types.Message):
    await message.reply(form.get_first_message())
    state = form.get_first_state()
    operations.set_user_state(message.from_user.id, state)

