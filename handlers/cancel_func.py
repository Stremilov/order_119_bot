from loader import dp
from handlers.start import msg_start
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


@dp.message(F.text == 'Главное меню')
async def menu(message: Message, state: FSMContext):
    await state.clear()
    await msg_start(message)
