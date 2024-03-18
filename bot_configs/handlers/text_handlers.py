import bot_configs.keyboards.text_keyboards as tkb
import bot_configs.keyboards.inline_keyboards as ikb
import bot_configs.messages as msg
from aiogram import types
from bot_configs import dp
import database.operations as operations
# from bot_configs.forms import form
from bot_configs.input_validators import is_correct_name, is_correct_age, is_correct_time, is_correct_duration_time
from bot_configs.states import States
import datetime


async def input_sleep_time(message: types.Message):
    current_retire_time = datetime.datetime.now().strftime("%H:%M")
    operations.set_user_current_retire_time(message.from_user.id, current_retire_time)
    await message.answer(text=msg.RETIRE_MODE_ACTIVATED, reply_markup=ikb.sleep_ikb)


async def process_main_keyboard(message: types.Message, user_id, state: States):
    handle_functions = {
        msg.BUTTON_GO_ASLEEP: input_sleep_time
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
    operations.update_time_info_for_user(user_id, 2.22)
    await message.reply(text=msg.AGE_REG_MES)


async def input_age(message: types.Message, user_id, text):
    user_age = text
    if not is_correct_age(user_age):
        await message.reply(text=msg.WARNING_AGE_MES)
        return

    operations.set_user_age(user_id, user_age)
    operations.set_user_state(user_id, States.BEST_RETIRE_TIME_REG)
    await message.reply(text=msg.BEST_RETIRE_TIME_MES)


async def input_best_retire_time(message: types.Message, user_id, text):
    best_retire_time = text
    if not is_correct_time(best_retire_time):
        await message.reply(text=msg.WARNING_TIME_MES)
        return

    operations.set_user_best_retire_time(user_id, best_retire_time)
    operations.set_user_state(user_id, States.WORST_RETIRE_TIME_REG)
    await message.reply(text=msg.LATEST_RETIRE_TIME_MES)


async def input_worst_retire_time(message: types.Message, user_id, text):
    worst_retire_time = text
    if not is_correct_time(worst_retire_time):
        await message.reply(text=msg.WARNING_TIME_MES)
        return

    operations.set_user_worst_retire_time(user_id, worst_retire_time)
    operations.set_user_state(user_id, States.BEST_WAKEUP_TIME_REG)
    await message.reply(text=msg.BEST_WAKEUP_TIME_MES)


async def input_best_wakeup_time(message: types.Message, user_id, text):
    best_wakeup_time = text
    if not is_correct_time(best_wakeup_time):
        await message.reply(text=msg.WARNING_TIME_MES)
        return

    operations.set_user_best_wakeup_time(user_id, best_wakeup_time)
    operations.set_user_state(user_id, States.WORST_WAKEUP_TIME_REG)
    await message.reply(text=msg.LATEST_WAKEUP_TIME_MES)


async def input_worst_wakeup_time(message: types.Message, user_id, text):
    worst_wakeup_time = text
    if not is_correct_time(worst_wakeup_time):
        await message.reply(text=msg.WARNING_TIME_MES)
        return

    operations.set_user_worst_wakeup_time(user_id, worst_wakeup_time)
    operations.set_user_state(user_id, States.BEST_DURATION_TIME_REG)
    await message.reply(text=msg.BEST_DURATION_TIME_MES)


async def input_best_duration_time(message: types.Message, user_id, text):
    best_duration_time = text
    if not is_correct_duration_time(best_duration_time):
        await message.reply(text=msg.WARNING_DURATION_TIME_MES)
        return

    operations.set_user_best_duration_time(user_id, best_duration_time)
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
        States.BEST_RETIRE_TIME_REG: input_best_retire_time,
        States.WORST_RETIRE_TIME_REG: input_worst_retire_time,
        States.BEST_WAKEUP_TIME_REG: input_best_wakeup_time,
        States.WORST_WAKEUP_TIME_REG: input_worst_wakeup_time,
        States.BEST_DURATION_TIME_REG: input_best_duration_time,
        States.START: process_main_keyboard  # добавить все остальные состояния
    }

    function = handle_functions.get(state)
    if function:
        await function(message, user_id, text)
    # elif state in form.get_form_states():  # запуск анкеты
    #     await form.handle_input(message, state)
