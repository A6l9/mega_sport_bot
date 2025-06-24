from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def change_delete_comment_kb(comment_id: int, reply_id: int, challenge_type: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Редактировать ответ ✏️", callback_data=f"edit-comm-answ-{challenge_type}:{comment_id}:{reply_id}")],
        [InlineKeyboardButton(text="Удалить ответ 🗑", callback_data=f"del-comm-answ-{challenge_type}:{comment_id}:{reply_id}")]
                ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
