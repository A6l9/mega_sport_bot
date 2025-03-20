import asyncio

from loader import dp, bot, logger
from handlers.custom.comments_n_posts_check import router as new_comments_n_posts_router
from handlers.custom.reply_to_comment import router as reply_comment_router
from handlers.custom.cancel_handler import router as cancel_router
from database.get_db_interface import db_interface


@dp.startup()
async def on_startup() -> None:
    await db_interface.initial()


async def main() -> None:
    bot_info = await bot.get_me()
    logger.info(f"The bot \"{bot_info.full_name}\" started working")
    dp.include_routers(reply_comment_router, new_comments_n_posts_router, cancel_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
