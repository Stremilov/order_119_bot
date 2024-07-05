import os
from typing import Callable
from aiogram.fsm.context import FSMContext
from PIL import Image, ImageDraw, ImageFont

from database.func import fetch_event_for_date

from aiogram.types import FSInputFile, Message, ReplyKeyboardMarkup


async def generate_schedule_image(date, state: FSMContext):
    text_color = (0, 0, 0)
    font_size = 32
    days_translation = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье",
    }
    image = Image.open("handlers/images/бронь_120.jpeg", mode="r").convert("RGB")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(
        "handlers/fonts/DejaVuSans-Bold.ttf", font_size, encoding="unic"
    )

    day = date.strftime("%d.%m")
    await state.update_data(day=day)
    data = fetch_event_for_date(day)
    day_of_week = days_translation[date.strftime("%A")]

    draw.text((50, 50), f"{day_of_week} {day}", fill=text_color, font=font)
    y_offset = 110
    font_size = 25
    font = ImageFont.truetype(
        "handlers/fonts/DejaVuSans.ttf", font_size, encoding="unic"
    )

    if isinstance(data, list):
        for startTime, endTime, reason, renter in data:
            draw.text(
                (50, y_offset),
                f"{startTime} - {endTime}\nТема: {reason}",
                fill=text_color,
                font=font,
            )
            y_offset += 77
    else:
        draw.text((10, y_offset), data, fill=text_color, font=font)
    image_path = "handlers/images/schedule.jpg"
    image.save(image_path)
    return image_path


async def send_image(
    photo_path,
    selected_date,
    keyboard_func: Callable[[], ReplyKeyboardMarkup],
    day,
    message: Message,
    state: FSMContext,
):
    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo,
            caption=f"Расписание на {selected_date}",
            reply_markup=keyboard_func(),
        )
        records = fetch_event_for_date(day)
        for startTime, endTime, reason, renter in records:
            await message.answer(
                f"Время: {startTime}-{endTime}\nТема: {reason}\nАрендатор: @{renter}"
            )
    else:
        await message.answer("Изображение с расписанием не найдено.")

    await state.clear()
