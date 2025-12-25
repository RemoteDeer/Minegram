from aiogram import BaseMiddleware
from aiogram.types import Message
import time

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 0.5):
        self.rate_limit = limit
        self.last_call = {}

    async def __call__(self, handler, event: Message, data):
        user = None

        if event.message:
            user = event.message.from_user
        elif event.callback_query:
            user = event.callback_query.from_user
        
        if not user:
            return await handler(event, data)

        user_id = user.id
        now = time.time()

        last_time = self.last_call.get(user_id)
        if last_time and now - last_time <  self.rate_limit:
            if event.message:
                await event.message.answer(f'Too many events.\nTry again in {self.rate_limit-now+last_time:.2f} seconds.')
                return
            elif event.callback_query:
                await event.callback_query.answer('Slow down!', show_alert=False)
                await event.callback_query.message.answer(f'Too many events.\nTry again in {self.rate_limit-now+last_time:.2f} seconds.')
                return
    
        self.last_call[user_id] = now
        return await handler(event, data)