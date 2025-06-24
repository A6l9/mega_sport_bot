import calendar
from uuid import uuid4
from datetime import datetime, timedelta

from pytz import timezone
from aiogram import F, Router
from aiogram.types import Message
from aiogram.enums import ChatType


from database.get_db_interface import db_interface
from database.db_initial import Base
from database import models
from config import proj_settings
from challenges_config import CHALLENGES_CONFIG
from load_services import logger, request_manager, async_scheduler
from decorators.disscusion_group_access import disscusion_group_access
from utils.check_end_date import check_challenge_end_date
from utils.check_keywords_in_message import check_message
from utils.extract_video_link import extract_video_link
from utils.get_video_title import get_video_title
from utils.pending_comments_processing import pending_comment_processing


router = Router(name="check_new_comments")


async def determine_model(chat_id: int) -> Base:
    return models.AthletxChallenges if abs(chat_id) == proj_settings.athletx_discussion_group_id else models.TerfitChallenges


async def receive_challenges(message: Message) -> None:
    message_text = message.text or message.caption

    model = await determine_model(message.chat.id)
    hashtag = "#athletxchallenge" if abs(message.chat.id) == proj_settings.athletx_discussion_group_id else "#terfitchallenge"

    if not message_text:
        return
    challenges = await db_interface.get_row(model=model, to_many=True, is_ended=False)
    await check_challenge_end_date(challenges, model=model)

    if await check_message(message_text) == hashtag:
        if not await db_interface.get_row(model=model, challenge_id=message.message_id):
            date_create = message.date.astimezone(tz=timezone("Europe/Moscow"))
            amount_days = calendar.monthrange(date_create.year, date_create.month)
            date_of_end = date_create + timedelta(days=amount_days[1])
            await db_interface.add_row(model, 
                                    challenge_id=message.message_id,
                                    text_challenge=message_text,
                                    date_create=date_create,
                                    date_of_end=date_of_end
                                                    )
            logger.debug("The challenge post was received successfully")


async def comments_processing(message: Message) -> None:
    model = await determine_model(chat_id=message.chat.id)

    challenge = await db_interface.get_row(model, challenge_id=message.message_thread_id)
    if not challenge:
        return
    status = await check_challenge_end_date([challenge], model=model)
    if not status:
        logger.debug(f"The challenge with ID {challenge.id} is expired.")
        return
    if challenge:            
        message_text = message.text or message.caption
        if message_text:
            video_link = await extract_video_link(message_text)
            if video_link:
                video_title = await get_video_title(video_link)

                challenge_type = "athletx" if abs(message.chat.id) == proj_settings.athletx_discussion_group_id else "terfit"
                assistant_id = CHALLENGES_CONFIG[challenge_type]["assistant_id"]
                admin_group_id = CHALLENGES_CONFIG[challenge_type]["admin_group"]
                if not video_title:
                    logger.debug("Couldn't to get video title, getting the video title will be delayed")
                    run_date = datetime.now() + timedelta(minutes=1)
                    task_id = str(uuid4())
                    async_scheduler.add_job(pending_comment_processing, 
                                                    trigger="date", 
                                                    run_date=run_date, 
                                                    kwargs={
                                                        "video_link": video_link,
                                                        "challenge_text": challenge.text_challenge,
                                                        "message_text": message_text,
                                                        "message_thread_id": message.message_thread_id,
                                                        "message_shifted_id": message.chat.shifted_id,
                                                        "message_id": message.message_id,
                                                        "assistant_id": assistant_id,
                                                        "admin_group_id": admin_group_id,
                                                        "task_id": task_id,
                                                        "amount_retries": 0
                                                            },
                                                    id=task_id,
                                                    misfire_grace_time=3600*48)
                    
                    async_scheduler.print_jobs()

                    return None

                logger.debug("Upload a message to assistant")
                await request_manager.tasks_queue.put((video_title,
                                                        challenge.text_challenge,
                                                        message_text,
                                                        message.chat.shifted_id,
                                                        message.message_thread_id,
                                                        message.message_id,
                                                        assistant_id,
                                                        admin_group_id
                                                        ))
        return


@router.message(F.chat.type.in_([ChatType.SUPERGROUP, ChatType.GROUP]))
@disscusion_group_access
async def disscusion_groups_router(message: Message) -> None:
    if message.message_thread_id:
        await comments_processing(message)
    else:
        await receive_challenges(message)
