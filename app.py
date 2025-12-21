import asyncio

from aiogram import Dispatcher
import sys, traceback

from loader import bot, storage, db
from handlers import router


async def on_startup():
    await db.connect()
    await db.create_table()

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
        await on_shutdown()

if __name__ == '__main__':
    try: 
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)