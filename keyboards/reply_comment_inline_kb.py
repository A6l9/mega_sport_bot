from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def reply_comment_keyboard(message_id: int):
    keyboard = [[InlineKeyboardButton(text="Ответить на комментарий ✉️", callback_data=f"reply-comment:{message_id}")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
