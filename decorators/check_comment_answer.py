from functools import wraps
from typing import Callable

from database.get_db_interface import db_interface
from challenges_config import CHALLENGES_CONFIG


def check_comment_answer(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> None:
        call = args[0]
        comment_id = call.data.split(":")[1]
        challenge_type, _ = call.data.split("-")[2].split(":")
        model = CHALLENGES_CONFIG[challenge_type]["model_comments"]
        comment = await db_interface.get_row(model, comment_id=int(comment_id))
        if comment:
            if not comment.is_answered:
                await func(*args, **kwargs)
            else:
                await call.answer("На этот комментарий уже есть ответ.")
        else:
            await call.answer("Произошла ошибка, комментария не существует или он был удален.")
    return wrapper
