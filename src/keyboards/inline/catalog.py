from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import src.database.requests as rq


async def catalog_level_1():
    level_1 = set(await rq.get_level_1())
    print(list(level_1))
    keyboard = InlineKeyboardBuilder()
    for level in level_1:
        keyboard.add(InlineKeyboardButton(text=level, callback_data=level))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()
