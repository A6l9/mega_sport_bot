from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from state_storage.reply_comment_states import States
from keyboards.cancel_inline_kb import cancel_keyboard
from loader import bot, logger, proj_settings
from decorators.check_comment_answer import check_comment_answer
from database.get_db_interface import db_interface


router = Router(name="reply_to_comment")


@router.callback_query(F.data.startswith("reply-comment:"))
@check_comment_answer
async def reply_to_comment(call: CallbackQuery, state: FSMContext) -> None:
    comment_id = call.data.split(":")[1]
    await call.message.answer("Введите ответ на комментарий 📝", reply_markup=cancel_keyboard())
    await state.set_state(States.write_comment_answer)
    await state.set_data(data={"message_id": call.message.message_id, "comment_id": comment_id})


@router.message(States.write_comment_answer)
async def take_comment_answer(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        await bot.send_message(text=message.text, chat_id=-proj_settings.discussion_group_id,
                            reply_to_message_id=data["comment_id"])
        await message.answer("Ответ на комментарий был успешно опубликован.")
        try:
            await bot.edit_message_reply_markup(message_id=data["message_id"], chat_id=-proj_settings.admins_group_id)
        except TelegramBadRequest as exc:
            logger.debug(exc)
        finally:
            await db_interface.change_comments_status(comment_id=int(data["comment_id"]), status=True)
            await state.clear()
    except TelegramBadRequest as exc:
        logger.debug(exc)
        await message.answer("Произошла ошибка, повторите попытку позже.")
        await state.clear()
