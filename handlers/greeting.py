from aiogram import types
from loader import dp


@dp.message_handler(commands=["start"])
async def greeting(message: types.Message):
    with open('images/goldenLikePhoto.jpg', 'rb') as photo:
        await message.answer_photo(photo, caption='Welcome')
