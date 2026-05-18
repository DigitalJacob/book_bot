import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logging(
        level: str = "INFO",
        log_file: str = "bot.log",
        console_output: bool = True,
        log_format: Optional[str] = None
) -> None:
    log_level = getattr(logging, level.upper(), logging.INFO)

    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    date_format = '%d-%m-%Y %H:%M:%S'
    formatter = logging.Formatter(log_format, date_format)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()

    if log_file:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10_485_760,
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    logging.getLogger('aiogram').setLevel(logging.WARNING)
    logging.getLogger('aiohttp').setLevel(logging.WARNING)

    logging.info(f"Logging configured (level: {level})")


def user_log_info(user) -> str:
    username = user.username or "no username"
    name_part = f" ({user.full_name})" if user.full_name and not user.username else ""
    return f"{user.id} (@{username}){name_part}"