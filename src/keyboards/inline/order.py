from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


order_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='История', callback_data='done'),
     InlineKeyboardButton(text='Текущий заказ', callback_data='in_progress')],
])

order_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='main_orders')],
])
