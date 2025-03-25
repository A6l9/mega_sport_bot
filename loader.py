from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import proj_settings


bot = Bot(token=proj_settings.bot_token)
dp = Dispatcher(storage=MemoryStorage())
