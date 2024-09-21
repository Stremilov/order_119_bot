from datetime import datetime, timedelta

from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database import Session
from database.repo_booktime import BookTimeRepository
from loader import form_router


@form_router.message(Command('weekly'))
@form_router.message(F.text == '📅Расписание на неделю')
@form_router.message(F.text == 'Прошлая неделя')
@form_router.message(F.text == 'Следующая неделя')
async def weekly_show(message: types.Message, state: FSMContext):
    if message.text in ['/weekly', '📅Расписание на неделю']:
        week = 0
        await state.clear()
    else:
        data = await state.get_data()
        week = data.get('week')

    if message.text == 'Прошлая неделя':
        week -= 1
    elif message.text == 'Следующая неделя':
        week += 1

    builder = ReplyKeyboardBuilder()
    if week > 0:
        builder.add(types.KeyboardButton(text='Прошлая неделя'))
    builder.add(types.KeyboardButton(text='Следующая неделя'))
    builder.adjust(2)

    days_translation = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье",
    }
    msg = ['Расписание на неделю \\(' +
           (datetime.today() + timedelta(weeks=week, days=0 - datetime.today().weekday())).strftime("%d\\.%m") + '\\-' +
           (datetime.today() + timedelta(weeks=week, days=6 - datetime.today().weekday())).strftime("%d\\.%m") + '\\)\n'
           ]

    for i in range(0, 7):
        day = datetime.today() + timedelta(weeks=week, days=i - datetime.today().weekday())
        records = BookTimeRepository(Session()).get_bookings_by_date(day.strftime('%d.%m'), fetch=True)
        if records:
            msg.append(f'{days_translation[day.strftime("%A")]}' + r'\(' + day.strftime(r"%d\.%m") + r'\)')
        for startTime, endTime, reason, renter in records:
            msg.append(
                f"```\nВремя: {startTime}-{endTime}\nТема: {reason}\nАрендатор: @{renter}```"
            )
        if records and i < 6:
            msg.append('')

    if len(msg) == 1:
        msg.append('Пусто')

    await message.answer(
        '\n'.join(msg),
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
        parse_mode='MarkdownV2'
    )

    await state.update_data(week=week)
