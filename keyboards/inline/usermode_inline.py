from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_approval_keyboard(ticket_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Одобрить", callback_data=f"approve_{ticket_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отклонить", callback_data=f"reject_{ticket_id}"
                )
            ],
        ]
    )
    return keyboard

def create_cancel_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Отклонить", callback_data="cancel_reject"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отменить бронь", callback_data="cancel_approve"
                )
            ],
        ]
    )
    return keyboard