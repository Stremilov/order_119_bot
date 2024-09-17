from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types


def main_kb_for_admin():
    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="📌Забронировать"))
    builder.add(types.KeyboardButton(text="📆Расписание"))
    builder.add(types.KeyboardButton(text="⌚История бронирования"))
    builder.add(types.KeyboardButton(text="Отменить бронь"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def main_kb_for_user():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="📆Расписание"))
    builder.add(types.KeyboardButton(text="⌚История бронирования"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
