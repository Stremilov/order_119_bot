from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from datetime import datetime, timedelta

from keyboards.reply.usermodes import more_schedule_kb_for_user
from loader import form_router

from states.states import HistoryForm
from utils.image import generate_schedule_image, send_image


@form_router.message(Command("history"))
@form_router.message(F.text == "⌚История бронирования")
@form_router.message(F.text == "Смотреть далее")
async def book_place(message: types.Message, state: FSMContext):
    await state.set_state(HistoryForm.askForDate)

    builder = ReplyKeyboardBuilder()
    today = datetime.today()
    for i in range(5):
        date_option = today - timedelta(days=i)
        builder.add(types.KeyboardButton(text=date_option.strftime("%d.%m")))
    builder.adjust(1)

    bot_message = await message.answer(
        "Выберите дату для просмотра истории бронирования",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
    )
    await state.update_data(
        last_user_message=message.message_id, last_bot_message=bot_message.message_id
    )


@form_router.message(HistoryForm.askForDate)
async def ask_for_date(message: types.Message, state: FSMContext):
    selected_date = message.text

    try:
        date = datetime.strptime(selected_date, "%d.%m")
        day = date.strftime("%d.%m")
    except ValueError:
        await message.answer(
            "Неверный формат даты. Пожалуйста, выберите дату из предложенных."
        )
        return

    photo_path = await generate_schedule_image(date, state)

    await send_image(
        photo_path, selected_date, more_schedule_kb_for_user, day, message, state
    )
