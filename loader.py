from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
