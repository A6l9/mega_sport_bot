from functools import wraps 
from typing import Callable

from loader import proj_settings


def admins_group_access(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> None:
        message = args[0]
        if abs(message.chat.id) == proj_settings.admins_group_id:
            await func(*args, **kwargs)
    return wrapper
