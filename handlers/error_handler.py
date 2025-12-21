import logging
from enum import Enum
from aiogram import Router, types
from aiogram.exceptions import TelegramAPIError, AiogramError

router = Router()

@router.errors()
async def errors_handler(update: types.Update, exception: Exception):
    """
    Global exception handler for all Aiogram/Telegram errors.
    Logs all known exceptions and catches everything else as well.
    """

    if isinstance(exception, TelegramAPIError):
        logging.warning(f"TelegramAPIError: {exception} | Update: {update}")
        return True

    if isinstance(exception, AiogramError):
        logging.error(f"AiogramError: {exception} | Update: {update}")
        return True

    logging.exception(f"Unhandled exception: {exception} | Update: {update}")
    return True