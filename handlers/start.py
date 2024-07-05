from aiogram import types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database.create_tables import session
from database.models import User
from loader import dp, get_user
import yaml


with open('texts.yml', 'r', encoding='utf-8') as file:
    txt_messages = yaml.safe_load(file)


def main_kb_for_admin():
    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="📌Забронировать"))
    builder.add(types.KeyboardButton(text="📆Расписание"))
    builder.add(types.KeyboardButton(text="Отменить бронь"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def main_kb_for_user():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="📆Расписание"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

@dp.message(CommandStart())
async def msg_start(message: types.Message):
    user = await get_user(message)
    if user.status == "left":
        await message.answer(txt_messages['greeting'], reply_markup=main_kb_for_user())
        await message.answer(txt_messages['howToUse'])
    else:
        await message.answer(txt_messages['greeting'], reply_markup=main_kb_for_admin())
        await message.answer(txt_messages['howToUse'])
        if not session.query(User).where(User.username == message.from_user.username).first():
            new_user = User(username=message.from_user.username, role="user", telegram_id=message.from_user.id)
            session.add(new_user)
            session.commit()
