from aiogram.types import CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from load_services import logger


router = Router(name="cancel_router")


@router.callback_query(F.data == "cancel")
async def cancel_handler(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest:
        logger.debug("This message does't have keyboard")
    await call.message.answer("Вы отменили предыдущее действие 🙅‍♂️")
