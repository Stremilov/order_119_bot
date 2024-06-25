from aiogram import types

from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_kb():
    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="Забронировать"))
    builder.add(types.KeyboardButton(text="Расписание"))
    builder.adjust(2)
    return builder.as_markup()