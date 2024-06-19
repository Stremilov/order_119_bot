import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from PIL import Image, ImageDraw, ImageFont
import io

from aiogram.filters import Command
from aiogram.types import FSInputFile

from loader import dp


def generate_schedule_image():
    width, height = 600, 1000
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    font_size = 20

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("/Users/levstremilov/Downloads/bot_rent_119/handlers/DejaVuSans.ttf", font_size)

    now = datetime.now()
    month = now.strftime("%B")
    year = now.year

    schedule_data = [
        "01 - Встреча с клиентом",
        "02 - Отчеты",
        "03 - Проектная работа",
        "04 - Обучение",
        "05 - Отпуск",
        "06 - Совещание",
        "07 - Встреча с командой",
        "08 - Анализ данных",
        "09 - Разработка",
        "10 - Тестирование",
        "11 - Презентация",
        "12 - Рабочий день",
        "13 - Планирование",
        "14 - Встреча с партнерами",
        "15 - Доклад",
        "16 - Анализ",
        "17 - Конференция",
        "18 - Вебинар",
        "19 - Семинар",
        "20 - Рабочий день",
        "21 - Совещание",
        "22 - Обучение",
        "23 - Анализ данных",
        "24 - Встреча с клиентом",
        "25 - Проектная работа",
        "26 - Отчеты",
        "27 - Планирование",
        "28 - Встреча с командой",
        "29 - Тестирование",
        "30 - Презентация",
        "31 - Заключение месяца"
    ]

    draw.text((10, 10), f"Расписание на {month} {year}", fill=text_color, font=font)

    y_offset = 40
    for item in schedule_data:
        draw.text((10, y_offset), item, fill=text_color, font=font)
        y_offset += 30

    image_path = "/Users/levstremilov/Downloads/bot_rent_119/images/schedule.jpg"
    image.save(image_path)
    return image_path

@dp.message(Command("schedule"))
async def send_schedule(message: types.Message):
    photo_path = generate_schedule_image()
    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo, caption="Вот расписание на месяц")
    else:
        await message.answer("Изображение с расписанием не найдено.")
