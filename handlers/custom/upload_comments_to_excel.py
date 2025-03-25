from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from database.get_db_interface import db_interface
from database.models import Comments
from utils.upload_to_excel import upload_comments_to_excel
from decorators.admins_group_access import admins_group_access
from loader import bot


router = Router(name="upload_comments")


@router.message(F.text.startswith("/upload_comments"))
@admins_group_access
async def upload_comments(message: Message, state: FSMContext) -> None:
    await state.clear()
    comments = await db_interface.get_row(Comments, to_many=True)
    if comments:
        await upload_comments_to_excel(comments)
        await bot.send_document(document=FSInputFile("comments.xlsx", filename="comments.xlsx"),
                                chat_id=message.chat.id)
    else:
        await message.answer("Комментарии пока не были написаны.")
