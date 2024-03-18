import sys
from aiogram.utils import executor
from bot_configs import dp, debug_manager
from database import Base, engine
from bot_configs.handlers.commands_handlers import *
from bot_configs.handlers.callback_handlers import *
from bot_configs.handlers.text_handlers import *

DEBUG_MODE = False


async def on_startup(_):
    print("Бот активирован")


if __name__ == '__main__':
    if DEBUG_MODE:
        sys.stderr = debug_manager
    Base.metadata.create_all(engine)
    executor.start_polling(dp, on_startup=on_startup)
