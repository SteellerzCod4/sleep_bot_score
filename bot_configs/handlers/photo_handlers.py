import bot_configs.keyboards as kb
import bot_configs.messages as msg
from aiogram import types
from bot_configs import dp
import database.operations as operations


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    user_id = str(message.from_user.id)
    photo_id = message.photo[0].file_id
