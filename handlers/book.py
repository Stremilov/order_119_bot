from datetime import datetime, timedelta

import yaml
from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database import Session
from database.repo_booktime import BookTimeRepository
from handlers.start import main_kb_for_user
from loader import bot, form_router
from states.states import BookForm

with open("texts.yml", "r", encoding="utf-8") as file:
    txt_messages = yaml.safe_load(file)


@form_router.message(Command("book"))
@form_router.message(F.text == "📌Забронировать")
async def book_place(message: types.Message, state: FSMContext):
    user = await bot.get_chat_member(
        chat_id=message.chat.id, user_id=message.from_user.id
    )
    if user.status == "left":
        await message.answer(
            "Бронировать аудиторию могут только руководители отделов",
            reply_markup=main_kb_for_user(),
        )
        return

    await state.set_state(BookForm.askForDate)

    builder = ReplyKeyboardBuilder()
    today = datetime.today()
    for i in range(21):
        date_option = today + timedelta(days=i)
        builder.add(types.KeyboardButton(text=date_option.strftime("%d.%m")))
    builder.adjust(5)

    bot_message = await message.answer(
        "Выберите дату, когда ты хочешь начать бронь",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
    )
    await state.update_data(
        last_user_message=message.message_id, last_bot_message=bot_message.message_id
    )


@form_router.message(BookForm.askForDate)
async def ask_for_date(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    last_user_message_id = user_data.get("last_user_message")
    last_bot_message_id = user_data.get("last_bot_message")

    selected_date = message.text
    await state.update_data(selected_date=selected_date)
    await state.set_state(BookForm.askForStartTime)

    book_repo = BookTimeRepository(Session())
    booked_times = book_repo.get_bookings_by_date(date=selected_date)
    booked_intervals = []
    for booking in booked_times:
        start_hour, start_minute = map(int, booking.startTime.split(":"))
        end_hour, end_minute = map(int, booking.endTime.split(":"))
        start_in_minutes = start_hour * 60 + start_minute
        end_in_minutes = end_hour * 60 + end_minute
        booked_intervals.append((start_in_minutes, end_in_minutes))

    builder = ReplyKeyboardBuilder()
    for hour in range(7, 23):
        for minute in [0, 30]:
            time_str = f"{hour:02d}:{minute:02d}"
            time_int = hour * 60 + minute
            if not any(start <= time_int < end for start, end in booked_intervals):
                builder.add(types.KeyboardButton(text=time_str))
    builder.adjust(4)

    bot_message = await message.answer(
        "Выберите время, когда ты хочешь начать бронь",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
    )
    await bot.delete_message(chat_id=message.chat.id, message_id=last_user_message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
    await state.update_data(
        last_user_message=message.message_id,
        last_bot_message=bot_message.message_id,
        selected_date=selected_date,
    )


@form_router.message(BookForm.askForStartTime)
async def ask_for_start_time(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    last_user_message_id = user_data.get("last_user_message")
    last_bot_message_id = user_data.get("last_bot_message")
    selected_date = user_data.get("selected_date")

    start_time = message.text
    await state.update_data(start_time=start_time)
    await state.set_state(BookForm.askForEndTime)

    book_repo = BookTimeRepository(Session())
    booked_times = book_repo.get_bookings_by_date(date=selected_date)
    booked_intervals = []
    for booking in booked_times:
        start_hour, start_minute = map(int, booking.startTime.split(":"))
        end_hour, end_minute = map(int, booking.endTime.split(":"))
        start_in_minutes = start_hour * 60 + start_minute
        end_in_minutes = end_hour * 60 + end_minute
        booked_intervals.append((start_in_minutes, end_in_minutes))

    start_hour, start_minute = (
        map(int, start_time.split(":")) if ":" in start_time else (int(start_time), 0)
    )

    builder = ReplyKeyboardBuilder()
    for hour in range(start_hour, 23):
        for minute in [0, 30]:
            if hour == start_hour and minute <= start_minute:
                continue
            time_str = f"{hour:02d}:{minute:02d}"
            time_int = hour * 60 + minute
            if not any(start <= time_int < end for start, end in booked_intervals):
                builder.add(types.KeyboardButton(text=time_str))
    builder.adjust(4)

    bot_message = await message.answer(
        "Выберите время, когда ты хочешь закончить бронь",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
    )
    await bot.delete_message(chat_id=message.chat.id, message_id=last_user_message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
    await state.update_data(
        last_user_message=message.message_id, last_bot_message=bot_message.message_id
    )


@form_router.message(BookForm.askForEndTime)
async def ask_for_end_time(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    last_user_message_id = user_data.get("last_user_message")
    last_bot_message_id = user_data.get("last_bot_message")
    selected_date = user_data.get("selected_date")

    start_time = user_data.get("start_time")
    end_time = message.text

    start_hour, start_minute = map(int, start_time.split(":"))
    end_hour, end_minute = map(int, end_time.split(":"))
    start_in_minutes = start_hour * 60 + start_minute
    end_in_minutes = end_hour * 60 + end_minute

    book_repo = BookTimeRepository(Session())
    booked_times = book_repo.get_bookings_by_date(date=selected_date)
    booked_intervals = []
    for booking in booked_times:
        b_start_hour, b_start_minute = map(int, booking.startTime.split(":"))
        b_end_hour, b_end_minute = map(int, booking.endTime.split(":"))
        b_start_in_minutes = b_start_hour * 60 + b_start_minute
        b_end_in_minutes = b_end_hour * 60 + b_end_minute
        booked_intervals.append((b_start_in_minutes, b_end_in_minutes))

    if any(
        (start_in_minutes < end and end_in_minutes > start)
        for start, end in booked_intervals
    ):
        await message.answer(
            "Выбранное время перекрывается с существующей бронью. Пожалуйста, выберите другое время."
        )
        return

    await bot.delete_message(chat_id=message.chat.id, message_id=last_user_message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
    await state.update_data(end_time=end_time)
    await state.set_state(BookForm.askForReason)

    bot_message = await message.answer(
        "Пожалуйста, укажите причину для бронирования",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.update_data(
        last_user_message=message.message_id, last_bot_message=bot_message.message_id
    )


@form_router.message(BookForm.askForReason)
async def ask_for_reason(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    last_user_message_id = user_data.get("last_user_message")
    last_bot_message_id = user_data.get("last_bot_message")
    selected_date = user_data.get("selected_date")
    start_time = user_data.get("start_time")
    end_time = user_data.get("end_time")
    reason = message.text

    book_repo = BookTimeRepository(Session())
    new_ticket = book_repo.create_ticket(
        date=selected_date,
        start_time=start_time,
        end_time=end_time,
        renter=message.from_user.username,
        reason=reason,
    )

    await bot.delete_message(chat_id=message.chat.id, message_id=last_user_message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)

    await message.answer(
        '\n'.join([
            '<b>Новая бронь</b>',
            f'\nДата:{new_ticket.date}',
            f'Время: {new_ticket.startTime}-{new_ticket.endTime}',
            f'Причина: {new_ticket.reason}']),
        parse_mode="html",
    )

    await state.set_state(BookForm.PendingApproval)
