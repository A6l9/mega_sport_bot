from typing import Callable

from aiogram.types import BotCommand, BotCommandScopeAllGroupChats

from loader import bot


async def set_commands() -> Callable:
    bot_commands = [
        BotCommand(command="upload_comments", description="Выгрузить комментарии в Excel")
    ]

    return await bot.set_my_commands(commands=bot_commands, scope=BotCommandScopeAllGroupChats())
