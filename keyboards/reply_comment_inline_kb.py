from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def reply_comment_keyboard(message_id: int, challenge_type: str):
    keyboard = [[InlineKeyboardButton(text="Ответить на комментарий ✉️", 
                                      callback_data=f"reply-comment-{challenge_type}:{message_id}")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
