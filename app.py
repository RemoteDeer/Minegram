import asyncio

from aiogram import Dispatcher

from loader import bot, storage, db
from utils.db_api import create_table
from handlers import router


async def on_startup():
    await db.connect()
    await create_table.run(db)

async def on_shutdown():
    await db.disconnect()
    await bot.session.close()

async def main():
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    await on_startup()
    try:
        await dp.start_polling(bot)
    finally:
        on_shutdown()

if __name__ == '__main__':
    asyncio.run(main())