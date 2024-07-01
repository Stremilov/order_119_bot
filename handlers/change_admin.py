from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.book import form_router
from handlers.start import main_kb
from loader import dp

import json

CONFIG_FILE = "config_data/admin_username.json"

def load_config():
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

config = load_config()
ADMIN_USERNAME = config["ADMIN_USERNAME"]

class ChangeForm(StatesGroup):
    askForConfirm = State()


def create_change_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить", callback_data=f"Change"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отклонить", callback_data=f"DontChange"
                )
            ],
        ]
    )
    return keyboard


@dp.message(Command('change'))
async def change_admin(message: types.Message, state: FSMContext):
    await state.set_state(ChangeForm.askForConfirm)
    if ADMIN_USERNAME == message.from_user.username:
        await message.answer(text="Напишите username человека в telegram, которому хотите передать руководство\nК примеру: example")
    else:
        await message.answer(text="Доступно только главному руководителю")


@form_router.message(ChangeForm.askForConfirm)
async def ask_for_confirm(message: types.Message, state: FSMContext):
    await state.update_data(new_admin_username=message.text)
    await message.answer(text=f"Передать руководство {message.text}?", reply_markup=create_change_keyboard())


@dp.callback_query(lambda call: call.data == "Change")
async def approve_booking(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_admin_username = data.get("new_admin_username")
    global ADMIN_USERNAME
    ADMIN_USERNAME = new_admin_username

    config["ADMIN_USERNAME"] = new_admin_username
    save_config(config)

    await call.message.answer(text=f"Руководство успешно передано {ADMIN_USERNAME}")

@dp.callback_query(lambda call: call.data == "DontChange")
async def dont_change_booking(call: types.CallbackQuery):
    await call.message.answer(text="Руководство не изменено", reply_markup=main_kb())
