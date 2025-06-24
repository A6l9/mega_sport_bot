from functools import wraps 
from typing import Callable

from config import proj_settings


def admins_group_access(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> None:
        message = args[0]
        if abs(message.chat.id) in [proj_settings.athletx_admins_group_id,
                                    proj_settings.terfit_admins_group_id]:
            await func(*args, **kwargs)
    return wrapper
