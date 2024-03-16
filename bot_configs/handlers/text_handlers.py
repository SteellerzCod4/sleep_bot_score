import bot_configs.keyboards.text_keyboards as tkb
import bot_configs.keyboards.inline_keyboards as ikb
import bot_configs.messages as msg
from aiogram import types
from bot_configs import dp
import database.operations as operations
# from bot_configs.forms import form
from bot_configs.input_validators import is_correct_name, is_correct_age, is_correct_time
from bot_configs.states import States


async def input_sleep_time(message: types.Message):
    await message.answer(text=msg.RETIRE_MODE_ACTIVATED, reply_markup=ikb.sleep_ikb)

async def process_main_keyboard(message: types.Message, user_id, state: States):
    handle_functions = {
        States.GO_TO_SLEEP : input_sleep_time
    }

    function = handle_functions.get(state)
    if function:
        await function(message)

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
    operations.set_user_state(user_id, States.BEST_RETIRE_TIME_REG)
    await message.reply(text=msg.BEST_RETIRE_TIME_MES)


async def input_best_retire_time(message: types.Message, user_id, text):
    best_retire_time = text
    if not is_correct_time(best_retire_time):
        await message.reply(text=msg.WARNING_TIME_MES)
        return

    operations.set_user_best_retire_time(user_id, best_retire_time)


@dp.message_handler()
async def handle_messages(message: types.Message):
    user_id = message.from_user.id
    state = operations.get_user_state(user_id)
    text = message.text

    handle_functions = {
        States.NAME_REG: input_name,
        States.AGE_REG: input_age,
        States.BEST_RETIRE_TIME_REG: input_best_retire_time,
        States.BEST_WAKEUP_TIME_REG: input_best_wakeup_time,
        States.START: process_main_keyboard# добавить все остальные состояния
    }

    function = handle_functions.get(state)
    if function:
        await function(message, user_id, text)
    # elif state in form.get_form_states():  # запуск анкеты
    #     await form.handle_input(message, state)
