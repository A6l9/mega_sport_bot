from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    edit_comment_answer = State()
    delete_comment_answer = State()
