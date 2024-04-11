from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог'), KeyboardButton(text='Корзина')],
    [KeyboardButton(text='Заказы'), KeyboardButton(text='Подбор')],
    [KeyboardButton(text='Настройки'), KeyboardButton(text='Помощь')],
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберете необходимую опцию')
