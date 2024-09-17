from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database.create_tables import session
from database.models import User, BookTime
from handlers.start import main_kb_for_user, main_kb_for_admin
from keyboards.inline.usermode_inline import create_cancel_keyboard
from loader import dp, bot, form_router, get_user
from states.states import UnBookForm


@form_router.message(Command("unbook"))
@form_router.message(F.text == "Отменить бронь")
async def book_place(message: types.Message, state: FSMContext):
    await state.set_state(UnBookForm.askForDescription)

    user = await get_user(message)
    if user.status == "left":
        await message.answer(
            "Отменять бронирование могут только руководители отделов",
            reply_markup=main_kb_for_user(),
        )
        return

    bookings = (
        session.query(BookTime)
        .filter(BookTime.renter == message.from_user.username)
        .order_by(BookTime.id)
        .all()
    )
    builder = ReplyKeyboardBuilder()
    for booking in bookings:
        builder.add(
            types.KeyboardButton(
                text=f"Дата: {booking.date} Начало: {booking.startTime} Конец: {booking.endTime}"
            )
        )
        builder.adjust(1)

    await message.answer(
        text="Выберите какую именно бронь вы хотите отменить",
        reply_markup=builder.as_markup(one_time_keyboard=True, resize_keyboard=True),
    )


@form_router.message(UnBookForm.askForDescription)
async def ask_for_date(message: types.Message, state: FSMContext):
    await state.set_state(UnBookForm.sendTicket)
    await state.update_data(selected_date=message.text)
    await message.answer(
        text="Вы уверены что хотите отменить бронь?",
        reply_markup=create_cancel_keyboard(),
    )


@dp.callback_query(lambda call: call.data == "cancel_approve")
async def approve_booking(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    date = user_data.get("selected_date")

    await call.message.delete()

    ticket = (
        session.query(BookTime)
        .filter(
            BookTime.date == date.split()[1],
            BookTime.startTime == date.split()[3],
            BookTime.endTime == date.split()[5],
        )
        .first()
    )
    user = session.query(User).filter_by(username=ticket.renter).first()
    session.delete(ticket)
    session.commit()
    if user:
        await bot.send_message(
            user.telegram_id,
            f"<b>Ваша бронь отменена</b>",
            parse_mode="html",
            reply_markup=main_kb_for_admin(),
        )


@dp.callback_query(lambda call: call.data == "cancel_reject")
async def reject_booking(call: types.CallbackQuery):
    await call.message.edit_text("Процесс отмены закончен")
