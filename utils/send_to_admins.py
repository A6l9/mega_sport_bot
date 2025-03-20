from aiogram.exceptions import TelegramBadRequest

from loader import bot, proj_settings, logger
from keyboards.reply_comment_inline_kb import reply_comment_keyboard


async def send_to_admins(message: str, challenge_id: int, group_id: int, comment_id: int) -> None:
    challenge_link = f"https://t.me/c/{group_id}/{challenge_id}"
    text = f"Новый комментарий к [челленджу]({challenge_link})\n\n[Ссылка на видео]({message})"
    try:
        await bot.send_message(chat_id=-proj_settings.admins_group_id,
                               text=text, 
                               parse_mode="markdown", 
                               reply_markup=reply_comment_keyboard(comment_id))
    except TelegramBadRequest as exc:
        logger.debug(exc)
