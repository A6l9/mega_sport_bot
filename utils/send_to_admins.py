import asyncio

from aiogram.exceptions import TelegramBadRequest

from loader import bot
from data_models import AdminMessage
from load_services import logger
from config import proj_settings
from challenges_config import CHALLENGES_CONFIG
from database import models
from database.get_db_interface import db_interface
from utils.forming_admin_message import forming_message
from keyboards.reply_comment_inline_kb import reply_comment_keyboard


async def determine_challenge_type(group_id: int) -> str:
    return "terfit" if int(f"100{group_id}") == proj_settings.terfit_discussion_group_id else "athletx"


async def send_to_admins(message: dict, challenge_id: int, group_id: int, 
                         comment_id: int, comment_text: str, admin_group_id: int) -> None:
    message_text, admin_message = await forming_message(message, group_id, challenge_id)

    challenge_type = await determine_challenge_type(group_id) 

    try:
        await bot.send_message(chat_id=-admin_group_id,
                               text=message_text, 
                               parse_mode="markdown", 
                               reply_markup=reply_comment_keyboard(comment_id, challenge_type))
        
        fields = {
            "comment_id": comment_id,
            "challenge_id": challenge_id, 
            "challenge_name": admin_message['challenge_name'],
            "full_name": admin_message['full_name'],
            "comment_text": comment_text,
            "result": str(admin_message['result']),
            "video_link": admin_message['video_link'],
        }
        model = CHALLENGES_CONFIG[challenge_type]["model_comments"]
        
        if challenge_type == "terfit":
            fields.update({
                "role": admin_message['role'],
                "club_name": admin_message['club_name'],
                "time_of_execution": admin_message['time_of_execution'],
            })

        else:
            fields.update({
                "phone_number": admin_message['phone_number']
            })

        await db_interface.add_row(model, **fields)

        await asyncio.sleep(2)
    except TelegramBadRequest as exc:
        logger.debug(exc)
