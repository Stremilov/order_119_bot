import os
from typing import Callable
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, ReplyKeyboardMarkup

from database import Session
from database.repositories.repo_booktime import BookTimeRepository
from utils.weekday_translation import get_weekday_ru


async def generate_schedule_image(date, state: FSMContext):
    text_color = (0, 0, 0)
    font_size = 32

    image = Image.open("handlers/images/бронь_120.jpeg", mode="r").convert("RGB")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(
        "handlers/fonts/DejaVuSans-Bold.ttf", font_size, encoding="unic"
    )

    day = date.strftime("%d.%m")
    await state.update_data(day=day)
    data = BookTimeRepository(Session()).get_bookings_by_date(day, fetch=True)
    day_of_week = get_weekday_ru(date.strftime("%A"))

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
        records = BookTimeRepository(Session()).get_bookings_by_date(day, fetch=True)

        formatted_date = selected_date.replace(".", "\\.")
        weekday_eng = datetime.strptime(selected_date, "%d.%m").strftime('%A')
        answers = [f'*{get_weekday_ru(weekday_eng)}, {formatted_date}*']
        for number, item in enumerate(records, 1):
            start_time, end_time, reason, renter = item
            answers.append('\n'.join([
                f"{start_time}\\-{end_time}",
                f"{number}\\. *{reason}*",
                f"{'@' + renter : >11}"
            ]))
        await message.answer('\n\n'.join(answers), parse_mode='MarkdownV2')
    else:
        await message.answer("Изображение с расписанием не найдено.")

    await state.clear()
