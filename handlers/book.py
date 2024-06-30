from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from datetime import datetime, timedelta

from database.create_tables import session, BookTime, User
from handlers.start import main_kb
from loader import dp, bot
import yaml

form_router = Router()
dp.include_router(form_router)

ADMIN_USERNAME = "stremilovv"


def get_admin_id():
    user = session.query(User).filter_by(username=ADMIN_USERNAME).first()
    return user.telegram_id if user else None


def create_approval_keyboard(ticket_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Одобрить", callback_data=f"approve_{ticket_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отклонить", callback_data=f"reject_{ticket_id}"
                )
            ],
        ]
    )
    return keyboard


def cancel_book(ticket_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Отмнить бронь", callback_data=f"cancel_{ticket_id}"
                )
            ],
        ]
    )
    return keyboard


class BookForm(StatesGroup):
    askForDate = State()
    askForStartTime = State()
    askForEndTime = State()
    PendingApproval = State()


with open("texts.yml", "r", encoding="utf-8") as file:
    txt_messages = yaml.safe_load(file)


@form_router.message(Command("book"))
@dp.message(F.text == "📌Забронировать")
async def book_place(message: types.Message, state: FSMContext):
    user = await bot.get_chat_member(chat_id="-1002154658638", user_id=message.from_user.id)
    if user.status == "left":
        await message.answer("Бронировать аудиторию могут только руководители", reply_markup=main_kb())
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

    booked_times = session.query(BookTime).filter_by(date=selected_date).all()
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
        last_user_message=message.message_id, last_bot_message=bot_message.message_id, selected_date=selected_date
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

    booked_times = session.query(BookTime).filter_by(date=selected_date).all()
    booked_intervals = []
    for booking in booked_times:
        start_hour, start_minute = map(int, booking.startTime.split(":"))
        end_hour, end_minute = map(int, booking.endTime.split(":"))
        start_in_minutes = start_hour * 60 + start_minute
        end_in_minutes = end_hour * 60 + end_minute
        booked_intervals.append((start_in_minutes, end_in_minutes))

    start_hour, start_minute = map(int, start_time.split(":")) if ":" in start_time else (int(start_time), 0)

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
    start_datetime = f"{start_time}"
    end_datetime = f"{end_time}"

    start_hour, start_minute = map(int, start_time.split(":"))
    end_hour, end_minute = map(int, end_time.split(":"))
    start_in_minutes = start_hour * 60 + start_minute
    end_in_minutes = end_hour * 60 + end_minute

    booked_times = session.query(BookTime).filter_by(date=selected_date).all()
    booked_intervals = []
    for booking in booked_times:
        b_start_hour, b_start_minute = map(int, booking.startTime.split(":"))
        b_end_hour, b_end_minute = map(int, booking.endTime.split(":"))
        b_start_in_minutes = b_start_hour * 60 + b_start_minute
        b_end_in_minutes = b_end_hour * 60 + b_end_minute
        booked_intervals.append((b_start_in_minutes, b_end_in_minutes))

    if any((start_in_minutes < end and end_in_minutes > start) for start, end in booked_intervals):
        await message.answer("Выбранное время перекрывается с существующей бронью. Пожалуйста, выберите другое время.")
        return

    new_ticket = BookTime(
        date=selected_date,
        startTime=start_datetime,
        endTime=end_datetime,
        renter=message.from_user.username,
    )
    session.add(new_ticket)
    session.commit()

    await bot.delete_message(chat_id=message.chat.id, message_id=last_user_message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)

    admin_id = get_admin_id()
    if admin_id:
        keyboard = create_approval_keyboard(new_ticket.id)
        await bot.send_message(
            admin_id,
            f"Новая заявка:\n\nДата: {new_ticket.date}\nВремя: {new_ticket.startTime}-{new_ticket.endTime}\nАвтор заявки: @{new_ticket.renter}",
            reply_markup=keyboard,
            parse_mode="html",
        )
    else:
        await message.answer("Не удалось найти администратора для отправки заявки")

    await message.answer(
        f"<b>Заявка отправлена</b>\n\nНачало: {new_ticket.startTime}\nКонец: {new_ticket.endTime}",
        parse_mode="html",
    )
    await state.set_state(BookForm.PendingApproval)


@dp.callback_query(lambda call: call.data.startswith("approve_"))
async def approve_booking(call: types.CallbackQuery):
    ticket_id = int(call.data.split("_")[1])
    ticket = session.query(BookTime).get(ticket_id)
    if ticket:
        ticket.status = "approved"
        session.commit()
        await call.message.edit_text(
            f"Бронь одобрена:\n\nДата: {ticket.date}\nНачало: {ticket.startTime}\nКонец: {ticket.endTime}\nАвтор заявки: @{ticket.renter}"
        )
        user = session.query(User).filter_by(username=ticket.renter).first()
        if user:
            await bot.send_message(
                user.telegram_id,
                f"<b>Ваша бронь одобрена</b>\n\nДата: {ticket.date}\nНачало: {ticket.startTime}\nКонец: {ticket.endTime}",
                parse_mode="html",
            )
    else:
        await call.message.edit_text("Ошибка: бронь не найдена")


@dp.callback_query(lambda call: call.data.startswith("reject_"))
async def reject_booking(call: types.CallbackQuery):
    ticket_id = int(call.data.split("_")[1])
    ticket = session.query(BookTime).get(ticket_id)
    if ticket:
        ticket.status = "rejected"
        session.delete(ticket)
        session.commit()
        await call.message.edit_text(
            f"Бронь отклонена:\n\nДата: {ticket.date}\nНачало: {ticket.startTime}\nКонец: {ticket.endTime}\nАвтор заявки: @{ticket.renter}"
        )
        user = session.query(User).filter_by(username=ticket.renter).first()
        if user:
            await bot.send_message(
                user.telegram_id,
                f"<b>Ваша бронь отклонена</b>\n\nДата: {ticket.date}\nНачало: {ticket.startTime}\nКонец: {ticket.endTime}",
                parse_mode="html",
            )
    else:
        await call.message.edit_text("Ошибка: бронь не найдена")
