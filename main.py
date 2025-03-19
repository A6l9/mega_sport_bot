import asyncio

from loader import dp, bot, logger
from database.get_db_interface import db_interface


@dp.startup()
async def on_startup() -> None:
    await db_interface.initial()


async def main() -> None:
    bot_info = await bot.get_me()
    logger.info(f"The bot \"{bot_info.full_name}\" started working")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
