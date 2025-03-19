import sys


def get_logger(logger):
    logger.remove()
    logger.add(sys.stdout, format="{function} | {time:HH:mm:ss} | {level} | {message}", backtrace=False)
    return logger
