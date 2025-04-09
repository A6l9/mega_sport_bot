from loguru import logger

from utils.logging import get_logger
from utils.request_manager import RequestManager


logger = get_logger(logger=logger)

request_manager = RequestManager()
workers = []
