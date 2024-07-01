import asyncio

import schedule
from aiogram.types import BotCommand

from handlers.book_checker import delete_past_bookings
from loader import dp, bot
from database.create_tables import engine, Base
import handlers


async def main() -> None:
    schedule.every().day.at("10:00:00").do(delete_past_bookings)
    await bot.set_my_commands([
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/book", description="Забронировать аудиторию"),
        BotCommand(command="/unbook", description="Отменить бронь"),
        BotCommand(command="/schedule", description="Расписание бронирования"),
        BotCommand(command="/change", description="Передать руководство (для главного руководителя)"),
    ])
    await dp.start_polling(bot)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    asyncio.run(main())
