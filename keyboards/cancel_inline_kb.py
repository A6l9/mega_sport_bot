from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def cancel_keyboard():
    keyboard = [[InlineKeyboardButton(text="Отменить 🙅‍♂️", callback_data="cancel")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
