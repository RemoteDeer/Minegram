from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data.config import OWNER_ID
from loader import db
from keyboards.keyboard_admin import menuAdmin

router = Router()

class UserSelectState(StatesGroup):
    viewing_user = State()

def parser_user_select_args(args_text):
    filter_params = {}
    
    for arg in args_text.split():
        if "=" in arg:
            key, value = arg.split("=", 1)
            if key == 'user_id':
                filter_params['user_id'] = int(value)
            else:
                filter_params[key] = value
    
    return filter_params

@router.message(Command('select_user'))
async def cmd_select_user(message: Message, command: CommandObject, state: FSMContext):

    if OWNER_ID != message.from_user.id:
        await message.answer("Insufficient Privilege ->\nSubscription Upgrade Required")
        return

    if not command.args:
        await message.answer("Error: Missing Arguments")
        return
    
    filter_params = parser_user_select_args(command.args)

    user = await db.select_user(**filter_params)

    if not user:
        await message.answer('User Not Found')
        return
    else:
        await state.set_state(UserSelectState.viewing_user)
        user_data = {
            'user_id' : user['user_id'],
            'username' : user['username'],
            'role' : user['role']
        }
        await state.update_data(user)

    await message.answer(f"User information:\n"
                         f"ID: {user_data['user_id']}\n"
                         f"Username: {user_data['username']}\n"
                         f"Role: {user_data['role']}",
                         reply_markup = menuAdmin
    )

@router.callback_query(UserSelectState.viewing_user, F.data.in_(['admin_user_delete', 'admin_promote_user', 'admin_demote_user']))
async def cbqr_user_delete(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    formatted = ""
    if callback.data == 'admin_user_delete':
        await db.delete_user(user_id=user_data['user_id'])
        await callback.answer('User Deleted')
        await callback.message.answer('User Deleted')
        await user_data.clear()
        return
    
    elif callback.data == 'admin_promote_user':
        await db.update_user_role(user_id=user_data['user_id'], role='admin')
        user_data['role'] = 'admin'
        await state.update_data(user_data)
        
        await callback.answer('User Promoted!')
        formatted = "User Promoted!\n"

    elif callback.data == 'admin_demote_user':
        await db.update_user_role(user_id=user_data['user_id'], role='user')
        user_data['role'] = 'user'
        await state.update_data(user_data)

        await callback.answer('User Demoted!')
        formatted = "User Demoted!\n"

    formatted += (
        "User information:\n"
        f"ID: {user_data['user_id']}\n"
        f"Username: {user_data['username']}\n"
        f"Role: {user_data['role']}\n"
    )

    await callback.message.edit_text(formatted, reply_markup = menuAdmin)