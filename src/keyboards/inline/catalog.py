from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import src.database.requests as rq

level_2_dict = {}
level_3_dict = {}
level_4_dict = {}
level_5_dict = {}
async def catalog_level_1():
    level_1 = set(await rq.get_level_1())
    print(list(level_1))
    keyboard = InlineKeyboardBuilder()
    for level in level_1:
        keyboard.add(InlineKeyboardButton(text=level, callback_data='level_1'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

async def catalog_level_2():
    level_2 = set(await rq.get_level_2())
    print(list(level_2))
    keyboard = InlineKeyboardBuilder()
    count = 0
    for level in level_2:
        level_2_dict[count] = level
        keyboard.add(InlineKeyboardButton(text=level, callback_data=f'level_2_{count}'))
        count += 1
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

async def catalog_level_3(level_2):
    level_3 = set(await rq.get_level_3(level_2_dict[int(level_2)]))
    print(list(level_3))
    keyboard = InlineKeyboardBuilder()
    count = 0
    for level in level_3:
        level_3_dict[count] = level
        keyboard.add(InlineKeyboardButton(text=level, callback_data=f'level_3_{level_2}_{count}'))
        count += 1
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

async def catalog_level_4(level_2, level_3):
    level_4 = set(await rq.get_level_4(level_2_dict[int(level_2)], level_3_dict[int(level_3)]))
    print(list(level_4))
    keyboard = InlineKeyboardBuilder()
    count = 0
    for level in level_4:
        level_4_dict[count] = level
        keyboard.add(InlineKeyboardButton(text=level, callback_data=f'level_4_{level_2}_{level_3}_{count}'))
        count += 1
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

async def catalog_level_5(level_2, level_3, level_4):
    level_5 = set(await rq.get_level_5(level_2_dict[int(level_2)], level_3_dict[int(level_3)], level_4_dict[int(level_4)]))
    print(list(level_5))
    keyboard = InlineKeyboardBuilder()
    count = 0
    for level in level_5:
        level_5_dict[count] = level
        keyboard.add(InlineKeyboardButton(text=level, callback_data=f'level_4_{level_2}_{level_3}_{level_4}_{count}'))
        count += 1
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()
