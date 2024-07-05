import asyncio

from aiogram.types import BotCommand

from loader import dp, bot
from database.create_tables import engine, Base
import handlers


async def main() -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Начать"),
            BotCommand(command="/help", description="Помощь"),
            BotCommand(command="/book", description="Забронировать аудиторию"),
            BotCommand(command="/unbook", description="Отменить бронь"),
            BotCommand(command="/schedule", description="Расписание бронирования"),
        ]
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    asyncio.run(main())
