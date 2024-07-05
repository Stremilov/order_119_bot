from aiogram import types

from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_kb():
    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="Забронировать"))
    builder.add(types.KeyboardButton(text="Расписание"))
    builder.adjust(2)
    return builder.as_markup()


def more_schedule_kb_for_admin():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Посмотреть еще"))
    builder.add(types.KeyboardButton(text="📌Забронировать"))
    builder.adjust(1)
    return builder.as_markup(one_time_kyeboard=True, resize_keyboard=True)


def more_schedule_kb_for_user():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Посмотреть еще"))
    builder.adjust(1)
    return builder.as_markup(one_time_kyeboard=True, resize_keyboard=True)
