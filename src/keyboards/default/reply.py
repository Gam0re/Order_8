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
settings_back_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='назад')],
], resize_keyboard=True, one_time_keyboard=True)

companys_Inkb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ENERGOLUX', callback_data='energolux_btn'), InlineKeyboardButton(text='TOSHIBA', callback_data='toshiba_btn')],
    [InlineKeyboardButton(text='KALASHNIKOV', callback_data='kalashnikov_btn'), InlineKeyboardButton(text='FERRUM', callback_data='ferrum_btn')],
    [InlineKeyboardButton(text='Подобрать', callback_data='podbor_btn')]
])