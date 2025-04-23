import calendar
from datetime import timedelta

from pytz import timezone
from aiogram import F, Router
from aiogram.types import Message
from aiogram.enums import ChatType


from database.get_db_interface import db_interface
from database.models import Challenges
from load_services import logger, request_manager
from decorators.disscusion_group_access import disscusion_group_access
from utils.check_end_date import check_challenge_end_date
from utils.check_keywords_in_message import check_message
from utils.extract_video_link import extract_video_link
from utils.get_video_title import get_video_title


router = Router(name="check_new_comments")


@router.message(F.chat.type.in_([ChatType.SUPERGROUP, ChatType.GROUP]))
@disscusion_group_access
async def check_comments_posts_dis_group(message: Message) -> None:
    if message.message_thread_id:
        challenge = await db_interface.get_row(Challenges, challenge_id=message.message_thread_id)
        if not challenge:
            return
        status = await check_challenge_end_date([challenge])
        if not status:
            logger.debug(f"The challenge with ID {challenge.id} is expired.")
            return
        if challenge:            
            message_text = message.text or message.caption
            if message_text:
                video_link = await extract_video_link(message_text)
                if video_link:
                    video_title = await get_video_title(video_link) or "Нет названия видео"
                    logger.debug("Upload a message to assistant")
                    await request_manager.tasks_queue.put((video_title,
                                                           challenge.text_challenge,
                                                           message_text,
                                                           message.chat.shifted_id,
                                                           message.message_thread_id,
                                                           message.message_id))
            return
    else:
        message_text = message.text or message.caption
        if not message_text:
            return
        challenges = await db_interface.get_row(model=Challenges, to_many=True, is_ended=False)
        await check_challenge_end_date(challenges)

        if await check_message(message_text):
            if not await db_interface.get_row(model=Challenges, challenge_id=message.message_id):
                date_create = message.date.astimezone(tz=timezone("Europe/Moscow"))
                amount_days = calendar.monthrange(date_create.year, date_create.month)
                date_of_end = date_create + timedelta(days=amount_days[1])
                await db_interface.add_row(Challenges, 
                                        challenge_id=message.message_id,
                                        text_challenge=message_text,
                                        date_create=date_create,
                                        date_of_end=date_of_end
                                                        )
                logger.debug("The challenge post was received successfully")
