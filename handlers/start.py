from aiogram import types
from aiogram.filters import CommandStart

from database import Session
from database.repo_user import UserRepository
from keyboards.reply.admin import main_kb_for_admin, main_kb_for_user
from loader import dp, get_user
import yaml


with open("texts.yml", "r", encoding="utf-8") as file:
    txt_messages = yaml.safe_load(file)


@dp.message(CommandStart())
async def msg_start(message: types.Message):
    user_repo = UserRepository(Session())
    user = await get_user(message)

    if user.status == "left":
        await message.answer(txt_messages["greeting"], reply_markup=main_kb_for_user())
        await message.answer(txt_messages["howToUse"])
        return
    await message.answer(txt_messages["greeting"], reply_markup=main_kb_for_admin())
    await message.answer(txt_messages["howToUse"])

    if not user_repo.get_user_by_username(message.from_user.username):
        user_repo.create_user(username=message.from_user.username, role="user", telegram_id=message.from_user.id)
