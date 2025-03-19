from functools import wraps 
from typing import Callable

from loader import proj_settings


def channel_access(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> None:
        message = args[0]
        if message.chat.id == proj_settings.channel_id:
            await func(*args, **kwargs)
    return wrapper
