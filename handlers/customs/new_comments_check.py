from aiogram import F, Router
from aiogram.types import Message
from aiogram.enums import ChatType

from database.get_db_interface import db_interface
from database.models import Challenges


router = Router(name="check_new_comments")


@router.message(F.chat.type.in_([ChatType.SUPERGROUP, ChatType.GROUP]))
async def check_new_comments(message: Message) -> None:
    challenge = await db_interface.get_row(Challenges, challenge_id=message.message_thread_id)
    if challenge:
        #TODO assistant interactions
        ...