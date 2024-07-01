from aiogram import types, F
from aiogram.filters import CommandStart, Command
from aiogram.filters.state import State, StatesGroup
from loader import dp, bot
import yaml


@dp.message(Command('help'))
async def show_help(message: types.Message):
    commands_list = (
        "Доступные команды:\n"
        "\n"
        "/help - <b>Получить помощь</b>\n"
        "/book - <b>Забронировать аудиторию</b>\n"
        "/schedule - <b>Расписание брони</b>\n"
        "/change - <b>Изменить руководителя</b>"
    )
    await message.answer(commands_list, parse_mode='html')
