from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply.admin import main_kb_for_admin, main_kb_for_user
from loader import dp, get_user


@dp.message(F.text == 'Главное меню')
async def menu(message: Message, state: FSMContext):
    await state.clear()
    user = await get_user(message)

    if user.status == "left":
        await message.answer('Главное меню', reply_markup=main_kb_for_user())
        return
    await message.answer('Главное меню', reply_markup=main_kb_for_admin())
