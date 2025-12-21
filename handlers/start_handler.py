from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from data.config import OWNER_ID
from keyboards.keyboard import menu
from loader import db

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    from_user = message.from_user
    
    await db.add_user(user_id=from_user.id, username=from_user.username)
    if from_user.id == OWNER_ID:
        await db.update_user_role(user_id=from_user.id, role='owner')
    await message.answer(f'Hello, {message.from_user.full_name}!\n'
                         f'Choose Service Option', 
                         reply_markup=menu
    )
    

@router.callback_query(F.data == 'menu')
async def cbqr_menu(callback: CallbackQuery):
    await callback.answer('Main menu was opened')
    await callback.message.edit_text('Choose Service Option', reply_markup=menu)


@router.callback_query(F.data == 'no_action')
async def cbqr_ignore(callback: CallbackQuery):
    await callback.answer()