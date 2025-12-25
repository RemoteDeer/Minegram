from loader import db, bot
import logging

async def on_startup_notify():
    admins = await db.select_admins()
    
    for admin in admins:
        print(admin['user_id'])
        try:
            await bot.send_message(admin['user_id'], "Bot is launched. Run /start")
        
        except Exception as err:
            logging.exception(err)