from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database.create_tables import session, BookTime, User
from handlers.change_admin import load_config
from handlers.start import main_kb
from keyboards.inline.usermode_inline import create_cancel_keyboard
from loader import dp, bot, form_router


config = load_config()
ADMIN_USERNAME = config["ADMIN_USERNAME"]

def get_admin_id():
    user = session.query(User).filter_by(username=ADMIN_USERNAME).first()
    return user.telegram_id if user else None

class UnBookForm(StatesGroup):
    askForDescription = State()
    sendTicket = State()


@form_router.message(Command("unbook"))
@dp.message(F.text == "Отменить бронь")
async def book_place(message: types.Message, state: FSMContext):
    await state.set_state(UnBookForm.askForDescription)

    user = await bot.get_chat_member(chat_id="-1002154658638", user_id=message.from_user.id)
    if user.status == "left":
        await message.answer( "Оставлять заявку на отмену брони могут только руководители", reply_markup=main_kb())
        return

    bookings = session.query(BookTime).filter(BookTime.renter == message.from_user.username).order_by(BookTime.id).all()
    builder = ReplyKeyboardBuilder()
    for booking in bookings:
        builder.add(types.KeyboardButton(text=f"Дата: {booking.date} Начало: {booking.startTime} Конец: {booking.endTime}"))
        builder.adjust(1)

    await message.answer(text="Выберите какую именно бронь вы хотите отменить",
                         reply_markup=builder.as_markup(one_time_keyboard=True, resize_keyboard=True)
    )


@form_router.message(UnBookForm.askForDescription)
async def ask_for_date(message: types.Message, state: FSMContext):
    await state.set_state(UnBookForm.sendTicket)
    await state.update_data(selected_date=message.text)
    await message.answer(text="Опишите причину по которой хотите отменить бронь")


@form_router.message(UnBookForm.sendTicket)
async def send_ticket(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    date = user_data.get("selected_date")
    description = message.text

    admin_id = get_admin_id()

    if admin_id:
        keyboard = create_cancel_keyboard()
        await bot.send_message(
            admin_id,
            f"<b>Заявка на отмену брони</b>\n\nДата: {date.split()[1]}\nВремя: {date.split()[3]}-{date.split()[5]}\nПричина: {description}\nАвтор заявки: @{message.from_user.username}",
            reply_markup=keyboard,
            parse_mode="html",
        )
    else:
        await message.answer("Не удалось найти администратора для отправки заявки")
    await message.answer(
        f"<b>Заявка на отмену брони отправлена</b>\n\nДата: {date.split()[1]}\nВремя: {date.split()[3]}-{date.split()[5]}\nПричина: {description}",
        parse_mode="html",
    )


@dp.callback_query(lambda call: call.data == "cancel_approve")
async def approve_booking(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    date = user_data.get("selected_date")

    await call.message.edit_text(
        "Заявка одобрена"
    )

    ticket = session.query(BookTime).filter(BookTime.date == date.split()[1], BookTime.startTime == date.split()[3],
                                            BookTime.endTime == date.split()[5]).first()
    user = session.query(User).filter_by(username=ticket.renter).first()
    session.delete(ticket)
    session.commit()
    if user:
        await bot.send_message(
            user.telegram_id,
            f"<b>Ваша бронь отменена</b>",
            parse_mode="html",
            reply_markup=main_kb()
        )


@dp.callback_query(lambda call: call.data == "cancel_reject")
async def reject_booking(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    date = user_data.get("selected_date")

    await call.message.edit_text(
        f"Заявка отклонена"
    )

    ticket = session.query(BookTime).filter(BookTime.date == date.split()[1], BookTime.startTime == date.split()[3],
                                            BookTime.endTime == date.split()[5]).first()
    user = session.query(User).filter_by(username=ticket.renter).first()
    if user:
        await bot.send_message(
            user.telegram_id,
            f"<b>Ваша заявка отклонена</b>",
            parse_mode="html",
            reply_markup=main_kb()
        )