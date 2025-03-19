import calendar
from datetime import datetime, timedelta

from pytz import timezone
from aiogram import Router
from aiogram.types import Message

from database.get_db_interface import db_interface
from database.models import Challenges
from decorators import channel_access
from utils.check_end_date import check_challenge_end_date
from utils.check_keywords_in_message import check_message


router = Router(name="new_posts_check")


@router.message()
@channel_access
async def new_post_check(message: Message) -> None:
    challenges = await db_interface.get_row(model=Challenges, to_many=True, is_ended=False)
    await check_challenge_end_date(challenges)
    
    if await check_message(message.text):
        if not await db_interface.get_row(model=Challenges, challenge_id=message.message_id):
            date_create = datetime.fromtimestamp(message.forward_date, tz=timezone("Moscow/Europe"))
            amount_days = calendar.monthrange(date_create.year, date_create.month)
            date_of_end = date_create + timedelta(days=amount_days)
            await db_interface.add_row(Challenges, 
                                       challenge_id=message.message_id,
                                       text_challenge=message.text,
                                       date_create=date_create,
                                       date_of_end=date_of_end
                                                    )
         
