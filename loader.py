from aiogram import Dispatcher, Bot, Router
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

form_router = Router()
dp.include_router(form_router)


async def get_user(message):
    user = await bot.get_chat_member(
        chat_id="-1002154658638", user_id=message.from_user.id
    )
    return user