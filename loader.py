from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from data import config
from database import Database

bot = Bot(
    token=str(config.TOKEN), 
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

storage = MemoryStorage()
db = Database()