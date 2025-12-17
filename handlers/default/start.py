import asyncpg
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from keyboards.keyboarduser import menu
from loader import db

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    try:
        await db.add_user(user.id, user.username)
        await message.answer(f'Hello, {message.from_user.full_name}!',)
        await message.answer('Choose Service Option', reply_markup=menu)
    except asyncpg.exceptions.UniqueViolationError:
        await message.answer('Choose Service Option', reply_markup=menu)

@router.callback_query(F.data == 'menu')
async def cbqr_menu(callback: CallbackQuery):
    await callback.answer('Main menu was opened')
    await callback.message.edit_text('Choose Service Option', reply_markup=menu)
    