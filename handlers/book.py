from aiogram import types, F
from aiogram.filters import CommandStart, Command
from aiogram.filters.state import State, StatesGroup
from loader import dp, bot
import yaml


with open('texts.yml', 'r', encoding='utf-8') as file:
    txt_messages = yaml.safe_load(file)


@dp.message(Command("book"))
async def book_place(message: types.Message):
    await message.answer(
        "Смотрю ты хочешь забронировать аудиторию\n"
        "Свободное время: <надо как-то сделать>"
    )
