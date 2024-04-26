from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def cart_kb(page, price):
    if page != -1:
        cart_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Удалить', callback_data=f'delete_{page}'),
             InlineKeyboardButton(text='+', callback_data=f'increment_{page}'),
             InlineKeyboardButton(text='-', callback_data=f'decrement_{page}')],
            [InlineKeyboardButton(text='Назад', callback_data=f'back_{page}'),
             InlineKeyboardButton(text='Каталог', callback_data='to_catalog'),
             InlineKeyboardButton(text='Вперед', callback_data=f'next_{page}')],
            [InlineKeyboardButton(text=f'Оформить заказ({price} Руб.)', callback_data='to_payment')]
        ])
    else:
        cart_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='На главную', callback_data='to_main')]
        ])
    return cart_kb

