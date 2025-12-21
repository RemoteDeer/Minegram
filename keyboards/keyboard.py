from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Minecraft', callback_data='minecraft_menu')],
    [InlineKeyboardButton(text='Requests', callback_data='requests_menu')],
    [InlineKeyboardButton(text='About me', callback_data='aboutme_menu')]
])

menuAboutme = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Update My Info', callback_data='aboutme_update'),
    InlineKeyboardButton(text='Delete my data', callback_data='aboutme_delete')],
    [InlineKeyboardButton(text='Return', callback_data='menu')]
])

menuMinecraft = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='List all worlds', callback_data='minecraft_list')],
    [InlineKeyboardButton(text='Return', callback_data='menu')]
])

menuRequests = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Read requests', callback_data='requests_list')],
    [InlineKeyboardButton(text='Return', callback_data='menu')]
])