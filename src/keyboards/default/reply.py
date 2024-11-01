from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог'), KeyboardButton(text='Корзина')],
    [KeyboardButton(text='Заказы'), KeyboardButton(text='Подбор')],
    [KeyboardButton(text='Настройки'), KeyboardButton(text='Помощь')],
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберете необходимую опцию')

help_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Позвонить'), KeyboardButton(text='Написать')],
    [KeyboardButton(text='Помощь на сайте')],
    [KeyboardButton(text='Главное меню')],
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберете необходимую опцию')

back_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')],
], resize_keyboard=True, one_time_keyboard=True)

settings_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Имя'), KeyboardButton(text='Номер')],
                                            [KeyboardButton(text='Главное меню')]],
                                  resize_keyboard=True, one_time_keyboard=True)

