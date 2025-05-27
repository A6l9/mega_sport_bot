from uuid import uuid4
from datetime import datetime, timedelta

from aiogram.types import Message
from apscheduler.triggers.date import DateTrigger

from utils.get_video_title import get_video_title
from load_services import request_manager, logger
from database.models import Challenges
from database.get_db_interface import db_interface


async def pending_comment_processing(video_link: str, 
                                     challenge_text: str, 
                                     message_text: str,
                                     message_thread_id: int,
                                     message_shifted_id: int,
                                     message_id: int,
                                     task_id: str,
                                     amount_retries: int) -> None:
    from load_services import async_scheduler

    logger.debug("Starting to process the pending task")

    video_title = await get_video_title(video_link)
    if not video_title:
        if amount_retries == 15:
            return
        
        logger.debug(f"Couldn't to get video title, getting the video title will be delayed. Try no. {amount_retries + 1}")

        run_date = datetime.now() + timedelta(minutes=10)
        async_scheduler.add_job(pending_comment_processing, 
                                                      trigger="date", 
                                                      run_date=run_date, 
                                                      kwargs={
                                                          "video_link": video_link,
                                                          "challenge_text": challenge_text,
                                                          "message_text": message_text,
                                                          "message_thread_id": message_thread_id,
                                                          "message_shifted_id": message_shifted_id,
                                                          "message_id": message_id,
                                                          "task_id": task_id,
                                                          "amount_retries": amount_retries + 1
                                                              },
                                                      id=task_id,
                                                      replace_existing=True,
                                                      misfire_grace_time=3600*48)

        async_scheduler.print_jobs()

        return None

    logger.debug("Upload a message to assistant")
    await request_manager.tasks_queue.put((video_title,
                                            challenge_text,
                                            message_text,
                                            message_shifted_id,
                                            message_thread_id,
                                            message_id))

    async_scheduler.print_jobs() 

    return None
