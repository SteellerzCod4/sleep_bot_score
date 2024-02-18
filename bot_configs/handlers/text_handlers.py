import bot_configs.keyboards as kb
import bot_configs.messages as msg
from aiogram import types
from bot_configs import dp
import database.operations as operations
from bot_configs.forms import form


@dp.message_handler()
async def handle_messages(message: types.Message):
    user_id = message.from_user.id
    state = operations.get_user_state(user_id)
    text = message.text

    handle_functions = {
                        # добавить все остальные состояния
                        }

    function = handle_functions.get(state)
    if function:
        await function(message, user_id, text)
    elif state in form.get_form_states():  # запуск анкеты
        await form.handle_input(message, state)

