from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from datetime import datetime, timedelta

from database import session
from database.models import BookTime

from handlers.start import main_kb_for_user
from loader import bot, form_router
import yaml

from states.states import BookForm


@form_router.message(Command("faq"))
async def book_place(message: types.Message):
    await message.answer("<b>Версия бота</b>: 1.0.0\n"
                         "Для поддержки бота и идей для улучшения писать @stremilovv", parse_mode="html")