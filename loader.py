from aiogram import Dispatcher, Bot
from config_data.config import BOT_TOKEN
from aiogram.contrib.middlewares.logging import LoggingMiddleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
