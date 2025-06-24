from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from database.get_db_interface import db_interface
from database.models import TerfitComments
from utils.upload_to_excel import upload_comments_to_excel
from utils.prepare_comments import prepare_comments
from decorators.admins_group_access import admins_group_access
from loader import bot
from challenges_config import CHALLENGES_CONFIG
from config import proj_settings


router = Router(name="upload_comments")


async def determine_challenge_type(group_id: int) -> str:
    return "terfit" if abs(group_id) == proj_settings.terfit_admins_group_id else "athletx"


@router.message(F.text.startswith("/upload_comments"))
@admins_group_access
async def upload_comments(message: Message, state: FSMContext) -> None:
    await state.clear()

    challenge_type = await determine_challenge_type(group_id=message.chat.id)

    comments = await db_interface.get_row(model=CHALLENGES_CONFIG[challenge_type]["model_comments"], to_many=True)
    if comments:
        prepared_comments = await prepare_comments(comments=comments)
        await upload_comments_to_excel(prepared_comments, challenge_type)
        await bot.send_document(document=FSInputFile(f"comments-{challenge_type}.xlsx", filename=f"comments-{challenge_type}.xlsx"),
                                chat_id=message.chat.id)
    else:
        await message.answer("Комментарии пока не были написаны.")
