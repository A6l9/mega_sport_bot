from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from state_storage.reply_comment_states import States
from keyboards.cancel_inline_kb import cancel_keyboard
from keyboards.change_delete_comment_inline_kb import change_delete_comment_kb
from loader import bot
from config import proj_settings
from challenges_config import CHALLENGES_CONFIG
from load_services import logger
from decorators.check_comment_answer import check_comment_answer
from database.get_db_interface import db_interface


router = Router(name="reply_to_comment")


@router.callback_query(F.data.startswith("reply-comment"))
@check_comment_answer
async def reply_to_comment_terfit(call: CallbackQuery, state: FSMContext) -> None:
    comment_id = call.data.split(":")[1]
    challenge_type, _ = call.data.split("-")[2].split(":")
    message_with_cancel_kb = await call.message.answer("Введите ответ на комментарий 📝", reply_markup=cancel_keyboard())
    await state.set_state(States.write_comment_answer)
    await state.set_data(data={"message_id": call.message.message_id, 
                               "comment_id": comment_id,
                               "admins_group_id": CHALLENGES_CONFIG[challenge_type]["admin_group"],
                               "discussion_group_id": CHALLENGES_CONFIG[challenge_type]["discussion_group"],
                               "challenge_type": challenge_type,
                               "message_with_cancel_kb_id": message_with_cancel_kb.message_id})


@router.message(States.write_comment_answer)
async def take_comment_answer(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        comment_answer = await bot.send_message(text=message.text, chat_id=-data.get("discussion_group_id", 0),
                            reply_to_message_id=data["comment_id"])
        await message.answer("Ответ на комментарий был успешно опубликован.")
        try:
            await bot.edit_message_reply_markup(message_id=data["message_id"], 
                                                chat_id=-data.get("admins_group_id", 0),
                                                reply_markup=change_delete_comment_kb(comment_id=data["comment_id"],
                                                                                      reply_id=comment_answer.message_id,
                                                                                      challenge_type=data["challenge_type"]))
            await bot.edit_message_reply_markup(chat_id=-data.get("admins_group_id", 0),
                                                message_id=data["message_with_cancel_kb_id"],
                                                reply_markup=None)
        except TelegramBadRequest as exc:
            logger.debug(exc)
        finally:
            await db_interface.change_comments_status_text_answer(comment_id=int(data["comment_id"]), 
                                                      comment_answer=message.text,
                                                      model=CHALLENGES_CONFIG[data["challenge_type"]]["model_comments"],
                                                      status=True)
            await state.clear()
    except TelegramBadRequest as exc:
        logger.debug(exc)
        await message.answer("Произошла ошибка. Повторите попытку позже.\n"
                             "Возможно, комментарий был удален или ответ на него недоступен по другой причине.")
        await state.clear()
