import asyncio

from aiogram.types import BotCommand

from loader import dp, bot
from database.create_tables import engine, Base
from utils.book_checker import delete_past_bookings
import handlers


async def main() -> None:
    delete_past_bookings()
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Начать"),
            BotCommand(command="/help", description="Помощь"),
            BotCommand(command="/book", description="Забронировать аудиторию"),
            BotCommand(command="/unbook", description="Отменить бронь"),
            BotCommand(command="/schedule", description="Расписание бронирования"),
            BotCommand(command="/history", description="История бронирования"),
            BotCommand(command="/faq", description="Часто задаваемые вопросы"),
        ]
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
