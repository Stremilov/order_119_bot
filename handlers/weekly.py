# from datetime import datetime, timedelta
# import logging
# from aiogram import F, types
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
#
# from database import Session
# from database.repositories.repo_booktime import BookTimeRepository
# from loader import bot, form_router
# from utils.custom_builder import StartReplyBuilder
# from utils.weekday_translation import get_weekday_ru
#
#
# @form_router.message(Command('weekly'))
# @form_router.message(F.text == '📅Расписание на неделю')
# @form_router.message(F.text == 'Прошлая неделя')
# @form_router.message(F.text == 'Следующая неделя')
# async def weekly_show(message: types.Message, state: FSMContext):
#     if message.text in ['/weekly', '📅Расписание на неделю']:
#         week = 0
#         last_user_msg_id = last_bot_msg_id = None
#         await state.clear()
#     else:
#         data = await state.get_data()
#         week = data.get('week')
#         last_user_msg_id = data.get("last_user_msg_id")
#         last_bot_msg_id = data.get("last_bot_msg_id")
#
#     if message.text == 'Прошлая неделя':
#         week -= 1
#     elif message.text == 'Следующая неделя':
#         week += 1
#
#     builder = StartReplyBuilder()
#     if week > 0:
#         builder.add(types.KeyboardButton(text='Прошлая неделя'))
#     builder.add(types.KeyboardButton(text='Следующая неделя'))
#     builder.adjust(2)
#
#     msg = [
#         'Расписание на неделю, ' +
#         (datetime.today() + timedelta(weeks=week, days=0 - datetime.today().weekday())).strftime("%d/%m") + ' \\- ' +
#         (datetime.today() + timedelta(weeks=week, days=6 - datetime.today().weekday())).strftime("%d/%m") + '\n\n'
#     ]
#
#     for i in range(0, 7):
#         day = datetime.today() + timedelta(weeks=week, days=i - datetime.today().weekday())
#         records = BookTimeRepository(Session()).get_bookings_by_date(day.strftime('%d.%m'), fetch=True)
#         if records:
#             msg.append(
#                 f"*{get_weekday_ru(day.strftime('%A'))}" + ', ' + day.strftime("%d/%m") + "*\n"
#             )
#         for number, item in enumerate(records, 1):
#             start_time, end_time, reason, renter = item
#
#             # Заменяем точки на /
#             formatted_reason = reason.replace('.', '/')
#             formatted_renter = renter.replace('.', '/')
#
#             # Экранируем символы для MarkdownV2
#             escaped_reason = formatted_reason.replace('-', '\\-').replace('_', '\\_').replace('*', '\\*')
#             escaped_renter = formatted_renter.replace('-', '\\-').replace('_', '\\_').replace('*', '\\*')
#
#             msg.append('\n'.join([
#                 f"{start_time}-{end_time}",
#                 f"{number}. *{escaped_reason}*",
#                 f"{'@' + escaped_renter : >11}",
#                 ''
#             ]))
#         if records and i < 6:
#             msg.append('')
#
#     if len(msg) == 1:
#         msg.append('Пусто')
#
#     bot_message = await message.answer(
#         '\n'.join(msg),
#         reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
#         parse_mode='MarkdownV2'
#     )
#
#     if last_bot_msg_id and last_user_msg_id:
#         await bot.delete_message(chat_id=message.chat.id, message_id=last_user_msg_id)
#         await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_msg_id)
#
#     await state.update_data(
#         week=week,
#         last_user_msg_id=message.message_id,
#         last_bot_msg_id=bot_message.message_id
#     )

from datetime import datetime, timedelta
import logging
from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database import Session
from database.repositories.repo_booktime import BookTimeRepository
from loader import bot, form_router
from utils.custom_builder import StartReplyBuilder
from utils.weekday_translation import get_weekday_ru


@form_router.message(Command('weekly'))
@form_router.message(F.text == '📅Расписание на неделю')
@form_router.message(F.text == 'Прошлая неделя')
@form_router.message(F.text == 'Следующая неделя')
async def weekly_show(message: types.Message, state: FSMContext):
    if message.text in ['/weekly', '📅Расписание на неделю']:
        week = 0
        last_user_msg_id = last_bot_msg_id = None
        await state.clear()
    else:
        data = await state.get_data()
        week = data.get('week', 0)
        last_user_msg_id = data.get("last_user_msg_id")
        last_bot_msg_id = data.get("last_bot_msg_id")

    if message.text == 'Прошлая неделя':
        week -= 1
    elif message.text == 'Следующая неделя':
        week += 1

    builder = StartReplyBuilder()
    if week > 0:
        builder.add(types.KeyboardButton(text='Прошлая неделя'))
    builder.add(types.KeyboardButton(text='Следующая неделя'))
    builder.adjust(2)

    # Создание сообщения
    msg = [
        'Расписание на неделю, ' +
        (datetime.today() + timedelta(weeks=week, days=0 - datetime.today().weekday())).strftime("%d.%m") + ' - ' +
        (datetime.today() + timedelta(weeks=week, days=6 - datetime.today().weekday())).strftime("%d.%m") + '\n\n'
    ]

    for i in range(0, 7):
        day = datetime.today() + timedelta(weeks=week, days=i - datetime.today().weekday())
        records = BookTimeRepository(Session()).get_bookings_by_date(day.strftime('%d.%m'), fetch=True)
        if records:
            msg.append(
                f"{get_weekday_ru(day.strftime('%A'))}" + ', ' + day.strftime("%d.%m") + '\n'
            )
        for number, item in enumerate(records, 1):
            start_time, end_time, reason, renter = item

            # Добавляем записи
            msg.append('\n'.join([
                f"{start_time}-{end_time}",
                f"{number}. {reason}",
                ''
            ]))
        if records and i < 6:
            msg.append('')

    if len(msg) == 1:
        msg.append('Пусто')

    # Отправляем сообщение в текстовом формате
    bot_message = await message.answer(
        '\n'.join(msg),
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )

    # Удаляем старые сообщения, если нужно
    if last_bot_msg_id and last_user_msg_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=last_user_msg_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_msg_id)

    # Обновляем состояние
    await state.update_data(
        week=week,
        last_user_msg_id=message.message_id,
        last_bot_msg_id=bot_message.message_id
    )
