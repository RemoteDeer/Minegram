from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menuRequestsCreator = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Add request', callback_data='requestsadd')],
    [InlineKeyboardButton(text='Read requests', callback_data='requestsread')],
    [InlineKeyboardButton(text='Reply request',  callback_data='requestsreply')],
    [InlineKeyboardButton(text='Return', callback_data='menu')]
])