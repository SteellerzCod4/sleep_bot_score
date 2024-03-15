import bot_configs.keyboards.text_keyboards as tkb
import bot_configs.messages as msg
from aiogram import types
from bot_configs import dp
import database.operations as operations
# from bot_configs.forms import form
from bot_configs.input_validators import is_correct_name, is_correct_age
from bot_configs.states import States


async def process_main_keyboard(message: types.Message):
    ...

async def input_name(message: types.Message, user_id, text):
    user_name = text
    if not is_correct_name(user_name):
        await message.reply(text=msg.WARNING_NAME_MES)
        return

    operations.set_user_name(user_id, user_name)
    operations.set_user_state(user_id, States.AGE_REG)
    await message.reply(text=msg.AGE_REG_MES)


async def input_age(message: types.Message, user_id, text):
    user_age = text
    if not is_correct_age(user_age):
        await message.reply(text=msg.WARNING_AGE_MES)
        return

    operations.set_user_name(user_id, user_age)
    operations.set_user_state(user_id, States.START)
    await message.reply(text=msg.REG_COMPLETE_MES, reply_markup=tkb.main_menu_kb)


@dp.message_handler()
async def handle_messages(message: types.Message):
    user_id = message.from_user.id
    state = operations.get_user_state(user_id)
    text = message.text

    handle_functions = {
        States.NAME_REG: input_name,
        States.AGE_REG: input_age,
        States.START: process_main_keyboard# добавить все остальные состояния
    }

    function = handle_functions.get(state)
    if function:
        await function(message, user_id, text)
    # elif state in form.get_form_states():  # запуск анкеты
    #     await form.handle_input(message, state)
