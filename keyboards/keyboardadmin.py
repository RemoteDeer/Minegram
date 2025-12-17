from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menuMinecraftAdmin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='List all worlds', callback_data='minecraftlistworld'),
     InlineKeyboardButton(text='Create world', callback_data='minecraftcreateworld')],
    [InlineKeyboardButton(text='Download world', callback_data='minecraftdownloadworld'),
     InlineKeyboardButton(text='Upload world', callback_data='minecraftuploadworld')],
    [InlineKeyboardButton(text='Launch world', callback_data='minecraftlaunchworld'),
     InlineKeyboardButton(text='Edit world', callback_data='minecrafteditworld')],
    [InlineKeyboardButton(text='Stop world', callback_data='minecraftstopworld'),
     InlineKeyboardButton(text='Delete world', callback_data='minecraftdeleteworld')],
    [InlineKeyboardButton(text='Return', callback_data='menu')]
])