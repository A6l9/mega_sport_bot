from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
from openai import AsyncOpenAI

from utils.logging import get_logger
from config import proj_settings


logger = get_logger(logger=logger)
bot = Bot(token=proj_settings.bot_token)
dp = Dispatcher(storage=MemoryStorage())

client = AsyncOpenAI(api_key="proj_settings.gpt_token", 
                     max_retries=2,
                     timeout=5)
