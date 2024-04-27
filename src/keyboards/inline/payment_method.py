from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


payment_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Картой', callback_data='card'),
     InlineKeyboardButton(text='Наличными при получении', callback_data='cash')],
])

product_availability = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Товар есть в наличии', callback_data='available'),
     InlineKeyboardButton(text='Товара нет в наличии', callback_data='unavailable')],
])
