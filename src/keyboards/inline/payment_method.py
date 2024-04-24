from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


payment_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Картой', callback_data='card'),
     InlineKeyboardButton(text='Наличными при получении', callback_data='cash')],
])