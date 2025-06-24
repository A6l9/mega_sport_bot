import asyncio

from aiogram.types import BotCommandScopeAllGroupChats

import load_services
from loader import dp, bot
from load_services import logger, request_manager, async_scheduler
from handlers.custom.comments_n_posts_check import router as new_comments_n_posts_router
from handlers.custom.upload_comments_to_excel import router as upload_comments_router
from handlers.custom.reply_to_comment import router as reply_comment_router
from handlers.custom.cancel_handler import router as cancel_router
from handlers.custom.change_delete_comm_answer import router as change_delete_router
from database.get_db_interface import db_interface
from utils.gpt_assistant import create_assistants
from set_commands import set_commands


@dp.startup()
async def on_startup() -> None:
    load_services.workers = [asyncio.create_task(request_manager.worker()) for _ in range(5)]
    async_scheduler.start()
    async_scheduler.print_jobs()
    await db_interface.initial()
    # await create_assistants()


@dp.shutdown()
async def on_shutdown() -> None:
    await request_manager.tasks_queue.join()
    for i_worker in load_services.workers:
        i_worker.cancel()


async def main() -> None:
    bot_info = await bot.get_me()
    logger.info(f"The bot \"{bot_info.full_name}\" started working")
    await bot.delete_my_commands(scope=BotCommandScopeAllGroupChats())
    await set_commands()
    dp.include_routers(reply_comment_router,
                       change_delete_router, 
                       upload_comments_router, 
                       new_comments_n_posts_router, 
                       cancel_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
