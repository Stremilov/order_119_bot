from aiogram import types

from utils.custom_builder import StartReplyBuilder


def main_kb():
    builder = StartReplyBuilder()

    builder.add(types.KeyboardButton(text="Забронировать"))
    builder.add(types.KeyboardButton(text="Расписание"))
    builder.adjust(3)
    return builder.as_markup()


def more_schedule_kb_for_admin():
    builder = StartReplyBuilder()
    builder.add(types.KeyboardButton(text="Посмотреть еще"))
    builder.add(types.KeyboardButton(text="📌Забронировать"))
    builder.adjust(1)
    return builder.as_markup(one_time_kyeboard=True, resize_keyboard=True)


def more_schedule_kb_for_user():
    builder = StartReplyBuilder()
    builder.add(types.KeyboardButton(text="Смотреть далее"))
    builder.adjust(1)
    return builder.as_markup(one_time_kyeboard=True, resize_keyboard=True)
