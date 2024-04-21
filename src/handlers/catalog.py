from aiogram import types, Router, F

from aiogram.filters import Command

from aiogram_dialog import DialogManager

import src.keyboards.inline.catalog as cl
import src.database.requests as rq
import src.states.dialog as dialog_states


catalog_router = Router()


# команда старт
@catalog_router.message(Command('catalog'))
@catalog_router.message(F.text == 'Каталог')
async def catalog_lvl1(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(dialog_states.dialogFSM.levels[0])

@catalog_router.callback_query(F.data == 'level_1')
async def catalog_lvl2(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберете категорию товара', reply_markup=await cl.catalog_level_2())

@catalog_router.callback_query(F.data.startswith('level_2'))
async def catalog_lvl3(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберете категорию товара', reply_markup=await cl.catalog_level_3(callback.data.split('_')[2]))

@catalog_router.callback_query(F.data.startswith('level_3'))
async def catalog_lvl4(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберете категорию товара', reply_markup=await cl.catalog_level_4(callback.data.split('_')[2], callback.data.split('_')[3]))

@catalog_router.callback_query(F.data.startswith('level_4'))
async def catalog_lvl5(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберете категорию товара', reply_markup=await cl.catalog_level_5(callback.data.split('_')[2], callback.data.split('_')[3], callback.data.split('_')[4]))

@catalog_router.callback_query(F.data.startswith('level_5'))
async def catalog_names(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар', reply_markup=await cl.catalog_get_names(callback.data.split('_')[2], callback.data.split('_')[3], callback.data.split('_')[4], callback.data.split('_')[5]))

@catalog_router.callback_query(F.data.startswith('name'))
async def catalog_names(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали товар')
    print(callback.data)
    item = (await rq.get_item(cl.name_dict[int(callback.data.split('_')[5])]))
    print(item)


@catalog_router.callback_query(F.data == 'to_main')
async def to_main(callback: types.CallbackQuery):
    await callback.answer('На главную')
    await callback.message.answer('Выберете категорию товара', reply_markup=await cl.catalog_level_1())
