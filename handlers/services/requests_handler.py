from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from data.config import OWNER_ID

from keyboards.keyboard import menuRequests
from keyboards.keyboard_requests import create_pagination_keyboard
from loader import db

router = Router()

class RequestListStates(StatesGroup):
    viewing_requests = State()

@router.callback_query(F.data == 'requests_menu')
async def cbqr_requests(callback: CallbackQuery):
    await callback.answer('Requests menu was opened')
    user = await db.select_user(user_id=callback.from_user.id)

    if user['role'] == 'user' or user['role'] == 'admin':
        await callback.message.edit_text('Requests menu',
                                         reply_markup = menuRequests)
    if user['role'] == 'owner':
        await callback.message.edit_text('Requests menu',
                                         reply_markup = menuRequests)

@router.message(Command('requests_add'))
async def cmd_requests_add(message: Message, command: CommandObject):
    from_user = message.from_user

    if from_user.id != OWNER_ID:
        await message.answer("Error: Insufficient Privilege")
    elif not command.args:
        await message.answer("Error: Missing text argument")
    else:
        text_req = command.args
        try:
            await db.requests_add(user_id=from_user.id, text_req=text_req)
            await message.answer("Request was added!")
        except Exception as e:
            await message.answer(f"Something went wrong: {e}")

def parser_request_args(args_text):
    pagination_params ={
        'page' : 1, 
        'per_page' : 5
    }

    filter_params = {}

    if not args_text:
        return pagination_params, filter_params
    
    for arg in args_text.split():
        if "=" in arg:
            key, value = arg.split("=", 1)
            if key == 'page':
                pagination_params['page'] = int(value)
            elif key == 'per_page':
                pagination_params['per_page'] = min(max(1, int(value)), 10)
            elif key == 'user_id':
                filter_params['user_id'] = int(value)
            else:
                filter_params[key] = value
    
    return pagination_params, filter_params

@router.message(Command("help"))
async def get_help_message(message: Message):
    await message.answer(
        "📋 **Requests List Command**\n\n"
        "**Usage:** `/requests_list [parameters]`\n\n"
        "**Parameters:**\n"
        "• `page=1` - Page number (default: 1)\n"
        "• `per_page=5` - Items per page (1-15, default: 5)\n"
        "• `status=open` - Filter by status (open/processing/accepted/rejected/closed)\n"
        "• `user_id=12345` - Filter by user ID\n"
        "• `username=Name` - Filter by username\n"
        "**Examples:**\n"
        "• `/requests_list`\n"
        "• `/requests_list page=2 per_page=10`\n"
        "• `/requests_list status=open user_id=1726168651`\n"
        "• `/requests_list username=Tuzdyq page=1 per_page=5`"
    )       


@router.callback_query(F.data == "requests_list")
async def cbqr_requests_read(callback: CallbackQuery, state: FSMContext):
    state_data = {
        'page' : 1,
        'per_page' : 5
    }
    
    total = await db.get_total_requests()
    per_page = state_data['per_page']
    total_pages = max(1, (total + per_page - 1) // per_page)
    await state.set_state(RequestListStates.viewing_requests)
    await state.update_data(state_data)

    formatted = await db.format_page(page=state_data['page'], per_page=state_data['per_page'])

    if not formatted:
        await callback.answer("No Requests Found")
        await callback.message.edit_text("📭 No Requests Found")
        state.clear()
        return

    keyboard = await create_pagination_keyboard(current_page=state_data['page'], total_pages=total_pages)
    
    await callback.answer("Page updated!")

    await callback.message.edit_text(
        formatted,
        reply_markup=keyboard
    )

@router.message(Command("requests_list"))
async def cmd_requests_list(message: Message, command: CommandObject, state: FSMContext):
    pagination_params, filter_params = parser_request_args(command.args)
    
    state_data = {
        **pagination_params,
        **filter_params
    }

    total = await db.get_total_requests(**filter_params)
    per_page = pagination_params['per_page']
    total_pages = max(1, (total + per_page - 1) // per_page)

    await state.set_state(RequestListStates.viewing_requests)
    await state.update_data(state_data)

    formatted = await db.format_page(page=pagination_params['page'], per_page=pagination_params['per_page'], **filter_params)

    if not formatted:
        await message.answer("📭 No Requests Found", show_alert=True)
        await state.clear()
        return
    
    keyboard = await create_pagination_keyboard(current_page=pagination_params['page'], total_pages=total_pages)
    
    await message.answer(
        formatted,
        reply_markup=keyboard
    )

@router.callback_query(RequestListStates.viewing_requests, F.data.in_(['requests_list_prev', 'requests_list_next', 'requests_list_refresh']))
async def cbqr_requests_list_update(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    current_page = state_data.get('page', 1)
    per_page = state_data.get('per_page', 5)

    if callback.data == 'requests_list_prev':
        new_page = current_page - 1
    elif callback.data == 'requests_list_next':
        new_page = current_page + 1
    else:
        new_page = current_page

    filter_params = {
        k: v for k, v in state_data.items()
        if k not in ['page', 'per_page', 'total', 'total_pages']
    }

    total = await db.get_total_requests(**filter_params)
    total_pages = max(1, (total + per_page - 1) // per_page)
    new_page = max(1, min(new_page, total_pages))

    state_data['page'] = new_page
    await state.update_data(state_data)


    formatted = await db.format_page(page=new_page, per_page=per_page, **filter_params)

    if not formatted:
        await callback.answer("📭 No Requests Found", show_alert=True)
        state.clear()
        return

    keyboard = await create_pagination_keyboard(current_page=new_page, total_pages=total_pages)

    if callback.data == 'requests_list_refresh':
        await callback.message.answer(
            formatted, 
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text(
            formatted, 
            reply_markup=keyboard
        )

    await callback.answer()
