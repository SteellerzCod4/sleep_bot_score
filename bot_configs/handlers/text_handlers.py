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
    new_time_info = operations.create_new_time_info(message.from_user.id)
    operations.set_user_current_retire_time(new_time_info.id, current_retire_time)
    await message.answer(text=msg.RETIRE_MODE_ACTIVATED, reply_markup=ikb.create_stop_sleep_keyboard(new_time_info.id))


async def choose_time_to_edit(message: types.Message):
    user_id = message.from_user.id
    operations.set_user_state(user_id, States.EDITING)
    user_attrs = [operations.get_user_attr(user_id, user_attr) for user_attr in ["name", "age"]]
    time_setting_attrs = [operations.get_user_time_settings_attr(user_id, setting_attr) for setting_attr in
                          ["best_retire_time", "worst_retire_time", "best_wakeup_time", "worst_wakeup_time",
                           "best_sleep_duration"]]
    all_attrs = user_attrs + time_setting_attrs
    await message.answer(text=msg.EDITING_MODE_ACTIVATED.format(*all_attrs), reply_markup=tkb.edit_time_kb)


async def process_main_keyboard(message: types.Message, user_id, state: States):
    handle_functions = {
        msg.BUTTON_GO_ASLEEP: input_sleep_time,
        msg.BUTTON_EDIT: choose_time_to_edit
    }

    function = handle_functions.get(state)
    if function:
        await function(message)


async def process_edit_keyboard(message: types.Message, user_id, state: States):
    button_text = message.text

    button2state = {
        msg.BUTTON_EDIT_NAME: States.NAME_REG,
        msg.BUTTON_EDIT_AGE: States.AGE_REG,
        msg.BUTTON_EDIT_WORST_RET_TIME: States.WORST_RETIRE_TIME_REG,
        msg.BUTTON_EDIT_BEST_RET_TIME: States.BEST_RETIRE_TIME_REG,
        msg.BUTTON_EDIT_WORST_WAKEUP_TIME: States.WORST_WAKEUP_TIME_REG,
        msg.BUTTON_EDIT_BEST_WAKEUP_TIME: States.BEST_WAKEUP_TIME_REG,
        msg.BUTTON_EDIT_SLEEP_DURATION_TIME: States.BEST_DURATION_TIME_REG
    }

    new_state = button2state.get(button_text)
    if new_state:
        operations.set_user_state(user_id, new_state)
        await message.answer(text=msg.PLS_INPUT_NEW_VALUE, reply_markup=tkb.ReplyKeyboardRemove())


async def input_name(message: types.Message, user_id, text):
    user_name = text
    if not is_correct_name(user_name):
        await message.reply(text=msg.WARNING_NAME_MES)
        return

    attr_is_already_exists = operations.get_user_attr(user_id, "name")
    print(f"attr_is_already_exists name: {attr_is_already_exists}")
    next_state = States.START if attr_is_already_exists else States.AGE_REG
    next_message = msg.REG_COMPLETE_MES if attr_is_already_exists else msg.AGE_REG_MES
    next_kb = tkb.main_menu_kb if attr_is_already_exists else tkb.ReplyKeyboardRemove()

    operations.set_user_name(user_id, user_name)
    operations.set_user_state(user_id, next_state)

    await message.answer(text=next_message, reply_markup=next_kb)


async def input_age(message: types.Message, user_id, text):
    user_age = text
    if not is_correct_age(user_age):
        await message.reply(text=msg.WARNING_AGE_MES)
        return

    attr_is_already_exists = operations.get_user_attr(user_id, "age")
    next_state = States.START if attr_is_already_exists else States.BEST_RETIRE_TIME_REG
    next_message = msg.REG_COMPLETE_MES if attr_is_already_exists else msg.BEST_RETIRE_TIME_MES
    next_kb = tkb.main_menu_kb if attr_is_already_exists else None

    operations.set_user_age(user_id, user_age)
    operations.set_user_state(user_id, next_state)

    await message.answer(text=next_message, reply_markup=next_kb)


async def input_best_retire_time(message: types.Message, user_id, text):
    best_retire_time = text
    if not is_correct_time(best_retire_time):
        await message.reply(text=msg.WARNING_TIME_MES)
        return

    attr_is_already_exists = operations.get_user_time_settings_attr(user_id, "best_retire_time")
    next_state = States.START if attr_is_already_exists else States.WORST_RETIRE_TIME_REG
    next_message = msg.REG_COMPLETE_MES if attr_is_already_exists else msg.LATEST_RETIRE_TIME_MES
    next_kb = tkb.main_menu_kb if attr_is_already_exists else None

    operations.set_user_best_retire_time(user_id, best_retire_time)
    operations.set_user_state(user_id, next_state)

    await message.answer(text=next_message, reply_markup=next_kb)


async def input_worst_retire_time(message: types.Message, user_id, text):
    worst_retire_time = text
    if not is_correct_time(worst_retire_time):
        await message.reply(text=msg.WARNING_TIME_MES)
        return

    attr_is_already_exists = operations.get_user_time_settings_attr(user_id, "worst_retire_time")
    next_state = States.START if attr_is_already_exists else States.BEST_WAKEUP_TIME_REG
    next_message = msg.REG_COMPLETE_MES if attr_is_already_exists else msg.BEST_WAKEUP_TIME_MES
    next_kb = tkb.main_menu_kb if attr_is_already_exists else None

    operations.set_user_worst_retire_time(user_id, worst_retire_time)
    operations.set_user_state(user_id, next_state)

    await message.answer(text=next_message, reply_markup=next_kb)


async def input_best_wakeup_time(message: types.Message, user_id, text):
    best_wakeup_time = text
    if not is_correct_time(best_wakeup_time):
        await message.reply(text=msg.WARNING_TIME_MES)
        return

    attr_is_already_exists = operations.get_user_time_settings_attr(user_id, "best_wakeup_time")
    next_state = States.START if attr_is_already_exists else States.WORST_WAKEUP_TIME_REG
    next_message = msg.REG_COMPLETE_MES if attr_is_already_exists else msg.LATEST_WAKEUP_TIME_MES
    next_kb = tkb.main_menu_kb if attr_is_already_exists else None

    operations.set_user_best_wakeup_time(user_id, best_wakeup_time)
    operations.set_user_state(user_id, next_state)

    await message.answer(text=next_message, reply_markup=next_kb)


async def input_worst_wakeup_time(message: types.Message, user_id, text):
    worst_wakeup_time = text
    if not is_correct_time(worst_wakeup_time):
        await message.reply(text=msg.WARNING_TIME_MES)
        return

    attr_is_already_exists = operations.get_user_time_settings_attr(user_id, "worst_wakeup_time")
    next_state = States.START if attr_is_already_exists else States.BEST_DURATION_TIME_REG
    next_message = msg.REG_COMPLETE_MES if attr_is_already_exists else msg.BEST_DURATION_TIME_MES
    next_kb = tkb.main_menu_kb if attr_is_already_exists else None

    operations.set_user_worst_wakeup_time(user_id, worst_wakeup_time)
    operations.set_user_state(user_id, next_state)

    await message.answer(text=next_message, reply_markup=next_kb)


async def input_best_duration_time(message: types.Message, user_id, text):
    best_duration_time = text
    if not is_correct_duration_time(best_duration_time):
        await message.reply(text=msg.WARNING_DURATION_TIME_MES)
        return

    attr_is_already_exists = operations.get_user_time_settings_attr(user_id, "best_sleep_duration")
    next_state = States.START if attr_is_already_exists else States.START
    next_message = msg.REG_COMPLETE_MES if attr_is_already_exists else msg.REG_COMPLETE_MES
    next_kb = tkb.main_menu_kb if attr_is_already_exists else tkb.main_menu_kb

    operations.set_user_best_duration_time(user_id, best_duration_time)
    operations.set_user_state(user_id, next_state)

    await message.answer(text=next_message, reply_markup=next_kb)


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
        States.START: process_main_keyboard,
        States.EDITING: process_edit_keyboard,
    }

    function = handle_functions.get(state)
    if function:
        await function(message, user_id, text)
    # elif state in form.get_form_states():  # запуск анкеты
    #     await form.handle_input(message, state)
