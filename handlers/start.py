from aiogram import types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database.create_tables import User, session
from loader import dp
import yaml


with open('texts.yml', 'r', encoding='utf-8') as file:
    txt_messages = yaml.safe_load(file)


def main_kb():
    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="📌Забронировать"))
    builder.add(types.KeyboardButton(text="📆Расписание"))
    builder.adjust(2)
    return builder.as_markup()

@dp.message(CommandStart())
async def msg_start(message: types.Message):
    await message.answer(txt_messages['greeting'], reply_markup=main_kb())
    await message.answer(txt_messages['howToUse'])
    if not session.query(User).where(User.username == message.from_user.username).first():
        new_user = User(username=message.from_user.username, role="user", telegram_id=message.from_user.id)
        session.add(new_user)
        session.commit()
