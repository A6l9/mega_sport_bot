from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from state_storage.change_delete_comments_states import States
from keyboards.cancel_inline_kb import cancel_keyboard
from keyboards.delete_or_no_inline_kb import delete_or_no_keyboard
from keyboards.change_delete_comment_inline_kb import change_delete_comment_kb
from keyboards.reply_comment_inline_kb import reply_comment_keyboard
from loader import bot
from config import proj_settings
from load_services import logger
from database.get_db_interface import db_interface


router = Router(name="change_delete_comment_answer")


@router.callback_query(F.data.startswith("edit-comm-answ:"))
async def edit_comment_answer_handler(call: CallbackQuery, state: FSMContext) -> None:
    _, comment_id, reply_id = call.data.split(":")
    message_with_cancel_kb = await call.message.answer("Введите измененный ответ на комментарий 📝", 
                                                       reply_markup=cancel_keyboard())
    await state.set_state(States.edit_comment_answer)
    await state.set_data(data={"message_id": call.message.message_id, 
                               "comment_id": comment_id, 
                               "reply_id": reply_id,
                               "message_with_cancel_kb_id": message_with_cancel_kb.message_id
                               })


@router.message(States.edit_comment_answer)
async def edit_comment_answer_take_answer(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        await bot.edit_message_text(text=message.text, 
                                    chat_id=-proj_settings.discussion_group_id,
                                    message_id=data["reply_id"])
        await message.answer("Ответ на комментарий был успешно изменен.")
        await state.clear()
        await db_interface.change_comments_status_text_answer(comment_id=int(data["comment_id"]), 
                                                    comment_answer=message.text,
                                                    status=True)
        try:
            await bot.edit_message_reply_markup(chat_id=-proj_settings.admins_group_id,
                                                message_id=data.get("message_with_cancel_kb_id"))
        except TelegramBadRequest as exc:
            logger.debug(exc)
    except TelegramBadRequest as exc:
        logger.debug(exc)
        await message.answer("Произошла ошибка. Повторите попытку позже.\n"
                             "Возможно, ответ на комментарий был удален или его изменение недоступно по другой причине.")
        await state.clear()

    
@router.callback_query(F.data.startswith("del-comm-answ:"))
async def delete_comment_answer_hanlder(call: CallbackQuery, state: FSMContext) -> None:
    _, comment_id, reply_id = call.data.split(":")
    await call.message.answer("Вы точно хотите удалить ответ на комментарий?", reply_markup=delete_or_no_keyboard())
    await state.set_state(States.delete_comment_answer)
    await state.set_data(data={"message_id": call.message.message_id, "comment_id": comment_id, "reply_id": reply_id})


@router.callback_query(F.data == "yes-delete", StateFilter(States.delete_comment_answer))
async def yes_delete_comment_answer(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        await bot.delete_message(chat_id=-proj_settings.discussion_group_id,
                                message_id=data["reply_id"])
        await call.message.answer("Ответ на комментарий был успешно удален.")
        try:
            await bot.edit_message_reply_markup(message_id=data["message_id"], 
                                                chat_id=-proj_settings.admins_group_id,
                                                reply_markup=reply_comment_keyboard(message_id=data["comment_id"]))
            await call.message.edit_reply_markup(reply_markup=None)
        except TelegramBadRequest as exc:
            logger.debug(exc)
        finally:
            await db_interface.change_comments_status_text_answer(comment_id=int(data["comment_id"]), 
                                                      comment_answer=None,
                                                      status=False)
            await state.clear()
    except TelegramBadRequest as exc:
        logger.debug(exc)
        await call.message.answer("Произошла ошибка. Повторите попытку позже.\n"
                             "Возможно, ответ на комментарий был удален или его удалиение недоступно по другой причине.")
        await state.clear()
