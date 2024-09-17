from datetime import datetime, timedelta

from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from loader import bot, get_user
from loader import form_router

from states.states import ScheduleForm

from utils.image import generate_schedule_image, send_image

from keyboards.reply.usermodes import (
    more_schedule_kb_for_user,
    more_schedule_kb_for_admin,
)


@form_router.message(Command("schedule"))
@form_router.message(F.text == "📆Расписание")
@form_router.message(F.text == "Посмотреть еще")
async def schedule_command(message: types.Message, state: FSMContext):
    await state.set_state(ScheduleForm.askForDate)

    builder = ReplyKeyboardBuilder()
    today = datetime.now()
    for i in range(20):
        date = today + timedelta(days=i)
        builder.add(types.KeyboardButton(text=date.strftime("%d.%m")))
    builder.adjust(4)

    bot_message = await message.answer(
        "Выберите дату для просмотра расписания",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
    )
    await state.update_data(
        last_user_message=message.message_id, last_bot_message=bot_message.message_id
    )


@form_router.message(ScheduleForm.askForDate)
async def process_date_selection(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    last_user_message_id = user_data.get("last_user_message")
    last_bot_message_id = user_data.get("last_bot_message")

    selected_date = message.text

    try:
        date = datetime.strptime(selected_date, "%d.%m")
        day = date.strftime("%d.%m")
    except ValueError:
        await message.answer(
            "Неверный формат даты. Пожалуйста, выберите дату из предложенных."
        )
        return

    await bot.delete_message(chat_id=message.chat.id, message_id=last_user_message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
    photo_path = await generate_schedule_image(date, state)

    user = await get_user(message)

    if user.status == "left":
        await send_image(
            photo_path, selected_date, more_schedule_kb_for_user, day, message, state
        )
    else:
        await send_image(
            photo_path, selected_date, more_schedule_kb_for_admin, day, message, state
        )
