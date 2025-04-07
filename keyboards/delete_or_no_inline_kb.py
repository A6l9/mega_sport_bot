from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def delete_or_no_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Да", callback_data="yes-delete")],
        [InlineKeyboardButton(text="Отменить 🙅‍♂️", callback_data="cancel")]
        ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
