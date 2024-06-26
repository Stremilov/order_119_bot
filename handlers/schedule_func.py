import os
from datetime import datetime, timedelta

from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from PIL import Image, ImageDraw, ImageFont

from database.create_tables import session, BookTime

from loader import dp, bot


class ScheduleForm(StatesGroup):
    askForDate = State()
    showSchedule = State()


def more_schedule_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Посмотреть еще"))
    builder.add(types.KeyboardButton(text="📌Забронировать"))
    builder.adjust(1)
    return builder.as_markup(one_time_kyeboard=True, resize_keyboard=True)


def fetch_event_for_date(date: str):
    records = session.query(BookTime).filter_by(date=date).all()
    if records:
        data = []
        for record in records:
            data.append((record.startTime, record.endTime, record.renter))
        return data
    else:
        return ""


def generate_schedule_image(date: datetime):
    width, height = 600, 400
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    font_size = 32
    days_translation = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье"
    }
    image = Image.open("handlers/images/бронь_120.jpeg", mode="r").convert("RGB")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(
        "handlers/fonts/DejaVuSans-Bold.ttf", font_size, encoding="unic"
    )

    day = date.strftime("%d.%m")
    data = fetch_event_for_date(day)
    day_of_week = days_translation[date.strftime("%A")]

    draw.text((50, 50), f"{day_of_week} {day}", fill=text_color, font=font)
    y_offset = 110
    font_size = 25
    font = ImageFont.truetype(
        "handlers/fonts/DejaVuSans.ttf", font_size, encoding="unic"
    )

    if isinstance(data, list):
        for startTime, endTime, renter in data:
            draw.text(
                (50, y_offset),
                f"{startTime} - {endTime}\n@{renter}",
                fill=text_color,
                font=font,
            )
            y_offset += 77
    else:
        draw.text((10, y_offset), data, fill=text_color, font=font)

    image_path = "handlers/images/schedule.jpg"
    image.save(image_path)
    return image_path


@dp.message(Command("schedule"))
@dp.message(F.text == "📆Расписание")
@dp.message(F.text == "Посмотреть еще")
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


@dp.message(ScheduleForm.askForDate)
async def process_date_selection(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    last_user_message_id = user_data.get("last_user_message")
    last_bot_message_id = user_data.get("last_bot_message")

    selected_date = message.text

    try:
        date = datetime.strptime(selected_date, "%d.%m")
    except ValueError:
        await message.answer(
            "Неверный формат даты. Пожалуйста, выберите дату из предложенных."
        )
        return

    await bot.delete_message(chat_id=message.chat.id, message_id=last_user_message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
    photo_path = generate_schedule_image(date)

    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo, caption=f"Расписание на {selected_date}", reply_markup=more_schedule_kb())
    else:
        await message.answer("Изображение с расписанием не найдено.")

    await state.clear()
