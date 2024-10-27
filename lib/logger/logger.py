import asyncio
import logging.config
import logging
from concurrent.futures import ThreadPoolExecutor

from pythonjsonlogger import jsonlogger

from config import LOGGING_LEVEL
from lib.logger.handler import AsyncFileHandler


def setup_logger() -> None:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "class": "logging.Formatter"
            }
        },
        "handlers": {
            "file": {
                "class": "lib.logger.handler.AsyncFileHandler",
                "filename": "log",
                "mode": "a",
                "formatter": "default",
                "encoding": "utf-8"
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "": {
                "handlers": ["file", "console"],
                "level": LOGGING_LEVEL,
                "propagate": True
            }
        }
    }

    logging.config.dictConfig(LOGGING)
    logging.debug('Logger configured')


setup_logger()


def get_logger():
    return logging.root


