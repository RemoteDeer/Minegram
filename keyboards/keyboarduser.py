from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Minecraft', callback_data='minecraft')],
    [InlineKeyboardButton(text='Requests', callback_data='requests')],
    [InlineKeyboardButton(text='Me', callback_data='me')]
])

menuMe = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Update username', callback_data='meusernameupdate'),
    InlineKeyboardButton(text='Delete my data', callback_data='medelete')],
    [InlineKeyboardButton(text='Return', callback_data='menu')]
])

menuMinecraft = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='List all worlds', callback_data='minecraftlistworld')],
    [InlineKeyboardButton(text='Return', callback_data='menu')]
])

menuRequests = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Add request', callback_data='requestsadd')],
    [InlineKeyboardButton(text='Read requests', callback_data='requestsread')],
    [InlineKeyboardButton(text='Return', callback_data='menu')]
])