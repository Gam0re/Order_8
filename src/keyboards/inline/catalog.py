from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog.widgets.kbd import Button

import src.database.requests as rq
from aiogram_dialog.widgets.text import Const
level_2_dict = {}
level_3_dict = {}
level_4_dict = {}
level_5_dict = {}
name_dict = {}

def lvl1_buttons_creator(btn_quantity):
    buttons = []
    for i in btn_quantity:
        i = str(i)
        buttons.append(Button(Const(i), id=i))
    return buttons

async def catalog_level_1():
    level_1 = set(await rq.get_level_1())
    print(list(level_1))
    keyboard = InlineKeyboardBuilder()
    for level in level_1:
        keyboard.add(InlineKeyboardButton(text=level, callback_data='level_1'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(1).as_markup()

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
    return keyboard.adjust(1).as_markup()
#
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
#
# async def catalog_level_4(level_2, level_3):
#     level_4 = set(await rq.get_level_4(level_2_dict[int(level_2)], level_3_dict[int(level_3)]))
#     print(list(level_4))
#     keyboard = InlineKeyboardBuilder()
#     count = 0
#     for level in level_4:
#         level_4_dict[count] = level
#         keyboard.add(InlineKeyboardButton(text=level, callback_data=f'level_4_{level_2}_{level_3}_{count}'))
#         count += 1
#     keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
#     return keyboard.adjust(2).as_markup()
#
# async def catalog_level_5(level_2, level_3, level_4):
#     level_5 = set(await rq.get_level_5(level_2_dict[int(level_2)], level_3_dict[int(level_3)], level_4_dict[int(level_4)]))
#     print(list(level_5))
#     keyboard = InlineKeyboardBuilder()
#     count = 0
#     for level in level_5:
#         level_5_dict[count] = level
#         keyboard.add(InlineKeyboardButton(text=level, callback_data=f'level_5_{level_2}_{level_3}_{level_4}_{count}'))
#         count += 1
#     keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
#     return keyboard.adjust(2).as_markup()
#
# async def catalog_get_names(level_2, level_3, level_4, level_5):
#     names = set(await rq.get_names(level_2_dict[int(level_2)], level_3_dict[int(level_3)], level_4_dict[int(level_4)], level_5_dict[int(level_5)]))
#     print(list(names))
#     keyboard = InlineKeyboardBuilder()
#     count = 0
#     for name in names:
#         name_dict[count] = name
#         keyboard.add(InlineKeyboardButton(text=name, callback_data=f'name_{level_2}_{level_3}_{level_4}_{level_5}_{count}'))
#         count += 1
#     keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
#     return keyboard.adjust(2).as_markup()
#
# async def catalog_get_item():
#     keyboard = InlineKeyboardBuilder()
#     keyboard.add(InlineKeyboardButton(text='В корзину', callback_data='to_cart'))
#     keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
#     return keyboard.adjust(2).as_markup()
