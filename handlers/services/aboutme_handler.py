from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.keyboard import menuAboutme
from loader import db

router = Router()

@router.callback_query(F.data == 'aboutme_menu')
async def cbqr_me(callback: CallbackQuery):
    await callback.answer('Profile menu was opened')
    from_user = callback.from_user
    me = await db.select_user(user_id=from_user.id)
    await callback.message.edit_text(f"Your information:\n"
                                     f"ID: {me['user_id']}\n"
                                     f"Username: {me['username']}\n"
                                     f"Role: {me['role']}", 
                                     reply_markup = menuAboutme
    )

@router.callback_query(F.data == 'aboutme_update')
async def cbqr_meusernameupdate(callback: CallbackQuery):
    await callback.answer('Your info was updated')
    from_user = callback.from_user
    await db.update_username(user_id=from_user.id, username=from_user.username)
    me = await db.select_user(user_id=from_user.id)
    await callback.message.reply('Your info was updated!')
    await callback.message.answer(f"Your information:\n"
                                  f"ID: {me['user_id']}\n"
                                  f"Username: {me['username']}\n"
                                  f"Role: {me['role']}", 
                                  reply_markup = menuAboutme
    )

@router.callback_query(F.data == 'aboutme_delete')
async def cbqr_medelete(callback: CallbackQuery):
    await callback.answer('Your data was deleted')
    from_user = callback.from_user
    await db.delete_user(user_id=from_user.id)
    await callback.message.answer("Your data was deleted.\n"
                                  "You can delete this chat"
    )