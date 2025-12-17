from aiogram import F, Router
from aiogram.types import CallbackQuery
import utils.db_api.postgresql

from keyboards.keyboarduser import menuMe
from loader import db

router = Router()

@router.callback_query(F.data == 'me')
async def cbqr_me(callback: CallbackQuery):
    await callback.answer('Profile menu was opened')
    user = callback.from_user
    me = await db.select_user(user_id=user.id)
    await callback.message.edit_text((f"Your information:\n"
                                     f"ID: {me['user_id']}\n"
                                     f"Username: {me['username']}\n"
                                     f"Role: {me['role']}"), 
                                    reply_markup = menuMe
    )

@router.callback_query(F.data == 'meusernameupdate')
async def cbqr_meusernameupdate(callback: CallbackQuery):
    await callback.answer('Your username was updated')
    user = callback.from_user
    await db.update_username(user_id=user.id, username=user.username)
    me = await db.select_user(user_id=user.id)
    await callback.message.edit_text(f"Your username was updated.\n"
                                     f"Your information:\n"
                                     f"ID: {me['user_id']}\n"
                                     f"Username: {me['username']}\n"
                                     f"Role: {me['role']}", 
                                     reply_markup = menuMe
    )

@router.callback_query(F.data == 'medelete')
async def cbqr_medelete(callback: CallbackQuery):
    await callback.answer('Your data was deleted')
    user = callback.from_user
    await db.delete_user(user_id=user.id)
    await callback.message.edit_text("Your data was deleted.\n"
                                     "You can delete this chat",
                                      reply_markup = menuMe
    )