from aiogram.types import CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext


router = Router(name="cancel_router")


@router.callback_query(F.data == "cancel")
async def cancel_handler(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.answer("Вы отменили предыдущее действие 🙅‍♂️")
