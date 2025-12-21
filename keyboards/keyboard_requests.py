from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db

async def create_pagination_keyboard(current_page, total_pages):

    buttons = []

    if current_page > 1:
        buttons.append(InlineKeyboardButton(
            text = "◀️ Prev",
            callback_data=f"requests_list_prev"
        ))
    
    buttons.append(InlineKeyboardButton(
        text=f"{current_page}/{total_pages}",
        callback_data="no_action"
    ))

    if current_page < total_pages:
        buttons.append(InlineKeyboardButton(
            text="Next ▶️",
            callback_data=f"requests_list_next"
        ))
    
    actions_button = [
        InlineKeyboardButton(text="🔄 Refresh", callback_data=f"requests_list_refresh"),
        InlineKeyboardButton(text="❌ Close", callback_data="menu")
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[buttons, actions_button]
    )