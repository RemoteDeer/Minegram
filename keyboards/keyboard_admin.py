from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menuAdmin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Promote User', callback_data='admin_promote_user')],
    [InlineKeyboardButton(text='Demote User', callback_data='admin_demote_user')],
    [InlineKeyboardButton(text='Return', callback_data='menu')]
])