from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from utils.logging import get_logger
from utils.request_manager import RequestManager


logger = get_logger(logger=logger)

request_manager = RequestManager()
workers = []

jobstores = {
    "default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")
}
async_scheduler = AsyncIOScheduler(jobstores=jobstores)
