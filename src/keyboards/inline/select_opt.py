from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

opt_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Закупщик', callback_data='opt'),
             InlineKeyboardButton(text='Пользователь', callback_data='user')]
            ])
