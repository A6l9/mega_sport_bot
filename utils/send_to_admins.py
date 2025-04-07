import asyncio

from aiogram.exceptions import TelegramBadRequest

from loader import bot
from load_services import logger
from config import proj_settings
from database.models import Comments
from database.get_db_interface import db_interface
from keyboards.reply_comment_inline_kb import reply_comment_keyboard


async def send_to_admins(message: str, challenge_id: int, group_id: int, comment_id: int, comment_text: str) -> None:
    challenge_link = f"https://t.me/c/{group_id}/{challenge_id}"
    
    message = message.get("data")

    challenge_name = message.get("challenge_name") or "Не указано"
    full_name = message.get("full_name") or "Не указано"
    role = message.get("role") or "Не указано"
    club_name = message.get("club") or "Не указано"
    result = message.get("result") or "Не указано"
    video_link = message.get("link")
    time_of_execution = message.get("time_of_execution") or "Не указано"

    text = f"Новый комментарий к [челленджу]({challenge_link})\n\n" \
           f"**Название челенджа:** {challenge_name}\n" \
           f"**ФИО:** {full_name}\n" \
           f"**Член клуба\Тренер:** {role}\n" \
           f"**Название клуба:** {club_name}\n" \
           f"**Результат:** {result}\n" \
           f"**Время выполнения:** {time_of_execution}\n\n" \
           f"[Ссылка на видео]({video_link})"
    try:
        await bot.send_message(chat_id=-proj_settings.admins_group_id,
                               text=text, 
                               parse_mode="markdown", 
                               reply_markup=reply_comment_keyboard(comment_id))
        await db_interface.add_row(Comments, 
                                   comment_id=comment_id,
                                   challenge_id=challenge_id, 
                                   challenge_name=challenge_name,
                                   full_name=full_name,
                                   role=role,
                                   club_name=club_name,
                                   comment_text=comment_text,
                                   result=str(result),
                                   time_of_execution=time_of_execution,
                                   video_link=video_link,
                                   )
        await asyncio.sleep(2)
    except TelegramBadRequest as exc:
        logger.debug(exc)
