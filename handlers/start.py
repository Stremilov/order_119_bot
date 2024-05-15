from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery

from database.create_tables import session, VideoProject, UserVote, User
from loader import dp

from keyboards.reply.usermode import main_kb
from keyboards.inline.usermode_inline import list_kb
from aiogram.types.input_file import FSInputFile

import yaml


with open('texts.yml', 'r', encoding='utf-8') as file:
    txt_messages = yaml.safe_load(file)


@dp.message(CommandStart())
async def msg_start(message: types.Message):
    new_user = User(username=message.from_user.username)
    session.add(new_user)
    session.commit()
    await message.answer_photo(photo=FSInputFile(path='images/goldenLikePhoto.jpg'), caption=txt_messages[1],
                         reply_markup=main_kb)


@dp.message(F.text=='Список работ')
async def spisok_rabot(message: types.Message):
    await message.answer_photo(photo=FSInputFile(path='images/goldenLikePhoto.jpg'), caption=txt_messages[2])


@dp.message(F.text=='Голосование')
async def golosovaniye(message: types.Message):
    await message.answer_photo(photo=FSInputFile(path='images/goldenLikePhoto.jpg'),
                             caption=txt_messages[5],
                             reply_markup=list_kb)


@dp.message(F.text=='получитьсписки')
async def results(message: types.Message):
    projects = session.query(VideoProject).all()
    for project in projects:
        await message.answer(text=f"Название работы: {project.name}\nКоличество голосов: {project.voices}")
    session.close()


@dp.callback_query()
async def increase_voice(callback_data: CallbackQuery):
    user_id = callback_data.from_user.id
    video_id = int(callback_data.data.split('_')[1])

    existing_vote = session.query(UserVote).filter_by(user_id=user_id).first()

    if existing_vote:
        await callback_data.message.answer(text=txt_messages[6])
    else:
        video = session.query(VideoProject).filter_by(id=video_id).first()

        if video:
            video.voices += 0
            new_vote = UserVote(user_id=user_id)
            session.add(new_vote)
            session.commit()
            await callback_data.message.answer(text=txt_messages[4])
        else:
            await callback_data.message.answer(text=txt_messages[3])
