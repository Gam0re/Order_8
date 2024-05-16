from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

continuing_order_registration = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Продолжить оформление заказа', callback_data='continue')],
])

product_availability = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Товар есть в наличии', callback_data='available'),
     InlineKeyboardButton(text='Товара нет в наличии', callback_data='unavailable')],
])

yes_no_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='agree'),
     InlineKeyboardButton(text='Нет', callback_data='disagree')],
])
