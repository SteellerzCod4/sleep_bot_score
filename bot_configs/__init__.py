from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from .config import ConfigData
from bot_configs.utilities.debug_manager import DebugManager
from .utilities.parse_cities import Cities

admins = [456022925, 523468577]
config_data = ConfigData()
bot = Bot(token=config_data.BOT_TOKEN)
dp = Dispatcher(bot)
cities = Cities(config_data.FILENAME_CITIES)
debug_manager = DebugManager(config_data, admins)
