from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import Any, ReplyKeyboardBuilder, ReplyKeyboardMarkup


class StartReplyBuilder(ReplyKeyboardBuilder):
    """
    Форк от ReplyKeyboardBuilder.\n
    При вызове as_markup(**kwargs) возвращает ReplyKeyboardMarkup, при этом добавляя
    кнопку "Главное Меню" в качестве последней строки клавиатуры
    """

    def __init__(self):
        super().__init__()

    def as_markup(self, **kwargs: Any) -> ReplyKeyboardMarkup:
        copied = self.copy()
        copied.row(KeyboardButton(text='Главное меню'))
        return copied.as_markup(**kwargs)
